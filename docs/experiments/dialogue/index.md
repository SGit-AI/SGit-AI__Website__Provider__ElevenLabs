---
title: Multi-speaker dialogue
description: "One request, several voices, consistent pacing across the turns — a two-voice cut is one endpoint away from a single-narrator reel."
lead: "A question and an answer, in two voices, generated in **one** call so the pacing holds across the turn. Concatenating two separate generations does not give you this, and the difference is audible."
order: 19
kind: experiment
family: beyond speech
app: dialogue
endpoints: "POST /v1/text-to-dialogue/with-timestamps"
state_chips: [unrun]
toc: true
---

{{lab-header}}

{{app}}

## What this tests

`POST /v1/text-to-dialogue` takes `inputs: [{ text, voice_id }, …]` and renders the whole exchange in one request with consistent pacing {{claim:dialogue-endpoint}}. The `/with-timestamps` variant returns the same character-level alignment as ordinary speech, so [everything the captions studio does](/experiments/captions/) works on a dialogue too.

For a single-narrator explainer this is one endpoint away rather than a rewrite, and it changes what a script can be: a rhetorical question that is actually asked by somebody else lands differently from one the narrator asks themselves.

## What to listen for

- **The seam.** Generate the same two lines separately, concatenate them by hand, and compare. If the single-call version does not sound more like a conversation, the endpoint is not earning its keep for your material.
- **Turn-taking pace.** Real exchanges overlap slightly and vary their gaps; a model that leaves an identical pause after every turn sounds like a phone tree.
- **Whether the voices stay distinct** when the text is technical and both speakers use the same vocabulary.

## Cost and availability

Billed as characters, at the model's rate — the same arithmetic as ordinary speech {{claim:tts-prices}}. Availability is per-account: if the endpoint is not on your plan the call comes back 402 or 404 {{claim:error-table}}, which is the vendor answering a question about your subscription rather than a fault in this page. The log shows the status and the `detail` body, which is the useful part.

Nobody here has run it {{claim:labs-unrun}}.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
