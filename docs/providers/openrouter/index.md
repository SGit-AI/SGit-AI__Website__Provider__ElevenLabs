---
title: OpenRouter — the sibling page, as a structural stub
description: "Not this site's subject. A stub of the sibling provider page, carried here to prove that adding a provider is one Markdown file with front-matter — and to supply the comparison table's other rows."
lead: "**This is not an OpenRouter site.** It is a deliberately short stub of the sibling provider page, published here for two reasons: it supplies the other rows of [the comparison](/comparison/), and it is the proof that adding a provider to this family is *one Markdown file with front-matter* rather than template surgery."
order: 70
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
  note: "Condensed from platforms/openrouter.md. The full page belongs at openrouter.providers.sgit.ai, which does not exist yet."
grants:
  - verb: spend
    object: budget
    reach: tenant
    reversible: true
    bounded_by: the key's own limit, with a monthly reset — a number chosen in advance
  - verb: send
    object: text
    reach: endpoint
    reversible: true
    bounded_by: each scene's narration goes to the model
  - verb: read
    object: audio
    reach: self
    reversible: true
    bounded_by: "the speech comes back; the platform publishes nothing"
not_granted: [publishing, world-visible side effects]
patterns:
  - provider: OpenRouter
    product: Chat and audio models
    server: "No"
    p0:
      verdict: never
      note: "possible; never acceptable"
    p1:
      verdict: yes
      note: "provisioned key with a limit and a reset"
    p2:
      verdict: yes
      note: "with a server, and not needed"
    p3:
      verdict: yes
      note: "shipped: sg.llm.* in the SG/Vault host"
---

<div class="note"><p><b>Scope.</b> This site reports on ElevenLabs. The full OpenRouter report — nine sections, its own cost table, its own failures — belongs at <code>openrouter.providers.sgit.ai</code> when that site exists. What follows is the minimum needed to make the comparison honest, plus the one measurement that is genuinely evidence for the whole argument.</p></div>

## Why it is the useful contrast

OpenRouter can **mint a key with a spend limit and a reset window**, and reports `limit`, `usage` and `limit_remaining` against it. So a key in a page has a blast radius somebody chose in advance. ElevenLabs text to speech has no equivalent at any price {{claim:no-per-key-spend-limit}} — which is the single sharpest difference between the two and the reason the comparison table earns its place.

## What it cost us, measured

| Date | Reel | Words | Requests | Cost |
|---|---|---:|---:|---:|
| 2 Sep 2026 | pitch landscape 1:55 | 304 | 13 | $0.1554 |
| 2 Sep 2026 | pitch landscape, re-render | 304 | 13 | $0.1533 |
| 2 Sep 2026 | pitch portrait 1:24 | 190 | 9 | $0.1112 |
| 3 Sep 2026 | aiuc-1 landscape 3:46 | 599 | 16 | $0.2997 |
| 3 Sep 2026 | aiuc-1 portrait 2:09 | 318 | 10 | $0.1708 |

About **$0.08 per minute of speech** {{claim:openrouter-cost-aiuc}}. Speech generation took 3.3–5.4 s for a whole reel in parallel, against 50–94 s for a local model. Transcript mismatches across 61 generations: zero {{claim:transcript-mismatches}}.

## What went wrong

- **The limit did its job** — a 402 at $4.79 of $5.00, because audio output requires $0.50 of headroom. The full framing is on [the patterns page](/patterns/), where it belongs: it is the one piece of evidence on this site that a bound is enforceable in practice rather than in a diagram {{claim:openrouter-402}}.
- **No speed control.** The model takes no pace parameter, so a portrait cut that had to fit under a three-minute limit lost a third of its script instead of 15% of its pace {{claim:openrouter-no-speed}}. That single missing knob is what sent us to evaluate a vendor whose API has one {{claim:speed-range}}.
- **An outro that lied.** A reel's closing narration said "no API cost" over a slide printing $0.1554, because one outro served both a free cut and a paid one. Caught by reading the closing frame; the rule now is that every outro says "the cost is on the screen".

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
