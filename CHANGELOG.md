# Changelog

All notable changes to this curriculum are recorded here.
The format follows Keep a Changelog, and versions follow Semantic
Versioning.

## [0.1.0] - 2026-11-12

### Added

- The full 30-chapter curriculum map in dependency order, as a
  checkbox progress table in the README, with every chapter honestly
  marked complete or planned.
- Chapter 1, Port Scanner: threaded TCP connect scanner with banner
  grabbing, plus a smoke test that proves it against localhost
  listeners.
- Chapter 2, DNS Resolver: DNS over raw UDP with hand-built query
  packets and full response parsing including compressed names, plus
  a smoke test against a local fake DNS server.
- Chapter 3, HTTP Forward Proxy: absolute-form proxying with request
  rewriting and response relay, plus a smoke test that fetches a
  localhost origin through the proxy.
- Chapter 4, Packet Parser: pcap reader decoding Ethernet, IPv4, TCP,
  and UDP, with a synthetic fixture generator and a smoke test that
  verifies generated packets decode to the encoded fields.
- Chapter 5, Hash Cracker: dictionary cracker with algorithm
  detection by digest length, plus fixtures (self-computed hashes of
  fake demo passwords, labelled as such) and a smoke test.
- Structured specifications for Chapters 6 to 30: objectives,
  mechanism outlines, and draft exercises for every planned chapter.
- MIT license, contributing guide, and the chapter anatomy every
  future chapter is reviewed against.
