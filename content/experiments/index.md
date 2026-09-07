---
title: Experiments — twelve labs against one API
description: "A dozen browser labs that exercise the ElevenLabs API feature by feature: voices, models, settings, timestamps, lexicons, concurrency, alignment, dialogue, sound, key scope and cost. Your key, your browser, nothing sent anywhere else."
lead: "This site is a report, and a report is worth more when the reader can re-run it. These are the labs the evaluation *should* have had — one per feature, each with the method written down, each printing a result you can paste back as evidence."
order: 5
toc: true
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
  note: "The bench came from the source vault; the other eleven labs were written for this site."
---

{{lab-header}}

<div class="warnbox"><p><b>Every lab here is unrun by its authors.</b> {{claim:labs-unrun}} They were written against the vendor's published request and response shapes by a session with no network access to the API and no key {{claim:egress-blocked}}. The one exception is <a href="/bench/">the bench</a>, which a human ran from their own browser on 5 September 2026 — and which is the source of every {{badge:verified}} claim on this site. If a lab is broken, the log at the bottom of it will tell you how, and <a href="https://github.com/SGit-AI/SGit-AI__Website__Provider__ElevenLabs">the repository</a> is where that becomes a fix.</p></div>

{{experiments}}

## How these are built

Every lab shares one runtime, [`lab.js`](/assets/lab.js) — about 350 lines, no dependencies, no build step, readable in one sitting. That is deliberate: a site whose argument is *watch where your credential goes* should let you watch. It does three things and nothing else.

1. **Keeps your keys in `localStorage`,** several of them, named, switchable — so a scoped key and a full key can be compared without retyping either. Nothing is sent to this site; there is no server here to send it to.
2. **Calls exactly one host,** `api.elevenlabs.io`, with your key in the `xi-api-key` header {{claim:api-key-shape}}, and logs every request it makes at the bottom of the page. A CI check on this repository fails the build if any other network origin appears in the built site {{claim:keys-local-only}}.
3. **Does the shared arithmetic** — characters to cost, alignment to words to cues, results to markdown you can paste back into whatever keeps your evidence.

## What to run first

If you have a key and ten minutes, in this order — it closes the four oldest open items on the [ledger](/ledger/#open-items) for about **fifteen cents**:

1. [The bench](/bench/), section 5 — **the names test**. Nobody has pressed this button since 5 September {{claim:names-test}}. Two minutes, and the site can finally say which names the model gets wrong.
2. [The pronunciation lab](/experiments/pronunciation/) — attach the lexicon and hear whether the aliases fix them {{claim:lexicon-hypothesis}}.
3. [The concurrency probe](/experiments/concurrency/) — find the wall, so the semaphore holds a measurement instead of a guess {{claim:concurrency-unknown}}.
4. [The captions studio](/experiments/captions/) — tune the cue rule against a real script and tell us what numbers you landed on {{claim:cue-rule}}.

The [cost model](/experiments/cost/) needs no key at all and answers the question people usually ask first.

## What a lab is not

It is not a product, it is not a proxy, and it is not a pattern to copy into an application you ship. Each of these asks you to put a full account credential into a web page, which is [pattern 0 with a ceiling](/patterns/) — defensible for the key's owner testing their own key, indefensible for anything with users. The publishable version of these pages has no key box at all, and it is [specified rather than built](/pattern-three/) {{claim:sg-tts-spec}}.
