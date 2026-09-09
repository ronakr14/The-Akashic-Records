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

Writes Markdown to 90-System/Health Report.md and prints a summary.
Run:  python .repo-metadata/health_report.py [--days 365] [--quiet]
"""
from __future__ import annotations
import os, re, sys, subprocess, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "90-System", "Health Report.md")
EXCLUDE_DIRS = {".git", ".obsidian", ".repo-metadata", "Attachments"}
STALE_DAYS = 365

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
LINK_SCOPE = "01-Knowledge/"                            # only this layer is expected to be linked


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


def main():
    global STALE_DAYS
    if "--days" in sys.argv:
        STALE_DAYS = int(sys.argv[sys.argv.index("--days") + 1])
    quiet = "--quiet" in sys.argv

    notes = {}                       # basename -> relpath  (last wins; collisions flagged)
    collisions = collections.defaultdict(list)
    data = {}                        # relpath -> dict(fm, out_links, text)
    for p in md_files():
        r = rel(p)
        base = os.path.basename(p)[:-3]
        if base in notes:
            collisions[base].append(r)
            if len(collisions[base]) == 1:
                collisions[base].insert(0, notes[base])
        notes[base] = r
        text = open(p, encoding="utf-8").read()
        data[r] = {"fm": parse_frontmatter(text), "out": link_targets(text), "base": base}

    valid = set(notes)
    inbound = collections.Counter()
    broken = []                      # (relpath, target)
    for r, info in data.items():
        for tgt in info["out"]:
            if tgt in valid:
                inbound[tgt] += 1
            else:
                broken.append((r, tgt))

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
            d = git_last_date(r)
            if d and (datetime.date.today() - d).days > STALE_DAYS:
                stale.append((r, d.isoformat(), (datetime.date.today() - d).days))

    moc_gap = sorted(
        r for r in knowledge_notes
        if os.path.dirname(r) in moc_domains
        and r not in moc_referenced
        and (data[r]["fm"] or {}).get("note_type") != "moc")

    # ---- write report ----
    today = datetime.date.today().isoformat()
    L = []
    L.append("---\nnote_type: glossary\nstatus: reference\n---")
    L.append(f"# Vault Health Report\n\nGenerated {today} · stale threshold {STALE_DAYS} days · "
             f"{len(data)} notes scanned\n")
    L.append(f"Link checks (orphans, MOC coverage) are scoped to `{LINK_SCOPE}` — the layer "
             f"meant to be connected. Broken links, stale, and frontmatter are checked vault-wide.\n")
    L.append("## Summary\n")
    L.append(f"| check | count |\n|---|---|")
    L.append(f"| broken wikilinks | {len(broken)} |")
    L.append(f"| orphan notes (in {LINK_SCOPE}) | {len(orphans)} |")
    L.append(f"| stale notes (>{STALE_DAYS}d) | {len(stale)} |")
    L.append(f"| missing frontmatter | {len(missing_fm)} |")
    L.append(f"| invalid frontmatter | {len(invalid_fm)} |")
    L.append(f"| MOC coverage gaps | {len(moc_gap)} |")
    L.append(f"| basename collisions | {len(collisions)} |")

    def section(title, rows):
        L.append(f"\n## {title}\n")
        if not rows:
            L.append("_none_")
        else:
            L.extend(rows)

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

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="").write("\n".join(L) + "\n")

    if not quiet:
        print(f"broken={len(broken)} orphans={len(orphans)} stale={len(stale)} "
              f"missing_fm={len(missing_fm)} invalid_fm={len(invalid_fm)} "
              f"moc_gap={len(moc_gap)} collisions={len(collisions)}")
        print(f"report -> {rel(OUT)}")


if __name__ == "__main__":
    main()
