---
title: The grant case — what we would do with 33 million characters
description: "The ElevenLabs Grants Program, its criteria checked one by one against this estate, the one where we are borderline and why, and what we would give back that no other grantee produces: a public, dated, state-badged record of what the API actually did."
lead: "The programme is called the **ElevenLabs Grants Program** and it is 33,000,000 characters over twelve months {{claim:grant-terms}}. This page checks their criteria against us honestly — including the one where we are borderline — and states what we would do that a normal grantee does not."
order: 55
toc: true
provenance:
  commit: 7d1916aca5f3
  date: 8 September 2026
  note: "Programme terms read from elevenlabs.io/startup-grants on 8 September 2026. Nothing here has been applied for."
---

<div class="warnbox"><p><b>Nothing has been applied for.</b> This page is the case, written before the application rather than after it, because <a href="/disclosures/">this site's disclosure page</a> promises that any programme is recorded there <b>first</b> — and an application is the first moment that promise is testable. The decision to apply is the project lead's and is not made here.</p></div>

## 1 · What the programme actually is

Not a "startup package": **the ElevenLabs Grants Program**, at `elevenlabs.io/startup-grants` {{claim:grant-terms}}.

<div class="tiles"><div class="tile cool"><b>33,000,000</b><span>characters, over twelve months</span><em>their page: "over 680 hours of Agents usage", "more than $5,500+ in value"</em></div><div class="tile cool"><b>1 week</b><span>to a decision, applications rolling</span><em>no deadline, one application per company</em></div><div class="tile hot"><b>&lt; 25</b><span>employees — the hard eligibility line</span><em>and no agencies or consulting firms</em></div><div class="tile hot"><b>0</b><span>characters that may be resold or exchanged</span><em>doing so terminates the grant immediately {{claim:grant-no-resale}}</em></div></div>

**Characters, not words.** 33M characters is roughly 5.5 million words of narration — worth being precise about, because every plan below is arithmetic on the character count and a word-based estimate would be six times wrong.

**And it converts.** After twelve months, or when 10,000 credits remain, the plan reverts to Free {{claim:grant-terms}}. So the honest planning assumption is *one year of headroom*, not a permanent subsidy — which is the difference between funding an exploration and funding a business model.

## 2 · The criteria, checked one at a time

Their eligibility list {{claim:grant-eligibility}}, against this estate, with the awkward one included rather than skipped.

| Their criterion | Us | Verdict |
|---|---|---|
| **A monetized product use case**, with a business or monetization strategy | The estate ships products commercialised through `sgraph.ai` — The Cyber Boardroom, MyFeeds.ai, RiskMandate.ai, VoiceDebrief.ai — and this site publishes [a pricing page](/pricing/) with the model stated in the open | **Fits** |
| **A valid business email** | Yes | **Fits** |
| **No short-term or one-off projects** | The video pipeline has produced four reels across two months; this site is on its fifth release in two days and carries a [public release history](/versions/). Neither is a campaign | **Fits** |
| **No projects for under-18s** | None. The audience is founders, engineers and boards | **Fits** |
| **Under 25 employees** | Comfortably | **Fits** |
| **One application per company** | One, from the company that holds the products | **Fits** |
| **Not an existing enterprise customer** | Correct — the only spend to date is a free tier and a self-paid key {{claim:first-video}} | **Fits** |
| **No agencies or consulting firms** | **This is the one to be careful about.** The people behind this estate do advisory work, and an application that reads as a consultancy asking for credits should be refused | **See below** |

### The borderline one, addressed rather than avoided

**A consultancy asking for characters to spend on client work is exactly what that rule exists to stop**, and it should stop it. The application that fits the rule is a **product company** applying for **its own product's** consumption: the sgit.ai estate's own tooling, its own videos, its own published research — none of it billed to a client, none of it resold {{claim:grant-no-resale}}, and all of it visible at the URL of this page.

The test is simple and they can run it in a minute: **is there a product, and is the grant paying for the product's own use?** The [pricing page](/pricing/) answers the second half in public — consumption is the customer's, on the customer's key, and we never touch it. A grant spent here cannot end up inside a client invoice, because there is no line item it could hide in.

## 3 · What 33 million characters would actually be spent on

Arithmetic, from measured workloads rather than ambition. Our first video used 1,821 characters {{claim:first-video}}; the estate's six existing cuts are about 15,550 {{claim:projected-reel-costs}}.

