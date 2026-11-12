# Chapter 30: Capstone: Your Own Recon Suite

**Status: planned.** Track: Capstone. Depends on: Chapters 1, 2, 6, 8, and 12.

## Objective

Combine the curriculum's recon tools into one suite with a shared target model: enumerate subdomains, resolve them, scan them, fingerprint services, probe web paths, and emit one report, the portfolio piece the whole map points at.

## The mechanism, in outline

- A suite is an interface problem: each tool's output must become the next tool's input without shell glue, so the data model (hosts, ports, services, findings) is designed first.
- Concurrency and rate policy are global decisions now, not per-tool accidents; the suite owns them.
- Reporting is a feature: the final artifact is a readable, evidence-linked report in the style of the vuln-report-kit.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Run the suite against a lab environment you built for it and review the report as a client would.
2. Add one tool from the planned list as a suite module without changing its CLI.
3. Write the suite's own threat model: what it must never do by accident.

## Defensive note (preview)

Suites amplify everything, including noise and mistakes; the capstone's defensive note is a review of the whole curriculum's telemetry, and its scope controls are the graduation requirement.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
