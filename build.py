#!/usr/bin/env python3
"""
build.py — the whole build system for elevenlabs.providers.sgit.ai.

Markdown in `content/` is the source of truth; this script renders it to static
HTML in `docs/`. No dependencies, no framework, no CDN: a site that argues for
credential hygiene should not ask a reader to trust forty transitive packages.

    python3 build.py            build docs/
    python3 build.py --check    build to a temp dir and diff against docs/ (CI)

Generated, not hand-written:
  * the comparison matrix          — from `patterns:` front-matter on provider pages
  * the ledger of claims           — from data/claims.yml, joined to every {{claim:id}}
  * the experiments index          — from the experiment pages' front-matter
  * each page's markdown twin      — docs/<path>/index.md, the house convention
"""

import html
import os
import re
import shutil
import sys
import tempfile
import filecmp
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
APPS = ROOT / "apps"
ASSETS = ROOT / "assets"
FILES = ROOT / "files"
DATA = ROOT / "data"
OUT = ROOT / "docs"

SITE = {
    "domain": "elevenlabs.providers.sgit.ai",
    "base": "https://elevenlabs.providers.sgit.ai",
    "title": "ElevenLabs, reported on",
    "vault_commit": "7d1916aca5f3",
    "version": "v1.0.0",
}

NAV = [
    ("The report", "/"),
    ("Experiments", "/experiments/"),
    ("Bench", "/bench/"),
    ("Patterns", "/patterns/"),
    ("Comparison", "/comparison/"),
    ("Ledger", "/ledger/"),
    ("Disclosures", "/disclosures/"),
]

NON_AFFILIATION = (
    "Independent work by SGit-AI. Not affiliated with, endorsed by, or sponsored by "
    "ElevenLabs. &ldquo;ElevenLabs&rdquo; identifies the API this page reports on; all "
    "trademarks belong to their owners."
)

# ---------------------------------------------------------------- tiny YAML ---
# A deliberate subset: mappings, sequences, sequences of mappings, inline lists,
# quoted scalars. Anything hairier belongs in prose, not in front-matter.


def yaml_load(text):
    lines = []
    for raw in text.split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, raw.strip()))
    val, _ = _yaml_block(lines, 0, 0)
    return val


def _scalar(s):
    s = s.strip()
    if not s:
        return ""
    if s[0] in "\"'" and s[-1] == s[0] and len(s) > 1:
        body = s[1:-1]
        if s[0] == '"':                       # only double quotes take escapes
            body = body.replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
        return body
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [_scalar(x) for x in _split_commas(inner)] if inner else []
    if s == "true":
        return True
    if s == "false":
        return False
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d*\.\d+", s):
        return float(s)
    return s


def _split_commas(s):
    out, depth, cur, quote = [], 0, "", None
    for ch in s:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote, cur = ch, cur + ch
        elif ch in "[{":
            depth, cur = depth + 1, cur + ch
        elif ch in "]}":
            depth, cur = depth - 1, cur + ch
        elif ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return [x.strip() for x in out]


def _yaml_block(lines, i, indent):
    if i >= len(lines):
        return {}, i
    if lines[i][1].startswith("- "):
        return _yaml_seq(lines, i, indent)
    return _yaml_map(lines, i, indent)


def _yaml_map(lines, i, indent):
    out = {}
    while i < len(lines):
        ind, text = lines[i]
        if ind < indent:
            break
        if ind > indent:  # defensive: a stray deeper line
            i += 1
            continue
        key, _, rest = text.partition(":")
        key, rest = key.strip(), rest.strip()
        if rest:
            out[key] = _scalar(rest)
            i += 1
        else:
            i += 1
            if i < len(lines) and lines[i][0] > ind:
                out[key], i = _yaml_block(lines, i, lines[i][0])
            else:
                out[key] = None
    return out, i