| Workload | Characters | What it produces |
|---|---:|---|
| **Re-narrate the estate's six existing cuts**, and keep them current | ~50,000 | Six videos with real subtitles from the alignment, replacing captions a platform gets wrong |
| **A published video per site**, across the `*.sgit.ai` network, twice a year | ~600,000 | 20-odd explainers, each with its own SRT and its own cost printed on the closing slide |
| **The open items on this site** — the names test, the concurrency probe, the voice-settings sweep, the model A/B, the dialogue and sound labs | ~200,000 | **The measurements nobody publishes**: where the concurrency wall is per tier, which names v3 gets wrong, what a settings sweep sounds like |
| **Localisation of the estate's core explainers** into 4–6 languages | ~2,500,000 | The caption band translated as well as the audio, which dubbing cannot do |
| **A narrated version of every page on this network** — the accessibility case | ~8,000,000 | ~1,100 documents at CC BY 4.0, readable by ear |
| **Agents, evaluated the way this site evaluates things** | ~4,000,000 | The one product family this site has scoped *out* of its key, reported on with the same ledger |
| **Headroom for the failures** | the rest | Because [the interesting half is what breaks](/#9-what-went-wrong) and re-runs are not free |

**That is a plan for the year, not a wish.** The first three lines are under a million characters — 3% of the grant — and they close every open item this site currently carries.

## 4 · What we would give back that a normal grantee does not

Every grantee builds a product with the credits. This estate would do that **and** publish the thing the vendor cannot produce for itself:

**A public, dated, state-badged record of what the API actually did.** [The ledger](/ledger/) already carries 45 claims, each with a verification state and a date, joined to the pages that make them at build time. A grant would extend it with figures nobody publishes:

- **The concurrency wall per tier** — untested by us and unpublished by anyone {{claim:concurrency-unknown}}.
- **Which names `eleven_v3` gets wrong**, and whether a lexicon fixes them {{claim:names-test}} {{claim:lexicon-hypothesis}}.
- **Latency distributions** rather than three samples {{claim:latency-5s}}, across models and hours.
- **What the tier gates actually gate** — we have already published one: PCM output is Pro-and-above, found by hitting it {{claim:pcm-gated}}.
- **The failures.** We have published four already, including [one that is our own bug](/video/) and one that contradicted the vendor's own documentation shape {{claim:stitching-v3}}.

**Why that is worth more than a case study.** A case study says the product works. This site says *what it cost on a named workload on a named date, what broke, and what we could not verify* — and it corrects itself in public when it is wrong, with the correction dated. **A vendor cannot buy that and cannot write it**, because coming from the vendor it would not be evidence. It is the single most useful artefact an independent grantee can produce, and this estate already produces it without a grant.

**And the licence makes it usable.** Everything here is CC BY 4.0 {{claim:grant-terms}} — the findings, the labs, the lexicon, the cue rule, the briefs. Their developer-relations team can quote any of it, including the parts that are unflattering, which is what makes the flattering parts worth quoting.

## 5 · What we would ask them to extend

Their criteria are sound. Two things they do not currently ask for, which we would volunteer and which we think should be part of the programme:

1. **Publish the grantee's own failure list.** The programme gets case studies; it does not get the *"we tried this and it did not work"* page. Make it optional and most will skip it — but the ones who write it are the ones whose products actually shipped, and it is the cheapest signal of that they could collect.
2. **A tier-gate manifest.** Half of what breaks a first integration is a feature gated behind a plan tier — output formats, key permissions, model availability — and the mapping is not in one place. We hit two of them in a single afternoon {{claim:pcm-gated}} {{claim:key-scope-observed}}. We would maintain that table publicly for the products we use, with dates, and hand it over.

Neither costs them anything. Both would have saved us a day.

## 6 · The disclosure ordering, which matters more than the money

[The disclosures page](/disclosures/) says there is no relationship, with a date, and commits to recording any programme **there first** — before it starts, not after it is granted.

**So the order is fixed:** the disclosures page records that an application has been made, on the day it is made; if it is accepted, the top of [the report](/) carries a line saying so, with the date; and every page produced with granted characters says that it was.

That is a cost, and it is the point. A site that discovers its own funding halfway down a page has already lost the argument it was making. **This page exists before the application so that the ordering can be checked afterwards.**
