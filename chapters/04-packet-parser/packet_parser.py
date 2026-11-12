#!/usr/bin/env python3
"""Chapter 4: a packet parser for pcap capture files.

Reads the libpcap file format directly: global header, then per-packet
records, then decodes Ethernet, IPv4, TCP and UDP headers with struct.
No capture library: the format is the lesson.

Usage:
    python3 make_fixture.py            # writes fixture.pcap (synthetic)
    python3 packet_parser.py fixture.pcap
"""

import argparse
import socket
import struct
import sys
from collections import Counter

# magic -> (struct endian prefix, timestamps are nanoseconds?)
PCAP_MAGICS = {
    0xA1B2C3D4: (">", False),   # big-endian, microseconds
    0xD4C3B2A1: ("<", False),   # little-endian, microseconds
    0xA1B23C4D: (">", True),    # big-endian, nanoseconds
    0x4D3CB2A1: ("<", True),    # little-endian, nanoseconds
}

IP_PROTO = {1: "icmp", 6: "tcp", 17: "udp"}
TCP_FLAGS = [(0x01, "FIN"), (0x02, "SYN"), (0x04, "RST"), (0x08, "PSH"),
             (0x10, "ACK"), (0x20, "URG"), (0x40, "ECE"), (0x80, "CWR")]


def parse_pcap(data):
    """Yield (ts_sec, ts_frac, frame_bytes) for each packet record."""
    if len(data) < 24:
        raise ValueError("file too short for a pcap global header")
    magic = struct.unpack(">I", data[:4])[0]
    if magic not in PCAP_MAGICS:
        raise ValueError("not a pcap file (magic 0x%08x)" % magic)
    endian, _nano = PCAP_MAGICS[magic]
    vmaj, vmin, _tz, _sig, _snap, linktype = struct.unpack(
        endian + "HHIIII", data[4:24])
    if linktype != 1:
        raise ValueError("only Ethernet (LINKTYPE_ETHERNET=1) supported, "
                         "got %d" % linktype)
    offset = 24
    while offset + 16 <= len(data):
        ts_sec, ts_frac, incl, _orig = struct.unpack(
            endian + "IIII", data[offset:offset + 16])
        offset += 16
        frame = data[offset:offset + incl]
        if len(frame) < incl:
            raise ValueError("truncated packet record")
        offset += incl
        yield ts_sec, ts_frac, frame


def mac(raw):
    return ":".join("%02x" % b for b in raw)


def parse_frame(frame):
    """Decode one Ethernet frame into a summary dict."""
    if len(frame) < 14:
        return {"kind": "runt", "len": len(frame)}
    dst, src, ethertype = struct.unpack(">6s6sH", frame[:14])
    info = {"kind": "eth", "src_mac": mac(src), "dst_mac": mac(dst),
            "ethertype": ethertype, "len": len(frame)}
    payload = frame[14:]
    if ethertype == 0x0806:
        info["kind"] = "arp"
        return info
    if ethertype != 0x0800 or len(payload) < 20:
        return info
    version = payload[0] >> 4
    ihl = (payload[0] & 0x0F) * 4
    if version != 4:
        return info
    total_len, _ident, _frag, ttl, proto = struct.unpack(
        ">HHHBB", payload[2:10])
    info.update(kind="ipv4", src=socket.inet_ntoa(payload[12:16]),
                dst=socket.inet_ntoa(payload[16:20]), ttl=ttl,
                proto=IP_PROTO.get(proto, str(proto)), ip_len=total_len)
    if ihl < 20 or (total_len and total_len < ihl):
        # Header length is invalid (IHL is in 32-bit words, minimum 5),
        # so there is no trustworthy layer-4 offset to decode from.
        return info
    l4 = payload[ihl:total_len] if total_len else payload[ihl:]
    if proto == 6 and len(l4) >= 20:
        sport, dport, _seq, _ack = struct.unpack(">HHII", l4[:12])
        flags = l4[13]
        info.update(sport=sport, dport=dport,
                    flags=",".join(n for bit, n in TCP_FLAGS if flags & bit))
    elif proto == 17 and len(l4) >= 8:
        sport, dport, ulen = struct.unpack(">HHH", l4[:6])
        info.update(sport=sport, dport=dport, udp_len=ulen)
    return info


def describe(info):
    if info["kind"] == "ipv4" and "sport" in info:
        line = ("ipv4 %s %s:%d -> %s:%d len %d ttl %d"
                % (info["proto"], info["src"], info["sport"], info["dst"],
                   info["dport"], info["len"], info["ttl"]))
        if info.get("flags"):
            line += " [%s]" % info["flags"]
        return line
    if info["kind"] == "ipv4":
        return ("ipv4 %s %s -> %s len %d ttl %d"
                % (info["proto"], info["src"], info["dst"], info["len"],
                   info["ttl"]))
    if info["kind"] == "arp":
        return "arp %s -> %s len %d" % (info["src_mac"], info["dst_mac"],
                                        info["len"])
    return "eth type 0x%04x len %d" % (info.get("ethertype", 0), info["len"])


def main(argv=None):
    ap = argparse.ArgumentParser(description="pcap packet parser")
    ap.add_argument("file", help="path to a .pcap capture file")
    ap.add_argument("--limit", type=int, default=0,
                    help="stop after N packets (default: all)")
    args = ap.parse_args(argv)

    with open(args.file, "rb") as fh:
        data = fh.read()
    counts = Counter()
    shown = 0
    try:
        for _ts_sec, _ts_frac, frame in parse_pcap(data):
            info = parse_frame(frame)
            counts[info.get("proto", info["kind"])] += 1
            if not args.limit or shown < args.limit:
                print(describe(info))
                shown += 1
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    total = sum(counts.values())
    summary = ", ".join("%s %d" % (k, counts[k]) for k in sorted(counts))
    print("%d packets: %s" % (total, summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