def _yaml_seq(lines, i, indent):
    out = []
    while i < len(lines):
        ind, text = lines[i]
        if ind < indent or not text.startswith("- "):
            break
        body = text[2:].strip()
        if ":" in body and not body.startswith(("\"", "'")):
            # a mapping whose first pair is on the dash line
            sub_lines = [(0, body)]
            j = i + 1
            while j < len(lines) and lines[j][0] > ind:
                sub_lines.append((lines[j][0] - (ind + 2), lines[j][1]))
                j += 1
            item, _ = _yaml_map(sub_lines, 0, 0)
            out.append(item)
            i = j
        else:
            out.append(_scalar(body))
            i += 1
    return out, i


# ------------------------------------------------------------- markdown ------
# A subset of GFM: headings, paragraphs, lists, tables, fenced code, block
# quotes, rules, inline emphasis/code/links. Enough for a report; small enough
# to read in one sitting.

INLINE_CODE = re.compile(r"`([^`]+)`")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
EM = re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])")
STRIKE = re.compile(r"~~([^~]+)~~")


def slugify(text):
    s = re.sub(r"<[^>]+>", "", text).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "section"


def inline(text, ctx):
    """Inline markdown → HTML. Code spans are extracted first so nothing
    inside them is interpreted."""
    spans = []

    def stash(m):
        spans.append(m.group(1))
        return f"\x00{len(spans) - 1}\x00"

    text = INLINE_CODE.sub(stash, text)
    text = shortcodes_inline(text, ctx)
    placeholders = {}

    def stash_html(fragment):
        placeholders[f"\x01{len(placeholders)}\x01"] = fragment
        return list(placeholders)[-1]

    # keep raw <chip …> etc. produced by shortcodes out of the escaper
    parts = re.split(r"(<[^>]+>)", text)
    text = "".join(stash_html(p) if p.startswith("<") and p.endswith(">") else html.escape(p, quote=False) for p in parts)

    text = LINK.sub(lambda m: _link(m, ctx), text)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = EM.sub(r"<em>\1</em>", text)
    text = STRIKE.sub(r"<s>\1</s>", text)
    text = text.replace("--", "&ndash;") if False else text
    for k, v in placeholders.items():
        text = text.replace(k, v)
    for i, code in enumerate(spans):
        text = text.replace(f"\x00{i}\x00", f"<code>{html.escape(code, quote=False)}</code>")
    return text


def _link(m, ctx):
    label, href, title = m.group(1), m.group(2), m.group(3)
    ext = href.startswith("http") and SITE["domain"] not in href
    attrs = f' title="{html.escape(title)}"' if title else ""
    if ext:
        attrs += ' rel="noopener"'
        ctx["external_links"].add(href)
    return f'<a href="{html.escape(href)}"{attrs}>{label}</a>'


