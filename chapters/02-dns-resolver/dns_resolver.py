#!/usr/bin/env python3
"""Chapter 2: a DNS resolver built on raw UDP packets.

Builds a DNS query packet byte by byte, sends it over UDP, and parses
the response, including compressed names. No resolver library does any
of the work: `socket` only moves the datagrams.

Usage:
    python3 dns_resolver.py example.com
    python3 dns_resolver.py example.com --type MX --server 127.0.0.1 --port 5353
"""

import argparse
import random
import socket
import struct
import sys

QTYPE = {"A": 1, "NS": 2, "CNAME": 5, "MX": 15, "TXT": 16, "AAAA": 28}
QTYPE_BY_ID = {v: k for k, v in QTYPE.items()}
QCLASS_IN = 1


def encode_name(name):
    """'example.com' -> b'\\x07example\\x03com\\x00' (length-prefixed labels)."""
    out = b""
    for label in name.rstrip(".").split("."):
        if len(label) > 63:
            raise ValueError("label too long: %r" % label)
        out += struct.pack("B", len(label)) + label.encode("ascii")
    return out + b"\x00"


def build_query(name, qtype):
    """Assemble header + question. Returns (packet_bytes, query_id)."""
    query_id = random.randrange(0, 65536)
    # flags 0x0100: recursion desired. QDCOUNT=1, all other counts 0.
    header = struct.pack(">HHHHHH", query_id, 0x0100, 1, 0, 0, 0)
    question = encode_name(name) + struct.pack(">HH", qtype, QCLASS_IN)
    return header + question, query_id


def decode_name(packet, offset):
    """Decode a possibly compressed name starting at offset.

    Returns (name, offset_after_name_in_original_stream). A byte whose
    top two bits are 11 is a pointer to elsewhere in the packet; that
    is how DNS fits repeated names into 512-byte-era messages.
    """
    labels = []
    jumped = False
    next_offset = None
    while True:
        length = packet[offset]
        if length == 0:
            if not jumped:
                next_offset = offset + 1
            break
        if length & 0xC0 == 0xC0:
            pointer = struct.unpack(">H", packet[offset:offset + 2])[0] & 0x3FFF
            if not jumped:
                next_offset = offset + 2
            offset = pointer
            jumped = True
            continue
        labels.append(packet[offset + 1:offset + 1 + length].decode("ascii"))
        offset += 1 + length
    return ".".join(labels), next_offset


def parse_response(packet, expected_id):
    """Parse header, skip questions, decode answer records."""
    qid, flags, qd, an, ns, ar = struct.unpack(">HHHHHH", packet[:12])
    if qid != expected_id:
        raise ValueError("response ID %d does not match query ID %d"
                         % (qid, expected_id))
    rcode = flags & 0x000F
    if rcode != 0:
        raise ValueError("server returned error rcode %d" % rcode)
    offset = 12
    for _ in range(qd):
        _, offset = decode_name(packet, offset)
        offset += 4  # QTYPE + QCLASS
    answers = []
    for _ in range(an + ns + ar):
        name, offset = decode_name(packet, offset)
        rtype, rclass, ttl, rdlen = struct.unpack(">HHIH",
                                                  packet[offset:offset + 10])
        offset += 10
        rdata = packet[offset:offset + rdlen]
        answers.append((name, QTYPE_BY_ID.get(rtype, str(rtype)),
                        ttl, format_rdata(packet, offset, rtype, rdata)))
        offset += rdlen
    return answers


def format_rdata(packet, rdata_offset, rtype, rdata):
    if rtype == 1 and len(rdata) == 4:      # A
        return socket.inet_ntoa(rdata)
    if rtype == 28 and len(rdata) == 16:    # AAAA
        return socket.inet_ntop(socket.AF_INET6, rdata)
    if rtype in (2, 5):                     # NS, CNAME: a name, may compress
        name, _ = decode_name(packet, rdata_offset)
        return name
    if rtype == 15:                        # MX: preference + name
        pref = struct.unpack(">H", rdata[:2])[0]
        name, _ = decode_name(packet, rdata_offset + 2)
        return "%d %s" % (pref, name)
    if rtype == 16:                        # TXT: length-prefixed strings
        texts, i = [], 0
        while i < len(rdata):
            ln = rdata[i]
            texts.append(rdata[i + 1:i + 1 + ln].decode("utf-8", "replace"))
            i += 1 + ln
        return " ".join(texts)
    return rdata.hex()


def default_server():
    """First nameserver from /etc/resolv.conf, else 1.1.1.1."""
    try:
        with open("/etc/resolv.conf") as fh:
            for line in fh:
                if line.startswith("nameserver"):
                    return line.split()[1]
    except OSError:
        pass
    return "1.1.1.1"


def resolve(name, qtype_name, server, port, timeout=5.0):
    qtype = QTYPE[qtype_name]
    packet, query_id = build_query(name, qtype)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        # connect() on a UDP socket sends nothing; it fixes the peer,
        # so the kernel delivers only datagrams from this server and
        # send/recv work without an address per call.
        sock.connect((server, port))
        sock.send(packet)
        data = sock.recv(4096)
    return parse_response(data, query_id)


def main(argv=None):
    ap = argparse.ArgumentParser(description="DNS resolver on raw UDP")
    ap.add_argument("name", help="domain name to resolve")
    ap.add_argument("--type", default="A", choices=sorted(QTYPE),
                    help="record type (default A)")
    ap.add_argument("--server", default=None,
                    help="DNS server IP (default: first in /etc/resolv.conf)")
    ap.add_argument("--port", type=int, default=53)
    ap.add_argument("--timeout", type=float, default=5.0)
    args = ap.parse_args(argv)

    server = args.server or default_server()
    try:
        answers = resolve(args.name, args.type, server, args.port, args.timeout)
    except (socket.timeout, OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    if not answers:
        print("no records")
        return 0
    for name, rtype, ttl, value in answers:
        print("%s\t%d\tIN\t%s\t%s" % (name, ttl, rtype, value))
    return 0


if __name__ == "__main__":
    sys.exit(main())
