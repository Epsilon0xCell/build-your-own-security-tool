#!/usr/bin/env python3
"""Chapter 3: an HTTP forward proxy.

Accepts absolute-form requests (GET http://host/path HTTP/1.1), opens
its own connection to the origin, rewrites the request to origin-form,
and relays the exchange. Everything between your machine and a website
can be inspected with the tool you build here; that is exactly why it
is also the classic interception primitive.

Usage:
    python3 http_proxy.py --listen 127.0.0.1 --port 8080
    curl --proxy http://127.0.0.1:8080 http://example.com/

Run it on your own traffic, on machines and networks you own or are
authorised to test.
"""

import argparse
import socket
import sys
import threading
from urllib.parse import urlsplit

MAX_HEAD = 65536


def read_head(conn):
    """Read until the blank line that ends the request head."""
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = conn.recv(4096)
        if not chunk:
            break
        buf += chunk
        if len(buf) > MAX_HEAD:
            raise ValueError("request head too large")
    head, _, rest = buf.partition(b"\r\n\r\n")
    return head, rest


def parse_request(head):
    """Split a request head into (method, target, version, headers).

    headers is a list of (name, value) pairs in wire order; duplicates
    are legal in HTTP, so a dict would silently drop information.
    """
    lines = head.decode("iso-8859-1").split("\r\n")
    method, target, version = lines[0].split(" ", 2)
    headers = []
    for line in lines[1:]:
        if ":" in line:
            name, value = line.split(":", 1)
            headers.append((name.strip(), value.strip()))
    return method, target, version, headers


def header_value(headers, name):
    for n, v in headers:
        if n.lower() == name.lower():
            return v
    return None


def build_upstream_request(method, target, version, headers, body_prefix):
    """Rewrite an absolute-form proxy request into origin-form.

    Returns (host, port, bytes_to_send, already_buffered_body_bytes).
    """
    if target.startswith("https://"):
        raise ValueError("https targets need CONNECT, which this proxy "
                         "does not implement")
    if target.startswith("http://"):
        parts = urlsplit(target)
        host = parts.hostname
        if not host:
            raise ValueError("absolute URL has no host: %s" % target)
        port = parts.port or 80
        path = parts.path or "/"
        if parts.query:
            path += "?" + parts.query
    else:  # origin-form already; destination comes from the Host header
        hostport = header_value(headers, "Host") or ""
        host, _, p = hostport.partition(":")
        port = int(p) if p else 80
        path = target
    skip = {"proxy-connection", "proxy-authorization", "connection"}
    out = ["%s %s %s" % (method, path, version)]
    sent_host = False
    for name, value in headers:
        if name.lower() in skip:
            continue
        if name.lower() == "host":
            sent_host = True
        out.append("%s: %s" % (name, value))
    if not sent_host:
        out.append("Host: %s" % host if port == 80
                   else "Host: %s:%d" % (host, port))
    # Ask the origin to close after responding: end-of-body detection
    # becomes "connection closed", which keeps the relay loop simple.
    out.append("Connection: close")
    head = ("\r\n".join(out) + "\r\n\r\n").encode("iso-8859-1")
    return host, port, head, body_prefix


def relay_body(client, upstream, first_chunk, content_length):
    """Forward a fixed-length request body, partly already read."""
    remaining = content_length - len(first_chunk)
    if first_chunk:
        upstream.sendall(first_chunk[:content_length])
    while remaining > 0:
        chunk = client.recv(min(65536, remaining))
        if not chunk:
            break
        upstream.sendall(chunk)
        remaining -= len(chunk)


def relay_response(upstream, client):
    """Stream the response back until the origin closes."""
    while True:
        chunk = upstream.recv(65536)
        if not chunk:
            break
        client.sendall(chunk)


def handle_client(client, addr):
    with client:
        try:
            head, rest = read_head(client)
            if not head:
                return
            method, target, version, headers = parse_request(head)
            if method == "CONNECT":
                client.sendall(b"HTTP/1.1 501 Not Implemented\r\n\r\n")
                print("rejected CONNECT %s (exercise: implement it)"
                      % target, file=sys.stderr)
                return
            host, port, out_head, _ = build_upstream_request(
                method, target, version, headers, rest)
            length = int(header_value(headers, "Content-Length") or 0)
            with socket.create_connection((host, port), timeout=10) as up:
                up.sendall(out_head)
                if length:
                    relay_body(client, up, rest, length)
                print("%s %s -> %s:%d" % (method, target, host, port),
                      file=sys.stderr)
                relay_response(up, client)
        except (OSError, ValueError) as exc:
            print("error from %s: %s" % (addr, exc), file=sys.stderr)


def main(argv=None):
    ap = argparse.ArgumentParser(description="HTTP forward proxy")
    ap.add_argument("--listen", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8080)
    args = ap.parse_args(argv)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((args.listen, args.port))
        server.listen(50)
        print("proxy listening on %s:%d" % (args.listen, args.port),
              file=sys.stderr)
        try:
            while True:
                client, addr = server.accept()
                threading.Thread(target=handle_client, args=(client, addr),
                                 daemon=True).start()
        except KeyboardInterrupt:
            print("stopped", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
