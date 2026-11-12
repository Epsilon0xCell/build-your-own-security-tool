#!/usr/bin/env python3
"""Smoke test for Chapter 5: crack the bundled fixture hashes.

The fixtures are self-computed digests of fake demo passwords in the
bundled wordlist. The cracker must recover all three plaintexts, one
per algorithm (sha256, md5, sha1), and exit 0.
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXPECTED = ["demo-swordfish", "demo-hunter2", "demo-correct-horse"]


def main():
    out = subprocess.run(
        [sys.executable, str(HERE / "hash_cracker.py"),
         str(HERE / "hashes.txt"), str(HERE / "wordlist.txt")],
        capture_output=True, text=True, timeout=60)
    print(out.stdout)
    assert out.returncode == 0, out.stderr
    for word in EXPECTED:
        assert "-> %s" % word in out.stdout, "did not crack %s" % word
    assert "3/3 cracked" in out.stdout
    print("SMOKE PASS: all three fixture hashes cracked, one per algorithm")
    return 0


if __name__ == "__main__":
    sys.exit(main())
