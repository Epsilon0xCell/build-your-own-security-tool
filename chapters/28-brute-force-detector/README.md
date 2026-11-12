# Chapter 28: Brute-Force Login Detector

**Status: planned.** Track: Detection and defence. Depends on: Chapter 25.

## Objective

Detect credential guessing in authentication logs: threshold, window, and distribution rules that separate attacks from users who forgot their passwords, tuned on the Chapter 20 lab's logs.

## The mechanism, in outline

- The signal is rate and shape: failures per account, per source, and per password across accounts each catch a different attack style (guessing versus spraying).
- Tuning is a measured trade-off between detection delay and false alarms on real user behaviour; the chapter plots both.
- Alert quality decides whether anyone reads the next alert; the output is a verdict with evidence, not a count.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Catch the Chapter 20 attack in its own logs with all three rules.
2. Show a spraying attack evading the per-account rule and being caught by the per-password rule.
3. Write the incident summary the detector should emit.

## Defensive note (preview)

This is detection engineering end to end: the chapter's rules, thresholds, and false-positive budget are the same artifacts a SOC ships.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
