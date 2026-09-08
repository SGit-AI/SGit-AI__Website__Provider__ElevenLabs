---
title: Voice-settings sweep
description: "Sweep one voice setting at a time — stability, similarity boost, style, speed — with everything else held constant and the seed fixed, then write down what you heard."
lead: "Four sliders, and the vendor's guidance on them is qualitative. This lab sweeps **one at a time**, holds everything else constant, fixes the seed, and makes you write down what you heard — which is the only part of this that is not arithmetic."
order: 13
kind: experiment
family: choosing
app: voice-settings
endpoints: "POST /v1/text-to-speech/{id}/with-timestamps"
state_chips: [unrun]
toc: true
---

{{lab-header}}

{{app}}

## What this tests

- **`speed`** is the setting that sent us here in the first place. Its documented range is **0.7–1.2**, default 1.0, with quality costs at the extremes {{claim:speed-range}}. The incumbent provider has no equivalent, and the absence cost a portrait cut a third of its script instead of 15% of its pace {{claim:openrouter-no-speed}}. The measurable question: **how much time does 1.15× actually save on your script**, and at what point does it stop sounding like a person? The "spoken length across the sweep" line answers the first half; your ears answer the second.
- **`stability`** trades expressiveness against consistency. On `eleven_v3` the vendor frames it as three modes — creative, natural, robust — rather than a continuum {{claim:labs-unrun}}. For narration of somebody else's compliance standard, hallucination is not a risk worth taking, so the interesting range is the top half.
- **`style`** costs latency and is worth 0 for most narration. This lab is where you confirm that rather than assume it.
- **`similarity_boost`** matters most for cloned voices; on a library voice the effect is usually small, which is itself worth measuring once.

## Method

One knob, five values, everything else pinned, seed fixed at 42 so the read is as repeatable as the vendor allows — the seed is documented as best-effort, which the [text-handling lab](/experiments/text-handling/) tests directly.

Latency is reported but is **not** the point here: a sweep is sequential, so the numbers include whatever your connection was doing at the time. The two columns that matter are **spoken length** — a real, comparable measurement — and **your note**, which is the only column that captures quality.

## What it costs

Five values of a 90-character line is about **$0.045** on v3, half that on flash {{claim:tts-prices}}. A full sweep of all four settings is under a quarter of a dollar, which is less than the cost of arguing about it.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
