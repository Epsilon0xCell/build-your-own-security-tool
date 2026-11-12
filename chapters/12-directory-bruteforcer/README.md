# Chapter 12: Directory and File Brute-Forcer

**Status: planned.** Track: Web tooling. Depends on: Chapter 11.

## Objective

Find hidden paths on a web server (admin panels, backups, config files) by requesting candidate names from a wordlist and reading the status codes, the ffuf and gobuster mechanism reduced to its core.

## The mechanism, in outline

- Existence leaks through responses: 200, 403, and 404 are all answers, and 403 often confirms a real path best.
- Soft-404s (custom error pages returning 200) defeat naive checks; calibration requests with random names establish the site's true not-found signature first.
- Extensions multiply the list (.php, .bak, .zip) and rate limits punish greed; threads and throttling are a trade-off you tune.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Run it against a local test site you control, with planted hidden paths.
2. Implement soft-404 calibration and show a false positive it removes.
3. Add extension fuzzing and recursive discovery of found directories.

## Defensive note (preview)

This is one of the loudest web techniques: WAFs and log review catch dictionary-shaped request bursts and 404 spikes quickly. Authorised testing only, against your own lab sites.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
