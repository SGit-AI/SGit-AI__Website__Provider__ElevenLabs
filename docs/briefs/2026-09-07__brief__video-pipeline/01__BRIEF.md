# Brief — make narrated videos for `elevenlabs.providers.sgit.ai`, narrated by ElevenLabs

**For:** the Claude Code agent working on `SGit-AI__Website__Provider__ElevenLabs`
**From:** the session that built the pipeline and shipped four reels with it
**Date:** 7 September 2026

You are getting a **working, measured video pipeline** — not a design. Four reels have been made with it (two landscape, two portrait, plus two more cuts), and every number in the docs here was observed rather than estimated. What you have that the pipeline's author did not is **network access to `api.elevenlabs.io`**, which makes you the first person able to run its fourth narration provider. That path is written and unrun. See `ELEVENLABS-FIRST-RUN.md` before anything else.

---

## 0 · Ninety-second version

```bash
cp -r materials/tooling <your repo>/tooling          # 724 KB, self-contained
cd <your repo>/tooling && bash bootstrap.sh && source ./env.sh
mkdir -p ../videos/<slug>/scripts && cp scripts/* ../videos/<slug>/scripts/
cp reel.template.json ../videos/<slug>/reel.json     # WRITE THE SCRIPT FIRST
cd ../videos/<slug>/scripts
FORMAT=landscape node 01-capture.mjs                 # shoot the stills
export ELEVENLABS_API_KEY=<your key>                 # environment only, never a file
TTS=elevenlabs VOICE=<voice_id> SPEED=1.1 FORMAT=landscape node 02-render.mjs
bash 03-frames.sh && node 04-doc.mjs                 # frames to check, storyboard
```

**The real manual is `materials/tooling/SKILL.md`.** It is 244 lines, complete, and written to be followed unattended. This brief is what changes for *you*; that file is how the thing works. Read it before writing a line of `reel.json`.

---

## 1 · The pipeline, in one paragraph

`reel.json` is the source of truth and is written **first** — scenes, each with `narration` (what is spoken and shown in the caption band), `caption` (four to eight words for the muted viewer, deliberately *not* the narration), and `shot` (a URL, optional `steps` to click/scroll the page into the right state, and annotation targets). `01-capture.mjs` drives Chromium, resolves each target to a real element, paints a spotlight on it and screenshots. `02-render.mjs` composes each still into a slide, narrates it with whichever TTS provider `TTS=` names, records the result in real time through a vendored `video-creator` tool, and remuxes to WebM. Then ffmpeg makes the MP4, `03-frames.sh` gives you stills to judge it without watching, and `04-doc.mjs` writes a storyboard page and PDF. The closing slide of every video prints the measured numbers of its own making, including the API cost.

Two reference reels are in `materials/examples/`, and two finished MP4s are in `materials/reference-videos/` so you can see the target before you aim at it.

---

## 2 · Read in this order

| # | File | Why |
|---|---|---|
| 1 | `ELEVENLABS-FIRST-RUN.md` | The unrun code path, its four likely failure points, and the fallback for each |
| 2 | `materials/tooling/SKILL.md` | The manual. Sections 0–5 are the workflow; the last two tables are every failure seen so far and its fix |
| 3 | `materials/examples/voicedebrief-deck.reel.json` | A slide-based reel — no capture, `layout.fit: contain`, `narrationShorts` for the portrait cut |
| 4 | `materials/examples/aiuc-1-graph.reel.json` | An app-driven reel — `shot.steps` clicks, `el:css:` targets |
| 5 | `materials/examples/*.FINDINGS.md` | What each run actually cost and what bit |
| 6 | `materials/elevenlabs/docs/03-timestamps-to-srt.md` | The capability that makes your videos better than the shipped four |

---

## 3 · What is different for you

| | The vault agent (me) | You |
|---|---|---|
| `api.elevenlabs.io` | **Refused** by the container's egress proxy | **Reachable** — this is the whole point |
| Narration used | Kokoro (free, local) and OpenRouter `gpt-audio` | **ElevenLabs**, never run before |
| Key storage | Owner-sealed in `.vault/elevenlabs/config.json` | **Environment variable for the run only.** You have no vault; do not invent a substitute |
| Repo visibility | A read-only-shared private vault | **A public GitHub repo.** Every mistake is public and permanent |
| Publishing | `sgit push --token …`, `build-catalogue.py` | Git commit into the site; `build-catalogue.py` is **not** for you |
| Chromium egress | Needed the `browser.mjs` bridge | `bootstrap.sh` probes it. If the direct-https probe passes, the bridge is harmless and you change nothing |

