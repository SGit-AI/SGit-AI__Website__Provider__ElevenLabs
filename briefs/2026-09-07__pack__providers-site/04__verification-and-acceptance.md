# 04: Verification And Acceptance

---

## 1. The Ledger Test, Which Runs First

**Every new claim carries one of the six states and appears in the ledger table.** The join is already done at build time, so this is checkable rather than aspirational: a claim that appears on a page and not in the table is a build failure.

**Including claims about our own work.** A sentence describing an unshipped tool takes the specification state. Code written and never executed takes the unrun state. **A projection carries its arithmetic.**

## 2. Acceptance Tests

| # | Test | Why it matters |
|---|---|---|
| 1 | The report names at least one capability the vendor does not frame as one | The capability block is the join to the estate's other work, and a feature list is not that |
| 2 | Every tool on the site maps to exactly one cell of the pattern by tier matrix | If a tool cannot be placed, one of the two axes is wrong |
| 3 | No page implies pattern three works here today | It is specified, not shipped, and the ledger has the state for it |
| 4 | Every credential rule names the product it applies to | The correction the site already had to make once |
| 5 | The disclosure is visible without scrolling on a page reached by deep link | A disclosure discovered at the bottom does the opposite of its job |
| 6 | The video walkthrough can be followed end to end by somebody with a key | It is the demonstration, and an unrunnable walkthrough is a claim |
| 7 | Its cost is measured, not projected | The state matters more than the number |
| 8 | The tried-and-abandoned page has three real entries | The failure ratio is the Explorer measure, and a site with no failures is a portfolio |
| 9 | Every cross-link into the family lands on a page, not a domain | The recorded family defect |
| 10 | Every page is still served as markdown at the stated path | The convention agents rely on, and it must survive every change |
| 11 | A section that could be replaced by a link to the vendor does not exist | The rule that stops this becoming an index of somebody else's documentation |
| 12 | The disclosures page states the current position with a date, whatever that position is | Its promise is to record first, which is only testable at the moment something changes |

## 3. What Done Does Not Include

- **A tier-three tool.** Step 6 accepts an honest label.
- **The parent hub.** Out of scope, and the composition rules here are what make it possible later.
- **Any migration from the tools site.** There is nothing to migrate for this provider.
- **The video toolchain.** The walkthrough uses what exists and does not build a renderer.
- **A second provider page beyond the existing stub.** The stub already proves the shape.

## 4. Two Regression Risks

**The markdown convention is the one that breaks silently.** It is the property agents rely on and nothing on a rendered page reveals its absence. Check it after every structural change.

**Root-absolute URLs broke once already**, at v0.1.0, because the site serves under a project path as well as its canonical name. **Any new page is a chance to reintroduce it**, and the fix is the same: relative to the page.

## 5. Rollback

Every step in the plan is additive except step 3, which edits existing pages. **Nothing in this pack deletes a page.** If a step is wrong, remove the section it added and the ledger entries it created; the build's own join will report any claim left orphaned, which is the mechanism working.

---

*Released under CC BY 4.0.*
