#!/usr/bin/env bash
# voices.sh — list voices as: voice_id · name · category · accent · gender · use_case
set -euo pipefail; : "${ELEVENLABS_API_KEY:?}"
curl -sS https://api.elevenlabs.io/v1/voices -H "xi-api-key: $ELEVENLABS_API_KEY" | python3 -c '
import json,sys
for v in sorted(json.load(sys.stdin)["voices"], key=lambda x:(x.get("category",""),x["name"])):
    l=v.get("labels") or {}; print(f'{v["voice_id"]}  {v["name"]:<18} {v.get("category",""):<12} {l.get("accent",""):<12} {l.get("gender",""):<8} {l.get("use_case","")}')'
