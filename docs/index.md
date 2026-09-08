---
title: ElevenLabs — text to speech with character-level timestamps
description: "An independent report on the ElevenLabs API: what it cost on a named workload on a named date, what broke, and which of four client-side credential patterns the product can actually support."
lead: "This is a report, not a tutorial. The vendor's documentation explains the API better than we can and stays fresher; what follows is what happened when we actually used it — **what it cost on a named workload on a named date, what broke, and which credential patterns the product can support.** Sections 8 and 9 are the point of the page."
order: 1
toc: true
wide: false
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
  note: "Prose from platforms/elevenlabs.md, with the figures behind it from four reels' worth of pipeline findings."
platform_grants:
  - verb: send
    object: text
    reach: endpoint
    reversible: true
    product: Text to speech
    note: the words you send leave for the model
  - verb: read
    object: audio+timing
    reach: self
    reversible: true
    product: Text to speech
    note: "character-level alignment — the capability the vendor does not frame as one"
  - verb: spend
    object: characters
    reach: tenant
    reversible: true
    product: any
    note: bounded by the plan's monthly quota and nothing narrower
  - verb: create
    object: voice
    reach: tenant
    reversible: true
    product: Voices — instant and professional cloning
    note: "**the row a reader will not expect.** A voice that did not exist before, from under two minutes of audio. Deletable, so reversible in the platform's terms — and consent is not a technical control"
  - verb: read
    object: audio
    reach: tenant
    reversible: true
    product: Speech to text (Scribe), forced alignment
    note: transcription of material you supply, priced by the hour
  - verb: send
    object: media
    reach: endpoint
    reversible: true
    product: Dubbing
    note: media you supply, re-voiced in another language
  - verb: send
    object: message
    reach: world
    reversible: false
    product: Agents (conversational)
    note: "**the only irreversible row this vendor offers.** A live agent speaks to a person, and a thing said to somebody cannot be unsaid"
grants:
  - verb: spend
    object: characters
    reach: tenant
    reversible: true
    bounded_by: the plan's monthly quota only — there is no per-key spend limit
  - verb: send
    object: text
    reach: endpoint
    reversible: true
    bounded_by: narration text leaves for the model
  - verb: read
    object: audio+timing
    reach: self
    reversible: true
    bounded_by: "character-level alignment — the new capability this API brings"
not_granted: [voice cloning, dubbing, agents]
patterns:
  - provider: ElevenLabs
    product: Text to speech (REST)
    server: "Yes — ours, until sg.tts ships"
    p0:
      verdict: never
      note: "CORS allows it; the account quota is the only bound"
    p1:
      verdict: no
      note: "no per-key spend limit exists"
    p2:
      verdict: yes
      note: "only with a server we run"
    p3:
      verdict: spec
      note: "sg.tts specified; terms file in the vault"
  - provider: ElevenLabs
    product: Agents (conversational)
    server: "Yes — the vendor's minter holds your key"
    p0:
      verdict: never
      note: "the vendor forbids it explicitly"
    p1:
      verdict: no
      note: "no bounded key to mint"
    p2:
      verdict: yes
      note: "vendor signed URL, 15 min; or a hostname allowlist — not both"
    p3:
      verdict: na
      note: "not attempted"
---

<div class="note"><p><b>How to read this page.</b> Every factual claim carries a chip saying how we know it: {{badge:verified}} we ran it and watched it work, on that date · {{badge:measured}} our own pipeline produced this number on a named workload · {{badge:docs}} we read it in the vendor's documentation on that date and never executed it · {{badge:spec}} it does not exist yet · {{badge:unrun}} we wrote it and never ran it · {{badge:projected}} arithmetic, with the workings shown. Click any chip for <a href="/ledger/">the ledger</a>, which lists all of them in one table.</p></div>

## What this site is, and is not

**It is narrower than the vendor's own environment, not better.** The vendor serves millions of users across every workload; this site serves one — narrating explainer videos from a scripted pipeline — and reports what that cost, where the key had to live, and what broke. A general-purpose interface cannot be narrow, which is why this one does not try to be: [the labs here](/experiments/) exist because the vendor's own console does not fit this workflow, not because it is inadequate.

