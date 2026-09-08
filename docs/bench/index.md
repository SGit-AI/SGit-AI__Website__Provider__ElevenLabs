---
title: The bench — text to speech, with timestamps
description: "The test bench: connect with your own key, list voices and models, generate with character-level timestamps, watch the words light up, build an SRT. The one page on this site that has actually been run."
lead: "The original test bench, and the only page here that has been **run against the live API** — on 5 September 2026, from a human's own browser. Every {{badge:verified}} chip on this site comes from a session with this page."
order: 10
kind: experiment
family: core
app: bench
endpoints: "GET /user/subscription · /voices · /models · POST /text-to-speech/{id}/with-timestamps"
state_chips: [verified]
toc: true
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
  note: "Ported from elevenlabs/index.html, the self-contained vault app, onto this site's shared lab runtime."
---

{{lab-header}}

{{app}}

## What this page proved, and what it did not

On 5 September 2026, from the project lead's browser inside a vault app frame: the subscription, voices and models endpoints answered, and three `with-timestamps` generations of a 187-character sample came back with audio and a per-character alignment {{claim:timestamps-roundtrip}}, in 5.0 to 5.8 seconds each {{claim:latency-5s}}. CORS was never the problem {{claim:cors-browser}}; the host's own content-security policy was {{claim:csp-blocks}}.

It did **not** prove that the cue rule produces readable subtitles {{claim:cue-rule}}, that any alias in the lexicon works {{claim:lexicon-hypothesis}}, or which names the model gets wrong {{claim:names-test}} — the button in section 5 exists precisely because nobody has pressed it. Three samples are three samples, not a latency distribution.

## The same page, under pattern three

This is the reason to publish a bench rather than a video of one: the argument fits in one screen.

<div class="beforeafter"><div class="ba now"><h4>What you are using now</h4><p><b>Pattern 0 with a ceiling.</b> Your key is in this page's JavaScript and in this browser's <code>localStorage</code>. It calls <code>api.elevenlabs.io</code> directly. Nothing bounds it but your plan's monthly quota {{claim:no-per-key-spend-limit}}.</p><p>Defensible because it is <em>your</em> key, <em>your</em> browser, and no key ships in the page. Not defensible as a thing to deploy for other people.</p></div><div class="ba then"><h4>What it would become</h4><p><b>Pattern 3.</b> No key box, no key in storage, nothing in the network tab. <code>sg.tts.speak()</code> asks the vault host; the host holds the sealed key, applies <code>maxCostPerSession</code>, and returns audio and alignment. {{claim:sg-tts-spec}}</p><p>Same page, same buttons, same output. The credential simply is not here. <a href="/pattern-three/">The specification →</a></p></div></div>

## What it will cost you to run

At list price, the sample in the text box is 187 characters — about **$0.019** on `eleven_v3`, or **$0.009** on flash {{claim:tts-prices}}. The whole session that produced this site's verified claims was about 750 characters, **$0.075** {{claim:bench-cost}}. This is a lab you can run for the price of a rounding error, which is exactly why the open items in [the ledger](/ledger/#open-items) are embarrassing rather than expensive.

The command-line equivalents of what this page does are [downloadable as files](/examples/) — `00-smoke.sh`, `tts-timestamps.mjs` and the rest — badged unrun, with the pipeline invocation beside them {{claim:examples-unrun}}.

If the request fails with a network error rather than an HTTP status, it is CORS or a host CSP and not your key {{claim:csp-blocks}}: open the console, check for a `connect-src` violation, and see [§9 of the report](/#9-what-went-wrong).

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
