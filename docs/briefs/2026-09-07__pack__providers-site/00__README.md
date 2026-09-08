# Briefing Pack: elevenlabs.providers.sgit.ai, v0.2

**version** v0.33.66
**date** 7 September 2026
**for** the agent working on the ElevenLabs provider site (assume no prior context)
**source briefs** the eight documents in `source-briefs/`, being one of 5 September and seven of 7 September
**status** PROPOSED. Nothing in this pack is built. The site it describes is live at v0.1.1

---

## Read These In Order

1. This file.
2. `01__audit-and-manifest.md`, which is what the site has today, checked page by page on 7 September, and what is missing against the briefs.
3. `02__architecture-and-decisions.md`, which is the two axes, the audiences, the page contract, and eleven numbered decisions.
4. `03__implementation-plan.md`, which is the sequence.
5. `04__verification-and-acceptance.md`, which is how you know you are done.
6. `05__open-questions.md`, which is what nobody has decided and you should not decide alone.

The eight source briefs are in `source-briefs/`. **Read `v0.33.65__strategy-brief__platforms-is-the-right-shelf...` first**, because the site you have already implements it and this pack extends it.

## The Governing Discipline

**The site is narrower than the vendor's own environment, not better.** It serves one workflow properly rather than every workflow adequately. Every decision below follows from that, and any feature that would only make sense for a general audience is out of scope.

**No claim without a state.** The site already gives every factual claim one of six verification states and joins them at build time so a claim cannot appear on a page without appearing in the ledger. **Everything added by this pack obeys that rule**, including claims about our own unshipped work, which take the specification or unrun state rather than being written as though they were true.

**Absences are stated as absences, not as roadmap.** A page that says a capability does not exist here is more credible than one that says it is coming.

## What Has Already Been Decided, And Should Not Be Reopened

| Decision | Where it was settled |
|---|---|
| The family is called **providers**, not platforms | 7 September, confirmed by the project lead. The word matches what the code already calls these services |
| The nine-section report structure, with cost and failures given the weight | 5 September. **Already implemented at v0.1.0** |
| Four credential patterns as the credential axis | 5 September. Already implemented |
| Disclosure exists before any relationship does, and is recorded there first | 5 September, and the site's own disclosures page already commits to it |
| A grant or credit award is a research subsidy, never inventory | 7 September. Two providers now restrict resale |
| Component code stays canonical in the tools site; this site holds the context | 7 September |
| Move and delete are separate reversible steps | 7 September |
| The six claim states are the evidence model | Site v0.1.0, which went further than the brief asked. **Adopt it, do not redesign it** |

## What The Audit Established

Checked against the live site on 7 September, not recalled:

- **The nine-section report, the four patterns and the ledger are built.** The patterns page fills in all four for this vendor rather than describing them in the abstract.
- **The site corrected one of its own source briefs.** The 5 September brief quoted the agent product's signed-URL rule as though it were the vendor's rule; the speech endpoint supports only key scoping. **The site's version is correct and the brief is superseded on that point.**
- **Twelve experiments exist**, and two of them, forced alignment and the captions studio, are the foundation of a workflow nobody on the site has connected yet.
- **Real measurements are published**, including three timestamped generations of a 187-character sample returning in 5.0 to 5.8 seconds and a verification session costing about $0.075.
- **The OpenRouter stub proves that adding a provider is one file with front matter**, which means the multi-provider shape is already solved.

## The Success Criterion

**One sentence.** A developer who has never seen this site can arrive with a specific job, learn in five minutes whether this provider can do it, what it will cost them, where their key has to live for their deployment shape, and what will break, and leave with a working example they ran themselves.

**And one for the estate.** A page on this site says what capabilities this provider adds to an agent that connects it, so the site joins the grant work rather than sitting beside it.

## Scope Boundary: What This Pack Does Not Cover

- **The parent hub at providers.sgit.ai.** It does not exist. This pack notes what the ElevenLabs site must do to be composable with it and stops there.
- **Any commercial model.** Resale is prohibited by both providers written about here. Nothing in this pack assumes credits can be passed on.
- **The video toolchain itself.** The rendering, assembly and encoding pieces are unbuilt and are not this site's job. What is in scope is the part this provider serves.
- **Migrating the tools site.** A separate specification covers it, and its discipline is that move and delete never happen in one commit.

---

*Released under CC BY 4.0.*
