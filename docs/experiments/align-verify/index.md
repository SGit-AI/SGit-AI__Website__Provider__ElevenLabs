---
title: Align and verify — subtitles for old renders, and a QA gate for new ones
description: "Forced alignment of audio you already have to the script it speaks, and Scribe transcription diffed against the expected text — the automatic version of catching an error by watching the video."
lead: "Two endpoints, both priced as speech-to-text, both cheap enough to run on everything you have ever published. One gives subtitles to videos rendered before any of this existed; the other catches the mistakes we have actually shipped."
order: 17
kind: experiment
family: timing
app: align-verify
endpoints: "POST /v1/forced-alignment · POST /v1/speech-to-text"
state_chips: [unrun]
toc: true
---

{{lab-header}}

{{app}}

## Forced alignment — the cheapest useful thing on the list

`POST /v1/forced-alignment` takes the audio (up to 3 GB or 10 hours) and the transcript as **plain text** — not JSON — up to 675,000 characters, and returns per-character and per-word timing over the text you supplied. It is priced at the speech-to-text rate of **$0.22 per hour of audio** {{claim:alignment-stt-price}}.

The estate this site comes from has six rendered cuts and the exact words each one speaks. Aligning all six costs **under two cents** and produces an SRT for every one — including the two cuts rendered with a local model that will never have API timestamps. Nobody has done it {{claim:labs-unrun}}.

Two ways to get it wrong, both easy:

- **Send the text the audio actually speaks.** A portrait cut usually has its own shorter script; sending the landscape one produces confident nonsense.
- **Put the intro first.** The title slide speaks before scene one, so it belongs at the top of the text, in the order the render spoke it.

## Scribe as a QA gate

`POST /v1/speech-to-text` with `model_id=scribe_v1` returns the text with per-word timing, at the same $0.22 per hour. On its own that is a transcript; diffed against the script, it is a gate.

Two failures this pipeline has shipped and then caught **by eye** would have been caught automatically:

1. a number spoken wrongly, which nobody notices until it is on YouTube;
2. an outro saying *"no API cost"* over a closing slide printing **$0.1554** — because one outro served both a free cut and a paid one {{claim:openrouter-cost-aiuc}}.

The diff normalises both sides — lower-cased, punctuation stripped — and lists what it could not line up. It is a word-level alignment diff, not a semantic one: it will flag "two thousand seven hundred and eighty-eight" against "2,788" as a mismatch, and that is correct behaviour, because [whether the model normalises numbers reliably](/experiments/text-handling/) is a separate question with its own lab.

A provider-independent gate is worth more than a provider's own transcript check: the incumbent returns a transcript of what it spoke and reported zero mismatches across 61 generations {{claim:transcript-mismatches}}, which is reassuring and unfalsifiable — it is the same system marking its own homework.

## What is unverified here

Everything. The request shapes come from the vendor's reference {{claim:alignment-stt-price}} {{claim:labs-unrun}}; the response parsing in this lab handles both the word-array and character-array shapes because we have not seen either one come back. If the field names have moved, the log will say so before the table does.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
