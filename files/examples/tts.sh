#!/usr/bin/env bash
# tts.sh "<text>" <voice_id> [out.mp3] — plain generation, MP3 to a file. ELEVEN_MODEL and SPEED honoured.
set -euo pipefail; : "${ELEVENLABS_API_KEY:?}"
TEXT="$1"; VOICE="$2"; OUT="${3:-/tmp/eleven-tts.mp3}"
curl -sS -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE?output_format=mp3_44100_128" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H 'content-type: application/json' \
  -d "$(python3 -c 'import json,sys,os;print(json.dumps({"text":sys.argv[1],"model_id":os.environ.get("ELEVEN_MODEL","eleven_v3"),"voice_settings":{"stability":0.5,"similarity_boost":0.75,"speed":float(os.environ.get("SPEED","1.0"))}}))' "$TEXT")" \
  -o "$OUT" -D /tmp/eleven-headers.txt
grep -i -E "^(HTTP|request-id)" /tmp/eleven-headers.txt | tr -d '\r'; echo "→ $OUT ($(stat -c %s "$OUT") bytes)"
