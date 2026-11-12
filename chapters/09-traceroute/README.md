# Chapter 9: Traceroute from ICMP and TTL

**Status: planned.** Track: Recon and discovery. Depends on: Chapter 4.

## Objective

Map the path packets take to a target by exploiting the TTL field: each router that decrements TTL to zero reports itself, revealing the route hop by hop.

## The mechanism, in outline

- IPv4 TTL exists to kill looping packets; routers discard at zero and send ICMP Time Exceeded, naming themselves in the process.
- Probes go out with TTL 1, 2, 3, ... and the replies, ordered by TTL, are the path.
- ICMP, UDP, and TCP probe variants see different paths because firewalls treat them differently; real tools offer all three.
- A hop that answers nothing is information too: filtering, not absence.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Trace routes to three destinations and identify where paths diverge.
2. Implement the TCP variant and compare its path to the ICMP one.
3. Graph RTT per hop over repeated runs and explain the variance.

## Defensive note (preview)

Traceroute is low-noise and usually lost in normal ICMP, but sequential TTL probes to one destination have a distinctive shape in flow records.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
