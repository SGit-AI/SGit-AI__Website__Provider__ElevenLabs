---
title: Text handling — normalisation, stitching and seeds
description: "Three A/Bs that decide how a script should be written: does the model normalise numbers reliably, does passing neighbouring scenes as context change the read, and does a fixed seed actually repeat?"
lead: "Three questions that decide **how a script is written**, not how it sounds. Each is a controlled A/B: same voice, same seed, one variable. Together they are the difference between rewriting four script files and leaving them alone."
order: 22
kind: experiment
family: text
app: text-handling
endpoints: "POST /v1/text-to-speech/{id}/with-timestamps"
state_chips: [unrun]
toc: true
---

{{lab-header}}

{{app}}

## 1 · Does it normalise numbers reliably?

The scripts in the source estate spell numbers out — *"two thousand seven hundred and eighty-eight"* — because two earlier engines needed it. But **the narration text is the caption text**, so the caption band shows the words rather than the digits, and a graph slide that says "2,788 nodes" on screen is better than one that says it in longhand.

`apply_text_normalization` takes `auto`, `on` or `off`. If `auto` reliably reads `2,788` as the number and `2026-09-03` as a date, four script files can be rewritten and the caption band improves everywhere. If it is unreliable, the longhand stays. This lab generates all three settings on the same line so the difference is audible rather than argued about.

Note what the alignment gives you here: `alignment` is over the text you **sent**, `normalized_alignment` over what the model actually **read** — so a caption showing your text should use the first, and a caption showing what was spoken should use the second {{claim:timestamps-roundtrip}}.

## 2 · Does stitching change the read?

Every scene in a scene-by-scene render is generated cold. `previous_text` and `next_text` pass the neighbouring scenes as context so prosody carries across the cut — and **context text is not billed** {{claim:tts-prices}}, so if it helps at all it is free.

**On `eleven_v3` this is not available at all** {{claim:stitching-v3}} — the API answers `400 unsupported_model`, which the first real render discovered by failing on its very first request. The lab now refuses the combination instead of spending a request to rediscover it, and stitching has to be tested on `eleven_multilingual_v2` or a flash model.

The measurable part is small: spoken length usually changes a little. The audible part is the whole point — whether the reel sounds like one read or like sixteen. Listen to the two clips back to back with the following scene in mind.

## 3 · Does a seed repeat?

The vendor documents `seed` as best-effort determinism. For a pipeline that wants to re-render a video a year from now and get the same file, "best-effort" is the difference between an archive and a lottery ticket.

Two generations, identical everything, same seed. Compare byte length and per-word drift. **Identical byte lengths are promising, not proof** — an encoder can produce the same length from a different waveform — but a *different* byte length settles it in the other direction immediately. If the seed does not hold, the reproducible-render answer is to commit the audio files rather than the parameters.

## What this costs, and what it settles

About **$0.05** for all three sections on v3 at the default texts {{claim:tts-prices}}. What it settles: whether four script files get rewritten, whether the render passes neighbouring scenes, and whether renders are reproducible from parameters or need their audio archived. None of it has been run {{claim:labs-unrun}}.
