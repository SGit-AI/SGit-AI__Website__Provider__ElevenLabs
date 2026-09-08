---
title: Release history
description: "Every release of this site, with what changed. The version is owned by admin/build/version.txt, must appear in the release commit's subject, and CI verifies the two agree before it tags anything."
lead: "Every release of this site, with what changed and when. The estate's convention: **one file owns the version**, the release commit's subject repeats it, and the pipeline refuses to tag anything if the two disagree."
order: 95
---

<div class="tablewrap"><table class="vers"><thead><tr><th>Version</th><th>Date</th><th>What changed</th></tr></thead><tbody>
<!-- releases -->
    <tr><td class="vnum">v0.2.1</td><td>2026-09-08</td><td>the first video: the ElevenLabs render path ran for the first time, and the site gained what it found — two tier refusals, a model that rejects stitching, a key that names its own missing permission, and an alignment exact to the millisecond that attributes the estate's drift to the encoder rather than the speech</td></tr>
    <tr><td class="vnum">v0.2.0</td><td>2026-09-08</td><td>the providers-site pack implemented (two-layer capability block, the tool-state tier axis and its intersection with the patterns, positioning, a disclosure line on every page, pattern three's exact scope, page-level family links); both briefs published raw at /briefs/ under CC BY 4.0 with a page reviewing what was accepted, modified and rejected; the video-pipeline brief processed into /video/ with its measured numbers, its four first-run failure points and the reason no video was made</td></tr>
    <tr><td class="vnum">v0.1.2</td><td>2026-09-07</td><td>fix the vendor citation in section 4 — a bare URL in angle brackets reached the browser as an unknown tag, so the URL a reader is supposed to check was invisible on the page</td></tr>
    <tr><td class="vnum">v0.1.1</td><td>2026-09-07</td><td>make every internal URL relative to its page — the site was serving under a GitHub Pages project path, where root-absolute URLs 404 the stylesheet, the lab runtime and the favicon</td></tr>
    <tr><td class="vnum">v0.1.0</td><td>2026-09-07</td><td>First release. The nine-section report with §8 and §9 given the visual weight; the four credential patterns and the generated provider × pattern matrix; the claim ledger, six verification states, joined to the pages that cite them at build time; the sg.tts specification, future tense throughout; the ported test bench and twelve browser labs, keys in localStorage and one host; the example scripts and the PLS lexicon as downloadable files; disclosures; the CI pipeline (validate → tag → deploy) with a secret scan, a reproducible-build check, the acceptance assertions and the lab runtime's own browser tests.</td></tr>
</tbody></table></div>

## How a release is made here

The same three steps as every other site in this estate — `validate` → `tag-release` → `deploy`, in that order, with a failure at any stage stopping the release rather than shipping past it.

**1 · The version is owned by one file.** `admin/build/version.txt`. Nothing else may invent one: the nav badge, the footer, `llms.txt` and the table above are all rendered from it, and the release gate fails if any of them disagree.

**2 · One command bumps it.**

```bash
bin/bump.py "what changed in this release"     # --major for vR.M+1.0
python3 build.py
admin/build/validate.sh
git commit -am "site v0.1.1: what changed in this release"
```

The commit subject is not decoration. `tag-release` reads `version.txt`, finds the commit in this history whose **subject** carries the same version, and tags that commit — which is `HEAD` on a direct push and `HEAD`'s parent when a pull request lands as a merge. If no commit carries the version, or the tag already exists on an earlier commit, the release stops: a version was reused rather than bumped.

**3 · Every push to the release branch is a minor.** The new tag must be the next `vR.M.N+1`, or a deliberate `vR.M+1.0`. The first run backfills tags for any historical release it can read out of the commit subjects.

## What the gate checks before anything is tagged

The four house checks, plus what this particular site promises:

| Check | Why it exists here |
|---|---|
| **The build is reproducible** — `docs/` must match `content/` | Markdown is the source of truth; a stale build would publish prose nobody wrote |
| **Version agreement** — `version.txt` against every page badge, the table above, and `llms.txt` | A blanket version bump that misses a page ships two versions of one site |
| **Internal links resolve**, and every canonical URL is on the host in `CNAME` | A moved page and a copy-pasted canonical are the two ways a static site quietly breaks |
| **Key-leak tripwire** — API keys, vault keys, private keys, over the whole tree including `docs/` | This repository is public; the vault its content came from was not. A leak here would be the site's own headline |
| **One host** — no third-party resource, and no network origin in any script but `api.elevenlabs.io` | It is the [labs'](/experiments/) central claim, so it is a build failure rather than a promise |
| **The report's nine sections, in order; every claim cited; the non-affiliation line in every footer; `sg.tts` in the future tense** | The [acceptance checklist](/ledger/), enforced instead of remembered |
| **The lab runtime parses and passes its own tests** | Thirty-four assertions over the key store and the alignment arithmetic, in a real browser, with no network |

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
