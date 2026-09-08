---
title: Cost model — no key, no network
description: "Paste a script or a reel.json and get characters, requests, per-model cost and plan fit, with every constant visible. Runs entirely in your browser; makes no network call at all."
lead: "Arithmetic you can check, on text you paste, with no key and no request to anybody. Cost figures go stale faster than anything else on this site — this page makes the staleness visible instead of hiding it in a table."
order: 21
kind: experiment
family: no key needed
app: cost
endpoints: "none — this page makes no network call"
state_chips: [projected]
toc: true
---

<div class="note"><p><b>No key bar on this page, because there is nothing to send.</b> Everything below is computed in
your browser from the text in the box and the list prices hard-coded in <a href="/assets/lab.js">lab.js</a>. It is the
only lab here that cannot cost you anything.</p></div>

{{app}}

## The arithmetic, stated

**Cost = characters ÷ 1,000 × the model's rate.** Rates, read 5 September 2026: `eleven_v3` and `eleven_multilingual_v2` **$0.10 per 1,000 characters**; `eleven_flash_v2_5` and `eleven_turbo_v2_5` **$0.05** {{claim:tts-prices}}. Context text passed as `previous_text` or `next_text` is not billed as generated characters, which is why [stitching](/experiments/text-handling/) is free.

Two things this page counts that a rate card does not:

- **Requests, not just characters.** A scene-by-scene render fires one request per scene, and the request count is what meets the concurrency limit — the failure mode that costs a render, rather than a rounding error on the bill {{claim:concurrency-unknown}}.
- **Your longest scene against the model's per-request limit.** `eleven_v3` takes 5,000 characters, `multilingual_v2` 10,000, flash and turbo 40,000 {{claim:char-limits}}. Our longest scene is about 420 characters, so limits are not a constraint for a scene-by-scene render — they bite only if somebody concatenates a whole reel into one request, which also destroys the per-scene timing the pipeline needs.

## Against what we actually paid

Section 3 puts this page's arithmetic beside real invoices from a different provider on named dates {{claim:openrouter-cost-aiuc}}. Only the left-hand column is evidence; the two right-hand columns are this page doing multiplication {{claim:projected-reel-costs}}.

The conclusion that survives the comparison: **v3 costs about what the incumbent cost, flash costs half**, and both are a rounding error against the value of the timestamps. The reason to switch is not price.

## Plan fit

At about 4,000 characters per video, a Creator plan's 220,000 characters is roughly 50 videos a month {{claim:creator-covers-50}} — arithmetic, not experience; we have never run a month of it. Section 4 does the same division on your own numbers. What it cannot tell you is whether the plan's **concurrency** allowance survives your render, which is the other half of choosing a tier and is [a different lab](/experiments/concurrency/).

## When these numbers go wrong

The day the vendor changes a price. Everything here carries the date it was read, and the [ledger](/ledger/) marks the whole class of pricing claims as vendor-documentation rather than measurement {{claim:tts-prices}}. If you find a rate that has moved, that is a correction worth sending: it invalidates a row on this site rather than a paragraph.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
