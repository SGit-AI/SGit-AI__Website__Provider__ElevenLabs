---
title: Comparison — provider × pattern
description: "One row per provider and product, one column per credential pattern. Generated from the front-matter of each provider page, so a new provider is one Markdown file rather than a table edit."
lead: "One row per provider and product, one column per pattern. **This table is generated** at build time from the `patterns:` front-matter on each provider page — the hand-written version of it drifted the moment a second provider appeared."
order: 30
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
---

{{comparison}}

## Read down the columns

**Column 0** is the same everywhere: possible, and never acceptable. It is in the table because "the browser can call it" is what people usually mean by "client-side", and CORS permitting a call says nothing about whether the credential is bounded {{claim:cors-browser}}.

**Column 1 is where the two providers part company.** OpenRouter can mint a key with a spend limit and a reset window, so a key in a page has a blast radius you chose. ElevenLabs cannot: scoping restricts *what* a key may call, never *how much* it may spend {{claim:no-per-key-spend-limit}}. There is no product configuration that makes column 1 available for ElevenLabs text to speech, which is why the row says ✗ rather than "not recommended".

**Column 2 needs a server, and the question is whose.** For ElevenLabs Agents the vendor runs the minter — you hand it your key and it issues a 15-minute signed URL {{claim:agents-only-signed-urls}}. For ElevenLabs text to speech there is no such endpoint, so the minter would be ours to build, host, secure and pay for. "Available with a server" and "available" are not the same claim, and the last column of the table says which.

**Column 3 is the one this estate can extend to any provider** by adding a verb to the host bridge and a terms file to `.vault/`. It is shipped for the model router and [specified for the voice API](/pattern-three/) {{claim:sg-tts-spec}}. It is the site's actual argument: *a browser application can use a paid API without ever holding the key, because the host holds it and enforces the terms.*

## How to add a provider

Write one Markdown file in `content/providers/` with a `patterns:` block in its front-matter, and this table grows a row. No template surgery, no edit to this page:

```yaml
patterns:
  - provider: Some Vendor
    product: The specific product, because a vendor is not one auth story
    server: "Yes — ours"
    p0:
      verdict: never
      note: "why, in six words"
    p1:
      verdict: yes
      note: "the bound, named"
    p2:
      verdict: no
      note: "no vendor minter for this product"
    p3:
      verdict: spec
      note: "" 
```

`verdict` is one of `yes` · `no` · `never` · `spec` · `na`. The [OpenRouter page](/providers/openrouter/) on this site exists as the proof: it is a stub of the sibling site's content, carrying nothing but front-matter and a short body, and it is where the second and third rows of the table above come from.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
