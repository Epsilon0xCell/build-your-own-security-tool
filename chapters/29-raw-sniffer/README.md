# Chapter 29: Live Packet Sniffer with Raw Sockets

**Status: planned.** Track: Detection and defence. Depends on: Chapter 4.

## Objective

Capture live traffic with raw sockets and feed it to the Chapter 4 parser, closing the loop from files to the wire, with display filters you implement yourself.

## The mechanism, in outline

- AF_PACKET sockets deliver frames before the IP stack consumes them; promiscuous mode decides whose frames you see.
- Capture and analysis separate for a reason: the capture loop must never drop because the printer is slow, so a ring buffer sits between them.
- Filters are predicates over parsed fields; implementing three (host, port, protocol) teaches the shape of tcpdump's BPF from the user's side.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Capture a Chapter 3 proxy session and reconstruct the request from raw frames.
2. Add host and port filters and verify them against generated traffic.
3. Measure drop counts under load and explain where they happen.

## Defensive note (preview)

Sniffing your own traffic on your own machines is administration; on anyone else's it is interception. The chapter's captures double as the evidence base for several defensive notes.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
