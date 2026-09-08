---
title: Ask this site
description: "A chat pane that answers from the site's own index, in your browser, with no key and no model — and will read the answer aloud with your own key if you give it one."
lead: "Two tiers in one pane. **The default one needs no key, no model and no request to anybody**: it matches your question against every page and every claim in the ledger and shows you what the site actually says. The second reads the answer aloud with your key."
order: 12
kind: experiment
family: no key needed
app: ask
endpoints: "none by default · POST /v1/text-to-speech/{id} only if you turn speech on"
state_chips: [verified]
toc: true
---

{{app}}

## Why it does not have a model behind it

Every other site would put a language model here, and this one deliberately does not. Three reasons, in the order they matter:

**A model would be a second host.** This site's central claim is that every page calls exactly one host, `api.elevenlabs.io`, in a request you start — and [a build check fails the site if any other origin appears in it](/ledger/#claim-keys-local-only) {{claim:keys-local-only}}. Adding a chat model would mean adding a provider, a key and an origin, and the claim would have to go. It is worth more than the feature.

**A matcher cannot make things up.** The pane returns the site's own sentences, with the state and date attached, and links to where each one lives. When it finds nothing it says so rather than generating a plausible paragraph — which on a site whose whole argument is *no claim without a state* is not a limitation, it is the requirement.

**It is the honest tier-one artefact.** [The capability tier axis](/patterns/#the-second-axis-what-the-tool-keeps) says a tier-one tool keeps no state and works for somebody with no key. This pane is that, and then it offers to become tier two — with the key panel written as a trust decision rather than a feature, which is the convention this estate already uses.

## What the speech tier actually sends

If you open the key panel and turn speech on, one thing is sent, to one host: **the answer text**. Not your question, not the page you are on, not an identifier. The sentence spoken is a claim from the ledger — text that is already published on this site — and it goes to `api.elevenlabs.io` in the same shape as [every lab here](/experiments/) {{claim:first-video}}.

It defaults to `eleven_flash_v2_5` because an answer is not narration: half the price, and the meter under the panel shows what you have spent {{claim:tts-prices}}.

## What it is not

It is not a support channel, it is not a model, and it is not an index of the vendor's documentation — asking it about an endpoint this site does not report on will correctly return nothing. For the vendor's API reference, [the vendor's own documentation](https://elevenlabs.io/docs) is better and fresher, which is the same rule the rest of this site obeys.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
