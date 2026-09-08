---
title: Key scope and quota probe
description: "Read-only probes of every endpoint class your key can reach, plus the subscription object — and the field that does not exist anywhere in it: a per-key spend limit."
lead: "Eight `GET` requests, no generation, no spend. What comes back tells you what your key may **do**. What does not come back — anywhere in the API — is any way to cap what it may **cost**. That absence is the whole argument of this site, made empirically rather than asserted."
order: 20
kind: experiment
family: operations
app: key-scope
endpoints: "GET /v1/user/subscription · /v1/user · /v1/voices · /v1/models · /v1/pronunciation-dictionaries · /v1/history · /v1/dubbing"
state_chips: [unrun]
toc: true
---

{{lab-header}}

{{app}}

## Scoped is not bounded

A key can be restricted in the dashboard to the endpoints it needs. A key for a render pipeline needs text-to-speech and voices-read; it does not need dubbing, voice creation, or history — and history is worth thinking about, because it holds the **text** of everything the account has ever generated.

Scoping limits *what a leaked key can do*. It does nothing at all to limit *how much of the account's quota it can burn* {{claim:no-per-key-spend-limit}}. There is no per-key spend limit, no daily window, and nothing that resets faster than the billing cycle {{claim:plan-quotas}}.

That is the difference between this vendor and the sibling one, and it is not a matter of degree. On the sibling provider a key carries a number you chose, and when the spend reaches it the platform refuses — we have the 402 to prove it {{claim:openrouter-402}}. Here, the only refusal comes when the account's month runs out.

## How to read the probe

- **200** — the key reaches this class of endpoint. If you did not intend it to, tighten the key in the dashboard and re-run.
- **403** — scoped out, or not on this plan. On a narrowly-scoped key, most rows *should* be 403; a table of 200s means a key that can do everything, which is what a leak would then be able to do.
- **401** on everything — the key is wrong, revoked, or sent under the wrong header name; auth is `xi-api-key`, not `Authorization` {{claim:api-key-shape}}.

## The tile that says "none"

The fourth tile in section 3 has no data behind it, because there is no field to read. Every other number on that row comes from `GET /v1/user/subscription`: characters used, characters allowed, the reset date — all **account-level** {{claim:plan-quotas}}. The API has no concept of a per-key budget, so a lab cannot show you one.

That is the empirical form of the claim the [report](/#5-the-bounding-primitive) makes in prose, and it is why [pattern 1](/patterns/) is marked unavailable in [the comparison](/comparison/) rather than merely discouraged.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
