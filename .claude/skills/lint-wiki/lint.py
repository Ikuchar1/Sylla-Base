#!/usr/bin/env python3
"""Mechanical lint for one course wiki. Stdlib only, Python 3.9+.

    python3 .claude/skills/lint-wiki/lint.py <TERM>/<COURSE>

Prints numbered findings, grouped. Reads the course's wiki/ pages and log.md. Raw files
are only listed and fingerprinted (same rule as /process-notes step 1); other courses
contribute filenames only.
"""
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

LINK = re.compile(r"!?\[\[([^\]\n]+?)\]\]")
CODE = re.compile(r"```.*?```|~~~.*?~~~|`[^`\n]*`|<!--.*?-->", re.S)
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
HUBS = {"index", "log", "glossary"}  # never orphans, never index entries, never collide
SKIP_RAW = ("_template.txt", "README.md")


def links(text):
    """Link targets, lowercased: [[a|b]], [[a#h]], ![[a]], [[a\\|b]], [[dir/a.md]]."""
    out = []
    for raw in LINK.findall(CODE.sub("", text)):
        t = raw.replace("\\|", "|").split("|")[0].split("#")[0].strip()
        if t:
            t = t.rsplit("/", 1)[-1].lower()
            out.append(t[:-3] if t.endswith(".md") else t)
    return out


def front(text):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    pairs = (ln.partition(":") for ln in (m.group(1).splitlines() if m else []))
    return {k.strip(): v.split("#")[0].strip().strip("'\"") for k, s, v in pairs if s}


def section(text, heading):
    m = re.search(r"^## %s\s*$(.*?)(?=^## |\Z)" % heading, text, re.M | re.S)
    return m.group(1) if m else ""


