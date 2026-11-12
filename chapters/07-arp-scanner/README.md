# Chapter 7: ARP Scanner and LAN Host Discovery

**Status: planned.** Track: Recon and discovery. Depends on: Chapter 4.

## Objective

Enumerate every live host on a local network segment by asking the question switches cannot ignore: who has this IP? Produces the host inventory port scanning a whole subnet would take far longer to build.

## The mechanism, in outline

- ARP resolves IP to MAC inside a subnet; requests are broadcast, so every host hears them, and the owner must answer.
- Raw sockets (AF_PACKET) are required because ARP is below IP; this is the curriculum's first privileged tool.
- Answers arrive asynchronously, so the tool is a listener with a table, not a request-response loop.
- The IP-to-MAC table it builds is also the baseline ARP spoofing detectors compare against.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Scan your home lab subnet and reconcile the results with your router's client list.
2. Detect a second MAC claiming the gateway IP in a capture you generate.
3. Add OUI lookup to name the vendor of each MAC address.

## Defensive note (preview)

ARP sweeps are broadcast and visible to every host and switch on the segment; network monitors flag full-subnet sweeps, and the reply table is prime detection data.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