**It is a report with a workbench attached, not a tutorial and not an index of somebody else's documentation.** If a section here could be replaced by a link to the vendor, it should be deleted, and the vendor's page is linked with the date we read it. What this site has that nobody else does is [what it cost on a named workload on a named date](/#8-what-it-cost), [what went wrong](/#9-what-went-wrong), and [which credential patterns the product can actually support](/patterns/).

**"Provider" here means one thing only: a service that serves models over an API** — the sense this estate's own code uses, where a constant of that name holds an entry per model service. It does not mean a customer who redistributes capability to the people they serve, which is the other established sense in this estate and is not what any page here is about.

**It is not an endorsement, and not the vendor's.** [No commercial relationship exists](/disclosures/), the page saying so shipped before there was anything to disclose, and every claim carries [the state that says how we know it](/ledger/).

## 1 · Disclosure

**None.** No credits, programme, or commercial relationship with ElevenLabs as of 5 September 2026. The key used for the one session reported in §8 is a Creator-tier key we pay for ourselves at list price. The full list — which currently has no entries in the "relationship" column — is at [/disclosures/](/disclosures/), and it shipped with this site's first version precisely so that the page's existence is not read as evidence of a relationship.

## 2 · What it grants

The rows an agent's grant gains when this platform is connected, as capability tuples — *verb × object class × reach*, with reversibility marked. This is the block a capability index joins on; it is emitted as front-matter in [this page's markdown](index.md) as well as in the table below.

{{grants}}

**Read the two tables as one argument.** The first is what an agent gains the moment this provider is connected at all; the second is what the key this evaluation actually used can reach. The gap between them is the work a scope does, and it is the only part of a credential story this vendor lets you control.

**The row worth stopping on is `create × voice × tenant`.** Connecting this provider gives an agent the capability to *produce a voice that did not exist* — instant cloning takes under two minutes of audio. That is a different order of thing from producing audio, no vendor page frames it as a capability, and the platform's controls for it are procedural rather than technical: professional cloning requires verification of the speaker, and instant cloning requires you to have the right to the recording you upload. **Consent is not something the API can check.** Our key is scoped to exclude it, and the [key-scope probe](/experiments/key-scope/) is how you check that yours is too.

**One row a reader might expect is deliberately absent.** It has been proposed that connecting a voice platform grants `send × audio × world`, irreversibly, on the reasoning that audio sent is sent. **Not for this product.** The text-to-speech endpoint returns audio to the caller; nothing leaves for the world, and the estate's own primitive distinguishes `endpoint` reach from `world` reach exactly here. The irreversible row this vendor does offer is Agents, in the table above, and it is scoped out of our key. Saying otherwise would tell a reader that generating narration publishes it — which is [the error §4 exists to prevent](/#4-where-the-key-goes), one product over. {{claim:agents-only-signed-urls}}

Two more things are worth saying in prose. First, **`read × audio+timing × self` is the new capability** — this API returns the start and end time of every character it speaks, which the pipeline that drove this evaluation never had from any other provider. Everything in the [captions studio](/experiments/captions/) is arithmetic on that array. Second, **nothing our key grants reaches the world.** The pipeline receives audio; publishing a video is a separate, human act by a person who watched it first. That distinction is the difference between a narration tool and a voice agent, and it is why Agents is scoped out of the key rather than merely unused.

## 3 · Which pattern — and for which product

A vendor with several products has several answers, so this section is indexed by product, not by vendor. The four patterns are defined on [/patterns/](/patterns/); the generated matrix, including the sibling provider, is at [/comparison/](/comparison/).

**Text to speech (the REST API — what we use).**

- **Pattern 0, key in the page:** technically available. CORS permits a browser to call `api.elevenlabs.io` directly {{claim:cors-browser}} — and the only bound on that key is the account's monthly quota {{claim:no-per-key-spend-limit}}. So a key in a published page is *pattern 0 with a ceiling*. **Never publish one.** Every lab on this site is the narrower case: the key's owner, testing their own key, in their own browser.
- **Pattern 1, bounded key in the page:** **not available.** ElevenLabs keys are *scoped*, not *bounded* — see §5.
- **Pattern 2, short-lived token:** available **only with a server we run**. The vendor offers no short-lived credential for TTS {{claim:agents-only-signed-urls}}. Such a minter would be ours to build, host and pay for; it does not exist.
- **Pattern 3, host holds the key:** [specified, not shipped](/pattern-three/) {{claim:sg-tts-spec}}.

**Agents (conversational).** Pattern 2 with the vendor's own signed URL (15 minutes), or a hostname allowlist — and the vendor's documentation says not to configure both on one agent {{claim:agents-only-signed-urls}}. **These mechanisms are the reason §4 exists, and they do not apply to text to speech.**

## 4 · Where the key goes

Every quote below carries the **product** it belongs to, the URL, and the date we read it. This is not pedantry: an earlier draft of our own strategy quoted the Agents rule on a TTS page, which would have sent a reader off to build a signed-URL minter for an endpoint that does not accept one.

