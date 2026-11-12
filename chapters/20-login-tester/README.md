# Chapter 20: Login Form Tester against a Local Lab

**Status: planned.** Track: Credentials and crypto. Depends on: Chapter 11.

## Objective

Test a login form's resistance to credential guessing using a lab authentication server built for this chapter, with lockout and rate limiting you can switch on to watch the attack fail.

## The mechanism, in outline

- The mechanism is Chapter 11's client plus session handling; the new content is server responses: lockout, backoff, CAPTCHA, and uniform error messages each change the attacker's arithmetic differently.
- Trying many passwords against one account and one password against many accounts (spraying) are different shapes with different detection profiles; the lab demonstrates both.
- Success is a session cookie, so the tester must handle cookies and redirects correctly or it reports false negatives.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Run a guessing attack against the lab with defences off, then on, and compare.
2. Implement spraying mode and chart attempts per account over time.
3. Write the lab's lockout policy yourself and tune it against the attack.

## Defensive note (preview)

This is the most directly detectable technique in the curriculum: auth logs show it plainly, and the chapter's detector (Chapter 28) is built from the lab's own logs. Never run it against services you do not own.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
