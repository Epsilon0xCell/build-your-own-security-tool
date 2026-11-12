# Chapter 26: Mini Signature Scanner (YARA-lite)

**Status: planned.** Track: Detection and defence. Depends on: Chapter 22.

## Objective

Scan files against human-written signatures (strings, byte patterns, and simple conditions) in a small rule language you design and implement.

## The mechanism, in outline

- Signatures are predicates over content: literal strings, hex patterns with wildcards, and occurrence conditions.
- Efficient matching is the engineering: one pass with all literals indexed (Aho-Corasick) instead of one scan per rule.
- False positives are a property of the rule, not the scanner; the chapter measures both on a labelled fixture set.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Write rules that catch the curriculum's own lab artifacts and nothing else.
2. Benchmark naive versus indexed matching on a large file tree.
3. Add a condition language: counts, offsets, and file size predicates.

## Defensive note (preview)

Signature scanning is the oldest detection mechanism there is; building it shows both its power (precision) and its limit (it finds what it already knows).

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
