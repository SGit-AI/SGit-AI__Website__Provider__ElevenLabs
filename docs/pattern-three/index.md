---
title: Pattern three, for a voice API — the sg.tts specification
description: "What a browser app would look like if the vault host held the ElevenLabs key and enforced the terms: no key box, a spend cap the app cannot reach, and terms that travel with the content. Specified, not shipped."
lead: "This is the site's argument made concrete: **a browser application using a paid speech API without ever holding the key.** Everything on this page is a specification. `sg.tts` does not exist; nothing here describes software you can run today."
order: 40
toc: true
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
  note: "From elevenlabs/docs/10-pattern-three-sg-tts.md, which is a specification and is treated as one."
---

<div class="warnbox"><p><b>Future tense, throughout.</b> {{claim:sg-tts-spec}} <code>sg.tts.speak()</code> is a verb the SG/Vault host <em>would</em> gain. It is not implemented, not scheduled here, and not something to plan a product around. The one piece that is real is the terms file — <code>.vault/elevenlabs/config.json</code> — which exists in the source vault today, in the same shape and under the same seal as the host's model-router config.</p></div>

## What would exist already, if the verb landed tomorrow

Two of the three pieces are in place, which is the only reason this specification is worth publishing rather than filing.

| Piece | State | What it is |
|---|---|---|
| The terms file | real | `.vault/elevenlabs/config.json` — owner-sealed key, endpoint, defaults (model, voice, speed, output format) and `limits` (`maxCostPerSession`, `maxCharsPerRequest`, `maxConcurrent`). Sealed with AES-256-GCM under a key derived from the vault's **write** key, so a read-key holder cannot open it |
| The permission floor | real | `.vault/**` is denied to every app frame under every grant a frame can be given. An app cannot read the terms file, let alone the key inside it |
| The host verb | {{badge:spec}} | `sg.tts.*`, beside the `sg.llm.*` that already does exactly this shape of thing for a model router |

## The verb, as specified

```js
// app side — would require "permissions": { "tts": { "speak": true } } in app.json;
// denied by default, as every host capability is.
const r = await sg.tts.speak({ text, voice?, model?, speed?, timestamps?: true });
// → { audio: Blob, durationSecs, alignment?: { characters, character_start_times_seconds,
//     character_end_times_seconds }, cost: { chars, usd, estimated: true } }

await sg.tts.available();   // { ok, reason?: 'ENOKEY' | 'EPERM' | 'EBUDGET' | 'EREADONLY' }
await sg.tts.voices();      // filtered by the policy's voice allow-list
await sg.tts.usage();       // this session's characters and estimated cost
```

What the host would do, in order:

1. **Open the terms file.** Owner-sealed, so only a session holding the vault's write key can open it; a read-only opener would get `ENOKEY`, exactly as the model-router verb does today.
2. **Enforce the limits.** Refuse over `maxCharsPerRequest`; keep a per-session character counter and refuse past `maxCostPerSession` at the model's list rate; hold a semaphore at `maxConcurrent` — which is also the mitigation for [the concurrency question](/experiments/concurrency/) that is still open {{claim:concurrency-unknown}}.
3. **Ask, the first time.** The first `speak()` in a session would raise the host's own prompt — *"this app wants to generate speech with the vault's key — estimated $0.02"* — outside the frame, where the app cannot suppress or fake it.
4. **Make the call at the host's origin** with the `xi-api-key` header, and strip the key from every error surfaced back to the frame.
5. **Return audio and alignment**, and nothing else. The frame gets a `Blob` and an array of numbers.

## Why this is the only pattern where the bound holds

<div class="beforeafter"><div class="ba now"><h4>The bench today — pattern 0 with a ceiling</h4><p>A key box at the top of the page. Your full account key, in the page's own JavaScript, calling the vendor directly. Bounded by the plan's monthly quota and nothing else {{claim:no-per-key-spend-limit}}.</p><p>The code that spends the money <b>holds the credential that authorises it</b>. Every safety property is a property of your restraint.</p><pre class="lang-js">const { items } = JSON.parse(
  localStorage.getItem('el.keys.v1'));
fetch('https://api.elevenlabs.io/v1/…', {
  headers: { 'xi-api-key': items[0].key }
});</pre></div><div class="ba then"><h4>The same page under pattern 3 — specified</h4><p>No key box. No key in the page, in storage, or in the network tab. The app asks; the host spends, meters and refuses.</p><p>The bounded thing <b>cannot reach the bounding thing</b>: the terms live below the permission floor, in the vault, with the content they govern. {{claim:sg-tts-spec}}</p><pre class="lang-js">const { audio, alignment, cost } =
  await sg.tts.speak({ text, timestamps: true });
// no key, anywhere in this frame</pre></div></div>

The difference is not cosmetic. In the left-hand version, a cross-site scripting bug in the page is an account compromise. In the right-hand version, it is a request the host will meter and cap — the attacker gets speech, up to `maxCostPerSession`, and never gets the key.

## What it would change for this estate

- The [bench](/bench/) and every lab here would drop the key box, and the pattern box at the top of each would change from *0 with a ceiling* to *3*.
- `app.json` would no longer need `"permissions": {"network": true}` for these pages — which is the grant that [bit us on day one](/#9-what-went-wrong) {{claim:csp-blocks}} and which is a real widening for any vault whose app holds private content.
- ElevenLabs would move, in [the comparison](/comparison/), from *needs a server* to *pattern 3, no server* — because for a vault app **the host is the server** that pattern 2 keeps asking for. That is the generalisation the family of sites exists to test.

## What would have to ship, precisely

So that this page is a specification with a scope rather than an aspiration. Three things, none of them in this repository:

| # | What | Where it would land | State |
|---|---|---|---|
| 1 | The host verb — `sg.tts.speak`, `available`, `voices`, `usage` — beside the `sg.llm.*` that already does this shape of thing | The SG/Vault host's bridge | {{badge:spec}} |
| 2 | The policy read: open the owner-sealed terms file, enforce `maxCharsPerRequest`, meter `maxCostPerSession`, hold a semaphore at `maxConcurrent` | The same host, reusing the model-router's own policy path | {{badge:spec}} |
| 3 | The consent prompt, raised **outside** the app frame so the app can neither suppress it nor fake it | The host's HUD, which already does this for a model call | {{badge:spec}} |

**What is already real:** the terms file at `.vault/elevenlabs/config.json`, in the same shape and under the same seal as the model router's; and the permission floor that denies `.vault/**` to every app frame under every grant. Two of three pieces, and the missing one is the verb.

**Until all three ship, no page on this site may say pattern three works here** — and the build enforces it: the gate rejects `sg.tts` written in the present tense anywhere in the built site. That check exists because this is exactly the kind of page where a specification quietly becomes a claim.

## What would still be true

The host is not magic. Under pattern 3 the terms are only as good as the numbers in them, the estimate is an estimate at list price rather than an invoice, and a compromised *host* is a compromised key — the trust moves, it does not vanish. What changes is **who chose the blast radius and where the choice is recorded**: a number in a file that travels with the content, rather than a promise about how carefully an application will behave.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
