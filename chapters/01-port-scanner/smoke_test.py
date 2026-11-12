#!/usr/bin/env python3
"""Smoke test for Chapter 1: scan localhost listeners we started.

Starts two TCP listeners on 127.0.0.1, picks one definitely-closed
port, runs the scanner CLI against all three, and asserts the two
listeners are reported open and the summary counts match.
"""

import socket
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def free_closed_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main():
    listeners = []
    open_ports = []
    for _ in range(2):
        srv = socket.socket()
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", 0))
        srv.listen(5)
        listeners.append(srv)
        open_ports.append(srv.getsockname()[1])
    closed = free_closed_port()
    spec = ",".join(str(p) for p in open_ports + [closed])
    try:
        out = subprocess.run(
            [sys.executable, str(HERE / "port_scanner.py"), "127.0.0.1",
             "--ports", spec, "--timeout", "2"],
            capture_output=True, text=True, timeout=60)
    finally:
        for srv in listeners:
            srv.close()
    print(out.stdout)
    assert out.returncode == 0, out.stderr
    for port in open_ports:
        assert "%d/tcp open" % port in out.stdout, "missed open port %d" % port
    assert "%d/tcp open" % closed not in out.stdout, "closed port reported open"
    assert "3 scanned, 2 open" in out.stdout, "summary line wrong"
    print("SMOKE PASS: both localhost listeners found, closed port excluded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
