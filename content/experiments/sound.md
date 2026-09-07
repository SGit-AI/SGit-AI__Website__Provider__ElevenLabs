---
title: Sound effects and music
description: "The sound-generation and music endpoints, with a per-second cost meter — and the house rule they were evaluated against: a two-second sting under the title slide, and nothing else."
lead: "Two endpoints that are easy to overuse. They are here with a cost meter and a house rule attached, because the interesting question is not *can it* — it obviously can — but *should it, under narration dense with numbers*."
order: 18
kind: experiment
family: beyond speech
app: sound
endpoints: "POST /v1/sound-generation · POST /v1/music"
state_chips: [unrun]
toc: true
---

{{lab-header}}

{{app}}

## The numbers

**Sound effects** take a prompt, a duration from 0.1 to 30 seconds (omit it for automatic), a prompt-influence control where high means literal, and an optional seamless loop for ambience. **$0.12 per minute** — so a two-second sting is about **$0.004** {{claim:tts-prices}}.

**Music** takes a natural-language prompt and a length from 3 seconds to 5 minutes. **$0.15 per minute** — a 30-second bed is about **$0.075**, which is the entire ElevenLabs spend behind this site's verified claims {{claim:bench-cost}}. The vendor states that music from paid plans is cleared for broad commercial use; **read the current terms yourself before publishing under a brand**, because that is a licence question and it is theirs to change.

## The rule these were evaluated against

A **two-second sting under the title slide, and nothing else.** A bed under narration hurts intelligibility, and every reel in the source estate is dense with numbers that a viewer has one chance to hear. If a sting is used, mix it about 18 dB under the voice and fade it before the first word — the render already knows when the first word starts, because [the alignment says so](/experiments/captions/).

That is a rule, not a finding. It was written from experience with a different medium and has never been A/B tested here {{claim:labs-unrun}}. This lab is where somebody disproves it: generate a bed, mix it under a real narration line, listen on a phone speaker at half volume, and write down which version you would rather watch.

## Where this fits the site's argument

Nowhere, and that is worth saying. These endpoints spend the same account quota as speech and carry the same credential story: a key scoped for narration does not need them, and a key that can reach them can spend the account's whole quota generating five-minute tracks {{claim:no-per-key-spend-limit}}. If you scope a key for a render pipeline, scope these out — and use [the key-scope probe](/experiments/key-scope/) to check that you actually did.
