# Chapter 24: Reverse Shell and Listener (Lab Pair)

**Status: planned.** Track: Fuzzing and exploitation. Depends on: Chapter 10.

## Objective

Build both ends of a remote shell for your own lab machines: a listener that accepts a connection and a client that connects back and executes the commands it receives, to understand the mechanics defenders detect.

## The mechanism, in outline

- The client initiates the connection outbound, which is why reverse shells cross NAT and inbound firewalls that stop listeners.
- The channel is a socket spliced to a shell's stdin and stdout; job control and PTYs are the difference between a toy and a usable shell.
- Encryption is absent by design in v1; the chapter ends by adding a simple encrypted variant and comparing what network inspection can still see.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Run the pair between two lab machines or containers and drive a session.
2. Add a PTY upgrade and note what changes interactively.
3. Capture the session with Chapter 29's sniffer and list its detectable features.

## Defensive note (preview)

This is the curriculum's most detected pattern: unknown processes making outbound connections to rare ports, beacon-like timing, and shell processes with socket parents (EDR gold). Lab machines only, always.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
