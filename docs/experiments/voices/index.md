---
title: Voice explorer
description: "List every voice the key can reach, filter by accent, gender and use case, shortlist candidates, and hear any of them say your own line rather than the vendor's demo sentence."
lead: "The vendor's library is large and the useful part of it is small. This lab lists what **your** key can reach, filters it down, and makes each candidate say **your** line — because a voice that sounds excellent reading a marketing sentence can still mangle a product name."
order: 11
kind: experiment
family: choosing
app: voices
endpoints: "GET /v1/voices · POST /v1/text-to-speech/{id}"
state_chips: [unrun]
toc: true
---

{{lab-header}}

{{app}}

## What this tests

Whether a voice is right for a workload is not answerable from a name and a preview clip. This lab answers three narrower questions that are:

1. **What does this key actually reach?** `premade` library voices, your own clones, anything shared with the account — the list is per-account, so it is a fact about your key, not about the vendor.
2. **How does a candidate handle the words you actually use?** The line in section 4 defaults to a real sentence from a real script. Swap it for the worst one you have: the one with a product name, an initialism and a version number in it.
3. **Which three are worth a real comparison?** The shortlist is kept in this browser's `localStorage` and exports as markdown, so the decision can be recorded somewhere durable instead of in a browser tab.

## Method, and its one deliberate omission

The vendor returns a `preview_url` for most voices, on their own CDN. **This lab does not fetch it.** Every page on this site claims to call exactly one host {{claim:keys-local-only}}, and quietly loading audio from a second one would make that claim false. The link is there to copy; the honest test is a generation of your own text, which costs about a cent and tells you more.

Shortlisting writes nothing to the network. Listing voices is a read and costs nothing {{claim:tts-prices}}.

## What we know, and what we do not

We know the endpoint answers from a browser, because we watched it do so {{claim:cors-browser}}. We know nothing at all about which voice suits this workload: the evaluation that produced this site used the premade "Adam" voice for every sample because it was the first one in the list, which is not a choice, it is an absence of one {{claim:timestamps-roundtrip}}.

For narration of technical explainers, the labels worth filtering on are `use_case: narration` or `informative_educational`, and a neutral accent. That is a starting hypothesis from the vendor's own metadata {{claim:labs-unrun}}, not a finding.

## What it costs

Listing is free. Each "speak my line" is one generation of your text — around **$0.006 for a 60-character line** on flash, twice that on v3 {{claim:tts-prices}}. Trying eight voices on one line costs less than a bus fare and settles an argument that otherwise runs for a week.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
