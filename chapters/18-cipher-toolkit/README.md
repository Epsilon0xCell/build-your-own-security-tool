# Chapter 18: Classical Cipher Toolkit and Breakers

**Status: planned.** Track: Credentials and crypto. Depends on: none (standalone).

## Objective

Implement Caesar, Vigenere, and XOR ciphers, then break each one: frequency analysis, key-length estimation, and known-plaintext recovery, to learn why keyspace and structure decide security.

## The mechanism, in outline

- Substitution preserves letter frequencies, so ciphertext betrays the plaintext's statistics.
- Vigenere hides frequency per position until the key length is found; index of coincidence finds it.
- XOR with a repeating key is Vigenere in binary; single-byte XOR falls to scoring candidate plaintexts by English likelihood.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Break a Vigenere ciphertext of unknown key length end to end.
2. Recover a repeating XOR key from a known plaintext fragment (crib dragging).
3. Score-based single-byte XOR breaker that ranks all 256 candidates.

## Defensive note (preview)

Classical ciphers appear in real malware and CTFs as obfuscation; defenders break them with exactly these statistics, which is why the chapter teaches attack and analysis as one skill.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
