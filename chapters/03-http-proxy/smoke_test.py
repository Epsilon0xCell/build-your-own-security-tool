#!/usr/bin/env python3
"""Smoke test for Chapter 3: fetch a localhost page through the proxy.

Starts a tiny origin server on 127.0.0.1 serving a known string, starts
the proxy on another port, then sends an absolute-form request with a
raw socket (the way a browser talks to a proxy) and asserts the origin
string comes back through it.
"""

import socket
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).parent
MARKER = "hello-from-origin"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = MARKER.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main():
    origin = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    origin_port = origin.server_address[1]
    threading.Thread(target=origin.serve_forever, daemon=True).start()
    proxy_port = free_port()
    proc = subprocess.Popen(
        [sys.executable, str(HERE / "http_proxy.py"),
         "--listen", "127.0.0.1", "--port", str(proxy_port)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        # Wait until the proxy accepts connections (up to ~5 seconds).
        import time
        deadline = time.time() + 5
        while True:
            if proc.poll() is not None:
                raise RuntimeError("proxy exited early: %s"
                                   % proc.stderr.read())
            try:
                with socket.create_connection(("127.0.0.1", proxy_port),
                                              timeout=0.2):
                    break
            except OSError:
                if time.time() > deadline:
                    raise
                time.sleep(0.1)
        with socket.create_connection(("127.0.0.1", proxy_port),
                                      timeout=5) as conn:
            conn.sendall(("GET http://127.0.0.1:%d/page HTTP/1.1\r\n"
                          "Host: 127.0.0.1:%d\r\n\r\n"
                          % (origin_port, origin_port)).encode())
            response = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                response += chunk
    finally:
        proc.terminate()
        origin.shutdown()
    text = response.decode("iso-8859-1")
    print(text.split("\r\n\r\n")[0])
    print("body:", text.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in text else "")
    assert "200" in text.split("\r\n", 1)[0], "no 200 status via proxy"
    assert MARKER in text, "origin body did not come back through the proxy"
    print("SMOKE PASS: absolute-form request relayed, origin body returned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
