#!/usr/bin/env bash
# test-labs.sh — run the lab.js self-test in a real browser and fail on any assertion.
# Needs a Chromium; set CHROME to point at one. No network is used by the test itself.
set -euo pipefail
cd "$(dirname "$0")/.."

CHROME="${CHROME:-}"
if [ -z "$CHROME" ]; then
  for c in /opt/pw-browsers/chromium-*/chrome-linux/chrome "$(command -v chromium || true)" \
           "$(command -v chromium-browser || true)" "$(command -v google-chrome || true)"; do
    [ -x "${c:-}" ] && CHROME="$c" && break
  done
fi
[ -n "$CHROME" ] || { echo "test-labs: no chromium found; set CHROME=/path/to/chrome" >&2; exit 2; }

port=$(( 8000 + RANDOM % 1000 ))
python3 -m http.server "$port" >/dev/null 2>&1 &
server=$!
trap 'kill $server 2>/dev/null || true' EXIT
sleep 1

out=$("$CHROME" --headless --disable-gpu --no-sandbox --virtual-time-budget=4000 \
      --dump-dom "http://localhost:$port/tools/lab-selftest.html" 2>/dev/null)

python3 - "$out" <<'PY'
import html, re, sys
dom = sys.argv[1]
m = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
text = html.unescape(m.group(1)) if m else '(no output — the page did not run)'
print(text)
sys.exit(0 if 'RESULT PASS' in text else 1)
PY
