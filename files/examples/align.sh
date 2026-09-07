#!/usr/bin/env bash
# align.sh <audio-or-video> <script.txt> [out.json] — forced alignment of an existing render to its script.
# Build script.txt from reel.json: intro + scenes + outro, one per line, using narrationShorts for a shorts.mp4.
set -euo pipefail; : "${ELEVENLABS_API_KEY:?}"
curl -sS -X POST https://api.elevenlabs.io/v1/forced-alignment -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "file=@$1" -F "text=<$2" -o "${3:-/tmp/eleven-align.json}"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));w=d.get("words",[]);print(len(w),"words aligned; last ends at",w[-1]["end"] if w else "?")' "${3:-/tmp/eleven-align.json}"
