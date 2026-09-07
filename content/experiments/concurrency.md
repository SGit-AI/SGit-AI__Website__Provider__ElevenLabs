---
title: Concurrency probe — where is the wall?
description: "Fire waves of parallel generations at 1, 2, 4, 8… until something fails, and record the request timeline, the 429s and the highest wave that survived. The one open item on this site that costs money to close."
lead: "Concurrent request limits scale with the plan, and a render that fires every scene at once — 10 to 16 requests — meets that limit before it meets any other. **We have never provoked one.** This lab does, deliberately, for a few cents."
order: 16
kind: experiment
family: operations
app: concurrency
endpoints: "POST /v1/text-to-speech/{id}"
state_chips: [unrun]
toc: true
---

{{lab-header}}

<div class="warnbox"><p><b>This is the one lab here that can cost more than pennies.</b> It generates real audio, in parallel, until something breaks. The estimate above the button is the worst case for the numbers you have set, computed before anything is sent — read it. Use the shortest text you can and the cheapest model; you are measuring a queue, not a voice.</p></div>

{{app}}

## What this tests

A `429` mid-render is the most likely first failure on a small plan {{claim:concurrency-unknown}}, and it is a bad failure: it arrives after you have paid for the requests that succeeded, halfway through a render, with a partly-built video. The number that prevents it — the semaphore width — is a plan-specific fact that nobody has measured for this account.

The ramp mode fires waves of 1, 2, 4, 8… and stops at the first wave with a failure. The wave before that is your answer.

## How to read the result

- **The timeline column** places each request by when it started and sizes it by how long it took. In a healthy wave the bars start together and end together; when they start together and finish in a staircase, requests are being queued somewhere between you and the model.
- **A 429 is not a bug**, it is the platform's own bound doing its job — the same class of event as [the 402 on the sibling provider](/patterns/), which is the one piece of evidence on this site that a bound is enforceable in practice {{claim:openrouter-402}}.
- **Distinguish 429 from 5xx and from a network error.** The vendor's error table maps them: 401 key, 402 quota or plan, 422 validation, 429 concurrency or rate, 5xx theirs {{claim:error-table}}. A `network` row in this table usually means CORS or a host CSP, not the API {{claim:csp-blocks}}.

## What to do with the number

Put it in the semaphore. In the pipeline this came from, that is `limits.maxConcurrent` in the vault's terms file — which is also exactly the field [the pattern-three host](/pattern-three/) would enforce on behalf of an app that cannot be trusted to enforce it itself {{claim:sg-tts-spec}}. Until somebody runs this, that field holds a guess.
