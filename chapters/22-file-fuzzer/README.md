# Chapter 22: Mutation Fuzzer for File Formats

**Status: planned.** Track: Fuzzing and exploitation. Depends on: Chapter 4.

## Objective

Mutate valid files (starting with the Chapter 4 pcap fixture) and feed them to a target parser, hunting the inputs that crash or hang it, and triaging what you find.

## The mechanism, in outline

- Mutation operators are small (bit flips, boundary numbers, truncation, duplication) because parsers fail at edges, not in middles.
- A corpus of valid seeds beats random bytes: structure survives mutation, so deep code paths stay reachable.
- Exit codes and timeouts are the oracle; sanitizer builds make the oracle precise, which the chapter sets up with a C parser.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Fuzz the Chapter 4 parser itself and fix what you find.
2. Build a corpus from fixtures across the curriculum and measure coverage of code paths.
3. Write a triage report for one crash: input, stack, suspected cause.

## Defensive note (preview)

File fuzzing is local and silent; the transferable defence is that every parser you ship should survive its own fuzzer, a test this curriculum applies to itself.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
