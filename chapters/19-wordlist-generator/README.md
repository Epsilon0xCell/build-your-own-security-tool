# Chapter 19: Targeted Wordlist Generator

**Status: planned.** Track: Credentials and crypto. Depends on: Chapter 5.

## Objective

Build wordlists tailored to a target from names, dates, places, and patterns, the OSINT-driven candidate generation behind targeted password attacks and audits.

## The mechanism, in outline

- Permutation with separators, case variants, and year suffixes covers how people actually construct memorable passwords.
- Leet substitutions and keyboard walks add the next ring of candidates at measurable cost.
- Output size explodes combinatorially; the tool reports candidate counts before generating, as a discipline.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Generate a list for a fictional persona and audit its size growth per feature.
2. Feed the output into Chapter 17 and measure fixture hit rates versus the generic list.
3. Add deduplication that preserves first-occurrence order.

## Defensive note (preview)

Generation is offline; the defensive mirror is checking new passwords against targeted lists built from the account holder's own public data during enrolment.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
