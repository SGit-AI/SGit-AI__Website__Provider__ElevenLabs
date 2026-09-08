---
title: The four client-side credential patterns
description: "Client side is not one thing. It is four patterns that differ in where the credential lives and what bounds it — and one of them is the only one where the bounded thing cannot reach the bounding thing."
lead: "\"Client side\" is not one thing. It is four patterns, and they differ in exactly two ways: **where the credential lives**, and **what bounds it**. Every provider page on this family of sites answers §3 by naming one of these — per product, because a vendor with several products has several answers."
order: 20
toc: true
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
  note: "From platforms/README.md, the spine every provider page links to."
---

<div class="note"><p><b>This page is shared, and it will move.</b> The patterns, the comparison matrix, the ledger and the disclosures belong to the whole <code>*.providers.sgit.ai</code> family rather than to one vendor. Version 1 carries them here; when <code>providers.sgit.ai</code> exists they move there and these URLs become redirects. Nothing on this page is ElevenLabs-specific — that is the point of it.</p></div>

## The four patterns

| # | Pattern | Where the credential lives | What bounds it | Verdict |
|---|---|---|---|---|
| **0** | Key in the page | In the delivered application | **Nothing** | **Never.** Anybody who opens the page has the key and the account. A plan quota is a ceiling, not a bound: it is the whole account's |
| **1** | Bounded key in the page | In the page, provisioned per user with a spending limit and a reset | **Money, and a reset window** | Acceptable where the platform can mint such a key. The limit *is* the blast radius, so choosing the number is a risk decision, not a default |
| **2** | Short-lived token | Not in the page. A server exchanges the real key for a token with a short life | **Time, and the server's policy** | The standard answer — and it needs a server: the vendor's, if it offers one for that product, otherwise yours |
| **3** | Host holds the key | Never in the application. The application asks the host, which holds the key and enforces the terms | **The host, which the application cannot reach** | The strongest, and this estate's own: the only pattern in which the bounded thing cannot reach the bounding thing |

The ladder is not a maturity model. Pattern 1 with a $5 limit can be a better answer than pattern 2 with a badly-scoped minter; the question is always *what is the blast radius, and who chose it.*

## Why pattern 3 is different in kind

Patterns 0 to 2 all end with a credential in the hands of the code that spends it — for a moment in pattern 2, for good in pattern 0. Pattern 3 does not: the application asks a host for a **result**, and the host holds the credential, applies the terms, and returns only the output.

In this estate the SG/Vault host already does this for one class of call: `sg.llm.chat()` runs in the host, at the real origin, with a key sealed in the vault at `.vault/llm/config.json`. The app frame never sees the key and cannot read `.vault/**` under any grant it can be given. The terms — allowed models, spend cap per session, per-app overrides — live in the vault with the content they govern, which means **the terms travel with the data**, and a vault shared read-only carries neither the key nor the ability to spend against it.

Whether that generalises past a model call is the open question this family of sites exists to answer. For a voice API the answer is written down and not yet built: [`sg.tts` would be the same shape](/pattern-three/) {{claim:sg-tts-spec}}.

## The one piece of evidence that any of this is enforceable

Arguments about blast radius are cheap. Here is a bound doing its job, observed, with a date:

<div class="fails"><div class="fail ok"><p class="who">3 September 2026 · the sibling provider</p><h3>A 402 that was the point, not the outage</h3><p>At <b>$4.79 used against a $5.00 limit</b> on a provisioned key, every audio request was refused: <code>402 — this request requires at least $0.50 in balance for audio output</code>, with <code>limit_source: openrouter_key_limit</code>. Two re-renders could not run until the limit was raised in the dashboard. {{claim:openrouter-402}}</p><p>That is <b>pattern 1 working exactly as designed.</b> The blast radius was the number we chose in advance; the platform refused before spending past it; raising the limit was a deliberate act by a human with a dashboard — a reinstatement, in the insurance vocabulary. It cost an afternoon, because we had not budgeted for the headroom rule. It could have cost the account.</p></div></div>

Note what makes it evidence rather than anecdote: the bound was **chosen before** the spend, **enforced by the platform** rather than by our code, and **visible in the refusal** — the error names the limit source. A ceiling that only appears in a monthly invoice is not this.

## Where the two providers sit

