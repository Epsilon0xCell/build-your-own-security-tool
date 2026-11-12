# Chapter 8: Subdomain Enumerator

**Status: planned.** Track: Recon and discovery. Depends on: Chapter 2.

## Objective

Discover a domain's subdomains by testing candidate names against DNS, building the external attack-surface list that recon starts from.

## The mechanism, in outline

- Each candidate name is one resolver query; a name that resolves exists, a name that returns NXDOMAIN does not.
- Wildcard DNS breaks the naive method: a domain answering everything must be detected first with random names, or every candidate looks real.
- Wordlist quality beats size; permutations of discovered names (dev-api, api-dev) find more than raw volume.
- Resolution through a public resolver and through the domain's own nameserver can give different answers; both views matter.

## What you will build

A working implementation in Python, in this directory, following the
anatomy of the completed chapters: numbered build steps, a runnable
tool, a smoke test against self-owned lab targets, and exercises.

## Exercises (draft)

1. Enumerate a domain you own and compare against its DNS zone or registrar records.
2. Implement wildcard detection and show it firing on a wildcard domain.
3. Chain output into Chapter 1: scan only the hosts that resolved.

## Defensive note (preview)

Bulk queries are visible to the resolver operator and often to the target's DNS provider; query patterns (dictionary-shaped bursts) are a known recon signal in DNS logs.

*This chapter is specified but not yet built. It is listed so the
curriculum map is complete and contributions can pick it up; see
CONTRIBUTING.md for how chapters get built. Nothing here is filler:
when the chapter is written, this file is replaced by the full
chapter following the anatomy of Chapters 1 to 5.*
