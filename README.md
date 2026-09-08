# elevenlabs.providers.sgit.ai

> **Independent work by SGit-AI. Not affiliated with, endorsed by, or sponsored by ElevenLabs.
> "ElevenLabs" identifies the API this page reports on; all trademarks belong to their owners.**

A report on one paid API — what it cost on a named workload on a named date, what broke, and which
of four client-side credential patterns the product can actually support — plus twelve browser labs
for re-running the parts of the evaluation that were never run.

The site's argument, stated once and demonstrated by the pages: **a browser application can use a paid
API without ever holding the key, because the vault host holds it and enforces the terms.** Everything
else is evidence for that.

**Live:** <https://elevenlabs.providers.sgit.ai> · **Source material:** the video vault at commit
`7d1916aca5f3`, 7 September 2026.

---

## The one thing to understand before reading the site

Almost everything written here about the API was written by a container that **could not reach
`api.elevenlabs.io`**. A small, specific set of things was verified in a real browser on 5 September 2026.
The site never blurs the two: every factual claim carries one of six states —

`verified` · `measured` · `vendor docs` · `specified, not shipped` · `written, not run` · `projected`

— rendered as a chip that links to [`/ledger/`](https://elevenlabs.providers.sgit.ai/ledger/), where all
32 claims sit in one table with their dates and the pages that make them. A claim cannot appear on a page
without appearing in that table: the join is done at build time and a missing one fails CI.

`sg.tts` **does not exist.** It is a specification, and the build fails if any page describes it in the
present tense.

## Layout

| Path | What |
|---|---|
| `content/**.md` | The source of truth. Markdown with front-matter; each page ships its own `.md` twin |
| `data/claims.yml` | Every claim on the site, once, with its state, date and provenance |
| `apps/*.html` | The interactive labs: one HTML fragment each, injected at `{{app}}` |
| `assets/` | `site.css`, `site.js`, `lab.js`, the favicon. Self-hosted, no build step, no dependencies |
| `files/` | Downloadable artefacts: the example scripts and the PLS lexicon |
| `build.py` | The whole build system — Markdown, front-matter, shortcodes, generated tables. No dependencies |
| `tools/` | The secret scan, the acceptance checks, the JavaScript syntax check, the lab self-test |
| `admin/build/` | `version.txt` owns the site version; `validate.sh` is the pre-release gate |
| `bin/bump.py` | The one command that bumps a release, in both the places that own it |
| `briefs/` | The briefs this site was built from, raw, published at `/briefs/` under CC BY 4.0 |
| `docs/` | The built site, committed. GitHub Pages serves this directory |

## Build

```bash
python3 build.py               # → docs/
admin/build/validate.sh        # the pre-release gate, all of it, in order
python3 -m http.server -d docs 8000
```

The gate, if you want the pieces separately: `python3 build.py --check` (docs/ matches
content/), `python3 tools/check_site.py` (the assertions), `tools/secret-scan.sh`,
`tools/check-js.sh`, `tools/test-labs.sh` (34 browser assertions over the lab runtime).
Pass `--no-browser` to `validate.sh` to skip the last one locally; CI never skips it.

Python 3.11+, no packages. Node syntax-checks the labs' JavaScript and a Chromium runs
their tests.

## Adding a provider

One Markdown file in `content/providers/` with a `patterns:` block in its front-matter. The comparison
matrix is generated from those blocks, so no table is edited and no template is touched.
[`content/providers/openrouter.md`](content/providers/openrouter.md) exists to prove it.

Long term, `/patterns/`, `/comparison/`, `/ledger/` and `/disclosures/` belong to the whole
`*.providers.sgit.ai` family and move to `providers.sgit.ai`; the templates are built so that the move
is a redirect rather than a rewrite.

## Releases — validate → tag → deploy

The estate's pipeline, in `.github/workflows/deploy-pages.yml`, in that order. A
failure at any stage stops the release rather than shipping past it.

```bash
bin/bump.py "what changed in this release"       # --major for vR.M+1.0
python3 build.py
admin/build/validate.sh
git commit -am "site v0.1.1: what changed in this release"
```

**One file owns the version** — `admin/build/version.txt`. The nav badge, the footer,
`llms.txt` and [the release history](content/versions.md) are all rendered from it, and
the gate fails if any of them disagree. **The commit subject is load-bearing**:
`tag-release` reads `version.txt`, finds the commit in the history whose *subject*
carries that version, and tags it — HEAD on a direct push, HEAD's parent when a pull
request lands as a merge. A version reused rather than bumped is an error, not a
silent overwrite. Every push to the release branch is a minor; the first run backfills
tags for any historical release it can read out of the commit subjects.

`dev` is the estate's release branch. This repository does not have one yet, so `main`
is treated as a release branch too — when `dev` is created, drop `main` from the
`tag-release` condition and this matches its siblings exactly.

## Rules this repository enforces in CI

- **The secret scan passes.** This repository is public; the vault its content came from was not.
- **No third-party anything.** No CDN, no web fonts, no analytics, no cookies. The only host any page
  talks to is `api.elevenlabs.io`, in a request the reader starts, and the check fails on any other origin
  appearing in the built site.
- **The site works wherever it is served** — the custom domain, a GitHub Pages project path, a local
  directory, a vault app frame. Every internal URL is relative to its page (`<html data-root>` carries the
  root for anything JavaScript needs), and a root-absolute one fails the build.
- **`docs/` matches the sources.** A stale build fails.
- **The nine sections of the report are present and in order**; every claim is cited; the non-affiliation
  line is in every footer; the word "partner" appears nowhere; `sg.tts` stays in the future tense.

## Keys

**No ElevenLabs API key is needed to build this site, and none was used to build it** — every page through
v0.2.0 was written, and every check still runs, with no key present. **On 8 September 2026 the project lead
supplied a key for one run**, to make [the first video](https://elevenlabs.providers.sgit.ai/video/); it was
held in one command's environment, written to no file, and **never committed** — the secret scan is a required
CI check precisely so that sentence is enforced rather than promised. A key you type into a lab is kept in
*your* browser's `localStorage` and sent to exactly one host. There is no server here to send it to.

## Corrections

Facts on this site have dates on them because they go stale. If a price has moved, a claim is wrong, or
a lab is broken, open an issue — a correction changes a row in the ledger, with the date it was made,
rather than quietly rewriting a paragraph. See [`HANDBACK.md`](HANDBACK.md) for the list of claims that
need somebody with API access to check.

## Licence

**The site's content** — every page, every markdown twin, `llms.txt`, `llms-full.txt` and the
published briefs — is **CC BY 4.0**, as across the `*.sgit.ai` network. The stamp is in the page
footer, at the foot of every raw markdown document and in both machine-readable indexes, and a
build check enforces it so it cannot drift.

**The code that builds it** — `build.py`, `assets/`, `apps/`, `tools/` — is **Apache-2.0**.
