#!/usr/bin/env python3
"""
Vault health report — deterministic, no LLM.

Scans the Obsidian vault and reports knowledge-decay signals:
  - broken wikilinks        [[X]] where X resolves to no note
  - orphan notes            no inbound and no outbound links
  - stale notes             last git commit older than STALE_DAYS
  - missing frontmatter     content notes lacking the schema keys
  - invalid frontmatter     enum values outside the schema
  - MOC coverage gaps       01-Knowledge notes no MOC links to

Plus a quality pass over 01-Knowledge/ content notes:
  - per-note score          completeness / connectedness / freshness / confidence
  - review-next queue       lowest-scoring notes, with the weakest dimension
  - promotion candidates    status lags what the score suggests
  - decayed notes           curated/evergreen notes that now score low
  - possible duplicates     near-identical titles or heavy content overlap

Writes Markdown to 90-System/Health Report.md, appends a row to
.repo-metadata/quality_history.csv, and prints a summary.

Run:    python .repo-metadata/health_report.py [--days 365] [--review N] [--quiet]
Gate:   add --check to exit 1 when broken/missing_fm/invalid_fm/collisions > 0
        (used by .githooks/pre-commit)
"""
from __future__ import annotations
import os, re, sys, subprocess, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "90-System", "Health Report.md")
HISTORY = os.path.join(ROOT, ".repo-metadata", "quality_history.csv")
EXCLUDE_DIRS = {".git", ".obsidian", ".repo-metadata", "Attachments", "99 Personal"}
STALE_DAYS = 365
REVIEW_N = 12
# --check exits non-zero when any of these are non-empty (hard schema/link violations).
# collisions, orphans, stale, dupes, moc_gap are reported but never block a commit.
BLOCKING = ("broken", "missing_fm", "invalid_fm")

DOMAIN = {"data-engineering","software-engineering","ai","career","cloud","database",
          "python","pkm","architecture","prompt","tool"}
NOTE_TYPE = {"concept","technology","project","adr","tutorial","interview","architecture",
             "glossary","snippet","template","prompt","moc"}
SOURCE_TYPE = {"web","book","github","obsidian","paper","video","course","self"}
STATUS = {"inbox","draft","reference","curated","evergreen"}
LEVEL = {"beginner","intermediate","advanced"}
STUB_TYPES = {"daily","idea","personal","log"}

WL = re.compile(r"(?<!!)\[\[([^\[\]]+?)\]\]")          # [[target]] / [[target|alias]] / [[t#h]]
FENCE = re.compile(r"```.*?```", re.S)                  # fenced code block
INLINE_CODE = re.compile(r"`[^`\n]+`")                 # inline `code` span
HEADING = re.compile(r"^#{2,}\s+\S", re.M)
AISUMMARY = re.compile(r"^#+\s*AI Summary\s*$", re.M | re.I)
WORD = re.compile(r"[A-Za-z0-9]+")
LINK_SCOPE = "01-Knowledge/"                            # only this layer is expected to be linked
SCORE_SCOPE = "01-Knowledge/"                           # quality scoring is scoped here

# status -> confidence proxy (schema has no explicit confidence field)
CONFIDENCE = {"inbox": 0.10, "draft": 0.30, "reference": 0.60, "curated": 0.80, "evergreen": 1.00}
WEIGHTS = {"completeness": 0.30, "connectedness": 0.30, "freshness": 0.20, "confidence": 0.20}
DIM_LABEL = {"completeness": "thin", "connectedness": "isolated",
             "freshness": "stale", "confidence": "immature"}
STOP = set("the a an of to and or in on for is are be was were with as by from this that it its "
           "into vs via not no if then than at over under about above can could should would".split())


def rel(p): return os.path.relpath(p, ROOT).replace("\\", "/")


def md_files():
    for dp, dn, fns in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in EXCLUDE_DIRS]
        for fn in fns:
            if fn.endswith(".md"):
                yield os.path.join(dp, fn)