def blob(data):
    """Same digest as `git hash-object <file>`."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: lint.py <TERM>/<COURSE>")
    course = Path(sys.argv[1]).resolve()
    wiki, root, code = course / "wiki", course.parents[1], course.name.lower()
    if not wiki.is_dir():
        sys.exit("no wiki/ in %s" % course)
    today = date.today().isoformat()

    pages = sorted(p for p in wiki.rglob("*.md") if p.name != "_TEMPLATE.md")
    stem = {p: p.stem.lower() for p in pages}
    rel = {p: p.relative_to(wiki).as_posix() for p in pages}
    text = {p: p.read_text(encoding="utf-8", errors="replace") for p in pages}
    meta = {p: front(text[p]) for p in pages}
    out = {p: links(text[p]) for p in pages}
    by_stem = {}
    for p in pages:
        by_stem.setdefault(stem[p], []).append(p)
    kind = {p: rel[p].split("/")[0] if "/" in rel[p] else "" for p in pages}
    lectures = [p for p in pages if kind[p] == "sources" and "syllabus" not in stem[p]]
    assignments = [p for p in pages if kind[p] == "assignments"]
    vault = {f.stem.lower() if f.suffix == ".md" else f.name.lower()
             for f in course.rglob("*") if f.is_file() and ".obsidian" not in f.parts}
    others = {}  # stem -> path, for every other course's wiki page
    for w in sorted(root.glob("*/*/wiki")):
        hidden = any(x[0] in "._" for x in w.relative_to(root).parts)
        if w.resolve() != wiki and not hidden:
            for p in w.rglob("*.md"):
                if p.name != "_TEMPLATE.md" and p.stem.lower() not in HUBS:
                    others.setdefault(p.stem.lower(), p.relative_to(root).as_posix())

    groups = {}

    def add(group, msg):
        groups.setdefault(group, []).append(msg)

    # Links
    missing, cross = {}, {}
    for p in pages:
        if stem[p] in ("index", "log"):
            continue
        for t in sorted(set(out[p])):
            if t not in vault:
                (cross if t in others else missing).setdefault(t, []).append(rel[p])
    for t, src in sorted(missing.items()):
        add("Broken links", "[[%s]] — no such page (linked from %s)"
            % (t, ", ".join(src)))
    for t, src in sorted(cross.items()):
        add("Links into another course", "[[%s]] in %s — only exists at %s"
            % (t, ", ".join(src), others[t]))

    # Index
    index = next((p for p in pages if rel[p] == "index.md"), None)
    listed = set(out[index]) if index else set()
    for t in sorted(listed - vault):
        if t in others:
            add("Links into another course", "[[%s]] in index.md — only exists at %s"
                % (t, others[t]))
        else:
            add("Index", "index.md lists [[%s]], which has no page" % t)
    for p in pages:
        if stem[p] not in HUBS and stem[p] not in listed:
            add("Index", "%s is missing from index.md" % rel[p])

    # Orphans: inbound links from anything but index, log, and the page itself
    inbound = {}
    for p in pages:
        if stem[p] not in ("index", "log"):
            for t in set(out[p]) - {stem[p]}:
                inbound.setdefault(t, set()).add(p)
    for p in pages:
        hub = stem[p] in HUBS or kind[p] == "analyses" or "syllabus" in stem[p]
        if not hub and not inbound.get(stem[p]):
            add("Orphans", "%s — no page links to it (index.md aside)" % rel[p])

    # Cross-references: a lecture's "Concepts introduced" must be cited back
    for s in lectures:
        for t in sorted(set(links(section(text[s], "Concepts introduced")))):
            for c in by_stem.get(t, []):
                if (kind[c] == "concepts" and meta[c].get("status") != "planned"
                        and stem[s] not in out[c]):
                    add("Missing cross-references", "%s lists [[%s]], but %s doesn't "
                        "cite it" % (rel[s], c.stem, rel[c]))

    # Names: unique across every course; sources/assignments/analyses carry the code
    for p in pages:
        s = stem[p]
        if s in HUBS:
            continue
        if s in others:
            add("Filename collisions", "%s — also %s" % (rel[p], others[s]))
        elif len(by_stem[s]) > 1 and p == by_stem[s][0]:
            add("Filename collisions", " and ".join(rel[q] for q in by_stem[s]))
        suffixed = kind[p] in ("sources", "assignments", "analyses")
        if suffixed and not s.endswith("-" + code):
            add("Missing course suffix", "%s should end in -%s" % (rel[p], code))

    # Status: planned stubs already taught or already tested; overdue work
    for c in pages:
        if kind[c] != "concepts" or meta[c].get("status") != "planned":
            continue
        s = stem[c]
        taught = [rel[q] for q in lectures if s in out[q]]
        if taught:
            add("Status", "%s is planned, but %s covers it"
                % (rel[c], ", ".join(taught)))
        for a in assignments:
            due = DATE.search(meta[a].get("due", ""))
            past = sorted(d.group() for line in text[a].splitlines()
                          if s in links(line)
                          for d in [DATE.search(line) or due]
                          if d and d.group() < today)
            if past:
                add("Status", "%s is planned, but %s tested it on %s"
                    % (rel[c], rel[a], past[-1]))
    for a in assignments:
        due, status = meta[a].get("due", ""), meta[a].get("status")
        if DATE.fullmatch(due) and due < today and status == "not-started":
            add("Status", "%s was due %s and is still not-started" % (rel[a], due))
        for line in text[a].splitlines():
            d = DATE.search(line)
            row = line.startswith("|") and "not-started" in line
            if row and d and d.group() < today:
                add("Status", "%s row due %s is still not-started"
                    % (rel[a], d.group()))

    # Raw files to ingest — /process-notes step 1: the newest log entry naming the
    # file; its "@ <hash>" vs the file's git hash. A legacy entry (no hash) counts as
    # processed, unless it's a session with a later "### YYYY-MM-DD" block.
    log = wiki / "log.md"
    log = log.read_text(encoding="utf-8") if log.exists() else ""
    entries = [ln for ln in log.splitlines() if ln.startswith("## [")]
    raw = (("lectures", "*.txt"), ("materials", "*"), ("sessions", "*.md"))
    for sub, pattern in raw:
        for f in sorted((course / sub).glob(pattern)):
            n, path = f.name, "%s/%s" % (sub, f.name)
            if (not f.is_file() or n[0] == "." or n in SKIP_RAW
                    or n.endswith(("-full.txt", "-chapter-index.md"))):
                continue
            named = re.compile(r"(^|[\s/])%s(?=[\s,;]|$)" % re.escape(n))
            last = next((e for e in reversed(entries) if named.search(e)), None)
            if not last:
                add("Raw files to process", "%s — new, no log entry" % path)
                continue
            h, logged = re.search(r"@ ([0-9a-f]{7,40})\b", last), DATE.search(last)
            data = f.read_bytes()
            if h and not blob(data).startswith(h.group(1)):
                add("Raw files to process", "%s — changed since its last entry (@ %s)"
                    % (path, h.group(1)))
            elif not h and sub == "sessions" and logged:
                blocks = re.findall(r"^### (\d{4}-\d{2}-\d{2})",
                                    data.decode("utf-8", "replace"), re.M)
                if any(b > logged.group() for b in blocks):
                    add("Raw files to process", "%s — has blocks dated after its last "
                        "entry" % path)

    total = sum(len(v) for v in groups.values())
    print("%s — %d mechanical findings (today %s)"
          % (course.relative_to(root).as_posix(), total, today))
    n = 0
    for g, msgs in groups.items():
        print("\n" + g)
        for m in msgs:
            n += 1
            print("%d. %s" % (n, m))


if __name__ == "__main__":
    main()
