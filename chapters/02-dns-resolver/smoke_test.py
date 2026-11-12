#!/usr/bin/env python3
"""Smoke test for Chapter 2: resolve through a fake local DNS server.

Runs a one-shot UDP server on 127.0.0.1 that answers any A query with
the documentation address 192.0.2.55 (TEST-NET-1, RFC 5737), using a
compression pointer for the answer name. The resolver must build a
well-formed query the fake server can parse, and decode the response,
pointer included.
"""

import socket
import struct
import subprocess
import sys
import threading
from pathlib import Path

HERE = Path(__file__).parent
ANSWER_IP = "192.0.2.55"


def serve_once(sock):
    data, addr = sock.recvfrom(4096)
    tid = data[:2]
    i = 12
    while data[i] != 0:
        i += data[i] + 1
    question = data[12:i + 5]
    header = tid + struct.pack(">HHHHH", 0x8180, 1, 1, 0, 0)
    answer = (b"\xc0\x0c" + struct.pack(">HHIH", 1, 1, 300, 4)
              + socket.inet_aton(ANSWER_IP))
    sock.connect(addr)
    sock.send(header + question + answer)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    thread = threading.Thread(target=serve_once, args=(sock,), daemon=True)
    thread.start()
    out = subprocess.run(
        [sys.executable, str(HERE / "dns_resolver.py"), "example.test",
         "--server", "127.0.0.1", "--port", str(port)],
        capture_output=True, text=True, timeout=30)
    thread.join(timeout=5)
    sock.close()
    print(out.stdout)
    assert out.returncode == 0, out.stderr
    assert ANSWER_IP in out.stdout, "resolver did not decode the A record"
    assert "example.test" in out.stdout, "resolver lost the answer name"
    print("SMOKE PASS: raw query built, compressed answer decoded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
