# Chapter 10: TCP Relay and Port Forwarder

**Status: planned.** Track: Network foundations. Depends on: Chapter 3.

## Objective

Forward a local listening port to a destination host and port, copying bytes both directions: the pivot primitive behind SSH tunnels, jump hosts, and half of all red-team infrastructure.

## The mechanism, in outline

- A relay is two sockets and two copy loops; the engineering is in half-close handling and not deadlocking when one side is slow.
- selectors or threads multiplex connections; the chapter uses an event loop to show the state machine explicitly.
- Binding the listener to 127.0.0.1 versus 0.0.0.0 is the difference between a private tunnel and a published service, and the chapter makes you say which you built.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Forward a lab service and drive real traffic through it.
2. Add per-connection logging of bytes moved, and read it as the defender would.
3. Chain two relays and measure the added latency.

## Defensive note (preview)

Relays create the traffic pattern defenders hunt during pivoting: one host holding long-lived connections in two directions, with matching byte counts. Egress monitoring sees the outer leg clearly.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
