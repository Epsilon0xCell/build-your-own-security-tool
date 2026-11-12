# Chapter 15: SQL Injection Probe

**Status: planned.** Track: Web tooling. Depends on: Chapter 11.

## Objective

Probe a parameter for SQL injection using error, boolean, and timing evidence, against a local lab application with a real database whose queries you can inspect.

## The mechanism, in outline

- Injection is a grammar confusion: user input becomes query syntax because the application concatenates strings.
- Three evidence channels exist: database errors leak syntax, boolean pairs (true and false conditions) change the page, and deliberate delays (SLEEP) answer through time when nothing else differs.
- Parameterised queries are the structural fix, and the lab app ships both the vulnerable and the fixed endpoint so you can watch the same probe fail.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Extract one character of a lab database value using only boolean responses.
2. Repeat with timing when the lab app hides all errors and differences.
3. Patch the lab app and demonstrate the probe's evidence channels all closing.

## Defensive note (preview)

Probes are visible in application and database logs (error spikes, delay patterns); the fixed endpoint's logs show what defenders alert on when probing fails too.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
