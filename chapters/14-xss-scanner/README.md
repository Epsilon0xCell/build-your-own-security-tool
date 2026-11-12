# Chapter 14: Reflected XSS Scanner

**Status: planned.** Track: Web tooling. Depends on: Chapters 11 and 13.

## Objective

Test a page's parameters for reflected cross-site scripting by injecting unique marker payloads and checking whether they return unencoded in the response, against a deliberately vulnerable lab app built for this chapter.

## The mechanism, in outline

- Reflection is detectable without executing anything: a unique token distinguishes your input from page content, and its surrounding context (HTML, attribute, script) decides exploitability.
- Encoding is the defence, so the scanner checks which characters survive unescaped rather than spraying a payload list.
- Context determines the working payload; the chapter classifies the reflection point before choosing one.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Build the lab app with three reflection contexts and scan it.
2. Show the scanner ignoring a properly encoded reflection.
3. Add DOM-based detection notes for a client-side variant.

## Defensive note (preview)

Scanner payloads are unmistakable in WAF logs and the payloads themselves are the detection signature; run only against the lab app and your own sites.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
