#!/usr/bin/env python3
"""Chapter 1: a TCP connect port scanner.

Scans a host for listening TCP ports using full connect() handshakes,
optionally grabbing the service banner each open port offers.

Usage:
    python3 port_scanner.py 127.0.0.1 --ports 22,80,443,8000-8010
    python3 port_scanner.py scanme.example --ports 1-1024 --banner

Only scan hosts you own or are explicitly authorised to test.
"""

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


def parse_ports(spec):
    """Turn '22,80,8000-8010' into a sorted list of port numbers."""
    ports = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            lo, hi = int(lo), int(hi)
            if lo > hi:
                raise ValueError("port range reversed: %s" % part)
            ports.update(range(lo, hi + 1))
        else:
            ports.add(int(part))
    bad = [p for p in ports if not 1 <= p <= 65535]
    if bad:
        raise ValueError("ports out of range: %s" % bad)
    if not ports:
        raise ValueError("no ports specified")
    return sorted(ports)


def scan_port(host, port, timeout, grab_banner):
    """Probe one port. Return (port, banner) if open, else None.

    A completed connect() means the three-way handshake finished, so
    something accepted the connection: the port is open. A refusal
    (RST) means closed. Silence until timeout usually means a filter
    dropped the packets, which a connect scan cannot distinguish from
    a very slow host, so we report it as not open.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            banner = ""
            if grab_banner:
                sock.settimeout(timeout)
                try:
                    # Many services speak first (SSH, SMTP, FTP). Send a
                    # newline too, for the ones that wait for a request.
                    sock.sendall(b"\r\n")
                    data = sock.recv(1024)
                    banner = data.decode("utf-8", "replace").strip()
                except (socket.timeout, ConnectionResetError, OSError):
                    banner = ""
            return (port, banner)
    except (socket.timeout, ConnectionRefusedError, OSError):
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="TCP connect port scanner")
    ap.add_argument("host", help="hostname or IP to scan (yours, or authorised)")
    ap.add_argument("--ports", default="21,22,23,25,53,80,110,143,443,445,"
                                       "993,995,1723,3306,3389,5432,5900,8080",
                    help="comma list and/or ranges, e.g. 22,80,8000-8010")
    ap.add_argument("--timeout", type=float, default=1.0,
                    help="seconds to wait per port (default 1.0)")
    ap.add_argument("--workers", type=int, default=100,
                    help="parallel connections (default 100)")
    ap.add_argument("--banner", action="store_true",
                    help="grab the banner of each open port")
    args = ap.parse_args(argv)

    if args.workers < 1:
        print("error: --workers must be at least 1", file=sys.stderr)
        return 2
    if args.timeout <= 0:
        print("error: --timeout must be greater than 0", file=sys.stderr)
        return 2

    try:
        ports = parse_ports(args.ports)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    try:
        target_ip = socket.gethostbyname(args.host)
    except socket.gaierror as exc:
        print("error: cannot resolve %s: %s" % (args.host, exc), file=sys.stderr)
        return 2

    print("Scanning %s (%s): %d ports" % (args.host, target_ip, len(ports)))
    open_ports = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(scan_port, target_ip, p, args.timeout,
                               args.banner): p for p in ports}
        for fut in as_completed(futures):
            result = fut.result()
            if result is not None:
                open_ports[result[0]] = result[1]

    for port in sorted(open_ports):
        line = "  %d/tcp open" % port
        if open_ports[port]:
            line += "  %s" % open_ports[port]
        print(line)
    print("%d scanned, %d open" % (len(ports), len(open_ports)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
