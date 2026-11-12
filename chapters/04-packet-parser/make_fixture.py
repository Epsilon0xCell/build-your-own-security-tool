#!/usr/bin/env python3
"""Build fixture.pcap: three synthetic packets, generated locally.

The fixture exists so the parser chapter works offline with captures
you made yourself. Addresses are private/documentation ranges and the
payloads are inert text. Transport checksums are set to zero, which
real captures also show when checksum offloading is on; the parser in
this chapter does not validate them. The IPv4 header checksum is
computed properly, because building it is half the lesson.
"""

import socket
import struct

SRC_MAC = bytes.fromhex("020000000001")
DST_MAC = bytes.fromhex("020000000002")


def ip_checksum(header):
    if len(header) % 2:
        header += b"\x00"
    total = sum(struct.unpack(">%dH" % (len(header) // 2), header))
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def ipv4(src, dst, proto, payload, ident):
    ihl = 20
    header = struct.pack(">BBHHHBBH", 0x45, 0, ihl + len(payload), ident,
                         0x4000, 64, proto, 0)
    header += socket.inet_aton(src) + socket.inet_aton(dst)
    csum = ip_checksum(header)
    header = header[:10] + struct.pack(">H", csum) + header[12:]
    return header + payload


def ethernet(payload, ethertype=0x0800):
    return DST_MAC + SRC_MAC + struct.pack(">H", ethertype) + payload


def tcp_packet(src, dst, sport, dport, flags, payload=b"", seq=1000):
    header = struct.pack(">HHIIBBHHH", sport, dport, seq, 0, 5 << 4,
                         flags, 65535, 0, 0)
    return ethernet(ipv4(src, dst, 6, header + payload, ident=seq))


def udp_packet(src, dst, sport, dport, payload):
    header = struct.pack(">HHHH", sport, dport, 8 + len(payload), 0)
    return ethernet(ipv4(src, dst, 17, header + payload, ident=7))


def main():
    syn = tcp_packet("192.168.0.2", "10.0.0.5", 5150, 80, flags=0x02)
    dns = udp_packet("192.168.0.2", "192.168.0.1", 5353, 53,
                     b"\x12\x34\x01\x00synthetic-query")
    http = tcp_packet("192.168.0.2", "10.0.0.5", 5150, 80, flags=0x18,
                      payload=b"GET / HTTP/1.0\r\n\r\n", seq=1001)
    packets = [syn, dns, http]
    out = [struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)]
    for i, frame in enumerate(packets):
        out.append(struct.pack("<IIII", 1700000000 + i, 250000 * i,
                               len(frame), len(frame)))
        out.append(frame)
    with open("fixture.pcap", "wb") as fh:
        fh.write(b"".join(out))
    print("wrote fixture.pcap with %d packets" % len(packets))


if __name__ == "__main__":
    main()
