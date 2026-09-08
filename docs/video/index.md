---
title: Narrated videos — the plan, and the render nobody has run
description: "A working, measured video pipeline meets the provider it would narrate with. What it costs, what the alignment buys, the four places the unrun path is most likely to break, and why this page is a plan rather than a film."
lead: "A pipeline that has shipped four reels meets a narration provider it has never been run against. This page is **the plan and the numbers, not a film** — nothing here has been rendered, and the reason is a rule rather than a shortage of time."
order: 45
toc: true
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
  note: "Processed from the video-pipeline brief, published raw at /briefs/2026-09-07__brief__video-pipeline/."
---

<div class="warnbox"><p><b>No video has been made.</b> {{claim:shim-unrun}} The pipeline is real and its numbers are measured {{claim:pipeline-shipped-reels}}; its ElevenLabs path is written and has never produced a sound. Everything below that describes a render is a plan, and everything that describes a cost is arithmetic. <a href="/briefs/">Why it was not run</a> is a decision with three reasons, and the first is that this site has never held a key.</p></div>

## 1 · The pipeline, in one paragraph

A script file is the source of truth and is written **first**: scenes, each with the narration that is spoken *and* drawn on screen in the caption band, a separate four-to-eight-word caption for the muted viewer, and a shot — a URL, optional steps to click or scroll the page into the right state, and annotation targets. A capture script drives Chromium, resolves each target to a real element, paints a spotlight on it and screenshots. A render script composes each still into a slide, narrates it with whichever provider is named, records the result in real time through a vendored recorder, and remuxes. ffmpeg makes the MP4; a frames script gives you stills to judge it without watching; a doc script writes a storyboard. **The closing slide of every video prints the measured numbers of its own making, including the API cost.**

Four reels have been made this way, with a local model and with a hosted one {{claim:pipeline-shipped-reels}}. The narration provider is a swappable shim, and this vendor is the fourth — the one that has never run {{claim:shim-unrun}}.

## 2 · What this provider would add that the shipped reels do not have

Every item is a claim [the report](/) already makes. Making the video *with* it is the demonstration, which is the reason to bother.

| What | Why it matters here | State |
|---|---|---|
| **A speed control on a paid voice** — `voice_settings.speed`, 0.7–1.2 | The incumbent has none, and a portrait cut lost a third of its script rather than 15% of its pace {{claim:openrouter-no-speed}} | {{badge:docs|5 Sep 2026}} |
| **Character-level timestamps → a real `.srt`** | YouTube's auto-captions render "2,788 nodes" as words and get product names wrong every time. Our own sidecar is strictly better and free once the alignment exists | {{claim:timestamps-roundtrip}} |
| **Chapters to the sentence** rather than to the scene | From the same alignment array, with no second call | {{claim:cue-rule}} |
| **A pronunciation dictionary** | In this pipeline the narration text *is* the caption text, so `sgit dot ai` is on screen where a viewer reads it as a typo. A lexicon moves the hack off the screen | {{claim:lexicon-hypothesis}} |
| **A seed, and prosody continuity across scenes** | A reproducible read, and a reel that sounds like one take rather than sixteen | {{badge:docs|5 Sep 2026}} |

