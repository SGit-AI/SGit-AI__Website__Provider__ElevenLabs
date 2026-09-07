#!/usr/bin/env bash
# stt.sh <audio-or-video> [out.json] — Scribe transcription with word timestamps (the QA gate, docs/05).
set -euo pipefail; : "${ELEVENLABS_API_KEY:?}"
curl -sS -X POST https://api.elevenlabs.io/v1/speech-to-text -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F model_id=scribe_v1 -F "file=@$1" -F timestamps_granularity=word -o "${2:-/tmp/eleven-stt.json}"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print(d.get("text","")[:400])' "${2:-/tmp/eleven-stt.json}"
