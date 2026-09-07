#!/usr/bin/env bash
# 00-smoke.sh — does the key work, what is the quota, and one sentence of audio.
# Usage: from the vault root, with the vault key present:
#   export ELEVENLABS_API_KEY=$(node tooling/scripts/vault-secrets.mjs open elevenlabs); bash elevenlabs/examples/00-smoke.sh
set -euo pipefail
: "${ELEVENLABS_API_KEY:?export ELEVENLABS_API_KEY first (node tooling/scripts/vault-secrets.mjs open elevenlabs)}"
API=https://api.elevenlabs.io/v1
echo "1/3 subscription"; curl -sS "$API/user/subscription" -H "xi-api-key: $ELEVENLABS_API_KEY" | python3 -c 'import json,sys;d=json.load(sys.stdin);print("  tier",d.get("tier"),"·",d.get("character_count"),"/",d.get("character_limit"),"chars used")'
echo "2/3 voices"; curl -sS "$API/voices" -H "xi-api-key: $ELEVENLABS_API_KEY" | python3 -c 'import json,sys;v=json.load(sys.stdin)["voices"];print("  ",len(v),"voices; first premade:",next((x["name"]+" "+x["voice_id"] for x in v if x.get("category")=="premade"),"?"))'
VOICE="${VOICE:-$(curl -sS "$API/voices" -H "xi-api-key: $ELEVENLABS_API_KEY" | python3 -c 'import json,sys;v=json.load(sys.stdin)["voices"];print(next(x["voice_id"] for x in v if x.get("category")=="premade"))')}"
echo "3/3 one sentence with timestamps → /tmp/eleven-smoke.mp3 (voice $VOICE)"
curl -sS -X POST "$API/text-to-speech/$VOICE/with-timestamps?output_format=mp3_44100_128" -H "xi-api-key: $ELEVENLABS_API_KEY" -H 'content-type: application/json' \
  -d '{"text":"This is the vault, opened read-only in the SG/Vault browser.","model_id":"'"${ELEVEN_MODEL:-eleven_v3}"'","voice_settings":{"stability":0.5,"similarity_boost":0.75,"speed":1.0}}' \
  | python3 -c 'import json,sys,base64;d=json.load(sys.stdin);open("/tmp/eleven-smoke.mp3","wb").write(base64.b64decode(d["audio_base64"]));a=d["alignment"];print("  ",len(a["characters"]),"characters timed, ends at",a["character_end_times_seconds"][-1],"s")'
echo "ok — play /tmp/eleven-smoke.mp3"