Everything else — the scripts, the render tool, the compositor, the failure table — transfers unchanged.

**`build-catalogue.py` and the `sgit` steps in §5 of `SKILL.md` do not apply to you.** Ignore them; §10 below is your publishing step.

---

## 4 · What ElevenLabs buys you that the four shipped reels do not have

This matters because it is the reason to bother, and because it is also *content for the site*. Every item below is a claim the provider page makes; making the video with it is the demonstration.

- **A speed control on a paid voice.** OpenRouter's `gpt-audio` has none, which is why the deck reel needed `narrationShorts` to fit under three minutes. `voice_settings.speed` takes 0.7–1.2; `SPEED=1.1` is a natural brisker read.
- **Character-level timestamps → a real `.srt`.** `TTS=elevenlabs` writes `narration-timings.<format>.json` beside the render log, with the alignment of every scene. `materials/elevenlabs/docs/03` has the grouping rule (characters → words → cues at 84 chars / 0.6 s gap / 6 s max). YouTube's auto-captions render "2,788 nodes" as words and get `sgit` wrong every time; uploading your own SRT is strictly better and free once you have the alignment.
- **Chapters to the sentence** rather than to the scene, from the same alignment.
- **A pronunciation dictionary**, which fixes a visible ugliness: today the narration text *is* the caption text, so `reel.json` says `sgit dot ai`, `A I U C one`, `S H A two five six` and the viewer reads that in the band. With a PLS lexicon the text says `sgit.ai` and the voice still says it right. `materials/elevenlabs/pronunciations.pls` is a starting lexicon — **never uploaded, never heard**. Build it as `docs/04` describes, then strip the phonetic spellings out of `reel.json`.
- **`seed`** for a reproducible read, and **`previous_text`/`next_text`** for prosody continuity across scenes (the render already passes neighbours).

**The one that writes itself:** a video *about* the timestamps API, whose own subtitles were generated from the timestamps it is describing, with the cost of making it printed on its closing slide. That is the site's §8 and §3 argued in ninety seconds, and no competitor page can do it.

---

## 5 · Cost, so you can budget before you spend

Measured, 5 September 2026, list price. `eleven_v3` is $0.10/1k characters; flash and turbo are $0.05.

| Workload | Characters | Cost on v3 |
|---|---|---|
| One scene, 187 chars (the bench sample) | 187 | $0.019 |
| A 2-minute landscape reel (~260 words) | ~1,600 | **~$0.16** |
| A 4-minute landscape reel (~600 words) | ~3,600 | **~$0.36** |
| A portrait cut of the same (tighter `narrationShorts`) | ~60–70% of the above | — |
| A re-render after a script fix | full price again | budget for three or four |

**Budget ~$1.50 for the first video** including the re-runs you will need, and drop to `ELEVEN_MODEL=eleven_flash_v2_5` for draft passes at half the price. The render prints the cost on the closing slide and in `render-log.<format>.json` automatically — that figure is priced from the published rate; the subscription character counter is the ground truth.

---

## 6 · The script rules that actually cost time when broken

From `SKILL.md` §1, repeated because they are the ones that bite:

1. **2.1 words per second.** Count words before any audio exists. Ten scenes want 200–260 words including intro and outro.
2. **The intro previews; scene one starts.** Otherwise the viewer hears the same sentence twice.
3. **The caption is not the narration.** Four to eight words, different from the sentence spoken over it.
4. **Element targets, never hand-typed rects.** `el:css:<selector>` inside an app, `el:heading:`/`el:table`/`el:code` on a page. Hand-typed rects were ±15 px off and the project lead spotted it on the storyboard.
5. **Anchor *above* the target.** `scrollTo` puts the text near the top and the resolver takes the first match at or below it; anchoring on the sentence *under* a table finds the next table, off-screen.
6. **Read every still before rendering.** ~3 s each. `"resolved": false` means fix the target and re-shoot.
7. **Portrait must land under 3:00** or YouTube will not treat it as a Short. Aim for a real margin — 2:51, not 2:58. Use `narrationShorts` plus `SPEED`.

---

## 7 · Three videos worth making first

Suggestions, in the order I would build them — each is short, each demonstrates a claim the site makes.

