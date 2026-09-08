# First run of `TTS=elevenlabs` — the path nobody has executed

`tooling/scripts/sg-tts-shim-elevenlabs.js` and the `TTS=elevenlabs` branch of `02-render.mjs` were **written on 5 September 2026 from the API reference, in a container that could not reach `api.elevenlabs.io`.** Every other provider path (`kokoro`, `local`, `openrouter`) has produced a shipped video. This one has never made a sound.

You are the first person who can run it. Do it on **one scene**, not a full reel, and work through the four failure points below before spending a render.

---

## Step 0 · Prove the account before touching the pipeline

```bash
export ELEVENLABS_API_KEY=<key>            # environment only
bash materials/elevenlabs/examples/00-smoke.sh     # key valid, quota, one sentence of audio
bash materials/elevenlabs/examples/voices.sh       # pick a voice_id — note it
curl -s https://api.elevenlabs.io/v1/models -H "xi-api-key: $ELEVENLABS_API_KEY" | jq '.[] | {model_id, name, can_do_text_to_speech}'
```

These example scripts are **also unrun**. If one is wrong, fix it and note the fix — the site's `elevenlabs.md` §9 wants exactly this kind of finding.

Record the `voice_id` you choose and put it in the site's ElevenLabs page. `pNInz6obpgDQGcFmaJgB` (premade "Adam") is the only voice this estate has ever exercised, in the bench, at 5.0–5.8 s per 187-character generation.

## Step 1 · One scene, one render

Make a throwaway reel with a single scene and about twenty words of narration, then:

```bash
cd videos/<throwaway>/scripts
TTS=elevenlabs VOICE=<voice_id> FORMAT=landscape node 02-render.mjs 2>&1 | grep --line-buffered -v UNDICI
```

Check three things in `../render-log.landscape.json`: the generation's `durationMs` is close to the audio you hear, `cost` is populated and sane, and `../narration-timings.landscape.json` exists with an `alignment` object per scene. If all three hold, the path works and you can render a real reel.

---

## The four things most likely to break, and the fix for each

### 1 · `pcm_44100` may not be on your plan — **most likely failure**

The shim requests `?output_format=pcm_44100` and converts 16-bit little-endian PCM straight to `Float32Array`, which avoids needing a decoder. **PCM output formats are gated to higher subscription tiers.** On a Creator-tier key this is likely to come back `401`/`422` with a `detail` naming the output format.

**Fix:** request MP3 and decode it in the page. In `sg-tts-shim-elevenlabs.js`, change the query to `output_format=mp3_44100_128` and replace the `pcm16ToFloat32` call with a decode:

```js
const bytes = Uint8Array.from(atob(j.audio_base64), c => c.charCodeAt(0));
const ctx = new (window.AudioContext || window.webkitAudioContext)();
const buf = await ctx.decodeAudioData(bytes.buffer);
const data = buf.getChannelData(0);          // Float32Array, mono
const SAMPLE_RATE_ACTUAL = buf.sampleRate;   // return this, not the constant
```

Return `{ data, sampleRate: SAMPLE_RATE_ACTUAL, durationSecs: buf.duration }`. Everything downstream takes the sample rate from the return value, so nothing else changes. **Note it in `FINDINGS.md` either way** — "pcm worked on tier X" is as useful a finding as the failure.

### 2 · `eleven_v3` may not be available on your key, or may reject the settings

The shim defaults to `model_id: eleven_v3` and sends `voice_settings.stability: 0.5`. Two risks: v3 may not be enabled for API use on your account, and v3 treats stability as three discrete modes (Creative 0.0 / Natural 0.5 / Robust 1.0) rather than a continuum — an arbitrary value can `422`.

**Fix:** `ELEVEN_MODEL=eleven_multilingual_v2` is the stable workhorse and takes a continuous stability. For narration of somebody else's compliance standard, **Natural (0.5) or Robust (1.0), never Creative** — Creative hallucinates. A `422` body's `detail` names the offending field; the shim surfaces it.

### 3 · Timestamps may not come back in the shape the shim expects

The shim reads `j.alignment` and `j.normalized_alignment`, each `{characters, character_start_times_seconds, character_end_times_seconds}`, and pushes both into `window.__ttsAlignments`, which `02-render.mjs` writes to `narration-timings.<format>.json`.

**Check rather than assume**: dump one response before trusting it. If `alignment` is null on your model (some models do not return it), the whole SRT/chapters/karaoke chain is unavailable on that model and you should switch models rather than work around it — the alignment is the reason to be here.

### 4 · Concurrency — `POOL=2` fires two generations at once

Never tested against the plan's concurrency limit. A `429` mid-render wastes the whole run.

**Fix:** run the first real reel with `POOL=1`. It is slower and it cannot 429. Raise it once you know the limit, and write the limit into the site's page — it is a fact nobody publishes.

---

## Two smaller things worth knowing

- **`SPEED` means something different here.** For Kokoro it is a duration scale applied after synthesis; for ElevenLabs it is `voice_settings.speed`, clamped by the shim to the API's 0.7–1.2. The shim already clamps, so a `SPEED=1.5` inherited from a Kokoro command line will silently become 1.2 rather than erroring. Check the closing slide, which prints the speed actually used.
- **The cost on the closing slide is list price arithmetic**, not a billed figure: characters × $0.10/1k for v3, × $0.05 for flash and turbo. Compare it once against `GET /v1/user/subscription`'s character counter before and after a render, and if it disagrees, fix the rate in `02-render.mjs` and say so in the findings.

---

## Optional, and high value: the pronunciation dictionary

Do this **after** the first successful render, not before.

1. Run the names test — the bench's one-click button, or just narrate a scene containing `sgit`, `sgit.ai`, `SG/Vault`, `SGraph`, `AIUC-1`, `SHA-256`, `llms.txt`, `OWASP`, `VoiceDebrief`, `v0.1.29`. Listen. Write down which ones are wrong.
2. Build the lexicon from `materials/elevenlabs/pronunciations.pls`, correcting it against what you actually heard. Aliases work on every model; **phoneme rules only on `eleven_flash_v2` and `eleven_v3`**.
3. Upload it (`docs/04` has the two curl calls), note the id and version, and pass `ELEVEN_DICT=<id>:<version_id>` to the render.
4. **Then strip the phonetic spellings out of `reel.json`** — `sgit dot ai` becomes `sgit.ai` — and re-render. The caption band will read like prose for the first time.

That last step is the visible payoff, and it is worth a before/after screenshot on the site.

---

## Write down what happened

Whatever you find, put it in that reel's `FINDINGS.md` and in the site's `elevenlabs.md` §9. Right now the site says the shim is unrun, which is honest but not interesting. **"It was run on this date, on this tier, and here is what broke" is the most valuable paragraph the page could gain**, and you are the only one who can write it.

---

*This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).*