def render_markdown(md, ctx):
    lines = md.split("\n")
    out, i = [], 0
    last, spins = -1, 0
    while i < len(lines):
        if i == last:                      # every branch must consume at least one line
            spins += 1
            if spins > 1:
                raise SystemExit(f"build: parser stuck at line {i + 1}: {lines[i]!r}")
        else:
            last, spins = i, 0
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # fenced code
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            body, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            cls = "shell" if lang in ("bash", "sh", "console", "shell") else (f"lang-{lang}" if lang else "")
            out.append(f'<pre class="{cls}">{html.escape(chr(10).join(body))}</pre>')
            continue

        # a block shortcode on a line of its own: {{app}}, {{ledger}}, {{comparison}}…
        if re.fullmatch(r"\{\{[a-z-]+\}\}", stripped):
            out.append(shortcodes_block(stripped, ctx))
            i += 1
            continue

        # raw html block (an <aside>, a stat-tile row, the app slot)
        if stripped.startswith("<") and not stripped.startswith("<http"):
            block = []
            while i < len(lines) and lines[i].strip():
                block.append(lines[i])
                i += 1
            out.append(shortcodes_block("\n".join(block), ctx))
            continue

        # heading
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            anchor = slugify(text)
            rendered = inline(text, ctx)
            if level >= 2:
                ctx["toc"].append((level, anchor, re.sub(r"<[^>]+>", "", rendered)))
            out.append(f'<h{level} id="{anchor}">{rendered}</h{level}>')
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r"(-{3,}|\*{3,})", stripped):
            out.append("<hr>")
            i += 1
            continue

        # table
        if "|" in stripped and i + 1 < len(lines) and re.fullmatch(r"\|?[\s:|-]+\|[\s:|-]*", lines[i + 1].strip()):
            head = _row(lines[i])
            aligns = [_align(c) for c in _row(lines[i + 1])]
            i += 2
            body = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                body.append(_row(lines[i]))
                i += 1
            th = "".join(f"<th{_style(a)}>{inline(c, ctx)}</th>" for c, a in zip(head, aligns + [None] * len(head)))
            trs = []
            for r in body:
                tds = "".join(f"<td{_style(a)}>{inline(c, ctx)}</td>" for c, a in zip(r, aligns + [None] * len(r)))
                trs.append(f"<tr>{tds}</tr>")
            out.append(
                '<div class="tablewrap"><table><thead><tr>' + th + "</tr></thead><tbody>" + "".join(trs) + "</tbody></table></div>"
            )
            continue

        # blockquote
        if stripped.startswith(">"):
            body = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                body.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + render_markdown("\n".join(body), ctx) + "</blockquote>")
            continue

        # lists
        if re.match(r"^\s*([-*]|\d+\.)\s+", line):
            block, base = [], len(line) - len(line.lstrip(" "))
            while i < len(lines) and (
                re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]) or (lines[i].strip() and (len(lines[i]) - len(lines[i].lstrip(" "))) > base)
            ):
                block.append(lines[i])
                i += 1
            out.append(_list(block, base, ctx))
            continue

        # paragraph
        para = [lines[i].strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not _breaks_paragraph(lines, i):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>" + inline(" ".join(para), ctx) + "</p>")
    return "\n".join(out)


def _breaks_paragraph(lines, i):
    """A paragraph ends at whatever starts another block. Note the space required
    after a bullet: `**bold at the start of a line**` is not a list item."""
    line = lines[i]
    if re.match(r"^\s*([-*]\s+|\d+\.\s+|#{1,6}\s|>|```)", line):
        return True
    if line.strip().startswith("<") and not line.strip().startswith("<http"):
        return True
    if "|" in line and i + 1 < len(lines) and re.fullmatch(r"\|?[\s:|-]+\|[\s:|-]*", lines[i + 1].strip()):
        return True
    return False


def _row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells, cur, esc = [], "", False
    for ch in line:
        if esc:
            cur, esc = cur + ch, False
        elif ch == "\\":
            esc = True
        elif ch == "|":
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
    cells.append(cur.strip())
    return cells


def _align(cell):
    cell = cell.strip()
    if cell.startswith(":") and cell.endswith(":"):
        return "center"
    if cell.endswith(":"):
        return "right"
    return None


def _style(a):
    return f' style="text-align:{a}"' if a else ""


def _list(block, base, ctx):
    ordered = bool(re.match(r"^\s*\d+\.\s+", block[0]))
    items, cur = [], None
    for line in block:
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        indent = len(line) - len(line.lstrip(" "))
        if m and indent == base:
            if cur is not None:
                items.append(cur)
            cur = [m.group(3)]
        elif cur is not None:
            cur.append(line[base:] if len(line) > base else line.strip())
    if cur is not None:
        items.append(cur)
    lis = []
    for item in items:
        first, rest = item[0], [x for x in item[1:] if x.strip()]
        body = inline(first, ctx)
        if rest:
            sub_base = min(len(x) - len(x.lstrip(" ")) for x in rest)
            body += render_markdown("\n".join(x[sub_base:] if len(x) > sub_base else x for x in rest), ctx)
        lis.append(f"<li>{body}</li>")
    tag = "ol" if ordered else "ul"
    return f"<{tag}>" + "".join(lis) + f"</{tag}>"


# ------------------------------------------------------------- shortcodes ----

STATES = {
    "verified": ("verified", "st-v", "Verified by execution on this date, by us."),
    "measured": ("measured", "st-m", "Measured by our own pipeline on a named workload and date."),
    "docs": ("vendor docs", "st-d", "Read from the vendor's documentation on this date. Never executed by us."),
    "spec": ("specified, not shipped", "st-s", "A specification. It does not exist yet."),
    "unrun": ("written, not run", "st-u", "Code we wrote and have never executed."),
    "projected": ("projected", "st-p", "Arithmetic, not an invoice. The workings are shown."),
}


def chip(state, date=None, claim_id=None, label=None):
    text, cls, why = STATES.get(state, ("unknown", "st-u", ""))
    body = label or text
    if date:
        body += f" {date}"
    title = html.escape(why)
    if claim_id:
        return f'<a class="chip {cls}" href="/ledger/#claim-{claim_id}" title="{title}">{html.escape(body)}</a>'
    return f'<span class="chip {cls}" title="{title}">{html.escape(body)}</span>'


def shortcodes_inline(text, ctx):
    def claim_ref(m):
        cid = m.group(1)
        c = ctx["claims_by_id"].get(cid)
        if not c:
            raise SystemExit(f"build: unknown claim id {cid!r} referenced by {ctx['page']}")
        ctx["claim_uses"].setdefault(cid, set()).add(ctx["page"])
        return chip(c["state"], c.get("date_label"), cid)

    text = re.sub(r"\{\{claim:([a-z0-9-]+)\}\}", claim_ref, text)
    text = re.sub(
        r"\{\{badge:([a-z]+)(?:\|([^}]+))?\}\}",
        lambda m: chip(m.group(1), m.group(2)),
        text,
    )
    return text


def shortcodes_block(block, ctx):
    m = re.fullmatch(r"\s*\{\{([a-z-]+)\}\}\s*", block)
    if not m:
        # a hand-written HTML block: inline shortcodes still expand inside it, so a
        # claim chip can sit in a stat tile without going through the escaper.
        return shortcodes_inline(block, ctx)
    name = m.group(1)
    fn = BLOCKS.get(name)
    if not fn:
        raise SystemExit(f"build: unknown block shortcode {{{{{name}}}}} on {ctx['page']}")
    return fn(ctx)


# ------------------------------------------------------- generated blocks ----

PATTERN_NAMES = {
    "0": "0 &middot; key in the page",
    "1": "1 &middot; bounded key in the page",
    "2": "2 &middot; short-lived token",
    "3": "3 &middot; host holds the key",
}
VERDICT_MARK = {
    "yes": ('<span class="v v-yes">&check;</span>', "available"),
    "no": ('<span class="v v-no">&times;</span>', "unavailable"),
    "never": ('<span class="v v-never">&#9888;</span>', "available and never acceptable"),
    "spec": ('<span class="v v-spec">&#9686;</span>', "specified here, not shipped"),
    "na": ('<span class="v v-na">&mdash;</span>', "not applicable"),
}


def block_comparison(ctx):
    rows = []
    for page in ctx["pages"]:
        fm = page["fm"]
        if not fm.get("patterns"):
            continue
        for entry in fm["patterns"]:
            cells = []
            for p in ("0", "1", "2", "3"):
                v = entry.get(f"p{p}") or {}
                verdict = v.get("verdict", "na")
                verdict = {True: "yes", False: "no"}.get(verdict, str(verdict).lower())
                if verdict not in VERDICT_MARK:
                    raise SystemExit(f"build: unknown pattern verdict {verdict!r} on {page['path']}")
                mark, meaning = VERDICT_MARK[verdict]
                note = html.escape(str(v.get("note", "")))
                cells.append(f'<td title="{meaning}">{mark}<span class="vnote">{note}</span></td>')
            rows.append(
                f'<tr><th scope="row"><a href="{page["url"]}">{html.escape(entry.get("provider", fm["title"]))}</a></th>'
                f'<td>{html.escape(str(entry.get("product", "")))}</td>'
                + "".join(cells)
                + f'<td>{html.escape(str(entry.get("server", "")))}</td></tr>'
            )
    head = "".join(f"<th>{n}</th>" for n in PATTERN_NAMES.values())
    legend = " &middot; ".join(f"{VERDICT_MARK[k][0]} {v}" for k, v in [(k, VERDICT_MARK[k][1]) for k in VERDICT_MARK])
    return (
        '<div class="tablewrap"><table class="cmp"><thead><tr><th>Provider</th><th>Product</th>'
        + head
        + "<th>Needs a server for the safe pattern</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
        + f'<p class="small dim legend">{legend}</p>'
        + '<p class="small dim">Generated at build time from the <code>patterns:</code> front-matter of every provider page. '
        "Adding a provider is one Markdown file; this table follows.</p>"
    )


def block_grants(ctx):
    fm = ctx["fm"]
    grants = fm.get("grants") or []
    rows = []
    for g in grants:
        rows.append(
            "<tr><td><code>{v}</code></td><td><code>{o}</code></td><td><code>{r}</code></td>"
            "<td>{rev}</td><td>{b}</td></tr>".format(
                v=html.escape(str(g.get("verb", ""))),
                o=html.escape(str(g.get("object", ""))),
                r=html.escape(str(g.get("reach", ""))),
                rev="reversible" if g.get("reversible") else "<b>irreversible</b>",
                b=html.escape(str(g.get("bounded_by", g.get("note", "")))),
            )
        )
    not_granted = fm.get("not_granted") or []
    ng = ", ".join(f"<code>{html.escape(str(x))}</code>" for x in not_granted)
    return (
        '<div class="tablewrap"><table class="grants"><thead><tr><th>verb</th><th>object class</th><th>reach</th>'
        "<th>reversibility</th><th>bounded by</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
        + (f'<p class="small"><b>Not granted</b> by a key scoped this way, and it should stay that way: {ng}.</p>' if ng else "")
        + '<p class="small dim">The same rows are emitted as front-matter in this page&rsquo;s '
        f'<a href="{ctx["page_url"]}index.md">markdown source</a>, so a capability index can join across '
        "providers without parsing English.</p>"
    )


def short_label(url):
    """A ledger row lists several pages; their full titles would each be a
    paragraph. The last path segment is what a reader recognises."""
    parts = [p for p in url.strip("/").split("/") if p]
    return html.escape(parts[-1] if parts else "the report")


def block_ledger(ctx):
    groups = {}
    for c in ctx["claims"]:
        groups.setdefault(c.get("group", "Other"), []).append(c)
    out = []
    for group, items in groups.items():
        out.append(f'<h3 id="{slugify(group)}">{html.escape(group)}</h3>')
        rows = []
        for c in items:
            used = sorted(ctx["claim_uses"].get(c["id"], set()), key=lambda u: ctx["page_urls"][u])
            links = ", ".join(
                f'<a href="{ctx["page_urls"][u]}" title="{html.escape(ctx["page_titles"][u])}">{short_label(ctx["page_urls"][u])}</a>'
                for u in used
            ) or '<span class="dim">&mdash;</span>'
            rows.append(
                f'<tr id="claim-{c["id"]}"><td>{inline(c["claim"], ctx)}</td>'
                f'<td>{chip(c["state"], c.get("date_label"))}</td>'
                f'<td class="small">{html.escape(str(c.get("source", "")))}</td>'
                f'<td class="small">{links}</td></tr>'
            )
        out.append(
            '<div class="tablewrap"><table class="ledger"><thead><tr><th>Claim</th><th>State</th>'
            "<th>How we know</th><th>Where it is said</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
        )
    counts = {}
    for c in ctx["claims"]:
        counts[c["state"]] = counts.get(c["state"], 0) + 1
    tiles = "".join(
        f'<div class="tile"><b>{counts.get(k, 0)}</b><span>{STATES[k][0]}</span></div>' for k in STATES if counts.get(k)
    )
    return f'<div class="tiles tiles-sm">{tiles}</div>' + "\n".join(out)


def block_experiments(ctx):
    cards = []
    for page in ctx["pages"]:
        fm = page["fm"]
        if fm.get("kind") != "experiment":
            continue
        chips = "".join(chip(s) for s in (fm.get("state_chips") or []))
        cards.append(
            f'<a class="card" href="{page["url"]}"><span class="tag">{html.escape(str(fm.get("family", "experiment")))}</span>'
            f'<h3>{html.escape(fm["title"])}</h3><p>{html.escape(str(fm.get("description", "")))}</p>'
            f'<p class="small">{html.escape(str(fm.get("endpoints", "")))}</p>'
            f'<div class="chips">{chips}</div><span class="go">Open the lab &rarr;</span></a>'
        )
    return '<div class="cards cards-tight">' + "".join(cards) + "</div>"


def block_examples(ctx):
    rows = []
    for f in sorted((FILES / "examples").iterdir()):
        first = ""
        for line in f.read_text().split("\n"):
            if line.startswith("#") and not line.startswith("#!"):
                first = line.lstrip("# ").strip()
                break
            if line.startswith("//"):
                first = line.lstrip("/ ").strip()
                break
        rows.append(
            f'<tr><td><a href="/files/examples/{f.name}" download><code>{f.name}</code></a></td>'
            f'<td class="small">{html.escape(first)}</td><td>{chip("unrun")}</td></tr>'
        )
    return (
        '<div class="tablewrap"><table><thead><tr><th>File</th><th>What it does</th><th>State</th></tr></thead>'
        "<tbody>" + "".join(rows) + "</tbody></table></div>"
    )


def block_app(ctx):
    name = ctx["fm"].get("app")
    if not name:
        raise SystemExit(f"build: {{{{app}}}} on {ctx['page']} with no `app:` in front-matter")
    return (APPS / f"{name}.html").read_text()


def block_lab_header(ctx):
    """The pattern box and the key bar: identical on every lab, so it is one file."""
    return (APPS / "_labheader.html").read_text()


BLOCKS = {
    "comparison": block_comparison,
    "ledger": block_ledger,
    "experiments": block_experiments,
    "examples": block_examples,
    "app": block_app,
    "grants": block_grants,
    "lab-header": block_lab_header,
}


# ------------------------------------------------------------------ shell ----


def nav_html(current):
    items = []
    for label, href in NAV:
        cls = "nl here" if href == current else "nl"
        items.append(f'<div class="ni"><a class="{cls}" href="{href}">{html.escape(label)}</a></div>')
    return (
        '<nav class="site"><div class="row">'
        '<a class="brand" href="/">elevenlabs<span>.providers.sgit.ai</span></a>'
        '<span class="stage-pill">v1</span>'
        '<button class="nav-toggle" type="button" aria-expanded="false" aria-label="Menu">Menu</button>'
        '<div class="nav-items">' + "".join(items) + "</div>"
        '<a class="gh" href="https://github.com/SGit-AI/SGit-AI__Website__Provider__ElevenLabs" rel="noopener">&#9733; Source</a>'
        "</div></nav>"
    )


def footer_html():
    return f"""<footer class="site"><div class="cols">
  <div>
    <div class="brandline">elevenlabs<span>.providers.sgit.ai</span></div>
    <p class="nonaff"><b>{NON_AFFILIATION}</b></p>
    <p>A report on what one paid API cost us, what broke, and which credential patterns it can actually support.
       Part of the <code>*.providers.sgit.ai</code> family. Source material: the video vault at commit
       <code>{SITE['vault_commit']}</code>, 7 September 2026.</p>
    <p class="verline">site {SITE['version']} &middot; <a href="/ledger/">the ledger</a> &middot; <a href="/disclosures/">disclosures</a> &middot; <a href="index.md" title="The same page as plain markdown">this page as markdown</a></p>
  </div>
  <div>
    <h4>The report</h4>
    <a href="/">ElevenLabs, nine sections</a>
    <a href="/#8-what-it-cost">&sect;8 What it cost</a>
    <a href="/#9-what-went-wrong">&sect;9 What went wrong</a>
    <a href="/examples/">Example files</a>
    <a href="/providers/openrouter/">OpenRouter (structural stub)</a>
  </div>
  <div>
    <h4>Experiments</h4>
    <a href="/experiments/">All experiments</a>
    <a href="/bench/">The test bench</a>
    <a href="/experiments/captions/">Captions studio</a>
    <a href="/experiments/concurrency/">Concurrency probe</a>
    <a href="/experiments/cost/">Cost model (no key)</a>
  </div>
  <div>
    <h4>The argument</h4>
    <a href="/patterns/">The four patterns</a>
    <a href="/comparison/">Comparison matrix</a>
    <a href="/pattern-three/">Pattern three: sg.tts</a>
    <a href="/ledger/">Claim ledger</a>
    <a href="/disclosures/">Disclosures</a>
  </div>
</div>
<div class="footnote"><p>No analytics. No cookies. No third-party fonts, scripts or CDN &mdash; every byte of this site
is served from this domain. The only network call any page here makes is the one <em>you</em> start, from a lab,
to <code>api.elevenlabs.io</code>.</p></div>
</footer>"""


def page_html(page, ctx, body):
    fm = page["fm"]
    desc = fm.get("description", "")
    prov = fm.get("provenance", {}) or {}
    toc = ""
    if fm.get("toc") and len(ctx["toc"]) > 2:
        links = "".join(
            f'<a class="lv{lv}" href="#{anchor}">{html.escape(text)}</a>' for lv, anchor, text in ctx["toc"] if lv == 2
        )
        toc = f'<aside class="toc"><b>On this page</b>{links}</aside>'
    provline = ""
    if prov:
        provline = (
            f'<p class="prov">Prose from the video vault at commit <code>{html.escape(str(prov.get("commit", SITE["vault_commit"])))}</code>, '
            f'{html.escape(str(prov.get("date", "")))}. '
            f'{html.escape(str(prov.get("note", "")))} '
            f'When the vault moves ahead, this page is behind &mdash; and says so rather than guessing.</p>'
        )
    lab = ' data-lab="1"' if fm.get("kind") == "experiment" or fm.get("app") else ""
    # lab.js is NOT deferred: each lab's own inline <script> runs during parse and
    # needs window.EL to exist by then. It is 12 KB, same-origin, and uncached only once.
    scripts = '<script src="/assets/lab.js"></script>' if lab else '<script src="/assets/site.js" defer></script>'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(fm['title'])} &mdash; {html.escape(SITE['title'])}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{SITE['base']}{page['url']}">
