---
title: The first video — what the render actually did
description: "The first ever run of the ElevenLabs render path: what broke, what was wrong in the predictions, and the measurement that settles a drift question open since September. Plus the plan the next one follows."
lead: "On 8 September 2026 the path that had never made a sound made one. **Two failures, one prediction wrong, one nobody made, and a measurement that closes an open question** — and a two-minute video at the end of it."
order: 45
toc: true
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
  note: "Processed from the video-pipeline brief, published raw at /briefs/2026-09-07__brief__video-pipeline/."
---

<div class="note"><p><b>This page changed state on 8 September 2026.</b> {{claim:first-video}} A key was supplied by the project lead for one run, held in one command's environment and written to no file. <b>The video and every material that made it live in an encrypted vault, not in this repository</b> — the repository carries the report and the findings, which is the half that is useful to a reader. What follows is what the run found; the plan it followed is further down, unchanged.</p></div>

## 0 · What the first run found

Four of the five predictions in the handover brief were testable. One was confirmed, one was wrong for this account, one could not be tested, and **one failure nobody predicted stopped the very first request**.

<div class="fails"><div class="fail"><p class="who">Confirmed — and it was the one called most likely</p><h3><code>pcm_44100</code> is refused below the Pro tier</h3><p><code>403 subscription_required</code>: <em>"Output format 'pcm_44100' is only available on the Pro tier and above."</em> {{claim:pcm-gated}} The shim asks for raw PCM to avoid a decoder; on anything below Pro that is a dead path, and the documented fallback — MP3 plus <code>decodeAudioData</code> — is the right one.</p></div><div class="fail"><p class="who">Nobody predicted this</p><h3>Stitching is rejected outright on v3</h3><p><code>400 unsupported_model</code>: <em>"Providing previous_text or next_text is not yet supported with the 'eleven_v3' model."</em> {{claim:stitching-v3}} The pipeline passes neighbouring scenes by default and this site's own <a href="/experiments/text-handling/">text-handling lab</a> offered the same combination, so <b>the first request failed before any audio existed</b>. The lab now refuses the combination rather than sending it.</p></div><div class="fail ok"><p class="who">Prediction wrong, for this account</p><h3><code>eleven_v3</code> runs on a free-tier key</h3><p>It is listed by <code>GET /v1/models</code> and it generated all nine scenes, with <code>stability: 0.5</code> accepted and no 422. {{claim:v3-on-free}} The guide's worry was reasonable and this account did not share it — which is why the answer had to be run rather than reasoned.</p></div><div class="fail ok"><p class="who">Scoped, not bounded — in one response body</p><h3>The key said exactly which permission it lacked</h3><p>Creating a pronunciation dictionary returned <code>401</code>: <em>"missing the permission <code>pronunciation_dictionaries_write</code>"</em>. {{claim:key-scope-observed}} The platform names a missing permission precisely and has nothing equivalent to say about spend. <b>The only ceiling on that key was the free tier's 10,000 characters a month</b> — which is the argument on <a href="/#5-the-bounding-primitive">§5</a>, arriving as an error message.</p></div></div>

## 0b · The measurement that settles the drift question

This estate has reported **100–500 ms of drift over two minutes** across four reels since September, cause unattributed. Decoding every MP3 to PCM and comparing with the alignment:

<div class="tiles"><div class="tile cool"><b>0.0 ms</b><span>difference between the alignment's last end time and the decoded audio</span><em>nine scenes out of nine {{claim:alignment-exact}}</em></div><div class="tile cool"><b>9 / 9</b><span>scenes where the timing was exact, not approximate</span><em>the alignment <em>is</em> the duration</em></div><div class="tile hot"><b>up to 1.8 s</b><span>of silent video per scene added by ffmpeg's <code>-shortest</code></span><em>our encoder, not their speech {{claim:shortest-trap}}</em></div><div class="tile hot"><b>993 px</b><span>the viewport Chromium gave for a <code>--window-size</code> of 1080</span><em>every slide silently cropped until it was measured</em></div></div>

**So the drift is not in the audio.** A render that advances by the alignment is correct; one that trusts an encoder to stop when the audio does is not — and this render proved it by doing exactly that, adding 14 seconds across ten scenes before the bug was found. The fix is `-t <alignment end>` instead of `-shortest`.

That is a question closed, a fortnight after it was asked, for the price of decoding nine files.

## 0c · What it cost, and where it is

<div class="tiles"><div class="tile cool"><b>1,821</b><span>characters, in 9 requests, no re-renders</span><em>the script was written first and not changed after the audio existed</em></div><div class="tile cool"><b>$0.18</b><span>at the published list rate for <code>eleven_v3</code></span><em>a free-tier key, so it was paid in quota rather than money</em></div><div class="tile cool"><b>2:15</b><span>two cuts — 1920×1080 at 4.45 MB, 1080×1920 at 4.30 MB</span><em>the portrait cut reuses the same audio and cost nothing</em></div><div class="tile cool"><b>28</b><span>subtitle cues, from the same responses as the audio</span><em>no second call, no alignment pass, no transcription</em></div></div>

**The video, the nine narrations, the alignments, the slides, the subtitles and the findings are in an encrypted vault, not in this repository.** A report site should carry the report; 9 MB of media per reel belongs where media belongs, and the estate already has a place for it. What is published here is what a reader can use: the numbers, the failures, and the method.

**What this run cannot tell you is how it sounds.** The agent that made it cannot listen to it. Every figure above is measured; no claim is made about the quality of the read, or about how `eleven_v3` pronounces `sgit` — [the site's oldest open item](/ledger/#open-items) is still open, and the first person to play the file closes it.

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