def parse_frontmatter(text):
    lines = text.replace("\r\n", "\n").split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    d = {}
    for l in lines[1:]:
        if l.strip() == "---":
            return d
        m = re.match(r"^([\w-]+):\s*(.*)$", l)
        if m:
            d[m.group(1)] = m.group(2).strip()
    return None  # no closing fence


def strip_body(text):
    """Text with frontmatter and code removed — for word counts and shingles."""
    t = text.replace("\r\n", "\n")
    if t.startswith("---\n"):
        end = t.find("\n---", 3)
        if end != -1:
            t = t[end + 4:]
    t = FENCE.sub(" ", t)
    t = INLINE_CODE.sub(" ", t)
    return t


def link_targets(text):
    body = INLINE_CODE.sub("", FENCE.sub("", text))
    out = []
    for m in WL.finditer(body):
        inner = m.group(1).split("|")[0].split("#")[0].strip()
        if inner:
            out.append(inner.split("/")[-1])   # tolerate [[folder/Name]]
    return out


def git_last_date(path):
    try:
        r = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%cs", "--", path],
                           capture_output=True, text=True, timeout=15)
        s = r.stdout.strip()
        return datetime.date.fromisoformat(s) if s else None
    except Exception:
        return None


def title_tokens(base):
    b = re.sub(r"\s+\d+$", "", base)          # "DuckDB 1" -> "DuckDB"
    return {w.lower() for w in WORD.findall(b)
            if len(w) > 2 and w.lower() not in STOP}


def top_terms(body, k=40):
    ws = [w.lower() for w in WORD.findall(body)
          if len(w) > 3 and w.lower() not in STOP]
    return {w for w, _ in collections.Counter(ws).most_common(k)}


NUMBERED = re.compile(r"^(.+?)\s+\d+$")


def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return inter / (len(a) + len(b) - inter)


def completeness_score(text, wc, out_resolved):
    s = 0.0
    if AISUMMARY.search(text):
        s += 0.15
    # body length: nothing under 150w, full credit at ~800w
    if wc > 150:
        s += 0.45 * min(1.0, (wc - 150) / (800 - 150))
    heads = len(HEADING.findall(text))
    s += 0.20 if heads >= 4 else (0.12 if heads >= 2 else (0.05 if heads == 1 else 0.0))
    s += 0.20 if out_resolved >= 3 else (0.10 if out_resolved >= 1 else 0.0)
    return min(1.0, s)


def freshness_score(gd, today):
    if gd is None:
        return 0.5
    age = (today - gd).days
    if age <= 90:
        return 1.0
    return max(0.0, 1.0 - (age - 90) / max(1, STALE_DAYS - 90))


