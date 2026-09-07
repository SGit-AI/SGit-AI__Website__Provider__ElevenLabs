---
title: Captions studio — from character timings to SRT
description: "Tune the cue rule against real alignment data: break at N characters, on a gap, or after N seconds. Live cue table, karaoke preview, SRT and VTT download. Works with no key if you paste an alignment."
lead: "This API returns the start and end time of **every character**. Everything below is arithmetic on that array — and the arithmetic is ours, not the vendor's, which means it is ours to get wrong."
order: 14
kind: experiment
family: timing
app: captions
endpoints: "POST /v1/text-to-speech/{id}/with-timestamps · or no call at all"
state_chips: [unrun]
toc: true
---

{{lab-header}}

<div class="note"><p><b>This lab runs without a key.</b> Paste an <code>alignment</code> object or a <code>words.json</code> array into section 1 and everything else works: the cue rule, the tables, the downloads. Only the karaoke preview needs audio, and only a live generation needs a key.</p></div>

{{app}}

## The technique, written down

Three steps, none of them provided by the vendor.

**1 · Characters to words.** A word is a maximal run of non-whitespace characters; its start is the first character's start and its end is the last character's end. Punctuation stays attached to its word, which is what a caption wants. Fifteen lines of JavaScript, in [`lab.js`](/assets/lab.js) where you can read it.

**2 · Words to cues.** Start a new cue when the running text would exceed **84 characters** (two lines of 42), when the gap to the next word is more than **0.6 s**, or when the cue would run longer than **6 s**. The three sliders above are those three numbers, and moving them re-cuts the whole subtitle file live.

**3 · Wrap.** Break each cue at the last space before 42 characters.

Those constants are a starting point that has never been checked against a human reading a finished video {{claim:cue-rule}}. If you tune them on real material, the numbers you land on are worth more than the ones here — send them back.

## Why bother, when the platform auto-captions

Because auto-captions do not have the text. YouTube renders "2,788 nodes" as *"two thousand seven hundred eighty eight nodes"* and gets product names wrong every time. We have the ground-truth text **and**, now, the ground-truth timing — so uploading our own sidecar is strictly better and costs nothing beyond the generation we were paying for anyway.

The same timing array gives three more things the pipeline never had: chapter marks accurate to the sentence rather than to the scene; a caption band that can highlight the word being spoken; and a drift check with a cause — compare the alignment's last end time against the recorder's own duration and you learn whether drift is in the audio or in the recording.

## What is verified here, and what is not

That the endpoint returns an alignment, and that it round-trips from a browser: verified, three samples, 5 September 2026 {{claim:timestamps-roundtrip}}. That the cue rule produces *readable* subtitles: unverified {{claim:cue-rule}}. That the alignment is accurate enough to highlight words in real time without visible lag: unverified — the karaoke preview above is where you would find out.
