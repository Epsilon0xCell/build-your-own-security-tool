# Chapter 2: DNS Resolver from Raw UDP

**Status: complete.** File: `dns_resolver.py`. Test: `smoke_test.py`.

## What you are building

A DNS resolver that constructs query packets byte by byte, sends them
over UDP, and parses the responses itself, including compressed names.
No `gethostbyname`, no resolver library: the wire format is the lesson,
and DNS is the protocol every other chapter keeps meeting.

## Why it works that way: the mechanism

A DNS message is a 12-byte header plus sections. The header carries a
random query ID, flags, and four counts. The question section encodes
the name as length-prefixed labels (`example.com` becomes
`7 example 3 com 0`) followed by the record type and class you want.

Two design facts explain the whole protocol:

- **It rides UDP** because a query and its answer usually fit in one
  datagram each, and the handshake cost of TCP would dwarf the lookup.
  The price is that the client owns reliability: timeouts, retries,
  and checking that the response ID matches the query ID, which is
  also the first line of defence against spoofed answers.
- **Names compress.** In responses, a two-byte pointer (top bits `11`)
  refers back to a name already in the packet. Answers almost always
  repeat the question name, so the pointer is how replies stay small.
  Parsing DNS means following those pointers without looping forever.

We send with a *connected* UDP socket. `connect()` on UDP sends
nothing; it fixes the peer so the kernel drops datagrams from anyone
else, one less spoofing surface to handle by hand.

## Build it

1. `encode_name()`: split the name into labels, prefix each with its
   length byte, terminate with zero.
2. `build_query()`: pack the header with `struct` (`>HHHHHH`), set the
   RD flag (0x0100, recursion desired), QDCOUNT 1, and append the
   question. Record the random ID.
3. Send the packet and read one datagram back.
4. `decode_name()`: walk labels; on a pointer byte, jump, decode, and
   return both the name and the position the *original* stream resumes
   at. Getting that second value right is the whole trick.
5. `parse_response()`: verify the ID, skip the questions, then read
   each resource record (name, type, class, TTL, data length, data)
   and format the data per type: dotted quad for A, `inet_ntop` for
   AAAA, a decoded name for CNAME and NS, preference plus name for MX,
   joined strings for TXT.

## Run it

The smoke test doubles as the demo: it runs a fake DNS server on
localhost that answers with a documentation address, and resolves
through it:

```text
$ python3 dns_resolver.py example.test --server 127.0.0.1 --port 53921
example.test	300	IN	A	192.0.2.55
```

Against your system resolver (the default, read from
`/etc/resolv.conf`) the same command works for any real name and other
record types: try `--type MX` or `--type TXT`.

## Smoke test

`smoke_test.py` starts a one-shot UDP server on 127.0.0.1 that answers
any A query with 192.0.2.55 (TEST-NET-1, RFC 5737, reserved for
documentation) using a compression pointer for the answer name, then
runs the resolver CLI against it:

```text
example.test	300	IN	A	192.0.2.55
SMOKE PASS: raw query built, compressed answer decoded
```

One environment note from building this chapter: the sandboxed build
machine blocked the `sendto` syscall entirely, which is why the
resolver uses connected UDP (`connect` plus `send`). That variant is
better anyway, for the filtering reason above.

## Exercises

1. Add retry with backoff: up to 3 attempts, doubling the timeout.
   What failure does each retry actually fix?
2. Follow a CNAME chain: when the answer is a CNAME and no A record
   follows, issue a new query for the target name.
3. Add the PTR type and reverse lookup for an IP in your lab.
4. Capture a real lookup with the Chapter 4 parser and decode the same
   bytes by hand. Where does the pointer in the answer point, and why
   that offset?

## Defensive note: how this appears in telemetry

Resolver traffic is metadata gold: DNS logs reveal which names a host
looked up, when, and how often, and defenders query them constantly.
Attackers know it, which is why exfiltration and command channels hide
in DNS TXT queries and long subdomain labels; detectors look for label
length, entropy, and query volume per name. Your resolver makes one
ordinary query at a time and is indistinguishable from system lookups.
The anomaly signals live at scale and in shape, not in single queries.
