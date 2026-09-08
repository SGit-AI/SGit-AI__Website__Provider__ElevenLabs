# 01: What The Site Has Today, And What Is Missing

**Audited 7 September 2026 against the live site at v0.1.1**, by fetching pages rather than by recollection. Every row below was seen. Where a row says absent, it means not found in the machine-readable index and not reachable from the pages fetched, which is weaker than proof and is the honest state of this audit.

---

## 1. What Exists

### The report and its spine

| Item | State |
|---|---|
| Nine-section report at the root, with cost and failures given visual weight | **Built**, and the v0.1.0 release note says so in those terms |
| Four credential patterns, described by where the credential lives and what bounds it | **Built** |
| All four patterns resolved for this vendor rather than left abstract | **Built**, and better than the brief asked |
| Provider by pattern matrix, generated rather than written | **Built** |
| Comparison page, one row per provider and product | **Built** |

**The patterns page is the strongest content on the site.** It states that this vendor cannot do pattern one at all, because a key here can be scoped to endpoints but not bounded by spend, with no per-key limit and no reset window shorter than the billing cycle, and that the current position is therefore pattern zero with a ceiling.

### The evidence model

| Item | State |
|---|---|
| Six claim states: verified, measured, docs, spec, unrun, projected | **Built** |
| Every claim joined to the ledger at build time, so a claim cannot appear on a page without appearing in the table | **Built** |
| Each claim carries its date and the pages that assert it | **Built** |

**This is the site's best feature and it exceeds every specification written for it.** Treat it as the contract for all new content.

### The experiments

Twelve, each exercising one feature: alignment and verification, the captions studio, a concurrency probe, a cost model that needs no key and no network, multi-speaker dialogue, a key scope and quota probe, a model comparison across four models on one text, a pronunciation lexicon lab, sound effects and music with a per-second meter, text handling with three comparisons, a voice-settings sweep, and a voice explorer.

**Two of these are load-bearing for work the briefs describe and are not yet presented that way.** Alignment returns word and character timing; the captions studio turns that timing into cues. Together they are the foundation of the video production workflow specified on 7 September, and nothing on the site says so.

### Disclosure

**Built, and built correctly.** Two platforms listed, both with no relationship, a self-paid key at list price, checked on a stated date, with a commitment that any future programme or grant is recorded there **first**, no paid placement, no affiliate links, and the page created before any relationship exists so that its later appearance cannot be read as a signal.

### The machine-readable surface

| Item | State |
|---|---|
| `llms.txt` with a title, a summary and described links | **Built**, and correctly formed for that convention |
| Every page served as markdown at a stated path | **Built**, and stated on the page rather than left to be discovered |
| `llms-full.txt` | **Absent** |

### Publication

Canonical at `elevenlabs.providers.sgit.ai`, mirrored on project pages. Two releases, both on 7 September, the second fixing root-absolute URLs that broke under a project path.

---

## 2. What Is Missing, In Order Of Value

### M1. What the platform grants. **The largest gap.**

The 5 September brief is explicit: **a page that lists an API surface without listing the capabilities it adds to an agent has documented the wrong half.** Nothing on the site does this.

The block belongs on the report, in the estate's own primitive form, a verb by an object class by a reach, with reversibility marked. For this provider it is roughly:

```
   send    x audio      x world      IRREVERSIBLE   (published speech is published)
   read    x credential x self       (a scoped key, and what it can reach)
   spend   x budget     x tenant     reversible, bounded only by the plan
   create  x voice      x tenant     (cloning: a voice that did not exist)
   read    x audio      x tenant     (transcription of material supplied)
```

**The cloning row is the one a reader will not expect and is the reason this matters.** Connecting this provider gives an agent the capability to produce a voice, which is a different order of thing from producing audio, and no vendor page will frame it that way.

This is what joins the site to the grant and mandate work. Without it the site is a well-made review; with it, it is the supply side of an assessment.

### M2. The capability tier ladder is absent as an axis

The site has one axis, the credential pattern, which is a property of the **provider**. The 7 September memo added a second, which is a property of **our tool**: what state it keeps.

| Tier | What it keeps | Site instance today |
|---|---|---|
| **1** | Nothing. A pure function in a page | **The cost model.** Its own description says no key, no network |
| **2** | Local storage on this device | **The bench**, and most experiments |
| **3** | A vault, so the key never enters the page | **`pattern-three` is a specification, not a tool** |

**These are orthogonal to the patterns and the intersection is the useful table.** A tier-two tool holding a key in local storage is pattern zero with a ceiling; a tier-three tool is pattern three. Say that once, on the patterns page, and the two axes stop competing.

**And tier three currently has no working thing.** The honest options are to ship one or to label the tier with the state the ledger already provides. The second is acceptable and the first is better.

### M3. No record of what was tried and found wanting

The Explorer role this site belongs to is measured partly on a failure ratio, on the stated reasoning that **if nothing fails we are building the obvious rather than exploring.** The ledger tracks unrun code; it does not record an experiment that ran and produced a disappointing answer.

**That page is the one no vendor will ever write**, and it is cheap: a dated list of what was tried, what the result was, and why it was not pursued.

### M4. The video production line is not assembled

Alignment and captions exist as separate experiments. The 7 September brief describes the workflow they serve: alignment gives word-level timing, which is what drives caption cues, text animation and slide transitions off the audio rather than guessing alongside it.

**Nothing on the site connects them**, and a page that walks one script through generation, alignment, captions and a timed render would be the most convincing thing on it.

**One platform gap belongs in the same section.** The estate ships a call for listening that records audio and returns text with the audio never entering the app frame. **There is no counterpart for speaking.** That is the natural first integration for this provider, it fits the existing bridge exactly, and it is what a tier-three tool would use.

### M5. Positioning is implied rather than stated

The site does not say what it is. **One paragraph, early**: this is narrower than the vendor's own environment rather than better, it serves the workflows we actually have, and a general-purpose interface cannot be narrow.

### M6. The audiences are not addressed by name

See decision D4 in the next file. Four readers arrive for different reasons and the site currently serves the second one best and the others by accident.

### M7. Composition with the family

The OpenRouter stub proves the shape works. **The rule the family has already broken once**, recorded on 20 August, is that a cross-link must point at the page that answers the question rather than at a domain. **A domain link is a referral, not a composition.**

### M8. Smaller items

- `llms-full.txt`, which earned specific praise elsewhere in this family.
- One sentence disambiguating which sense of provider is meant, since the word has four established senses in this estate and one of them means a customer who distributes capability.
- The grant application named on the disclosures page as a pending action, so the page's promise to record it first is visibly live rather than theoretical.

---

## 3. What Moves In From Elsewhere

**Nothing yet, and this is the correction to make early.** The 7 September specification for the providers pack found that most of the tooling assumed to be moving off the tools site was specified in March and never built, so **half of what reads as a move is a write.** For this provider specifically there is no existing tooling to move at all: this site is the first instance.

**So this pack builds rather than migrates**, and the deletion-candidates discipline does not apply here. It applies to the sibling provider.

---

*Released under CC BY 4.0.*
