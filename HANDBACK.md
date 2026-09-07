# Handback — what this site could not verify, and who could

Written 7 September 2026, at the end of the build. Nothing in this list was guessed at on the site; every
item is badged there and appears in [`/ledger/`](https://elevenlabs.providers.sgit.ai/ledger/).

**No ElevenLabs API key was requested, used, or committed while building this site.** Nothing in the build
calls the API, and nothing needs to. Every item below needs somebody's *own* key, in their *own* browser,
for a few minutes.

## 1 · Claims that need re-verification by somebody with API access

In the order that closes the most open items for the least money. Total, at list price: **about fifteen cents.**

| # | Claim to settle | Where | Cost | Ledger id |
|---|---|---|---|---|
| 1 | Does the key work at all, and what is the quota? | `files/examples/00-smoke.sh` | free + one sentence | `examples-unrun` |
| 2 | **Which names does `eleven_v3` mispronounce?** Nobody has ever pressed this button | [/bench/](https://elevenlabs.providers.sgit.ai/bench/) §5 | ~$0.012 | `names-test` |
| 3 | Do the aliases in `pronunciations.pls` fix them? | [/experiments/pronunciation/](https://elevenlabs.providers.sgit.ai/experiments/pronunciation/) | ~$0.02 | `lexicon-hypothesis` |
| 4 | Where is the concurrency wall on the plan in use? | [/experiments/concurrency/](https://elevenlabs.providers.sgit.ai/experiments/concurrency/) | ~$0.05 | `concurrency-unknown` |
| 5 | Does the cue rule produce readable subtitles on a real reel? | [/experiments/captions/](https://elevenlabs.providers.sgit.ai/experiments/captions/) | ~$0.04 | `cue-rule` |
| 6 | Does forced alignment match the already-published cuts to their scripts? | [/experiments/align-verify/](https://elevenlabs.providers.sgit.ai/experiments/align-verify/) | <$0.02 for all six | `alignment-stt-price` |
| 7 | Is the latency figure (5.0–5.8 s, three samples) representative? | [/experiments/models/](https://elevenlabs.providers.sgit.ai/experiments/models/) | ~$0.03 | `latency-5s` |
| 8 | Do the list prices still hold? | the vendor's pricing page | free | `tts-prices`, `plan-quotas` |
| 9 | Does `apply_text_normalization: auto` read `2,788` correctly? | [/experiments/text-handling/](https://elevenlabs.providers.sgit.ai/experiments/text-handling/) | ~$0.03 | — |
| 10 | Does a fixed seed actually repeat? | same lab, §4 | ~$0.02 | — |

Every lab prints its result as a markdown table with a timestamp. Paste it into an issue on this
repository and the ledger row changes state, with the date.

## 2 · Things nobody can verify from here

- **`sg.tts` needs host-side work in SG/Vault**, which is not in this repository. Until it ships, ElevenLabs
  cannot reach pattern 3 and the labs cannot drop their key boxes.
- **Pattern 2 has no server.** For text to speech the vendor offers no short-lived credential, so a minter
  would be ours to build, host and pay for. It does not exist and this repository is not the place for it.
- **The render shim** (`TTS=elevenlabs`) lives in the video vault, not here. It has never been executed.

## 3 · Things skipped in this version, and why

- **DNS was not confirmed.** `docs/CNAME` is set to `elevenlabs.providers.sgit.ai`, following the brief.
  Note that this repository's own description says `elevenlabs.provider.sgit.ai` (singular). **Somebody who
  owns the zone must confirm which is right before this goes live**; it is a one-line change in `build.py`.
- **The pipeline expects a `dev` branch, and this repository has none.** The estate's
  convention is `dev` = release branch (validate → tag → deploy), `main` = deploy-only.
  Until `dev` exists, `main` is treated as a release branch too; create `dev` and drop
  `main` from the `tag-release` condition in `.github/workflows/deploy-pages.yml` to
  match the siblings exactly. GitHub Pages also needs pointing at the workflow
  (Settings → Pages → Source: GitHub Actions) — the pipeline builds and uploads
  `docs/` rather than serving a branch directory.
- **A third-party secret-scanning Action was not added.** `tools/secret-scan.sh` runs the required patterns
  over the whole tree, including the built site, and is a required CI check. A vendored Action would have
  been a third-party dependency in a repository whose whole argument is about what you take a dependency on,
  and the org-licence requirements of the obvious candidate would have failed the build rather than the scan.
- **The labs were not exercised.** Twelve of the thirteen have never made a request. They are badged
  `written, not run` everywhere they appear, including on their own pages.
- **Visual comparison against `sgit.ai` was done from its stylesheet**, not from a rendered screenshot: the
  tokens, type scale and component idioms are copied from the house `assets/site.css`. If the estate's style
  has moved since, this site is behind.

## 4 · What a reviewer should check first

1. That the [ledger](https://elevenlabs.providers.sgit.ai/ledger/) matches what the pages say — the build
   joins them, but the *wording* of a claim is a human judgement.
2. That §4 of the report names the product on every quote. Getting this wrong once would send a reader off
   to build a signed-URL minter for an endpoint that does not accept one.
3. That nothing on the site reads as an official vendor property. No logo, no wordmark, no brand colour,
   no "partner", disclosures in the nav.
