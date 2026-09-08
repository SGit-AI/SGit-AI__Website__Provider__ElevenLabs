---
title: Example files, and the lexicon
description: "The example scripts and the PLS pronunciation lexicon as downloadable files, with the invocation beside them. All of them written from the vendor's reference, none of them ever run."
lead: "Files, not screenshots of files. Every one of these was **written from the vendor's reference by a session that could not reach the API**, and none has ever been executed. They are published because unrun code with a badge is more useful than no code — and because the first person to run one will know more than the people who wrote it."
order: 60
toc: true
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
---

<div class="warnbox"><p><b>Badged unrun, and meant literally.</b> {{claim:examples-unrun}} {{claim:egress-blocked}} Expect a wrong field name, a changed response shape, or an endpoint that has moved. If you run one and it works — or does not — the correction path is <a href="https://github.com/SGit-AI/SGit-AI__Website__Provider__ElevenLabs">this site's repository</a>, and the <a href="/ledger/">ledger</a> row changes state with the date.</p></div>

## The scripts

{{examples}}

Each expects a key in the environment and nothing else — no SDK, no `npm install`, no dependency you have to trust:

```bash
export ELEVENLABS_API_KEY=...            # your own key, for one shell
bash 00-smoke.sh                          # is the key alive, what is the quota, one sentence of audio
bash voices.sh                            # voice_id · name · category · accent · gender · use case
bash tts.sh "the text" <voice_id> out.mp3
node tts-timestamps.mjs "the text" <voice_id> /tmp/out   # → .wav + .words.json + .srt
bash align.sh render.mp4 script.txt       # forced alignment of an existing video to its script
bash stt.sh render.mp4                    # Scribe transcription, for the QA diff
```

In the estate they came from, the key is not typed at all — it is opened from the vault's sealed config for the life of one command:

```bash
export ELEVENLABS_API_KEY=$(node tooling/scripts/vault-secrets.mjs open elevenlabs)
```

`tts-timestamps.mjs` is the interesting one: it asks for `pcm_44100` so the bytes go straight into a `Float32Array` with no decoder, wraps them in a 44-byte RIFF header by hand, then does the [characters → words → cues arithmetic](/experiments/captions/) and writes an SRT beside the WAV. It is 33 lines and has no dependencies. It has also never been run {{claim:examples-unrun}}.

## The lexicon

<p><a class="btn" href="/files/pronunciations.pls" download>Download pronunciations.pls</a> &nbsp; {{claim:lexicon-hypothesis}}</p>

A PLS lexicon for the estate's own vocabulary — `sgit`, `sgit.ai`, `SG/Vault`, `SGraph`, `AIUC-1`, `SHA-256`, `llms.txt`, `OWASP`, `PT-BR`, `José`, `v0.1.29`. Nobody publishes one of these, which is the only reason it is worth shipping: it is a starting point for anyone whose narration contains product names, initialisms and version numbers.

**It is a hypothesis.** It has never been uploaded, and not one alias in it has ever been heard aloud. Two facts govern how to use it {{claim:phoneme-models}}:

- **alias** rules are text substitution before synthesis, and work on every model;
- **phoneme** rules (IPA or CMU Arpabet) are honoured only by `eleven_flash_v2` and `eleven_v3` — other models ignore them **silently**, which is the failure mode to design against.

Start with aliases; move a word to a phoneme only when an alias still comes out wrong. The [pronunciation lab](/experiments/pronunciation/) exists to do exactly that comparison, and prints the result as markdown you can paste back into the file.

## Why they matter more here than usual

In the pipeline these came from, **the narration text is the caption text** — the words the voice speaks are drawn on screen. So every pronunciation hack is visible: the scripts in that vault say `sgit dot ai`, `A I U C one`, `S H A two five six`, `version zero point one point twenty-nine`, and viewers read them in the caption band as typos.

A lexicon moves the hack off the screen: the text says `sgit.ai`, the voice says it right, and the caption band reads like prose for the first time. That is a change a viewer would notice before they noticed the voice.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
