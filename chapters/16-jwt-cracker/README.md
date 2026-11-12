# Chapter 16: JWT Decoder and Weak-Secret Cracker

**Status: planned.** Track: Web tooling. Depends on: Chapter 5.

## Objective

Decode JSON Web Tokens, verify their signatures yourself, and crack weak HMAC secrets with the Chapter 5 dictionary mechanism, including the classic alg=none and key-confusion failure modes.

## The mechanism, in outline

- A JWT is three base64url segments; the signature covers the first two, so decoding is trivial and trust rests entirely on verification.
- HS256 verification is HMAC with a shared secret, which makes offline dictionary attack possible whenever the secret is weak.
- The alg field is attacker-controlled input to the verifier; accepting none, or treating an RSA public key as an HMAC secret, are the two canonical implementation failures.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Generate tokens with a demo secret, crack them, and forge an admin token for your lab app.
2. Demonstrate alg=none against a deliberately naive verifier you write.
3. Write the verifier correctly and show both attacks failing.

## Defensive note (preview)

Forged tokens in logs look like valid sessions; detection lives in key hygiene (long random secrets, pinned algorithms) and in impossible-session analytics, not in spotting the forgery itself.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
