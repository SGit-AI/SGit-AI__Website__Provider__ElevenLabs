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
| `tools/` | The secret scan, the acceptance checks, the JavaScript syntax check |
| `docs/` | The built site, committed. GitHub Pages serves this directory |

## Build

```bash
python3 build.py               # → docs/
python3 build.py --check       # CI: rebuild to a temp dir and diff against docs/
python3 tools/check_site.py    # the acceptance checklist, as assertions
tools/secret-scan.sh           # the required secret scan
tools/check-js.sh              # syntax-check every inline lab script
python3 -m http.server -d docs 8000
```

Python 3.11+, no packages. Node is used only to syntax-check the labs' JavaScript.

## Adding a provider

One Markdown file in `content/providers/` with a `patterns:` block in its front-matter. The comparison
matrix is generated from those blocks, so no table is edited and no template is touched.
[`content/providers/openrouter.md`](content/providers/openrouter.md) exists to prove it.

Long term, `/patterns/`, `/comparison/`, `/ledger/` and `/disclosures/` belong to the whole
`*.providers.sgit.ai` family and move to `providers.sgit.ai`; the templates are built so that the move
is a redirect rather than a rewrite.

## Rules this repository enforces in CI

- **The secret scan passes.** This repository is public; the vault its content came from was not.
- **No third-party anything.** No CDN, no web fonts, no analytics, no cookies. The only host any page
  talks to is `api.elevenlabs.io`, in a request the reader starts, and the check fails on any other origin
  appearing in the built site.
- **`docs/` matches the sources.** A stale build fails.
- **The nine sections of the report are present and in order**; every claim is cited; the non-affiliation
  line is in every footer; the word "partner" appears nowhere; `sg.tts` stays in the future tense.

## Keys

**No ElevenLabs API key was requested, used, or committed at any point in building this site**, and none
is needed to build it. A key you type into a lab is kept in *your* browser's `localStorage` and sent to
exactly one host. There is no server here to send it to.

## Corrections

Facts on this site have dates on them because they go stale. If a price has moved, a claim is wrong, or
a lab is broken, open an issue — a correction changes a row in the ledger, with the date it was made,
rather than quietly rewriting a paragraph. See [`HANDBACK.md`](HANDBACK.md) for the list of claims that
need somebody with API access to check.

Apache-2.0.
