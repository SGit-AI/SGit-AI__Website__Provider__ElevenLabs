# 02: The Two Axes, The Audiences, The Page Contract, And Eleven Decisions

---

## 1. The Two Axes

The site has one and needs both. They are orthogonal and each answers a different question.

**The credential axis is a property of the provider.** Where does the key live and what bounds it: nothing, a spend limit, a clock, or a host the application cannot reach. This is already built and it is the site's best analytical content.

**The capability axis is a property of our tool.** What state does it keep: none, this device, or a vault. This decides what a tool can do, whether it survives being downloaded, and whether it works for somebody who has no key at all.

```
                    TIER 1              TIER 2              TIER 3
                    no state            local storage       vault
                    +-----------------+-----------------+-----------------+
   PATTERN 0        | the cost model  | the bench       |                 |
   key in page      | needs no key    | key on device   |                 |
                    +-----------------+-----------------+-----------------+
   PATTERN 1        |                 |                 |                 |
   bounded key      |   NOT AVAILABLE FROM THIS PROVIDER                  |
                    +-----------------+-----------------+-----------------+
   PATTERN 2        |                 | needs a server  |                 |
   short-lived      |                 | agents only     |                 |
                    +-----------------+-----------------+-----------------+
   PATTERN 3        |                 |                 | pattern-three   |
   host holds key   |                 |                 | SPECIFIED ONLY  |
                    +-----------------+-----------------+-----------------+
```

**Say the intersection once, on the patterns page**: a tier-two tool holding a key in local storage is pattern zero with a ceiling, and a tier-three tool is pattern three. After that the two axes stop competing for the same explanation.

**And the empty column is the honest finding.** This provider cannot do pattern one, and tier three is specified rather than shipped, so the site's own recommended pattern is one it has not yet demonstrated. The ledger has a state for exactly that and the page should use it rather than avoiding the subject.

## 2. Who This Is For

Four readers. The site currently serves the second one very well and the others incidentally.

### A. The builder deciding whether to use this provider at all

**Wants:** can it do the specific thing, what will it cost me, what will break.
**Is served by:** the report's cost and failure sections, the cost model, the model comparison.
**Fails if:** the site reads as an endorsement, or the cost is a price list rather than a measured workload.

### B. The builder who has chosen and is stuck on credentials

**Wants:** where does my key live given how I deploy.
**Is served by:** the patterns page and the comparison matrix. **This is the site's sharpest existing content and its main reason to exist.**
**Fails if:** the rule quoted is the vendor's general rule rather than the rule for the endpoint being used. **The site has already caught this once and the correction is the site's most valuable single paragraph.**

### C. The agent building the next provider page, or a tool on top of this one

**Wants:** a pattern to copy and a contract to obey.
**Is served by:** the markdown-at-every-path convention, the OpenRouter stub, the examples, the ledger contract.
**Fails if:** the conventions are true and unstated. Say them.

### D. The vendor's own developer relations

**Wants:** to know what an independent evaluation found, and whether it is fair.
**Is served by:** the ledger and the disclosures page.
**Fails if:** a relationship exists and the page did not record it first. **This audience is why the disclosure page was built before there was anything to disclose**, and a grant application makes it live.

**Explicitly not an audience:** somebody learning what speech synthesis is. That reader is served better by the vendor, and serving them is how a narrow site becomes a broad one badly.

## 3. The Page Contract

The nine sections are built. **Three changes and one addition.**

| # | Section | Change |
|---|---|---|
| 1 | Disclosure | **At the top of each page, one line**, as well as on its own page. A reader who finds it at the bottom rereads everything above it with suspicion |
| 2 | **What it grants** | **New. The capability block.** Verb by object class by reach, with reversibility marked. See M1 in the audit |
| 3 | Which pattern | Add the tier intersection, once |
| 4 | Where the key goes | **Per product, never per vendor.** This is the correction the site itself found |
| 5 | The bounding primitive | Keep, and keep the sentence about what it does **not** bound |
| 6 | Minimal working example | Exists as the examples page. Link it from the report |
| 7 | What we use it for | **Thin.** Name the actual workflows, or the site is a review rather than a report |
| 8 | What it cost | Built |
| 9 | What went wrong | Built, and see D7 |

## 4. Decisions

Each carries a status. Blocking means do not proceed past the step that needs it.

| # | Decision | Status |
|---|---|---|
| **D1** | The two axes both appear, and their intersection is stated once on the patterns page | **Accepted** |
| **D2** | The capability block is added to the report, in the estate's primitive form | **Accepted.** It is why this site belongs to this estate |
| **D3** | Credential rules are stated per product, never per vendor | **Accepted**, and already proven necessary |
| **D4** | The four audiences are named in the pack and served by artefact, not by a page each | **Accepted** |
| **D5** | Tier three is either shipped as a working tool or carries the specification state visibly | **Accepted**, method open |
| **D6** | The site states that it is narrower than the vendor console rather than better | **Accepted** |
| **D7** | A dated record of what was tried and abandoned is published | **Accepted.** It is the page no vendor writes |
| **D8** | The video line is assembled as one walkthrough: generate, align, caption, time | **Accepted**, and it is the strongest demonstration available from what already exists |
| **D9** | A speech counterpart to the existing listen call is proposed to the platform team | **Proposed**, and outside this site's own delivery |
| **D10** | Every cross-link points at a page, never at a domain | **Accepted.** The family's recorded defect |
| **D11** | The grant application is disclosed as pending before it is made | **Blocking on the project lead.** The page promises to record a relationship first, and an application is the first moment that promise is testable |

## 5. What Must Not Happen

- **No claim without a state.** Including claims about our own unbuilt work.
- **No page that could be replaced by a link to the vendor.** If a section adds nothing the vendor does not publish, delete it.
- **No pattern zero described neutrally.** It is never acceptable for a published page and the site should keep saying so.
- **No silent broadening.** Every feature that serves a general audience rather than a named workflow moves this site toward being a worse version of the vendor's own.
- **No paid placement, ever**, and no page that reads as one because the disclosure arrived late.

---

*Released under CC BY 4.0.*
