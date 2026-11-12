# Chapter 27: Honeypot: Fake Login Service that Logs Attempts

**Status: planned.** Track: Detection and defence. Depends on: Chapters 1 and 24.

## Objective

Run a fake SSH-style login service that accepts nothing, logs everything, and profiles who knocks: the simplest deception tool, and a safe way to watch real attack traffic on your own network.

## The mechanism, in outline

- The service speaks just enough protocol to hold a conversation: banner, prompts, plausible delays.
- Value comes from the log schema: source, timing, credentials tried, session behaviour, designed before the service is.
- Isolation is the safety property: the honeypot must be able to give an attacker nothing real, even if its own code fails.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Deploy on a lab VM and collect a week of attempts.
2. Rank attempted credentials and compare with Chapter 19's generator output.
3. Feed the logs into Chapter 25 and build the summary report.

## Defensive note (preview)

A honeypot is pure sensor: any interaction with it is suspicious by definition, which is why its alerts need almost no tuning. Its own footprint should be indistinguishable from a real, quiet service.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
