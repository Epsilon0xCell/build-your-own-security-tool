# Chapter 23: Stack Buffer Overflow Lab

**Status: planned.** Track: Fuzzing and exploitation. Depends on: Chapter 21.

## Objective

Exploit a deliberately vulnerable C program in a local lab: overflow its stack buffer, control the instruction pointer, and understand precisely which modern mitigations stop you and why.

## The mechanism, in outline

- The stack holds saved registers and the return address beside buffers; writing past a buffer rewrites control data.
- ASLR, stack canaries, and non-executable memory each break one step of the classic exploit, and the lab toggles them one at a time.
- Reliable exploitation is offset measurement, not luck: cyclic patterns locate the exact overwrite point.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Crash the lab binary and find the offset with a cyclic pattern.
2. Redirect execution to a function already in the binary.
3. Rebuild with each mitigation and document which step each one defeats.

## Defensive note (preview)

Exploitation is local lab work; the telemetry lesson is in the crash artifacts: defenders collect exactly the core dumps and faulting offsets this chapter teaches you to read.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