| Platform | Pattern in use | Evidence |
|---|---|---|
| OpenRouter | **1** — a provisioned key with a limit ($5, later $10) for the render pipeline; **3** for the vault's own AI chat through `sg.llm.*` | The 402 above {{claim:openrouter-402}}; the cost table on [the stub page](/providers/openrouter/) |
| ElevenLabs | **0 with a ceiling** — the key's owner testing their own key in their own browser; **2** would need a server we do not run; **3** is specified and not shipped | [The report](/), §3 and §5 {{claim:no-per-key-spend-limit}} |

**ElevenLabs cannot do pattern 1 at all.** A key can be *scoped* to endpoints; it cannot be *bounded* by spend. There is no per-key limit and no reset window shorter than the billing cycle {{claim:no-per-key-spend-limit}}. So "put a bounded key in the page" — the honest answer for the sibling provider — has no implementation here, and a key in a page is pattern 0 with the account's quota as its only ceiling. That single asymmetry is why [the comparison table](/comparison/) is worth generating.

## The second axis: what the tool keeps

The four patterns are a property of **the provider**: where the credential lives and what bounds it. There is a second axis, and it is a property of **our tool**: what state it keeps. It decides whether a tool works for somebody with no key at all, and whether it survives being downloaded and run from somewhere else.

| Tier | What it keeps | Works with no key? | Survives being downloaded? |
|---|---|---|---|
| **1** | Nothing. A pure function in a page | **Yes** | Yes, completely |
| **2** | This browser's `localStorage`, on this device | No | Yes, and it carries no key with it |
| **3** | A vault, which holds the key the page never sees | Yes — the *vault* holds the key | **No.** A vault app's calls fail on a static host, because the key is sealed to its owner |

**The intersection is the useful statement, and it is one sentence:** a tier-two tool holding a key in `localStorage` is **pattern 0 with a ceiling**, and a tier-three tool is **pattern 3**. Said once, the two axes stop competing to explain the same thing.

<div class="tablewrap"><table class="cmp"><thead><tr><th>&nbsp;</th><th>Tier 1 · no state</th><th>Tier 2 · this device</th><th>Tier 3 · a vault</th></tr></thead><tbody><tr><th scope="row">Pattern 0 · key in the page</th><td><a href="/experiments/cost/">the cost model</a><span class="vnote">no key, no network call at all</span></td><td><a href="/bench/">the bench</a> and ten more labs<span class="vnote">your key, your device, one host</span></td><td><span class="v v-na">&mdash;</span></td></tr><tr><th scope="row">Pattern 1 · bounded key</th><td colspan="3" class="dim">Not available from this provider at any tier — there is no per-key spend limit to mint</td></tr><tr><th scope="row">Pattern 2 · short-lived token</th><td><span class="v v-na">&mdash;</span></td><td><span class="v v-no">&times;</span><span class="vnote">would need a server we run; the vendor mints one for Agents only</span></td><td><span class="v v-na">&mdash;</span></td></tr><tr><th scope="row">Pattern 3 · host holds the key</th><td><span class="v v-na">&mdash;</span></td><td><span class="v v-na">&mdash;</span></td><td><a href="/pattern-three/">sg.tts</a><span class="vnote">specified, not shipped</span></td></tr></tbody></table></div>

**Two honest wrinkles in that grid.** The first: [the captions studio](/experiments/captions/) is a tier-two tool with a tier-one mode — paste an alignment and it needs no key, no network and no account. It is placed at tier two because that is its full form, but the keyless mode is the more interesting half and it is why the cue rule can be tuned by somebody who has never bought a character. The second is the empty column: **tier three has no working tool here.** The site's own recommended pattern is the one it has not demonstrated {{claim:sg-tts-spec}}, and the honest thing is to say so in the same breath as recommending it.

## What this means for the labs on this site

Every [experiment here](/experiments/) asks you to paste your own key into your own browser. That is **pattern 0 with a ceiling, deliberately, in the narrow case where it is defensible**: the key's owner, testing their own key, on their own device, with no key shipped in the page and nothing sent anywhere but the vendor {{claim:keys-local-only}}. It is not a pattern to publish, and the box saying so sits at the top of every lab rather than in a footnote.

The version of those labs that would be publishable is [pattern three](/pattern-three/), where the page has no key box at all. It does not exist yet {{claim:sg-tts-spec}}.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