**Agents product** — read 5 September 2026 at <https://elevenlabs.io/docs/eleven-agents/customization/authentication>: "Never expose your ElevenLabs API key client-side." Signed URLs "are valid for 15 minutes… the conversation must be initiated within the 15 minute window"; allowlists use exact hostname matching; "Do not configure signed URLs and allowlists together on the same agent." {{claim:agents-only-signed-urls}}

**Text-to-speech product** — there is no equivalent page. The key goes in the `xi-api-key` request header {{claim:api-key-shape}}, and the only vendor-side control is **scoping a key to endpoints** in the dashboard. No signed URL, no allowlist, no origin check. A TTS key is a bearer credential for the account's quota, and the vendor's client-side warning above is written about a different product — which does not make it wrong here, only unenforceable here.

Where the key goes in our own estate, for completeness: owner-sealed at `.vault/elevenlabs/config.json` (AES-256-GCM under a key derived from the vault's *write* key, so a read-key holder cannot open it), opened for the life of one shell command. A key pasted into a lab on this site goes to this browser's `localStorage` and nowhere else {{claim:keys-local-only}}.

## 5 · The bounding primitive

**The plan's monthly character quota**, reported by `GET /v1/user/subscription` {{claim:plan-quotas}}. That is the whole bound, and it belongs to the account, not to the key.

Per key, ElevenLabs gives you **scope, not spend**: a key can be restricted to endpoints — text-to-speech yes, dubbing no — which limits *what a leaked key can do*, and does nothing at all to limit *how much of your quota it can burn* {{claim:no-per-key-spend-limit}}.

**What it does not cap:**

- Any single key can consume the whole account's quota.
- Nothing resets faster than the billing cycle — there is no daily or weekly window to fall back to.
- There is no per-key limit, and therefore no equivalent of the thing that saved us on the sibling provider: a refusal at a ceiling you chose in advance {{claim:openrouter-402}}.

A leaked ElevenLabs key is bounded by the plan. A leaked OpenRouter provisioned key is bounded by the number you typed when you minted it. That difference is the entire reason the [comparison table](/comparison/) earns its place on this site.

## 6 · The minimal working example

The smallest thing that runs, as a file rather than a snippet — and every one of these is **written from the vendor's reference and never executed** {{claim:examples-unrun}}, because the container that wrote them could not reach the API {{claim:egress-blocked}}.

{{examples}}

The pipeline invocation they were written for:

```bash
export ELEVENLABS_API_KEY=$(node tooling/scripts/vault-secrets.mjs open elevenlabs)
node examples/tts-timestamps.mjs "<text>" <voice_id> /tmp/out   # → .wav + .words.json + .srt
```

The interactive version is [the bench](/bench/), which *has* run: it is the source of every {{badge:verified}} chip on this page. The rest of the labs — [twelve of them](/experiments/) — extend the bench to the features this evaluation did not reach, and they are all {{claim:labs-unrun}}.

## 7 · What we use it for

Nothing in a shipped video yet, and it is worth saying that plainly before the numbers.

The workload is a video pipeline that renders explainer reels from a `reel.json` script: one narration string per scene, rendered to audio, composited over stills with the narration text on screen as a caption band. It has run with three speech providers — a local Kokoro model ($0), an OpenRouter-hosted `gpt-audio` (paid, measured in §8), and now this one, evaluated. Four reels, six cuts, are published.

What this API would change, ranked by how much it improves those videos rather than by how impressive it is:

1. **Character-level timestamps** — SRT sidecars, chapters accurate to the sentence, and a word-synced caption band. None of it is possible with either incumbent provider, and all of it is arithmetic on one response field. This is the reason for the evaluation.
2. **A speed control back.** `voice_settings.speed`, 0.7–1.2 {{claim:speed-range}}. The incumbent has none, and the cost of that was a portrait cut losing a third of its script rather than 15% of its pace {{claim:openrouter-no-speed}}.
3. **A pronunciation dictionary**, so the narration text can say `sgit.ai` instead of `sgit dot ai` — because in this pipeline **the narration text is the caption text**, so every pronunciation hack is on screen where viewers read it as a typo {{claim:phoneme-models}}.
4. **Forced alignment of the six existing cuts** — subtitles for videos already published, including the two Kokoro cuts that will never have API timestamps, for about two cents {{claim:alignment-stt-price}}.
5. **Scribe as a QA gate** — transcribe the finished file, diff it against the script, and catch automatically the two failures we have shipped and then caught by eye.

Items 1–3 have a lab each on this site. None of the five has been run.

## 8 · What it cost

<p class="small dim">Figures as of <b>7 September 2026</b>. List prices move; every number below carries the date, the workload size, the model and the request count, because "$0.30 for a 3:46 video" without them is not a fact, it is a vibe.</p>

<div class="tiles"><div class="tile cool"><b>$0.075</b><span>the entire ElevenLabs spend behind this report — one bench session, 5 Sep 2026</span><em>≈750 characters, 4 generations, <code>eleven_v3</code>, list price {{claim:bench-cost}}</em></div><div class="tile cool"><b>5.0–5.8&thinsp;s</b><span>round trip for a 187-character sample with timestamps, three samples</span><em>voice <code>pNInz6obpgDQGcFmaJgB</code>, <code>eleven_v3</code>, 5 Sep 2026 {{claim:latency-5s}}</em></div><div class="tile hot"><b>$0.2997</b><span>what the same class of workload cost on the incumbent: a 3:46 reel</span><em>599 words, 16 requests, <code>openai/gpt-audio</code>, 3 Sep 2026 {{claim:openrouter-cost-aiuc}}</em></div><div class="tile hot"><b>$0.18–0.36</b><span>projected for that reel here — flash to v3</span><em>3,600 characters × list rate; no such render has been paid for {{claim:projected-reel-costs}}</em></div></div>

**What we actually paid ElevenLabs, in full:** one bench session on 5 September 2026 — four generations of the same 187-character sample on `eleven_v3` with timestamps, about 750 characters, **$0.075** at the list rate of $0.10 per 1,000 characters {{claim:tts-prices}}. That is the entire measured spend. Everything else in this section is arithmetic, and is labelled as such.

**Projected, with the arithmetic shown.** Our scripts run about 6 characters per word; the word counts are measured from the four reels we have rendered {{claim:openrouter-cost-aiuc}}. Characters × the model's list rate:

| Reel | Words (measured) | ≈ chars | Flash @ $0.05/1k | v3 @ $0.10/1k | Actually paid (incumbent) |
|---|---:|---:|---:|---:|---:|
| AIUC-1 landscape 3:46 | 599 | 3,600 | $0.18 | $0.36 | $0.2997 |
| AIUC-1 portrait 2:09 | 318 | 1,900 | $0.10 | $0.19 | $0.1708 |
| VoiceDebrief deck landscape 4:17 | 699 | 4,200 | $0.21 | $0.42 | — (local model, $0) |
| VoiceDebrief deck portrait 2:51 | 480 | 2,900 | $0.14 | $0.29 | — (local model, $0) |
| VoiceDebrief pitch landscape 1:55 | 304 | 1,800 | $0.09 | $0.18 | $0.1554 |
| VoiceDebrief pitch portrait 1:24 | 190 | 1,150 | $0.06 | $0.12 | $0.1112 |
| **All six, one pass** | **2,590** | **15,550** | **$0.78** | **$1.56** | |

{{badge:projected}} for the two ElevenLabs columns — no reel has been rendered with this API. {{badge:measured}} for the words and for the right-hand column. The conclusion the arithmetic supports: **v3 costs about what the incumbent costs; flash costs half** — and both are a rounding error against the value of the timestamps, which is the only sound reason to switch.

**And one more measured figure, added 8 September 2026:** the first video made with this API — nine scenes, 1,821 characters, 2:08 of speech, two cuts — cost **$0.18 at list price** and was paid in a free tier's quota rather than in money {{claim:first-video}}. Zero re-renders, because the script was written first. [The full account is on /video/](/video/).

**Plan arithmetic.** At about 4,000 characters per video, a Creator plan's 220,000 monthly characters is roughly 50 videos a month {{claim:creator-covers-50}}. Rates and quotas: {{claim:plan-quotas}}, {{claim:tts-prices}}.

**Run the arithmetic on your own script** in the [cost model](/experiments/cost/) — it needs no key and makes no network call.

## 9 · What went wrong

The section nobody else writes. Four things, in the order they cost us time.

<div class="fails"><div class="fail"><p class="who">The host, not the vendor</p><h3>The app frame's CSP ate every request</h3><p>The first Connect from inside the vault app failed with <code>connect-src blob: data:</code> — the SG/App host locks every app frame to <em>no network at all</em>, by design, and the bench reported the generic <em>Failed to fetch</em>. Nothing to do with the key, the CORS headers, or the vendor. {{claim:csp-blocks}}</p><p><b>Fixed by</b> <code>"permissions": {"network": true}</code> in <code>app.json</code>, which omits the meta tag and makes the host's HUD show a standing "direct network access" chip, so the exception is never silent. <b>Right for this vault</b> — nothing in it is confidential except the sealed keys, which sit below the permission floor and are unreachable from any frame regardless. <b>Wrong for a vault whose app holds private content</b>: that grant is per-app and it is a real widening.</p></div><div class="fail"><p class="who">Us, not the vendor</p><h3>The container that wrote all of this could not reach the API</h3><p><code>api.elevenlabs.io:443</code> was refused to the authoring container by the egress proxy — <code>connect_rejected</code>, organization policy — from curl and from Node, on the regional hosts too. {{claim:egress-blocked}}</p><p>So the render shim {{claim:shim-unrun}}, every example script {{claim:examples-unrun}}, the pronunciation-dictionary upload {{claim:lexicon-hypothesis}} and every lab on this site {{claim:labs-unrun}} were written from the vendor's reference and have never been executed. <b>This is why the site is badged the way it is.</b> The one exception is the bench, run from a human's own browser, which is the reason there are any {{badge:verified}} chips at all.</p></div><div class="fail ok"><p class="who">Caught in review, before it shipped</p><h3>The mechanism we nearly documented was the wrong product's</h3><p>An earlier draft carried the Agents rules — "never expose your key client-side", the 15-minute signed URL, the hostname allowlist — as if they governed text to speech. They do not: <b>the TTS REST API has neither mechanism.</b> {{claim:agents-only-signed-urls}}</p><p>Had it shipped, a reader could have spent a week building a signed-URL minter for an endpoint that does not accept one. The conclusion survived the correction — TTS still needs a server for pattern 2 — but the mechanism named did not. Hence the rule this page obeys: <b>every quote carries its product.</b></p></div><div class="fail open"><p class="who">Still open</p><h3>Concurrency is unknown, and our render fires 16 requests at once</h3><p>Concurrent request limits scale with the plan. Our render fires every scene in parallel — 10 to 16 requests — so a <code>429</code> mid-render is the most likely first failure on a small plan, and we have never provoked one to find out where the wall is. {{claim:concurrency-unknown}}</p><p>The <a href="/experiments/concurrency/">concurrency probe</a> exists to answer exactly this, at a cost of a few cents. Nobody has run it. Until somebody does, the honest planning number for a Starter or Creator plan is <em>unknown</em>, and the mitigation — a semaphore in the shim — is written but untested.</p></div></div>

### And what went wrong the first time somebody ran it

On 8 September 2026 the render path ran for the first time {{claim:first-video}}. Three of the four things that broke are the vendor's, and one is ours:

<div class="fails"><div class="fail"><p class="who">Their tier gate</p><h3>PCM output is Pro-and-above</h3><p><code>403</code>, naming the format. {{claim:pcm-gated}} The shim asks for PCM to skip a decoder, so on any lower tier that is a dead path with a six-line fallback.</p></div><div class="fail"><p class="who">Their model</p><h3>Stitching is not available on v3</h3><p><code>400 unsupported_model</code> for <code>previous_text</code>/<code>next_text</code>. {{claim:stitching-v3}} The first request failed before any audio existed, and <a href="/experiments/text-handling/">the lab that offered the same combination</a> now refuses it.</p></div><div class="fail ok"><p class="who">Their key scoping, working</p><h3>The 401 that names its own permission</h3><p><em>&ldquo;missing the permission <code>pronunciation_dictionaries_write</code>&rdquo;</em>. {{claim:key-scope-observed}} Precise about what the key may <em>do</em>, silent about what it may <em>spend</em> — which is <a href="/#5-the-bounding-primitive">§5</a> arriving as an error message.</p></div><div class="fail"><p class="who">Ours</p><h3>The encoder added 14 seconds of silence</h3><p>ffmpeg's <code>-shortest</code> with a looped still ran past the end of the audio, up to 1.8 s per scene. {{claim:shortest-trap}} <b>The provider's timing was exact to the millisecond</b> {{claim:alignment-exact}} — the drift was entirely ours, which is the first time this estate has been able to say which.</p></div></div>

### What has not gone wrong, because nobody has tried it

The most useful thing in this section is the list of failures we have *not yet had the opportunity to have.* {{claim:names-test}} {{claim:cue-rule}} {{claim:labs-unrun}} Every one of them has a lab on this site, and each lab prints a result you can paste back into the vault as evidence.

The full list of what remains unverified — and who could verify it — is [the open items](/ledger/#open-items), which is the last section of the ledger.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