1. **"The bench, in ninety seconds."** Paste a key, list voices, generate with timestamps, watch the words light up, build the SRT. App-driven capture: `shot.steps` clicks, `el:css:` targets. This is `materials/examples/aiuc-1-graph.reel.json`'s shape. **Ship its own SRT alongside it** and say so on screen.
2. **"Four patterns."** Slides, no capture at all — write the stills as an HTML deck or export them, hand-write `capture-log.json` with a `source` string, `layout.fit: contain`, `IMG=images`. This is `materials/examples/voicedebrief-deck.reel.json`'s shape. The strongest ninety seconds on the site, because it is the argument.
3. **"What it cost and what went wrong."** The §8/§9 sections read aloud over the real numbers. Nobody else publishes this, which is exactly why it is worth a video.

For each: landscape first, then a portrait cut under 3:00, plus a title and description. `materials/examples/*.PUBLISH.md` shows the shape of those, chapters included.

---

## 8 · Secret hygiene — the rules changed when the repo went public

The pipeline was built inside a private vault. Your repo is on GitHub and public. Three rules:

- **The key lives in the environment for the life of one command.** `export ELEVENLABS_API_KEY=…` before the render, and nowhere else. Never in `reel.json`, never in a script, never in a `.env` that could be committed, never in a shell history file you then commit.
- **Grep before every commit:** `grep -rInE "sk_[A-Za-z0-9]{32,}|sk-or-v1-|xi-api-key: sk_|hf_[A-Za-z0-9]{20}"` must print nothing. The env var *names* appear in `02-render.mjs`; a value never may. Wire this into CI as a required check — the same scan the site's own acceptance list asks for.
- **The render logs are committed artefacts.** Check `render-log.*.json` and `narration-timings.*.json` before adding them: they carry request ids and character counts, which are fine, but read them once rather than assuming.

Nothing in the pipeline writes the key anywhere; the risk is you, in a hurry, at the end of a long run.

---

## 9 · Publishing into the site

The vault's catalogue app does not exist here, so decide where video lives on the site before you make one. What I would do:

- MP4 (H.264 + AAC, `+faststart`) as the delivered file — **not** WebM. WhatsApp refuses WebM, iOS Safari plays H.264 natively, YouTube takes either, and the MP4 is smaller (3.7 MB against 10.1 for the same two minutes).
- A `videos/<slug>/` folder per reel holding `reel.json`, the stills, both cuts, the storyboard, the logs and `FINDINGS.md` — the same shape as the examples, because the storyboard and the findings are themselves publishable content for a site whose thesis is *show the working*.
- **Watch GitHub's limits:** 100 MB per file hard, and Pages is a soft 1 GB with 100 GB/month of bandwidth. A 4 MB reel is nothing; twenty reels plus stills is worth a thought. If video becomes the site's bulk, host the files elsewhere and embed.
- Put the `.srt` next to the MP4 and reference it from the `<video>` element as a `<track>`. It is the demonstration, not a nicety.

---

## 10 · Done means

- [ ] `bootstrap.sh` ran; `source ./env.sh` done in the shell that renders.
- [ ] `reel.json` written **before** any capture, word count checked against 2.1 wps.
- [ ] Every still read; no `"resolved": false` left.
- [ ] `ELEVENLABS-FIRST-RUN.md` worked through on a one-scene reel **before** the full render.
- [ ] Landscape rendered, frames checked (title, a middle scene, the closing slide), MP4 made.
- [ ] Portrait cut under 3:00 with real margin.
- [ ] `.srt` generated from `narration-timings.*.json` and shipped with the video.
- [ ] `FINDINGS.md` written with the real numbers — including what the ElevenLabs path did on its first ever run, which is new information for everyone.
- [ ] Secret grep clean; key never left the environment.
- [ ] Title, description and chapters written.

---

## 11 · What I could not tell you

- **Whether the shim works.** It has never executed. `ELEVENLABS-FIRST-RUN.md` is my best guess at where it breaks and how to fix each one, but it is a guess.
- **Which names `eleven_v3` mispronounces.** The names test was written and never run, so `pronunciations.pls` is a hypothesis.
- **How the API behaves under the render's concurrency.** `POOL=2` fires two generations at once; a bigger pool fires more. The plan's concurrency limit has never been tested against it.
- **Whether the drift figure changes with a different provider.** The four reels drifted 100–500 ms over two minutes, cause unknown. With character timestamps you can finally attribute it: sum the alignments' last end times and compare with the recorder's `actualMs`. That measurement has never been possible before and takes about ten minutes.

---

*This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).*