<link rel="alternate" type="text/markdown" href="index.md" title="This page as markdown">
<link rel="stylesheet" href="/assets/site.css">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{scripts}
</head>
<body{lab}>
{nav_html(page['nav_match'])}
<main class="doc{' doc-wide' if fm.get('wide') else ''}">
<p class="crumb"><a href="/">elevenlabs.providers.sgit.ai</a>{page['crumb']}</p>
<h1>{html.escape(fm['title'])}</h1>
{f'<p class="lead">{inline(fm["lead"], ctx)}</p>' if fm.get('lead') else ''}
{provline}
{toc}
{body}
<p class="pagenav"><a href="/ledger/">Every claim on this site, with its state &rarr;</a>
<a href="/disclosures/">Disclosures &rarr;</a></p>
</main>
{footer_html()}
</body>
</html>
"""


# ------------------------------------------------------------------ build ----


def read_page(path):
    text = path.read_text()
    if not text.startswith("---"):
        raise SystemExit(f"build: {path} has no front-matter")
    _, fm_text, body = text.split("---", 2)
    fm = yaml_load(fm_text)
    rel = path.relative_to(CONTENT)
    slug = str(rel.with_suffix("")).replace("index", "").strip("/")
    url = "/" + (slug + "/" if slug else "")
    return {"path": path, "fm": fm, "body": body.lstrip("\n"), "url": url, "src_md": text}


def build(out_dir):
    out_dir = Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    claims = yaml_load((DATA / "claims.yml").read_text())
    for c in claims:
        c["date_label"] = c.get("date", "")
    claims_by_id = {c["id"]: c for c in claims}

    pages = sorted((read_page(p) for p in CONTENT.rglob("*.md")), key=lambda p: (p["fm"].get("order", 500), p["url"]))
    page_urls = {p["path"].name: p["url"] for p in pages}
    page_urls = {str(p["path"]): p["url"] for p in pages}
    page_titles = {str(p["path"]): p["fm"]["title"] for p in pages}

    ctx_shared = {
        "claims": claims,
        "claims_by_id": claims_by_id,
        "claim_uses": {},
        "pages": pages,
        "page_urls": page_urls,
        "page_titles": page_titles,
        "external_links": set(),
    }

    # two passes: the first collects claim usage so the ledger can join on it.
    for _ in range(2):
        rendered = {}
        for page in pages:
            fm = page["fm"]
            crumbs = ""
            if page["url"] != "/":
                parts = [x for x in page["url"].strip("/").split("/") if x]
                parent = "/" + parts[0] + "/"
                if len(parts) > 1 and any(q["url"] == parent for q in pages):
                    crumbs = ' / <a href="' + parent + '">' + parts[0] + "</a>"
                elif len(parts) > 1:
                    crumbs = " / " + parts[0]
                crumbs += f" / {html.escape(fm['title'])}"
            page["crumb"] = crumbs
            page["nav_match"] = "/" + (page["url"].strip("/").split("/")[0] + "/" if page["url"] != "/" else "")
            ctx = dict(ctx_shared)
            ctx.update({"page": str(page["path"]), "page_url": page["url"], "fm": fm, "toc": []})
            body = render_markdown(page["body"], ctx)
            rendered[page["url"]] = (page, ctx, body)

    for url, (page, ctx, body) in rendered.items():
        target = out_dir / url.strip("/") / "index.html" if url != "/" else out_dir / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page_html(page, ctx, body))
        (target.parent / "index.md").write_text(page["src_md"])

    # static assets, verbatim
    shutil.copytree(ASSETS, out_dir / "assets")
    shutil.copytree(FILES, out_dir / "files")
    (out_dir / "CNAME").write_text(SITE["domain"] + "\n")
    (out_dir / ".nojekyll").write_text("")
    (out_dir / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['base']}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE['base']}{u}</loc></url>" for u in sorted(rendered))
    (out_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>\n"
    )
    (out_dir / "llms.txt").write_text(llms_txt(rendered))
    print(f"build: {len(rendered)} pages, {len(claims)} claims → {out_dir}")
    unused = [c["id"] for c in claims if c["id"] not in ctx_shared["claim_uses"]]
    if unused:
        print("build: claims in the ledger that no page cites: " + ", ".join(unused))
    return rendered


def llms_txt(rendered):
    lines = [
        f"# {SITE['domain']}",
        "",
        "> An independent report on the ElevenLabs API: what it cost on a named workload on a named date,",
        "> what broke, and which of four client-side credential patterns the product can actually support.",
        "> Not affiliated with, endorsed by, or sponsored by ElevenLabs.",
        "",
        "Every factual claim on this site carries one of six states: verified, measured, vendor docs,",
        "specified-not-shipped, written-not-run, projected. The full list is at /ledger/.",
        "Every page is also served as markdown at <page>/index.md.",
        "",
        "## Pages",
    ]
    for url, (page, _ctx, _body) in sorted(rendered.items()):
        lines.append(f"- [{page['fm']['title']}]({SITE['base']}{url}): {page['fm'].get('description', '')}")
    return "\n".join(lines) + "\n"


def main():
    if "--check" in sys.argv:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "docs"
            build(target)
            diff = dircmp_report(target, OUT)
            if diff:
                print("build --check: docs/ is stale. Run `python3 build.py` and commit.", file=sys.stderr)
                for d in diff[:40]:
                    print("  " + d, file=sys.stderr)
                sys.exit(1)
            print("build --check: docs/ matches the sources.")
        return
    build(OUT)


def dircmp_report(a, b, prefix=""):
    out = []
    cmp = filecmp.dircmp(str(a), str(b))
    out += [f"only in build: {prefix}{x}" for x in cmp.left_only]
    out += [f"only in docs/: {prefix}{x}" for x in cmp.right_only]
    out += [f"differs: {prefix}{x}" for x in cmp.diff_files]
    for sub in cmp.common_dirs:
        out += dircmp_report(Path(a) / sub, Path(b) / sub, prefix + sub + "/")
    return out


if __name__ == "__main__":
    main()
