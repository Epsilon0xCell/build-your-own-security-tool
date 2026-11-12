# Contributing

Contributions are welcome in three shapes: completing a planned
chapter, porting a finished chapter to another language, and
improving a finished chapter (clearer mechanism sections, better
exercises, stronger smoke tests).

## Completing a planned chapter

Each planned chapter's README is its specification: objective,
mechanism outline, and draft exercises. A completed chapter replaces
that file and follows the anatomy of Chapters 1 to 5 exactly:

1. **What you are building**: one paragraph.
2. **The mechanism**: the protocol or primitive from first
   principles, in terms a reader who finished the earlier chapters
   can follow. No hand-waving past the interesting part.
3. **Build it**: numbered steps that map visibly onto the code.
4. **Complete implementation**: one runnable file (or a small number)
   in the chapter directory, standard library only unless the chapter
   itself is about a library.
5. **Run it**: real commands with real output captured from an actual
   run.
6. **Smoke test**: `smoke_test.py` (or the language equivalent) that
   proves the tool performs its core function against local,
   self-owned targets only: localhost listeners, self-generated
   fixtures, self-computed hashes. It must pass from a clean checkout.
7. **Exercises**: at least three, each extending the mechanism rather
   than adding decoration.
8. **Defensive note**: how the tool appears in telemetry and what
   detects it. No chapter ships without one.

Update the README progress table in the same pull request: flip the
checkbox, and only when the smoke test passes.

## Language ports

Ports live beside the Python original (for example
`port_scanner.go` in the chapter directory) and must implement the
same core behaviour and pass an equivalent smoke test. The chapter
text stays shared; do not fork the README per language.

## Rules for every contribution

- **Authorised use only.** Tools and tests target systems the
  contributor owns: localhost, lab VMs, containers, fixtures. No
  third-party targets, no captured real-world data, no credentials
  that protect anything real. Fixture secrets must be self-generated
  and labelled as fixtures.
- **No filler.** If a section has nothing true and specific to say,
  write less. Planned chapters stay marked planned until they meet
  the anatomy above in full.
- **Style.** Plain prose, short paragraphs, hyphenated compound
  adjectives, no em dashes. Code comments explain why, not what.
- **Tests are not optional.** A pull request that changes a tool
  runs its chapter's smoke test and says so in the description.

## Pull request process

1. Open an issue first for a new chapter completion or a port, so two
   people do not build the same chapter.
2. One chapter per pull request.
3. Keep the diff reviewable: implementation, chapter text, and the
   progress-table flip.

By contributing you agree your work is released under the MIT
license in this repository.
