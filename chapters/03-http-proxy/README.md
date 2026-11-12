# Chapter 3: HTTP Forward Proxy

**Status: complete.** File: `http_proxy.py`. Test: `smoke_test.py`.

## What you are building

A forward proxy for plain HTTP: it accepts requests in the absolute
form a browser sends to a proxy (`GET http://host/path HTTP/1.1`),
opens its own connection to the origin, rewrites the request into the
origin form the server expects, and relays the exchange. Build this
and you understand, from the inside, the interception primitive that
tools like Burp Suite and mitmproxy are built on.

## Why it works that way: the mechanism

HTTP has two request shapes:

- **Origin-form**, sent to servers directly: `GET /path HTTP/1.1` plus
  a `Host` header saying which site.
- **Absolute-form**, sent to proxies: `GET http://host/path HTTP/1.1`,
  because the proxy, not the client, chooses where to connect.

A forward proxy is therefore a translator plus a relay: parse the
absolute URI to find the destination, strip proxy-specific headers
(`Proxy-Connection`, `Proxy-Authorization`), forward any request body
using `Content-Length`, and stream the response back.

Two simplifications keep this build honest and small. We add
`Connection: close` upstream, so end of the response body is simply
the origin closing the connection; no chunked decoding needed in the
relay loop. And we refuse `CONNECT` with 501: CONNECT is how HTTPS
tunnelling through proxies works, and implementing it is an exercise
below, because a tunnel the proxy cannot see inside is also the exact
boundary of what HTTP interception can inspect.

## Build it

1. Accept connections in a loop; hand each client to a thread.
2. `read_head()`: read until the blank line (`\r\n\r\n`) that ends the
   request head; keep any bytes past it, they are the start of the
   body and throwing them away corrupts uploads.
3. `parse_request()`: split the request line, then headers into an
   ordered list of pairs. HTTP allows duplicate headers, so a dict
   would silently lose information.
4. `build_upstream_request()`: parse the absolute URI for host and
   port, rebuild the request line in origin form, drop proxy headers,
   ensure a `Host` header, add `Connection: close`.
5. Relay: send the head, forward exactly `Content-Length` body bytes
   (counting the buffered remainder from step 2), then copy the
   response back in chunks until the origin closes.
6. Log one line per request to stderr: method, target, destination.
   In a proxy, the log is the product.

## Run it

```text
$ python3 http_proxy.py --listen 127.0.0.1 --port 8080
proxy listening on 127.0.0.1:8080
GET http://example.com/ -> example.com:80
```

Then point a client at it: `curl --proxy http://127.0.0.1:8080
http://example.com/`.

## Smoke test

`smoke_test.py` starts a tiny origin server on 127.0.0.1 serving a
known string, starts the proxy on a second port, and sends an
absolute-form request through it with a raw socket:

```text
HTTP/1.0 200 OK
...
body: hello-from-origin
SMOKE PASS: absolute-form request relayed, origin body returned
```

## Exercises

1. Implement `CONNECT`: on `CONNECT host:443`, connect upstream, reply
   `200 Connection Established`, then copy bytes both ways. Notice
   what your request log can no longer see, and write down why.
2. Add a `--dump` flag that saves each request and response to a file
   named by timestamp. You have now built the core of an intercepting
   proxy; compare its dump format to a HAR file.
3. Handle chunked transfer encoding in responses instead of relying
   on `Connection: close`.
4. Refuse requests to link-local and loopback destinations when the
   proxy is bound to a non-loopback interface, and explain in the
   README of your fork which attack that prevents. (Chapter 17's SSRF
   probe returns to this.)

## Defensive note: how this appears in telemetry

A forward proxy centralises web traffic, which is why enterprises run
them on purpose: one log of every site every client visited. The same
property makes an *unauthorised* proxy a finding: egress to unusual
ports, HTTP traffic where a proxy PAC file says none should exist, and
CONNECT tunnels with long lifetimes all stand out. On the host, watch
for proxy settings appearing in browser or environment configuration
that IT did not put there. Interception is a position, not a program;
defenders audit who holds it.
