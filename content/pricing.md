---
title: Pricing — consumption, and what we charge for
description: "Consumption goes to the vendor on your own key, at their published rate. We charge for deployment and support. We do not resell characters, and the vendor's own terms are why."
lead: "**We do not sell speech.** Consumption is billed by the vendor, on your key, at their published rate — we never touch it. What we sell is the part that is actually ours: getting it deployed against a real workload, and keeping it working. **These prices are proposed, not sold** {{claim:pricing-proposed}}."
order: 50
toc: true
provenance:
  commit: 7d1916aca5f3
  date: 8 September 2026
  note: "Consumption figures are measured from this estate's own renders; the rates are the vendor's, read on the date shown."
---

## The rule that shapes this page

**Granted characters cannot be resold.** The vendor says so in one sentence {{claim:grant-no-resale}}, and reselling them terminates the grant immediately. The same logic applies to paid capacity: an intermediary who buys characters and sells them on has become a reseller of somebody else's product, at somebody else's margin, with somebody else's terms.

So this estate does not do it, and the pricing follows from that rather than working around it:

<div class="beforeafter"><div class="ba now"><h4>What we do not do</h4><p><b>Resell characters.</b> Not granted ones, not bought ones, not bundled into a per-minute price with a margin on top.</p><p><b>Hold your key.</b> Not in our database, not in our environment, not "temporarily for setup".</p><p><b>Mark up consumption.</b> If your invoice from the vendor and your invoice from us do not add up to what you expected, one of them is wrong.</p></div><div class="ba then"><h4>What we do</h4><p><b>Your key, your account, your invoice.</b> You sign up, you hold the credential, you see every character you spend on the vendor's own dashboard.</p><p><b>We charge for our work</b> — the integration, the deployment, the pipeline, the support — which is the part you cannot get from the vendor and cannot get from a price list.</p><p><b>And we publish what it cost us</b>, so you can check the arithmetic before you talk to us. <a href="/experiments/cost/">The cost model needs no key</a>.</p></div></div>

## 1 · Consumption — what you pay the vendor

Not us. These are the vendor's published rates, read on the date shown, and the [cost model](/experiments/cost/) does this arithmetic on your own script with no key and no network call {{claim:tts-prices}}.

| What | Rate | A worked figure from our own use |
|---|---|---|
| Text to speech, `eleven_v3` / `multilingual_v2` | **$0.10 per 1,000 characters** | Our first video: 1,821 characters, **$0.18** {{claim:first-video}} |
| Text to speech, `flash_v2_5` / `turbo_v2_5` | **$0.05 per 1,000 characters** | The same video on flash: **$0.09** |
| Speech to text, forced alignment | **$0.22 per hour of audio** | Six existing cuts aligned: **under two cents** {{claim:alignment-stt-price}} |
| Sound effects · music | $0.12 · $0.15 per minute | A two-second title sting: about **$0.004** |

**Plan quotas, not spend limits.** A monthly character allowance is the only ceiling this vendor offers; there is no per-key spend limit and nothing resets faster than the billing cycle {{claim:no-per-key-spend-limit}}. That is a fact about the vendor rather than about us, and it is why [§5](/#5-the-bounding-primitive) exists.

**Rule of thumb from measured work:** about **$0.16 for a two-minute narrated video** on the expensive model, half that on flash {{claim:video-cost-projection}}. A team producing one video a week spends under ten dollars a year on speech. **Consumption is almost never the number that decides anything** — which is exactly why nobody should be selling it to you with a margin.

## 2 · Deployment — what you pay us

Three lines, priced by the thing being done rather than by the characters that flow through it. **All three are proposed rather than sold** {{claim:pricing-proposed}}.

| Line | Unit | Indicative | What it is |
|---|---|---|---|
| **Bring-your-own-key deployment** | fixed, per workload | **£4,000–£9,000** | Your workload, running on your key, in your environment: the script format, the render or integration path, key custody reviewed against [the four patterns](/patterns/), the concurrency limit **measured on your plan** rather than guessed, and a `FINDINGS.md` written the way [ours are](/video/) |
| **Support and maintenance** | recurring, monthly | **£600–£1,800 / month** | The vendor moves: prices, models, output-format gating, alignment shapes. We watch the ones your workload depends on, keep the integration current, and answer the 3 a.m. question. Cancellable monthly; no minimum term |
| **Custody, when it ships** | per vault, recurring | {{badge:spec}} | [Pattern three](/pattern-three/) — the host holds the key, the app never sees it, the terms live with the content. **It does not exist yet** {{claim:sg-tts-spec}} and is priced only when it does |

**Why a fixed fee rather than per-minute.** A per-minute price is a resale price with extra steps: it ties our revenue to your consumption, which gives us an interest in your consumption going up. The interesting work is one-off — finding your concurrency wall, deciding where the key lives, getting the caption timing right — and it does not get more expensive because you rendered more videos this month.

**What is included in every line.** Everything on this site: [the twelve labs](/experiments/), [the examples](/examples/), the lexicon, the cue rule, [the briefs we were given](/briefs/), and the [claim ledger](/ledger/) that says how far each of them can be trusted. All of it CC BY 4.0, all of it usable without talking to us.

## 3 · What it costs to leave

Stated here because a page that does not state it is hiding something.

- **The key is yours**, and was never ours. Revoke it in the vendor's dashboard; nothing of ours stops working, because nothing of ours was holding it.
- **The scripts, the renders, the findings are yours**, in your repository or your vault, in formats — JSON, Markdown, MP4, SRT — that need no tool of ours to read.
- **Support is monthly.** Stop paying and it stops; the deployment keeps running because it runs on your infrastructure with your credential.
- **The integration is readable.** [The generator that made our first video](/video/) is about eighty lines with no dependencies. That is the standard: if you cannot read the thing that spends your money, do not buy it from us.

## 4 · The honest part

**Nobody has paid these prices.** {{claim:pricing-proposed}} They are published at this stage for the same reason the [failures](/#9-what-went-wrong) are: a number in the open can be argued with, and a number on application cannot.

**We are not the cheapest way to do this.** If your workload is one narrated video a month, the vendor's own console plus [our labs](/experiments/), both free, are the right answer and you should not hire anybody. The deployment line earns its keep when the workload is on a pipeline, the key custody is a real question, and somebody has to own the answer when the output format gets gated behind a tier {{claim:pcm-gated}}.

**And there is no relationship with the vendor.** [None](/disclosures/), checked and dated — not a reseller agreement, not a preferred-vendor tier, not a referral fee. If that ever changes it is recorded on the disclosures page **first**, and this page gets a line at the top saying so.
