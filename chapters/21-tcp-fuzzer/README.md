# Chapter 21: Dumb Fuzzer for a TCP Service

**Status: planned.** Track: Fuzzing and exploitation. Depends on: Chapter 1.

## Objective

Send malformed and oversized inputs to a network service and watch for crashes: generation and mutation fuzzing against a deliberately fragile server written for this chapter.

## The mechanism, in outline

- A fuzzer is a loop: generate input, deliver, monitor health, record what breaks it; the intelligence is in the bookkeeping.
- Health checking needs an independent channel (a banner probe), or a hang and a crash look identical.
- Crashing inputs must be minimised and saved byte-exact, or the finding cannot be reproduced or fixed.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Find the lab server's crash with random data, then with structure-aware mutations, and compare input counts.
2. Add automatic minimisation of a crashing input.
3. Restart-and-resume: make the fuzzer survive its target's death.

## Defensive note (preview)

Fuzzing looks like an attack because it is one, against software you own; in telemetry it resembles the Chapter 12 brute-forcer's burst pattern with malformed payloads in the logs.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
