# Briefing pack — narrated videos for the ElevenLabs provider site

Hand this folder to the Claude Code session working on `SGit-AI__Website__Provider__ElevenLabs`.

**Read in this order:**

1. **`BRIEF.md`** — what the pipeline is, what changes now that the repo is public and the API is reachable, what ElevenLabs buys you that the four shipped reels do not have, costs, and three videos worth making first.
2. **`ELEVENLABS-FIRST-RUN.md`** — **read before spending a render.** The `TTS=elevenlabs` path has never been executed. Four likely failure points, each with a concrete fix.
3. **`materials/tooling/SKILL.md`** — the actual manual, 244 lines, written to be followed unattended. Everything else here is context for it.

**What's in `materials/`:**

| Folder | What |
|---|---|
| `tooling/` | The whole pipeline, 724 KB, self-contained: `bootstrap.sh`, the seven scripts, the vendored `video-creator` render tool, the four TTS shims, `reel.template.json`, and the upstream design notes. Copy it into your repo and run `bootstrap.sh` |
| `examples/` | Four worked reels — `reel.json`, `FINDINGS.md`, `PUBLISH.md` (titles, descriptions, chapters), plus a capture log and a render log. Two shapes: app-driven capture and slide-based, no capture |
| `reference-videos/` | Two finished MP4s — a 1:55 landscape and a 1:22 portrait. Watch these first; they are the target |
| `elevenlabs/` | The API notes that matter for the pipeline (TTS, models/voices, timestamps→SRT, pronunciation, pricing, auth/errors), the plan, the starting PLS lexicon, and the example shell scripts |
| `claude/` | The `make-a-video` skill, the lessons file, and two slash commands, if you want them in your own `.claude/` |

**The four things to get right:**

- **Write `reel.json` first**, before shooting anything. 2.1 words per second is the length; count before any audio exists.
- **The `TTS=elevenlabs` path is unrun.** One scene first, not a full reel.
- **The repo is public.** The key goes in the environment for the life of one command and nowhere else. Grep before every commit.
- **Portrait cuts must land under 3:00** with real margin, or YouTube will not treat them as Shorts.

`env.sh` is deliberately not included — it is container-specific and `bootstrap.sh` rewrites it. Run `bootstrap.sh` again after every pull; a stale `env.sh` from another machine is the cause of the `spawnSync …/ffmpeg… ENOENT` failure at the end of a render.

---

*This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).*
