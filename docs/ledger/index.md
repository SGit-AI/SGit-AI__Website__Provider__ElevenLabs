---
title: The ledger — every claim, and how we know it
description: "Every factual claim this site makes, in one table, with its verification state, its date and the pages that say it. Six states, from verified-by-execution to specified-and-not-shipped."
lead: "Almost everything written about this API here was written by a machine that **could not reach the API**. A small, specific set of things was verified in a real browser on 5 September 2026. The distinction between the two is the most useful thing this site has, so it is a table rather than a disclaimer."
order: 80
toc: true
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
  note: "Assembled from the source vault's own materials inventory."
---

## The six states

| Chip | Means | What you may do with it |
|---|---|---|
| {{badge:verified}} | We ran it and watched it work, on that date, in a named place | Treat as fact for that date and that setup |
| {{badge:measured}} | Our own pipeline produced this number on a named workload | Treat as fact about *our* workload; yours will differ |
| {{badge:docs}} | Read in the vendor's documentation on that date; never executed by us | Check it against the vendor before you rely on it — and tell us if it moved |
| {{badge:spec}} | A written specification for something that does not exist | Never plan around it. Future tense only |
| {{badge:unrun}} | Code we wrote and have never executed | Read it, then run it and find out. Expect it to be wrong somewhere |
| {{badge:projected}} | Arithmetic, with its workings shown | Re-do the arithmetic with your own numbers |

Every chip on this site links here. Every claim below names where it is said, so a claim cannot appear on a page without appearing in this table — the join is done at build time.

{{ledger}}

## Open items

The honest list of what is unfinished, so that nothing here is presented as done. It matches the handover brief this site was built from, and it is the first thing to fix.

<div class="fails"><div class="fail open"><h3>The names-pronunciation test has not been run</h3><p>The bench has had the button since 5 September 2026. Nobody has pressed it. Until somebody does, this site cannot say which names <code>eleven_v3</code> mispronounces, and <code>pronunciations.pls</code> is a hypothesis rather than a lexicon. {{claim:names-test}}</p><p><b>Cost to close it:</b> about 120 characters, roughly $0.012, and two minutes of listening. <a href="/experiments/pronunciation/">The lab is here.</a></p></div><div class="fail open"><h3><code>sg.tts</code> is unimplemented</h3><p>It needs host-side work in SG/Vault, which is not in this repository. Until it lands, ElevenLabs cannot reach pattern 3 and the labs on this site cannot drop their key boxes. {{claim:sg-tts-spec}}</p></div><div class="fail open"><h3>Pattern 2 has no server</h3><p>For text to speech the vendor offers no short-lived credential, so a minter would be ours to run. Nobody has written one, and this site is not the place for it. {{claim:agents-only-signed-urls}}</p></div><div class="fail open"><h3>The render shim and every example file are unrun</h3><p>Written by a container with no egress to the API. {{claim:shim-unrun}} {{claim:examples-unrun}} The same is true of <a href="/experiments/">every lab on this site</a>. {{claim:labs-unrun}}</p></div><div class="fail open"><h3>Concurrency is unknown</h3><p>The plan's concurrent-request limit against a render that fires 16 requests at once has never been tested. {{claim:concurrency-unknown}} <a href="/experiments/concurrency/">The probe exists</a>; it costs a few cents to run.</p></div><div class="fail open"><h3>These pages will move</h3><p>Long term, the patterns, comparison, ledger and disclosures belong at <code>providers.sgit.ai</code>, shared by every provider site. Version 1 carries them here, and the templates are built so that the move is a redirect rather than a rewrite.</p></div></div>

## What we would need a human with API access to check

Handed back rather than guessed at. This is the list in [`HANDBACK.md`](https://github.com/SGit-AI/SGit-AI__Website__Provider__ElevenLabs/blob/main/HANDBACK.md) in the repository, kept short enough to work through in an afternoon:

1. **The smoke test** — `examples/00-smoke.sh`. Does the key work, what is the quota, does one sentence come back? Everything else depends on it.
2. **Which names v3 gets wrong** — the [pronunciation lab](/experiments/pronunciation/), the "names to test" sample, and two minutes of listening.
3. **Whether the alias rules in `pronunciations.pls` fix them** — the same lab, with the dictionary attached.
4. **Where the concurrency wall is** on the plan in use — the [concurrency probe](/experiments/concurrency/), which is the only lab here that can cost more than pennies if you set the numbers high.
5. **Whether the cue rule produces readable subtitles** on a real reel rather than on a 187-character sample — the [captions studio](/experiments/captions/) {{claim:cue-rule}}.
6. **Whether forced alignment matches the Kokoro-rendered cuts** to their scripts, which would give subtitles to six already-published videos for about two cents {{claim:alignment-stt-price}}.
7. **Whether the list prices in the tables here still hold.** They carry the date they were read; they are the fastest-staling thing on the site {{claim:tts-prices}}.

None of these needs a key from anyone; each needs somebody's own key, in their own browser, for a few minutes. Results paste back as markdown from every lab.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
