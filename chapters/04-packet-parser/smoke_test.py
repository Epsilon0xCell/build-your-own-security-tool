#!/usr/bin/env python3
"""Smoke test for Chapter 4: generate the fixture, parse it, verify.

Runs make_fixture.py in a temp directory, then runs the parser on the
result and asserts the three synthetic packets decode to the fields
the generator put in: a TCP SYN to port 80, a UDP packet to port 53,
and a TCP packet carrying flags PSH and ACK.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent


def main():
    with tempfile.TemporaryDirectory() as tmp:
        gen = subprocess.run([sys.executable, str(HERE / "make_fixture.py")],
                             cwd=tmp, capture_output=True, text=True,
                             timeout=30)
        assert gen.returncode == 0, gen.stderr
        print(gen.stdout.strip())
        out = subprocess.run(
            [sys.executable, str(HERE / "packet_parser.py"), "fixture.pcap"],
            cwd=tmp, capture_output=True, text=True, timeout=30)
    print(out.stdout)
    assert out.returncode == 0, out.stderr
    assert "tcp 192.168.0.2:5150 -> 10.0.0.5:80" in out.stdout
    assert "[SYN]" in out.stdout
    assert "udp 192.168.0.2:5353 -> 192.168.0.1:53" in out.stdout
    assert "[PSH,ACK]" in out.stdout
    assert "3 packets: tcp 2, udp 1" in out.stdout
    print("SMOKE PASS: fixture generated and all three packets decoded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
