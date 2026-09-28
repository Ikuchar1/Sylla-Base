---
description: Ingest raw lecture notes and materials into a course wiki
argument-hint: [COURSE] (e.g. CS-101, or "all")
---

Ingest raw class content into the course wiki. Target: **$1** (if empty or "all",
process every course folder in the current term).

Courses live at `<TERM>/<COURSE>/` (e.g. `fall-2026/CS-101/`). A bare course code
means the current term; pass `<TERM>/<COURSE>` to target an older one.

Read the repo `CLAUDE.md` first if you have not this session.

## 1. Find unprocessed raw files

For the target course, list `<TERM>/<COURSE>/lectures/*.txt`, `.../materials/*`, and `.../sessions/*.md`
(skip `_template.txt` and `README.md`). Session files are Claude-written Q&A logs — `YYYY-MM-DD-class.md` from class mode,
`hw-<assignment>.md` from homework mode. Treat a class session like a lecture: it gets
a source page and feeds concept pages. A homework session is **not** a source page —
its stuck/unstuck entries and gotchas fold into that assignment's page in
`wiki/assignments/`, and its concept links update the concept pages. A raw file is **unprocessed** if `wiki/log.md` has no entry naming it.
Report what you found before writing anything.

## 2. Ingest each file (one at a time — never batch-write)

For each unprocessed raw file:

**a. Plan.** Read the whole file. List the concept pages it touches — both new pages
and existing ones in `wiki/concepts/` that need updating. Reserve new names in
`wiki/index.md` before writing them, so a crashed run leaves a trace.

**b. Source page.** Write `wiki/sources/lecture-YYYY-MM-DD.md` (or `deck-<slug>.md`)
from `wiki/sources/_TEMPLATE.md`. This is what that single class session covered.

**c. Concept pages.** For each concept, create or update
`wiki/concepts/<specific-kebab-name>.md` from `wiki/concepts/_TEMPLATE.md`.
- Concept pages **accumulate** across lectures. Updating means integrating the new
  material into the existing page, not replacing it.
- Make the smallest edit that incorporates the new information. Preserve what is there.
- Filenames must be specific enough to be globally unique — `social-norm.md`, not
  `norm.md`. In the root vault wikilinks resolve by filename across every course and
  term, so a collision between two courses breaks both links.

**d. Cross-reference.** Add `[[wikilinks]]` between related concepts in both
directions — **within this course only**. Each course folder is its own Obsidian vault,
so a link to another course's page is dead there; never link across courses. If new
material **contradicts** an existing page, do not silently overwrite — add a
`> [!warning] Contradiction` callout naming both sources and flag it in your report.

**e. Assignments.** If the material maps to a graded item, update that page in
`wiki/assignments/` — add newly-covered concepts to its "Concepts I need" list. Flip a
concept page from `status: planned` to `status: active` once a lecture actually covers it.

**f. Index + log.** Update `wiki/index.md` with each new page and its one-line
summary. Append one entry to `wiki/log.md`:
`## [YYYY-MM-DD] ingest | <source file> → N concepts, M updated`

## 3. Report

Summarize: files ingested, pages created vs updated, contradictions found, and any
gaps (unfinished sentences, "???", a missing lecture on a scheduled class day per
`course.md`).

## Hard rules

- **Never modify `lectures/`, `materials/`, or `assignments/`.** Immutable raw layer.
  Gaps and corrections go in the wiki, never back into the raw notes.
- **Never overwrite a `## Pins` section.** Those are the student's own corrections and
  outrank anything you generate.
- Cite sources on every claim: `[[lecture-2026-08-27]]`.
- Do not blur the student's notes with your own knowledge. Outside knowledge gets marked
  `> [!note] Outside the notes`.
- `.pptx` cannot be read as text — convert to PDF or ask the user to export it.