def main():
    global STALE_DAYS, REVIEW_N
    if "--days" in sys.argv:
        STALE_DAYS = int(sys.argv[sys.argv.index("--days") + 1])
    if "--review" in sys.argv:
        REVIEW_N = int(sys.argv[sys.argv.index("--review") + 1])
    quiet = "--quiet" in sys.argv
    check = "--check" in sys.argv
    today = datetime.date.today()

    notes = {}                       # basename -> relpath  (last wins; collisions flagged)
    collisions = collections.defaultdict(list)
    data = {}                        # relpath -> dict(fm, out, base, text, body, wc)
    for p in md_files():
        r = rel(p)
        base = os.path.basename(p)[:-3]
        if base in notes:
            collisions[base].append(r)
            if len(collisions[base]) == 1:
                collisions[base].insert(0, notes[base])
        notes[base] = r
        text = open(p, encoding="utf-8").read()
        body = strip_body(text)
        data[r] = {"fm": parse_frontmatter(text), "out": link_targets(text),
                   "base": base, "text": text, "body": body,
                   "wc": len(WORD.findall(body))}

    valid = set(notes)
    inbound = collections.Counter()
    out_resolved = collections.Counter()   # relpath -> count of resolving outbound links
    broken = []                             # (relpath, target)
    for r, info in data.items():
        for tgt in info["out"]:
            if tgt in valid:
                inbound[tgt] += 1
                out_resolved[r] += 1
            else:
                broken.append((r, tgt))

    gitdate = {}
    def gd(r):
        if r not in gitdate:
            gitdate[r] = git_last_date(r)
        return gitdate[r]

    # classify notes
    orphans, missing_fm, invalid_fm, stale = [], [], [], []
    knowledge_notes, moc_referenced, moc_domains = set(), set(), set()
    for r, info in data.items():
        if r.startswith("01-Knowledge/"):
            knowledge_notes.add(r)
            if (info["fm"] or {}).get("note_type") == "moc":
                moc_domains.add(os.path.dirname(r))
                for tgt in info["out"]:
                    if tgt in valid:
                        moc_referenced.add(notes[tgt])

    for r, info in data.items():
        fm = info["fm"]
        ntype = (fm or {}).get("note_type", "")
        is_stub = ntype in STUB_TYPES or r.startswith(("00-Daily/", "04-Writing/Ideas/"))
        has_out = bool(info["out"])
        has_in = inbound[info["base"]] > 0

        if r.startswith(LINK_SCOPE) and ntype != "moc" and not has_out and not has_in:
            orphans.append(r)

        if not is_stub and not r.startswith("90-System/"):
            if fm is None:
                missing_fm.append(r)
            elif ntype != "moc":
                errs = []
                for k, allowed in (("domain", DOMAIN), ("note_type", NOTE_TYPE),
                                   ("source_type", SOURCE_TYPE), ("status", STATUS),
                                   ("level", LEVEL)):
                    if fm.get(k) not in allowed:
                        errs.append(f"{k}={fm.get(k)!r}")
                if errs:
                    invalid_fm.append((r, ", ".join(errs)))

        if not r.startswith(("00-Daily/", "04-Writing/Ideas/")):
            d = gd(r)
            if d and (today - d).days > STALE_DAYS:
                stale.append((r, d.isoformat(), (today - d).days))

    moc_gap = sorted(
        r for r in knowledge_notes
        if os.path.dirname(r) in moc_domains
        and r not in moc_referenced
        and (data[r]["fm"] or {}).get("note_type") != "moc")

    # ---- quality scoring (01-Knowledge content notes, MOCs excluded) ----
    scores = []   # dict per note
    for r in sorted(knowledge_notes):
        info = data[r]
        fm = info["fm"] or {}
        if fm.get("note_type") == "moc":
            continue
        status = fm.get("status", "draft")
        dims = {
            "completeness": completeness_score(info["text"], info["wc"], out_resolved[r]),
            "connectedness": min(1.0, (out_resolved[r] + inbound[info["base"]]) / 8.0),
            "freshness": freshness_score(gd(r), today),
            "confidence": CONFIDENCE.get(status, 0.30),
        }
        overall = sum(WEIGHTS[k] * v for k, v in dims.items())
        weakest = min(("completeness", "connectedness", "freshness", "confidence"),
                      key=lambda k: dims[k])
        scores.append({"r": r, "base": info["base"], "status": status,
                       "pct": round(overall * 100), "dims": dims, "weakest": weakest,
                       "deg": out_resolved[r] + inbound[info["base"]], "wc": info["wc"]})

    mean_pct = round(sum(s["pct"] for s in scores) / len(scores)) if scores else 0
    below = [s for s in scores if s["pct"] < 50]
    promote = [s for s in scores
               if s["status"] in ("draft", "reference") and s["pct"] >= 75]
    decayed = [s for s in scores
               if s["status"] in ("curated", "evergreen") and s["pct"] < 60]
    review = sorted(scores, key=lambda s: s["pct"])[:REVIEW_N]

    # ---- possible duplicates (non-stub notes with frontmatter) ----
    cand = []
    for r, info in data.items():
        fm = info["fm"]
        if fm is None or fm.get("note_type") in (STUB_TYPES | {"moc"}):
            continue
        if fm.get("subdomain") == "index":       # index / catalog notes are templated by design
            continue
        if r.startswith(("00-Daily/", "04-Writing/Ideas/", "99 Personal/")):
            continue
        cand.append((r, info["base"], fm.get("domain", ""), fm.get("note_type", ""),
                     title_tokens(info["base"]), top_terms(info["body"])))

    dupes = []
    for i in range(len(cand)):
        r1, b1, d1, n1, t1, k1 = cand[i]
        for j in range(i + 1, len(cand)):
            r2, b2, d2, n2, t2, k2 = cand[j]
            tj = jaccard(t1, t2)
            kj = jaccard(k1, k2)
            m1 = NUMBERED.match(b1)
            m2 = NUMBERED.match(b2)
            numbered = (m1 and m1.group(1) == b2) or (m2 and m2.group(1) == b1)
            near_title = tj >= 0.75 and len(t1 & t2) >= 2
            near_body = kj >= 0.55 and d1 == d2 and n1 == n2
            if numbered or near_title or near_body:
                kind = "numbered" if numbered else ("title" if near_title else "content")
                dupes.append((1.0 if numbered else max(tj, kj), kind, r1, r2, tj, kj))
    dupes.sort(reverse=True)

    # ---- write report ----
    ts = today.isoformat()
    L = []
    L.append("---\nnote_type: glossary\nstatus: reference\n---")
    L.append(f"# Vault Health Report\n\nGenerated {ts} · stale threshold {STALE_DAYS} days · "
             f"{len(data)} notes scanned\n")
    L.append(f"Link checks (orphans, MOC coverage) and quality scoring are scoped to "
             f"`{LINK_SCOPE}` — the layer meant to be connected and curated. Broken links, "
             f"stale, frontmatter, and duplicates are checked vault-wide.\n")

    L.append("## Summary\n")
    L.append("| check | count |\n|---|---|")
    L.append(f"| broken wikilinks | {len(broken)} |")
    L.append(f"| orphan notes (in {LINK_SCOPE}) | {len(orphans)} |")
    L.append(f"| stale notes (>{STALE_DAYS}d) | {len(stale)} |")
    L.append(f"| missing frontmatter | {len(missing_fm)} |")
    L.append(f"| invalid frontmatter | {len(invalid_fm)} |")
    L.append(f"| MOC coverage gaps | {len(moc_gap)} |")
    L.append(f"| basename collisions | {len(collisions)} |")
    L.append(f"| possible duplicates | {len(dupes)} |")

    L.append("\n## Quality (01-Knowledge content notes)\n")
    L.append("| metric | value |\n|---|---|")
    L.append(f"| notes scored | {len(scores)} |")
    L.append(f"| mean score | {mean_pct}/100 |")
    L.append(f"| below 50 | {len(below)} |")
    L.append(f"| promotion candidates | {len(promote)} |")
    L.append(f"| decayed (curated/evergreen scoring <60) | {len(decayed)} |")
    L.append("\nScore = 0.30·completeness + 0.30·connectedness + 0.20·freshness + 0.20·confidence. "
             "Confidence is derived from `status`. Deterministic heuristic, not a substitute for reading the note.")

    def section(title, rows):
        L.append(f"\n## {title}\n")
        L.append("\n".join(rows) if rows else "_none_")

    section("Broken wikilinks", [f"- `{t}` <- {r}" for r, t in sorted(broken)])
    section(f"Orphan notes in {LINK_SCOPE} (no links in or out)",
            [f"- {r}" for r in sorted(orphans)])
    section("Stale notes", [f"- {r} — last commit {d} ({n}d ago)"
                            for r, d, n in sorted(stale, key=lambda x: -x[2])])
    section("Missing frontmatter", [f"- {r}" for r in sorted(missing_fm)])
    section("Invalid frontmatter", [f"- {r} — {e}" for r, e in sorted(invalid_fm)])
    section("MOC coverage gaps (01-Knowledge notes no MOC links to)",
            [f"- {r}" for r in moc_gap])
    section("Basename collisions (ambiguous wikilink targets)",
            [f"- `{b}` -> " + ", ".join(paths) for b, paths in sorted(collisions.items())])

    section(f"Review next (lowest {REVIEW_N} by score)",
            [f"- **{s['pct']}/100** · {s['weakest']} ({DIM_LABEL[s['weakest']]}) · "
             f"`{s['status']}` · {s['deg']} links · {s['wc']}w — {s['r']}"
             for s in review])
    section("Promotion candidates (status lags score)",
            [f"- **{s['pct']}/100** · `{s['status']}` — {s['r']}"
             for s in sorted(promote, key=lambda s: -s["pct"])])
    section("Decayed notes (curated/evergreen now scoring <60)",
            [f"- **{s['pct']}/100** · `{s['status']}` · weakest: {s['weakest']} — {s['r']}"
             for s in sorted(decayed, key=lambda s: s["pct"])])

    L.append("\n## Knowledge quality scores\n")
    L.append("| score | cmpl | conn | frsh | conf | status | note |")
    L.append("|--:|--:|--:|--:|--:|---|---|")
    for s in sorted(scores, key=lambda s: (-s["pct"], s["r"])):
        d = s["dims"]
        L.append(f"| {s['pct']} | {d['completeness']:.2f} | {d['connectedness']:.2f} | "
                 f"{d['freshness']:.2f} | {d['confidence']:.2f} | {s['status']} | "
                 f"{s['r'].split('/', 1)[1]} |")

    section("Possible duplicates",
            [f"- {kind} overlap (title {tj:.2f} / content {cj:.2f}) — `{r1}`  ↔  `{r2}`"
             for _, kind, r1, r2, tj, cj in dupes])

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="").write("\n".join(L) + "\n")

    counts = {"broken": len(broken), "orphans": len(orphans), "stale": len(stale),
              "missing_fm": len(missing_fm), "invalid_fm": len(invalid_fm),
              "moc_gap": len(moc_gap), "collisions": len(collisions), "dupes": len(dupes)}

    # append a row only when the metrics changed since last run, so drift stays legible
    hdr = ("date,notes_scanned,scored,mean_pct,below50,promote,decayed,"
           "broken,orphans,stale,missing_fm,invalid_fm,moc_gap,collisions,dupes")
    row = (f"{len(data)},{len(scores)},{mean_pct},{len(below)},{len(promote)},{len(decayed)},"
           f"{counts['broken']},{counts['orphans']},{counts['stale']},{counts['missing_fm']},"
           f"{counts['invalid_fm']},{counts['moc_gap']},{counts['collisions']},{counts['dupes']}")
    hist_lines = []
    if os.path.exists(HISTORY):
        with open(HISTORY, encoding="utf-8") as fh:
            hist_lines = fh.read().splitlines()
    prev = hist_lines[-1].split(",", 1)[1] if len(hist_lines) > 1 else None
    if row != prev:
        with open(HISTORY, "a", encoding="utf-8", newline="") as fh:
            if not hist_lines:
                fh.write(hdr + "\n")
            fh.write(f"{ts},{row}\n")

    if not quiet:
        print(" ".join(f"{k}={v}" for k, v in counts.items()))
        print(f"scored={len(scores)} mean={mean_pct}/100 below50={len(below)} "
              f"promote={len(promote)} decayed={len(decayed)}")
        print(f"report -> {rel(OUT)}")

    if check:
        failed = {k: counts[k] for k in BLOCKING if counts[k]}
        if failed:
            print("FAIL (--check): " + ", ".join(f"{k}={v}" for k, v in failed.items()),
                  file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
