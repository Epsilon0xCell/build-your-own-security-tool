# Chapter 11: HTTP Client from Raw Sockets

**Status: planned.** Track: Web tooling. Depends on: Chapter 3.

## Objective

Speak HTTP to a server with nothing between you and the socket: request construction, header handling, chunked and fixed-length bodies, redirects, and cookies, reimplemented to expose what libraries hide.

## The mechanism, in outline

- An HTTP exchange is text headers, a blank line, and a body whose end is decided by Content-Length, chunked framing, or connection close; the client must implement all three.
- Redirects are just responses; following them is a policy decision (how many, cross-host or not) the library was making for you.
- Cookies are state the protocol does not have; the client tracks Set-Cookie and returns Cookie, which is the entire session mechanism.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Fetch a page that redirects twice and log each hop's status and headers.
2. Download a file served with chunked encoding and verify its hash.
3. Implement basic authentication and a persistent cookie jar.

## Defensive note (preview)

Hand-rolled clients have distinctive fingerprints (header order, missing fields, unusual User-Agent) that WAFs and bot detectors score; your client will be recognisably not a browser.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
