# Chapter 5: Hash Cracker

**Status: complete.** Files: `hash_cracker.py`, `wordlist.txt`,
`hashes.txt`. Test: `smoke_test.py`.

## What you are building

A dictionary cracker: given a file of password hashes and a wordlist,
it hashes every candidate and reports which passwords produced the
target hashes. The bundled fixtures are hashes we computed ourselves,
on this machine, of fake demo passwords in the bundled wordlist. They
protect nothing; they exist so the cracker has something real to find.

## Why it works that way: the mechanism

A cryptographic hash is one-way: you cannot run it backwards. But you
do not need to. Passwords are not random strings, they are chosen by
humans from a small, skewed space of words, names, and patterns. So
the attack runs the hash *forwards*: take a candidate, hash it,
compare. The hash function itself tells you when you win, because it
is deterministic: the same input always produces the same digest.

Three facts shape every real cracking tool, and all three are visible
in this small one:

- **Algorithm detection is length.** A hex MD5 digest is 32
  characters, SHA-1 is 40, SHA-256 is 64. The cracker groups targets
  by length and only runs the relevant algorithm per group.
- **Speed is the whole game.** The mechanism never changes; hashcat is
  this loop with GPUs, smarter candidate generation (rules that mangle
  words), and better dictionaries. Our loop tries thousands of words
  per second in pure Python; a GPU rig tries billions against fast
  hashes.
- **Salting is the defence that matters.** An unsalted hash can be
  attacked once for all users at once (and precomputed in rainbow
  tables). A unique salt per password forces per-user work, and a
  slow password hash (bcrypt, scrypt, Argon2) makes each guess
  expensive. Nothing in this chapter's fixtures is salted, on purpose:
  you are studying the attack in its cleanest form.

## Build it

1. Load targets: one hex digest per line, skip comments and blanks,
   reject lines that are not hex of a known digest length.
2. Group digests by detected algorithm, so each candidate word is
   hashed once per algorithm actually present, not once per hash.
3. Stream the wordlist (never load it whole; real lists are
   gigabytes) and for each word compute the digest per group and test
   membership in a set.
4. On a match, record the plaintext, drop the digest from its group,
   and stop early when nothing remains.
5. Print each crack as it happens, then a summary with the candidate
   count, so a long run shows progress honestly.

## Run it

```text
$ python3 hash_cracker.py hashes.txt wordlist.txt
sha256:d54f1150f4ac76fb4196a2dc6838d3da33f7fa4760eeaac98801196c4779fd78 -> demo-swordfish
md5:428f79cd513ff223ca3a002e4911f5ab -> demo-hunter2
sha1:b00c2c9356b88467325926760ff9f88e2312131a -> demo-correct-horse
tried 16 candidates: 3/3 cracked
```

Sixteen candidates, not thirty-one: the cracker stopped as soon as
every target fell, and the third target sat at line 16 of the list.

## Smoke test

`smoke_test.py` runs the cracker on the bundled fixtures and asserts
all three plaintexts are recovered, one per algorithm, with exit
code 0:

```text
SMOKE PASS: all three fixture hashes cracked, one per algorithm
```

## Exercises

1. Add mangling rules: capitalise the first letter, append `1`,
   append the current year, leetspeak substitutions. Re-crack with a
   wordlist that contains only the base words and watch the fixtures
   fall to rules instead of dictionary entries.
2. Benchmark: time 100,000 MD5 candidates and 100,000 SHA-256
   candidates. Compute hashes per second for each and explain the
   ratio from the algorithms' designs.
3. Write the defender's version: a checker that reports whether a
   proposed password appears in a given wordlist, without storing the
   password.
4. Extend the loader to accept `user:hash` lines (the shape of a
   leaked database row) and print cracks per user. Use only fixtures
   you generate yourself.

## Defensive note: how this appears in telemetry

Offline cracking leaves no telemetry on your network at all, which is
precisely why credential defence is about denying the attacker the
hashes and making each guess expensive: salted, slow password hashing
(Argon2id, bcrypt), MFA so a cracked password alone is insufficient,
and breach monitoring for your organisation's domains. Where cracking
does surface is upstream: the database theft, the LSASS dump, the
`/etc/shadow` read. Defenders instrument those reads, because by the
time hashes are in a cracker, the observable part of the attack is
already over.
