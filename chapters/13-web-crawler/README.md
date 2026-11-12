# Chapter 13: Web Crawler and Link Extractor

**Status: planned.** Track: Web tooling. Depends on: Chapters 11 and 4.

## Objective

Walk a site the way a search engine does: fetch a page, extract links and forms, queue the unseen, and produce the site map that every web assessment starts from.

## The mechanism, in outline

- URLs need normalising (relative links, fragments, default ports) before they can be deduplicated, or the crawler loops forever.
- Breadth-first order plus a visited set is the whole algorithm; politeness (rate, robots.txt) is policy layered on it.
- Forms and parameters are attack surface, so the crawler records them as first-class output, not just pages.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Crawl a local copy of a small site and diff the map against its file tree.
2. Extract every form's fields and methods into a report.
3. Add depth and scope limits and prove out-of-scope links are never fetched.

## Defensive note (preview)

Crawlers resemble scanners in logs but at human-plausible rates; scope creep onto third-party sites is both a detection event and an authorisation breach.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
