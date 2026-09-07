#!/usr/bin/env bash
# Syntax-check every inline <script> in apps/*.html and every file in assets/*.js.
# The site ships no build step for its JavaScript, so this is the only thing standing
# between a typo and a dead lab.
set -euo pipefail
cd "$(dirname "$0")/.."
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
fail=0
for f in assets/*.js; do node --check "$f" || fail=1; done
for f in apps/*.html; do
  python3 - "$f" "$tmp" <<'PY'
import re, sys, pathlib
src, tmp = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
for n, block in enumerate(re.findall(r"<script>(.*?)</script>", src.read_text(), re.S)):
    (tmp / f"{src.stem}.{n}.js").write_text(block)
PY
done
for f in "$tmp"/*.js; do [ -e "$f" ] || continue; node --check "$f" || { echo "  ^ in ${f##*/}"; fail=1; }; done
[ "$fail" = 0 ] && echo "check-js: all scripts parse."
exit $fail
