# Chapter 4: Packet Parser for PCAP Files

**Status: complete.** Files: `packet_parser.py`, `make_fixture.py`.
Test: `smoke_test.py`.

## What you are building

A reader for the libpcap capture format: it opens a `.pcap` file,
walks its packet records, and decodes Ethernet, IPv4, TCP, and UDP
headers into one summary line per packet, plus protocol counts. This
is the offline half of every network tool you will ever use, and the
foundation for the sniffer and detector chapters later in the map.

## Why it works that way: the mechanism

A pcap file is a 24-byte global header followed by records: per
packet, a 16-byte record header (timestamp seconds and microseconds,
captured length, original length) and then the frame bytes.

The global header starts with a magic number that smuggles in two
facts: the byte order of the file and whether timestamps are micro or
nanoseconds. Read the magic as big-endian: `0xA1B2C3D4` means the file
is big-endian; `0xD4C3B2A1` means the same fields stored
little-endian; the `0xA1B23C4D` family is the nanosecond variant.
Every multi-byte field after that must be unpacked with the endianness
the magic announced, which is why the parser keys its `struct` format
off the first four bytes.

Frames then decode as nested envelopes: Ethernet says where the IP
packet starts (offset 14, when the EtherType is 0x0800), the IPv4
header length field (IHL) says where the transport header starts, and
TCP or UDP fields follow. Nothing in the format is self-describing
beyond that chain; a parser is just disciplined offset arithmetic,
plus the IPv4 header checksum that lets you verify you got it right.

## Build it

1. Read the global header; select endianness from the magic; reject
   non-Ethernet link types rather than decoding them wrong.
2. Iterate records: read the 16-byte record header, slice exactly
   `incl_len` frame bytes, advance.
3. Parse Ethernet: destination and source MAC, EtherType. Branch on
   EtherType: ARP gets a summary, 0x0800 continues to IPv4.
4. Parse IPv4: version and IHL from the first byte, total length, TTL,
   protocol, source and destination addresses with `inet_ntoa`.
5. Parse the transport header at offset IHL: ports for TCP and UDP,
   and for TCP the flag byte expanded to names (SYN, ACK, PSH, ...).
6. Count as you go and print a protocol summary at the end; in real
   analysis the counts are usually the first useful answer.

The fixture generator builds the mirror image: it assembles three
frames with `struct`, computing the IPv4 header checksum properly
(one's complement sum over the header), and wraps them in a pcap
container. Transport checksums are zero, as captures with checksum
offloading also show; the parser does not validate them.

## Run it

```text
$ python3 make_fixture.py
wrote fixture.pcap with 3 packets
$ python3 packet_parser.py fixture.pcap
ipv4 tcp 192.168.0.2:5150 -> 10.0.0.5:80 len 54 ttl 64 [SYN]
ipv4 udp 192.168.0.2:5353 -> 192.168.0.1:53 len 61 ttl 64
ipv4 tcp 192.168.0.2:5150 -> 10.0.0.5:80 len 72 ttl 64 [PSH,ACK]
3 packets: tcp 2, udp 1
```

## Smoke test

`smoke_test.py` runs the generator in a temp directory, parses the
result, and asserts all three packets decode to the exact fields the
generator encoded, including both flag combinations and the summary
counts:

```text
SMOKE PASS: fixture generated and all three packets decoded
```

## Exercises

1. Add IPv6 decoding: fixed 40-byte header, next-header chain for TCP
   and UDP. Generate a v6 fixture packet to prove it.
2. Verify the IPv4 header checksum while parsing and flag packets
   where it fails. Run it on the fixture: it must pass. Corrupt one
   byte and watch it fail.
3. Add a `--follow` mode that groups packets into flows (the 4-tuple
   of both addresses and both ports) and prints one line per flow
   with packet and byte totals.
4. Decode the DNS message inside the fixture's UDP packet using
   Chapter 2's `decode_name`. The two chapters were designed to meet
   here.

## Defensive note: how this appears in telemetry

It does not: parsing a file is silent. That is the point of the
chapter pairing in this curriculum. Chapters 1 to 3 generate traffic a
defender can see; this one builds the defender's reading skill on the
same protocols. In real investigations this exact work, opening a
capture and establishing who talked to whom, on which ports, with
which flags, is the first hour of network forensics, and the counts
summary is usually what an incident timeline is built from.
