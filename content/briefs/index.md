---
title: The briefs, and what was done with them
description: "Every brief this site was built from, published raw, with a decision-by-decision account of what was accepted, what was modified, what was rejected and why."
lead: "This site was commissioned by briefs. They are published here **in full**, next to what was actually done with each instruction — including the three findings that were wrong, the one proposed capability row that was rejected, and the parts that are blocked on somebody else."
order: 85
toc: true
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
  note: "The raw documents are at /briefs/, licensed CC BY 4.0 as they arrived."
---

<div class="note"><p><b>Why publish the brief.</b> The same discipline as the rest of this site: <b>the claim and its evidence travel together</b>. A site that publishes what it was asked to build can be checked against it. One that publishes only the result cannot, and asks you to take its judgement on trust — which is the thing this site keeps declining to do.</p></div>

## Pack one · the providers-site pack, 7 September 2026

Six documents: an audit of the live site at v0.1.1, two axes and eleven decisions, an eight-step plan, twelve acceptance tests, eight open questions. **[Read it raw](/briefs/2026-09-07__pack__providers-site/00__README.md)** — [audit](/briefs/2026-09-07__pack__providers-site/01__audit-and-manifest.md) · [architecture](/briefs/2026-09-07__pack__providers-site/02__architecture-and-decisions.md) · [plan](/briefs/2026-09-07__pack__providers-site/03__implementation-plan.md) · [acceptance](/briefs/2026-09-07__pack__providers-site/04__verification-and-acceptance.md) · [open questions](/briefs/2026-09-07__pack__providers-site/05__open-questions.md).

### What shipped, at v0.2.0

