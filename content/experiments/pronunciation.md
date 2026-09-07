---
title: Pronunciation lab — lexicons, and the test nobody has run
description: "Edit a PLS lexicon in the browser, create a versioned dictionary from rules, then generate the same text with and without it. The A/B that turns a hypothesis into a lexicon."
lead: "In this pipeline **the narration text is the caption text**, so every pronunciation hack is on screen where viewers read it as a typo. A dictionary moves the hack off the screen. Whether these particular rules work has never been tested by anybody."
order: 15
kind: experiment
family: text
app: pronunciation
endpoints: "POST /v1/pronunciation-dictionaries/add-from-rules · POST /v1/text-to-speech/{id}/with-timestamps"
state_chips: [unrun]
toc: true
---

{{lab-header}}

{{app}}

## The problem, concretely

Four script files in the source vault contain, verbatim: `sgit dot ai`, `A I U C one`, `S H A two five six`, `llms dot txt`, `version zero point one point twenty-nine`. Each of those is a workaround for a text-to-speech engine, and each of them is drawn on screen under the picture, where a viewer reads it as a mistake.

With a dictionary the script says `sgit.ai` and the voice still says it correctly. That is a change a viewer notices before they notice the voice.

## The two rule types, and the trap

| Rule | What it does | Works on |
|---|---|---|
| **alias** | text substitution before synthesis: `sgit.ai` → `ess-git dot A I` | every model |
| **phoneme** | exact pronunciation in IPA or CMU Arpabet | **`eleven_flash_v2` and `eleven_v3` only** |

Other models ignore phoneme rules **silently** {{claim:phoneme-models}} — no error, no warning, just the old pronunciation. That is the trap this lab is built to expose: generate with a phoneme rule on `eleven_multilingual_v2` and listen to nothing happen. Up to three dictionaries may be attached to a request, and each request pins a **version**, so a dictionary edit does not silently change an old render.

## The open item

The lexicon shipped on this site — [`pronunciations.pls`](/files/pronunciations.pls) — is **a hypothesis** {{claim:lexicon-hypothesis}}. It has never been uploaded and not one alias in it has been heard. Neither has the prior question: which names the model gets wrong **without** any dictionary at all {{claim:names-test}}.

Section 4 is the point of the page. Generate both sides, listen, mark each token right or wrong, copy the markdown, and the site gains its first piece of evidence about pronunciation. The default text is the names sample; it costs about **$0.02 for both sides** on v3 {{claim:tts-prices}}.

## A shortcut worth knowing

On `eleven_v3` you can write IPA inline in the text between slashes — `/ˈsɪdʒɪt/` — which is a fast way to find a transcription that works *before* committing it to a dictionary version {{claim:labs-unrun}}. Find it inline, then move it into a rule; do not ship inline phonetics in narration text, because that text is what appears on screen.
