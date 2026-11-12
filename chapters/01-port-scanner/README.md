# Chapter 1: Port Scanner

**Status: complete.** File: `port_scanner.py`. Test: `smoke_test.py`.

## What you are building

A TCP connect scanner: given a host and a set of ports, it reports which
ports accept a connection, and optionally reads the banner each service
offers. This is the first tool in the curriculum because every later
recon chapter assumes you can answer the most basic question about a
target: what is listening?

## Why it works that way: the mechanism

TCP opens a connection with a three-way handshake: SYN, SYN-ACK, ACK.

- If a service is listening, the host answers your SYN with SYN-ACK.
  Your operating system completes the handshake when you call
  `connect()`, and the call returns successfully.
- If nothing is listening, the host answers with RST and `connect()`
  fails with `ConnectionRefusedError`.
- If a firewall silently drops the packet, nothing answers and
  `connect()` fails by timeout. A connect scan cannot tell a filtered
  port from a dead host, and this scanner is honest about that: it
  reports only what it proved, open ports.

So "scanning" needs no raw packets and no privileges: the kernel's own
TCP stack does the handshake, and the result of `connect()` is the
measurement. What a scanner adds is scale (many ports, many threads)
and bookkeeping. Banner grabbing is a second, separate step: once the
connection exists, many services (SSH, SMTP, FTP) state their name and
version before you send anything.

## Build it

1. Parse the port specification. Accept single ports, comma lists, and
   ranges (`22,80,8000-8010`) and expand them into a sorted set,
   rejecting anything outside 1 to 65535.
2. Resolve the hostname once, up front, so a DNS failure stops the run
   before a hundred threads repeat it.
3. Write `scan_port()`: one `socket.create_connection()` with a
   timeout. Success means open; refusal or timeout means not open.
4. Run the probes in a `ThreadPoolExecutor`. Connect scanning is almost
   all waiting, so threads parallelise it well; 100 workers against a
   LAN host is comfortable.
5. Optional banner step: on an open socket, read up to 1024 bytes. Send
   a bare CRLF first, because some services wait for any input before
   replying.
6. Print open ports sorted ascending, then a one-line summary. Sort at
   print time, not completion time: results arrive out of order.

## Run it

Against a demo listener started on port 18080 of localhost (a
five-line throwaway server that answers with `DemoService/1.0 ready`):

```text
$ python3 port_scanner.py 127.0.0.1 --ports 22,80,18080,18081 --banner
Scanning 127.0.0.1 (127.0.0.1): 4 ports
  18080/tcp open  DemoService/1.0 ready
4 scanned, 1 open
```

## Smoke test

`smoke_test.py` starts two real listeners on 127.0.0.1, picks one
definitely closed port, runs the scanner CLI over all three, and
asserts both listeners are found and the closed port is not reported:

```text
Scanning 127.0.0.1 (127.0.0.1): 3 ports
  41065/tcp open
  43993/tcp open
3 scanned, 2 open
SMOKE PASS: both localhost listeners found, closed port excluded
```

(Port numbers differ per run; they are ephemeral ports the test
requested from the OS.)

## Exercises

1. Add a `--service` mode that maps open ports to service names using
   `socket.getservbyport`, and compare its answers to the banners.
2. Add UDP scanning for one port and document why its results are
   weaker (no handshake, so silence is ambiguous). Chapter 2's
   resolver gives you the UDP practice.
3. Make the scanner read targets from a file, one host per line, and
   print a combined report.
4. Measure: time a 1 to 1024 scan of localhost at 10, 100, and 500
   workers. Where does more parallelism stop helping, and why?

## Defensive note: how this appears in telemetry

A connect scan completes real handshakes, so it looks like ordinary
connection attempts in host logs and NetFlow: one source touching many
destination ports in a short window. Detection is a counting problem:
SIEM rules flag fan-out (one source, many distinct ports, high failure
ratio) and firewalls log the RSTs. A full handshake is exactly what
makes this scan reliable, and exactly what makes it visible. Chapter 4
teaches you to read captures like the ones this scan leaves behind.
