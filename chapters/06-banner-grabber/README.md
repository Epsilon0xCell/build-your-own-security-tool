# Chapter 6: Banner Grabber and Service Fingerprinter

**Status: planned.** Track: Recon and discovery. Depends on: Chapter 1.

## Objective

Given a host and open ports, identify what each service actually is: protocol, product, and version where the service reveals it, from banners and probe responses rather than port-number guesses.

## The mechanism, in outline

- Services split into speak-first (SSH, SMTP, FTP) and speak-on-request (HTTP) families; the fingerprinter needs a probe table, not one behaviour.
- Passive fingerprinting reads the greeting; active fingerprinting sends a harmless malformed request and reads the error, which often reveals more.
- Version strings map to known vulnerability ranges, which is why this output feeds every later recon chapter.
- Timing and TCP behaviour (window size, options order) fingerprint the OS separately from the application.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Fingerprint five services on your own lab machines and compare against nmap -sV output.
2. Add one probe of your own design for a service the table misses.
3. Record where banner and probe disagree, and decide which you trust and why.

## Defensive note (preview)

Services log unexpected probes and malformed requests; fingerprinting is quieter than scanning but not silent, and version disclosure in banners is itself a finding defenders act on.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
