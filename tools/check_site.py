#!/usr/bin/env python3
"""
check_site.py — the pre-release gate: the acceptance checklist as assertions over
the built site.

The first four are the house gate, inherited from the sibling sites in this estate
unchanged in intent — version agreement, internal links, canonical host, key-leak
tripwire. The rest are this site's own promises, which are worth no more than the
checks that enforce them.

Everything here is something a human would otherwise have to re-read the whole site
to confirm. Run after `python3 build.py`; `admin/build/validate.sh` runs both.

    python3 tools/check_site.py
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
DOMAIN = "elevenlabs.providers.sgit.ai"

# The one host any page here may talk to. Anchors to the vendor's documentation
# are links a reader clicks, not resources the page loads, so they are checked
# separately (see resource_loads).
ALLOWED_JS_ORIGINS = {
    "https://api.elevenlabs.io",
    # An XML namespace is an identifier, never fetched: it appears in the PLS
    # lexicon the pronunciation lab writes out, and nothing resolves it.
    "http://www.w3.org",
}

NON_AFFILIATION = "Not affiliated with, endorsed by, or sponsored by ElevenLabs"

# `sg.tts` does not exist. These are the ways a page would accidentally claim it does.
PRESENT_TENSE_SGTTS = [
    r"sg\.tts\b[^.<]{0,20}\b(is|does|provides|handles|holds|runs|works|exists|supports|returns|gives)\b",
    r"\b(uses|using|calls|calling|with) sg\.tts\b(?![^<]{0,80}(would|will|specified|spec))",
    r"sg\.tts\b[^<]{0,40}\bavailable today\b",
]

failures = []
notes = []


def fail(msg):
    failures.append(msg)


def pages():
    return sorted(OUT.rglob("index.html"))


def check_non_affiliation():
    for p in pages():
        if NON_AFFILIATION not in p.read_text():
            fail(f"non-affiliation line missing from {p.relative_to(OUT)}")


def check_forbidden_words():
    """'partner' is never used about a vendor here — see the disclosures page."""
    for p in list(pages()) + list(OUT.rglob("*.md")):
        for n, line in enumerate(p.read_text().split("\n"), 1):
            if re.search(r"\bpartner\w*\b", line, re.I):
                fail(f"the word 'partner' appears in {p.relative_to(OUT)}:{n}")


def check_sgtts_tense():
    for p in pages():
        text = p.read_text()
        for pattern in PRESENT_TENSE_SGTTS:
            for m in re.finditer(pattern, text, re.I):
                fail(f"sg.tts in the present tense in {p.relative_to(OUT)}: …{m.group(0)}…")


def resource_loads(html):
    """Everything the browser fetches without the reader asking."""
    out = []
    out += re.findall(r'<script[^>]+src=["\']([^"\']+)', html)
    out += re.findall(r'<link[^>]+href=["\']([^"\']+)', html)
    out += re.findall(r'<img[^>]+src=["\']([^"\']+)', html)
    out += re.findall(r'@import\s+["\']([^"\']+)', html)
    out += re.findall(r'url\((https?://[^)]+)\)', html)
    return out


def check_no_third_party():
    for p in pages():
        for url in resource_loads(p.read_text()):
            if url.startswith(("http://", "https://", "//")) and DOMAIN not in url:
                fail(f"third-party resource loaded by {p.relative_to(OUT)}: {url}")
    for css in OUT.rglob("*.css"):
        for url in re.findall(r'url\((https?://[^)]+)\)', css.read_text()) + re.findall(r'@import\s+["\']([^"\']+)', css.read_text()):
            fail(f"third-party resource in {css.relative_to(OUT)}: {url}")


def check_js_origins():
    """The claim on every lab: one host, and you can check it."""
    for js in list(OUT.rglob("*.js")) + list(OUT.rglob("index.html")):
        text = js.read_text()
        if js.suffix == ".html":
            text = "\n".join(re.findall(r"<script>(.*?)</script>", text, re.S))
        for url in set(re.findall(r'["\'](https?://[^"\'\s]+)', text)):
            origin = "/".join(url.split("/")[:3])
            if origin not in ALLOWED_JS_ORIGINS:
                fail(f"script in {js.relative_to(OUT)} references {origin}")


def check_shortcodes():
    for p in pages():
        for m in re.findall(r"\{\{[a-z:|.\- ]+\}\}", p.read_text()):
            fail(f"unexpanded shortcode {m} in {p.relative_to(OUT)}")


def check_links():
    built = {str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file()}
    for p in pages():
        base = p.parent.relative_to(OUT)
        for href in re.findall(r'href=["\']([^"\'#?]+)', p.read_text()):
            if href.startswith(("http://", "https://", "mailto:", "//")):
                continue
            target = (Path(href.lstrip("/")) if href.startswith("/") else base / href)
            target = Path(os.path.normpath(str(target)))
            candidates = {str(target), str(target / "index.html")}
            if not candidates & built:
                fail(f"dead internal link in {p.relative_to(OUT) if p != OUT / 'index.html' else 'index.html'}: {href}")


def check_relative_urls():
    """The site must work wherever it is served: the custom domain, a GitHub Pages
    project path, a local directory, a vault frame. A root-absolute internal URL
    works in exactly one of those, and shipping one left the first deploy
    unstyled — so it is a build failure now, not a review item."""
    for p in pages():
        for m in re.finditer(r'\b(?:href|src)="(/[^"]*)"', p.read_text()):
            fail(f"{p.relative_to(OUT)}: root-absolute URL {m.group(1)} — must be relative to the page")
    for js in OUT.rglob("*.js"):
        for m in re.finditer(r"""fetch\(\s*['"](/[^'"]*)""", js.read_text()):
            fail(f"{js.relative_to(OUT)}: fetch of a root-absolute URL {m.group(1)} — use EL.asset()")


def check_no_swallowed_urls(_seen=set()):
    """A bare <https://…> in markdown reaches the browser as an unknown tag and the
    URL vanishes. It is invisible in the source and invisible on the page, which is
    the worst combination, so the build refuses it."""
    for p in pages():
        for m in re.finditer(r"<https?:[^>]*>", p.read_text()):
            fail(f"{p.relative_to(OUT)}: a bare URL is being parsed as a tag: {m.group(0)[:60]}")


def check_nine_sections():
    text = (OUT / "index.html").read_text()
    wanted = ["1 · Disclosure", "2 · What it grants", "3 · Which pattern", "4 · Where the key goes",
              "5 · The bounding primitive", "6 · The minimal working example", "7 · What we use it for",
              "8 · What it cost", "9 · What went wrong"]
    pos = -1
    for w in wanted:
        i = text.find(w)
        if i < 0:
            fail(f"the report is missing section: {w}")
        elif i < pos:
            fail(f"the report's sections are out of order at: {w}")
        else:
            pos = i


def check_every_claim_cited():
    sys.path.insert(0, str(ROOT))
    import build  # noqa: E402
    claims = build.yaml_load((ROOT / "data" / "claims.yml").read_text())
    html = "\n".join(p.read_text() for p in pages())
    for c in claims:
        if f"claim-{c['id']}" not in html:
            fail(f"claim {c['id']!r} is in the ledger but cited by no page")
        if c["state"] not in build.STATES:
            fail(f"claim {c['id']!r} has an unknown state {c['state']!r}")
        if c["state"] in ("verified", "measured", "docs") and not c.get("date"):
            fail(f"claim {c['id']!r} is {c['state']} but carries no date")


def check_key_bar_and_pattern_box():
    """Every page that can take a key says, at the top, what pattern that is."""
    for p in pages():
        text = p.read_text()
        if 'id="keybar"' in text and "Which pattern this is" not in text:
            fail(f"{p.relative_to(OUT)} asks for a key without the pattern box")
        if "type=\"password\"" in text and "value=" in text.split("type=\"password\"")[1][:120]:
            fail(f"{p.relative_to(OUT)} ships a value in a password field")


def check_version_agreement():
    """House check 1. One file owns the version; everything else is rendered from
    it. A blanket bump that misses a page ships two versions of one site."""
    version = (ROOT / "admin" / "build" / "version.txt").read_text().strip()
    if not re.fullmatch(r"v\d+\.\d+\.\d+", version):
        fail(f"admin/build/version.txt does not carry a vX.Y.Z version: {version!r}")
        return
    for p in pages():
        for badge in re.findall(r'class="ver"[^>]*>(v\d+\.\d+\.\d+)<', p.read_text()):
            if badge != version:
                fail(f"{p.relative_to(OUT)}: version badge {badge} != {version}")
    for name in ("llms.txt", "llms-full.txt"):
        if version not in (OUT / name).read_text():
            fail(f"{name} does not mention {version}")
    history = (OUT / "versions" / "index.html").read_text()
    rows = re.findall(r'class="vnum">(v\d+\.\d+\.\d+)<', history)
    if version not in rows:
        fail(f"the release history has no row for {version}")
    for v in rows:
        if rows.count(v) > 1:
            fail(f"the release history lists {v} more than once")
            break


def check_canonical_host():
    """House check 3. Every canonical and og:url is on the host in CNAME, and every
    page declares one — a copy-pasted canonical is how a static site quietly
    de-indexes itself."""
    host = (OUT / "CNAME").read_text().strip()
    for p in pages():
        text = p.read_text()
        claimed = re.findall(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', text)
        claimed += re.findall(r'<meta[^>]+property="og:url"[^>]+content="([^"]+)"', text)
        if not claimed:
            fail(f"{p.relative_to(OUT)}: no canonical link")
        for url in claimed:
            if not url.startswith(f"https://{host}/") and url != f"https://{host}":
                fail(f"{p.relative_to(OUT)}: canonical/og:url is not on {host} -> {url}")


def check_vault_key_tripwire():
    """House check 4, as a belt to tools/secret-scan.sh's braces: an sgit vault key
    is <passphrase>:<uuid>, and it unlocks everything the vault holds."""
    shape = re.compile(r"[A-Za-z0-9_-]{20,}:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
    for f in ROOT.rglob("*"):
        if not f.is_file() or ".git/" in str(f) or f.suffix in {".png", ".jpg", ".webp", ".ico", ".woff2", ".zip", ".pdf"}:
            continue
        try:
            if shape.search(f.read_text()):
                fail(f"{f.relative_to(ROOT)}: contains a vault-key-shaped string")
        except (UnicodeDecodeError, OSError):
            continue


def check_cname():
    cname = (OUT / "CNAME").read_text().strip()
    if cname != DOMAIN:
        fail(f"CNAME is {cname!r}, expected {DOMAIN!r}")


def check_markdown_twins():
    for p in pages():
        if not (p.parent / "index.md").exists():
            fail(f"no markdown twin beside {p.relative_to(OUT)}")


def main():
    if not OUT.exists():
        print("docs/ not built — run python3 build.py first", file=sys.stderr)
        sys.exit(2)
    for fn in [check_version_agreement, check_links, check_relative_urls, check_canonical_host, check_vault_key_tripwire,
               check_non_affiliation, check_forbidden_words, check_sgtts_tense, check_no_third_party,
               check_js_origins, check_shortcodes, check_no_swallowed_urls, check_nine_sections,
               check_every_claim_cited, check_key_bar_and_pattern_box, check_cname, check_markdown_twins]:
        fn()
    if failures:
        print(f"check_site: {len(failures)} problem(s)\n", file=sys.stderr)
        for f in failures:
            print("  ✗ " + f, file=sys.stderr)
        sys.exit(1)
    print(f"check_site: {len(list(pages()))} pages pass every acceptance assertion.")
    for n in notes:
        print("  · " + n)


if __name__ == "__main__":
    main()