| Step | What it asked | What was done |
|---|---|---|
| 1 | A capability block: what connecting this provider grants an agent | **Done, in two layers.** The block already existed for our own key; §2 now carries what the *platform* can grant per product above it, including the row the pack was right about — see below |
| 2 | The capability-tier axis, and its intersection with the credential patterns | **Done.** [The matrix is on the patterns page](/patterns/#the-second-axis-what-the-tool-keeps), and every tool on this site is placed in exactly one cell |
| 3 | Positioning, a disclosure line at the top of every page, the per-product rule | **Done.** The strip above this page is the disclosure line; the positioning paragraph is on [the report](/#what-this-site-is-and-is-not) |
| 6 | Tier three resolved either way | **Done, the honest way.** [`/pattern-three/`](/pattern-three/) now names exactly what would have to ship, and carries the specification state at the top |
| 7 | Composition, and `llms-full.txt` | **Done.** Family links point at pages rather than domains; the *provider* disambiguation is on the report. `llms-full.txt` already shipped at v0.1.0 |
| 4, 5, 8 | The video walkthrough, the tried-and-abandoned page, what we use it for | **Not done, deliberately.** Each is blocked on something real — see the ordering note below |

### Three findings in the audit were wrong

Checked against the live site rather than recalled, which is the standard the audit set for itself.

<div class="fails"><div class="fail ok"><p class="who">Corrected</p><h3><code>llms-full.txt</code> was not absent</h3><p>It shipped at v0.1.0 and returns 200. The audit's M8 and step 7 asked for a file the site already had. Cheap to check, and the reason the ledger exists.</p></div><div class="fail ok"><p class="who">Corrected</p><h3>The capability block existed</h3><p>M1 called it &ldquo;the largest gap&rdquo; and said nothing on the site did it. §2 has carried verb × object class × reach, with reversibility marked and emitted as front-matter, since v0.1.0. <b>The real gap was narrower and better:</b> the block described what <em>our scoped key</em> grants, not what the <em>platform</em> can grant. That is now two layers.</p></div><div class="fail"><p class="who">Rejected</p><h3><code>send × audio × world</code>, irreversible</h3><p>The pack proposed a row saying that connecting a voice provider grants an agent the capability to send audio into the world, irreversibly. <b>It is the same over-generalisation as the signed-URL claim this site already had to correct, from the same source brief.</b></p><p>The text-to-speech endpoint returns audio <em>to the caller</em>. Nothing leaves for the world; the estate's own primitive distinguishes <code>endpoint</code> reach from <code>world</code> reach precisely here. This vendor's genuinely irreversible row is <b>Agents</b>, which §2 names and which our key is scoped out of. Shipping the proposed row would tell a reader that generating narration publishes it — the error §4 exists to prevent, one product over.</p></div></div>

### And one finding it could not have made

While checking the audit's claim that §4 was built correctly, the citation in §4 turned out to be **invisible**: `<https://…>` is a GFM autolink, this site's renderer had no autolink rule, and the angle brackets reached the browser as an unknown tag — so the URL a reader is told to check was dropped from the page entirely. Fixed in [v0.1.2](/versions/), with a build check so it cannot return.

**A page-level audit cannot catch a URL that is not in the DOM.** That is an argument for the pack's own acceptance tests being machine-checked rather than read, which is where the rest of this site's rules already live.

### The ordering problem in the plan

Three steps are blocked, and two of them are blocked by the plan's own gates:

- **Step 5, what was tried and abandoned**, wants three real entries and no euphemisms. Almost nothing on this site has been run: the honest failures we have are already [the four cards in §9](/#9-what-went-wrong). Until the labs are run it would be padding, and the pack says itself that step 4 seeds it. It is step 4b, not step 5.
- **Step 4, the video walkthrough**, requires a cost that is *measured* and a walkthrough somebody with a key can follow end to end. **Nobody here has a key**, and the site's own acceptance rule is that none was requested, used or committed at any point in the build. What could be built without one is built: [the video plan](/video/).
- **Step 8, what we use it for**, is blocked on the project lead's answer to the pack's own open question 3 — which of the named workflows are real and which are intended.

## Pack two · the video-pipeline brief, 7 September 2026

A working, measured video pipeline — 724 KB of tooling, four reels made with it, every number observed — handed over so this site can make narrated videos with the provider it reports on. **[Read it raw](/briefs/2026-09-07__brief__video-pipeline/00__README.md)** — [the brief](/briefs/2026-09-07__brief__video-pipeline/01__BRIEF.md) · [the first-run guide](/briefs/2026-09-07__brief__video-pipeline/02__ELEVENLABS-FIRST-RUN.md).

**What was done: it is published as a plan, with its numbers badged, at [/video/](/video/), and it has not been executed.** Three reasons, in order of weight:

1. **No key, and that is a rule rather than an inconvenience.** This site's acceptance list says no ElevenLabs key was requested, used or committed at any point in its build, and every {{badge:verified}} chip on it comes from a human's own browser rather than from this repository. Asking for a key to make a video would trade the site's most distinctive property for a two-minute film.
2. **The toolchain is not this site's to hold.** The pack above records the estate's decision that component code stays canonical where it lives and these sites hold the context; the same pack's scope boundary says the video toolchain is out of scope. Vendoring 724 KB of a render pipeline into a report site would contradict both, and the brief's own value — the measured numbers, the failure points, the script rules — transfers without it.
3. **The interesting half needs a person, not an agent.** The brief's own last section is *what I could not tell you*: whether the shim works, which names the model mispronounces, how the API behaves under the render's concurrency, whether the drift figure changes. Those are answered by running it, once, with a key — and then they are {{badge:verified}} rather than {{badge:unrun}}.

### What the brief changed on this site anyway

- **[/video/](/video/) exists**: the pipeline, what this provider adds to it, the measured costs, the script rules that cost time when broken, the four failure points the unrun path is most likely to hit, and the three videos worth making first.
- **Its secret-hygiene requirement was already met.** The brief asks for the key-shape grep to be wired into CI as a required check; [that shipped at v0.1.0](/versions/) and its pattern set is a superset of the one the brief specifies.
- **Its publishing advice is recorded** where the decision will be made: MP4 rather than WebM, the SRT shipped as a `<track>` beside the video, and GitHub's file and bandwidth limits.

## The rule both packs share, and this site keeps

**No claim without a state.** Everything added by either pack obeys the [ledger](/ledger/) contract, including claims about work that does not exist: a specification takes {{badge:spec}}, code written and never executed takes {{badge:unrun}}, and a projection carries its arithmetic. The join is done at build time, so a claim that appears on a page and not in the table fails the build rather than the review.