**The video that writes itself:** one *about* the timestamps API, whose own subtitles were generated from the timestamps it is describing, with the cost of making it printed on its closing slide. That is [§8](/#8-what-it-cost) and [§3](/#3-which-pattern-and-for-which-product) argued in ninety seconds, and no vendor page can do it.

## 3 · What it would cost

{{claim:video-cost-projection}} — the arithmetic, not an invoice.

| Workload | Characters | `eleven_v3` @ $0.10/1k | flash @ $0.05/1k |
|---|---:|---:|---:|
| One scene (the 187-character bench sample) | 187 | $0.019 | $0.009 |
| A 2-minute landscape reel, ~260 words | ~1,600 | **$0.16** | $0.08 |
| A 4-minute landscape reel, ~600 words | ~3,600 | **$0.36** | $0.18 |
| A portrait cut of the same, tighter script | 60–70% of the above | — | — |
| A re-render after a script fix | full price again | — | — |

**Budget about $1.50 for a first video** including the three or four re-runs a first script needs, and draft on flash at half the price {{claim:tts-prices}}. The render prints its own cost on the closing slide; the account's character counter is the ground truth, and comparing the two once is [an experiment nobody has run](/experiments/key-scope/).

## 4 · The script rules that cost time when broken

Measured on six cuts, and repeated here because they are the ones that bite {{claim:pipeline-wps}}:

1. **2.1 words per second.** Count words before any audio exists. Ten scenes want 200–260 words including intro and outro.
2. **The intro previews; scene one starts.** Otherwise the viewer hears the same sentence twice.
3. **The caption is not the narration.** Four to eight words, different from the sentence spoken over it.
4. **Element targets, never hand-typed rectangles.** Hand-typed ones were ±15 px off and a human spotted it on the storyboard.
5. **Anchor above the target.** The resolver takes the first match at or below the anchor, so anchoring on the sentence *under* a table finds the next table, off-screen.
6. **Read every still before rendering.** About three seconds each, against a render you would otherwise throw away.
7. **A portrait cut must land under 3:00 with real margin** — 2:51, not 2:58 — or the platform will not treat it as a Short.

## 5 · Before spending a render: where the unrun path probably breaks

Four predictions from the pipeline's author, who wrote the path from the vendor's reference and could not reach the API to test it {{claim:first-run-risks}} {{claim:egress-blocked}}. **Run one scene, not a reel**, and work through these first.

<div class="fails"><div class="fail open"><p class="who">Most likely</p><h3><code>pcm_44100</code> may not be on the plan</h3><p>The shim asks for raw PCM so the bytes go straight into a <code>Float32Array</code> with no decoder. <b>PCM output formats are gated to higher subscription tiers</b>, so on a Creator-tier key this is likely to come back 401 or 422 naming the output format.</p><p><b>The fix is six lines:</b> ask for <code>mp3_44100_128</code> and decode it in the page with <code>decodeAudioData</code>, returning the buffer's own sample rate rather than the constant. Everything downstream reads the sample rate from the return value. <b>Write down which way it went</b> — "PCM worked on tier X" is as useful a finding as the failure.</p></div><div class="fail open"><p class="who">Second most likely</p><h3><code>eleven_v3</code> may not be enabled, or may reject the settings</h3><p>Two risks in one: v3 may not be available for API use on a given key, and it treats stability as <b>three discrete modes</b> rather than a continuum, so the shim's default of 0.5 can 422.</p><p><b>The fallback</b> is <code>eleven_multilingual_v2</code>, which is the stable workhorse and takes a continuous stability. For narrating somebody else's compliance standard: Natural or Robust, <b>never Creative</b> — hallucination in a video about a standard is not a risk worth taking.</p></div><div class="fail open"><p class="who">Check, do not assume</p><h3>The alignment may not come back in the expected shape</h3><p>The shim reads <code>alignment</code> and <code>normalized_alignment</code> and writes both beside the render log. Dump one response before trusting it. <b>If a model returns no alignment, the whole SRT, chapters and karaoke chain is unavailable on that model</b> — and since the alignment is the entire reason to be here, the answer is to change model rather than to work around it.</p></div><div class="fail open"><p class="who">Wastes a whole run</p><h3>The render fires two generations at once</h3><p>Against a concurrency limit nobody has measured {{claim:concurrency-unknown}}. A 429 halfway through a render wastes everything generated before it.</p><p><b>Run the first real reel with a pool of one.</b> It is slower and it cannot 429. Raise it once <a href="/experiments/concurrency/">the probe</a> has found the wall — and then write the number down, because nobody publishes it.</p></div></div>

## 6 · Three videos worth making first

Each is short, and each demonstrates a claim this site already makes.

1. **"The bench, in ninety seconds."** Paste a key, list voices, generate with timestamps, watch the words light up, build the SRT. **Ship its own `.srt` alongside it and say so on screen** — the subtitles are the demonstration, not a nicety.
2. **"Four patterns."** Slides, no capture at all. The strongest ninety seconds available, because [it is the argument](/patterns/).
3. **"What it cost and what went wrong."** [§8](/#8-what-it-cost) and [§9](/#9-what-went-wrong) read aloud over the real numbers. Nobody else publishes this, which is exactly why it is worth a video.

Landscape first, then a portrait cut under 3:00, with a title, a description and chapters.

## 7 · Where video would live, when there is one

Decided in advance, because the answer is cheaper before there are twenty files:

- **MP4, H.264 + AAC, `+faststart`** as the delivered file — not WebM {{claim:mp4-vs-webm}}.
- **The `.srt` beside the MP4**, referenced from the `<video>` element as a `<track>`.
- **A folder per reel** holding the script, the stills, both cuts, the storyboard, the logs and the findings — the same shape the pipeline already produces, because on a site whose thesis is *show the working*, the storyboard and the findings are themselves the content.
- **Watch the limits.** 100 MB per file is hard and Pages is a soft 1 GB with 100 GB a month of bandwidth. A 4 MB reel is nothing; twenty reels plus stills is worth a thought before it is a problem.

## 8 · Why this is a plan and not a film

Three reasons, in order of weight, and the [briefs page](/briefs/) carries the full account.

**This site has never held a key** {{claim:keys-local-only}}, and its acceptance list says so as a property rather than a circumstance. Every {{badge:verified}} chip here came from a human's own browser. Trading that for a two-minute film would be a bad exchange.

**The toolchain is not this site's to hold.** The estate's rule is that component code stays canonical where it lives and these sites hold the context; vendoring a render pipeline into a report site contradicts it, and everything the brief is actually worth — the measured numbers, the failure points, the script rules — transfers without the 724 KB.

**The interesting half needs a person.** The brief's own closing section is *what I could not tell you*: whether the shim works, which names the model mispronounces {{claim:names-test}}, how the API behaves under the render's concurrency {{claim:concurrency-unknown}}, whether the drift is in the audio or the recording {{claim:pipeline-drift}}. Those are answered by one person, once, with a key.

## 9 · What the first run would settle

The ledger rows that would change state, in the order a single afternoon would close them:

| Claim | Today | After one render |
|---|---|---|
| The ElevenLabs render path {{claim:shim-unrun}} | written, not run | verified, or a documented failure — **both are findings** |
| The four first-run predictions {{claim:first-run-risks}} | predictions | four answers, and the one that broke is the interesting one |
| The lexicon {{claim:lexicon-hypothesis}} and the names test {{claim:names-test}} | a hypothesis nobody has heard | a list of what the model gets wrong |
| The concurrency wall {{claim:concurrency-unknown}} | unknown | a number, published, that nobody else publishes |
| Where the drift comes from {{claim:pipeline-drift}} | unattributed since September | attributed, in about ten minutes of arithmetic |

**That is the most valuable content this site could gain, and it cannot be written by the machine that built it.**

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
