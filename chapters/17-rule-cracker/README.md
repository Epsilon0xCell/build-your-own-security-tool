# Chapter 17: Rule-Based Hash Cracker

**Status: planned.** Track: Credentials and crypto. Depends on: Chapter 5.

## Objective

Extend the Chapter 5 cracker with mangling rules: case changes, suffixes, substitutions, and combinations, which is where real cracking yield actually comes from.

## The mechanism, in outline

- Rules are functions from word to wordlist; a small rule set multiplies a dictionary by orders of magnitude.
- Yield is empirical: rules are ordered by observed success in real leaks, and the chapter measures each rule's hits on a generated fixture set.
- Generation order matters for time-to-first-crack; stream candidates rule-major versus word-major and compare.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Implement the hashcat-style rule subset used in the chapter.
2. Measure marginal yield per rule on fixtures you generate.
3. Add a two-word combination mode and budget its cost before running it.

## Defensive note (preview)

Still offline and silent; the defensive lesson deepens: password policy should test candidates against rules, not just dictionaries, before accepting them.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
