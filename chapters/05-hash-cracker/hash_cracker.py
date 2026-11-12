#!/usr/bin/env python3
"""Chapter 5: a dictionary hash cracker.

Reads target hashes (one per line), detects the algorithm from the
digest length, and tries every word in a wordlist until each hash is
matched. This is the whole mechanism behind real cracking: the speed
of tools like hashcat comes from hardware and rules, not from a
different idea.

Usage:
    python3 hash_cracker.py hashes.txt wordlist.txt
    python3 hash_cracker.py hashes.txt wordlist.txt --algo sha256

The bundled hashes.txt contains self-computed hashes of the fake demo
passwords in the bundled wordlist.txt. They protect nothing.
"""

import argparse
import hashlib
import sys

LENGTH_TO_ALGO = {32: "md5", 40: "sha1", 56: "sha224", 64: "sha256",
                  96: "sha384", 128: "sha512"}
HEX = set("0123456789abcdef")


def load_hashes(path):
    """Return {digest: None} for valid hex lines, comments skipped."""
    targets = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            digest = line.strip().lower()
            if not digest or digest.startswith("#"):
                continue
            if set(digest) <= HEX and len(digest) in LENGTH_TO_ALGO:
                targets[digest] = None
            else:
                print("skipping unrecognised line: %s" % digest,
                      file=sys.stderr)
    return targets


def group_by_algo(targets, forced_algo=None):
    groups = {}
    for digest in targets:
        algo = forced_algo or LENGTH_TO_ALGO[len(digest)]
        groups.setdefault(algo, set()).add(digest)
    return groups


def crack(targets, wordlist_path, forced_algo=None):
    """Try every candidate against every still-uncracked hash."""
    groups = group_by_algo(targets, forced_algo)
    remaining = sum(len(v) for v in groups.values())
    tried = 0
    with open(wordlist_path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            word = line.rstrip("\n")
            if not word:
                continue
            tried += 1
            for algo, digests in groups.items():
                if not digests:
                    continue
                candidate = hashlib.new(algo, word.encode()).hexdigest()
                if candidate in digests:
                    targets[candidate] = word
                    digests.discard(candidate)
                    remaining -= 1
                    print("%s:%s -> %s" % (algo, candidate, word))
            if remaining == 0:
                break
    return tried


def main(argv=None):
    ap = argparse.ArgumentParser(description="dictionary hash cracker")
    ap.add_argument("hashes", help="file of hex digests, one per line")
    ap.add_argument("wordlist", help="candidate passwords, one per line")
    ap.add_argument("--algo", choices=sorted(set(LENGTH_TO_ALGO.values())),
                    help="force one algorithm instead of length detection")
    args = ap.parse_args(argv)

    targets = load_hashes(args.hashes)
    if not targets:
        print("error: no usable hashes in %s" % args.hashes, file=sys.stderr)
        return 2
    tried = crack(targets, args.wordlist, args.algo)
    found = sum(1 for v in targets.values() if v is not None)
    print("tried %d candidates: %d/%d cracked"
          % (tried, found, len(targets)))
    return 0 if found == len(targets) else 1


if __name__ == "__main__":
    sys.exit(main())
