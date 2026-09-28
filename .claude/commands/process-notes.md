---
description: Ingest raw lecture notes and materials into a course wiki
argument-hint: [COURSE] (e.g. CS-101, or "all")
---

Ingest raw class content into the course wiki. Target: **$1** (if empty or "all",
process every course folder in the current term).

Courses live at `<TERM>/<COURSE>/` (e.g. `fall-2026/CS-101/`). A bare course code
means the current term; pass `<TERM>/<COURSE>` to target an older one.

Read the repo `CLAUDE.md` first if you have not this session, then the course's
`course.md` — its `wiki-style` decides how this ingest works.

## Depth: overview, not transcript

The PDF stays in `materials/` forever. The wiki is the **highlights** plus a pointer to
it — never a re-transcription. Short pages are the whole point: the parts that can't be
recovered by reopening the slides (contradictions, the class discussion, the student's
own questions) get buried when a page restates every bullet.

- A concept page rarely needs more than ~60 lines. A source page: a slide map and the
  argument in a few lines.
- If a section just restates slides, cut it and cite the slide range instead.
- **No gotcha / tip callouts.** Only two callout types go in the wiki:
  `> [!warning] Contradiction` and `> [!note] Outside the notes`.

## 1. Find unprocessed raw files

List `<TERM>/<COURSE>/lectures/*.txt`, `.../materials/*`, and `.../sessions/*.md`
(skip `_template.txt`, `README.md`, and `*-chapter-index.md`). A raw file is
**unprocessed** if `wiki/log.md` has no entry naming it.

- **Class session** (`YYYY-MM-DD-class.md`, from class mode) — treat like a lecture: it
  gets a source page and feeds concept pages.
- **Homework session** (`hw-<assignment>.md`) — **not** a source page. Its wrong guesses
  and what fixed them fold into that assignment's page in `wiki/assignments/`; its
  concept links update the concept pages.
- **Textbook** (a big PDF) — if there's no `<book>-full.txt` yet, extract it once with
  `pdftotext` and build `<book>-chapter-index.md` (chapter → line range). Ingest only the
  chapters the student names, by grepping the text — never the whole book at once.

Report what you found in a few lines before writing anything.

## 2. Ingest each file (one at a time — never batch-write)

**a. Plan.** Read the whole file. List the pages it touches — new ones and existing ones
that need updating. Reserve new names in `wiki/index.md` first, so a crashed run leaves
a trace.

**b. Source page.** Write `wiki/sources/<name>.md` from `wiki/sources/_TEMPLATE.md`:
`lecture-YYYY-MM-DD`, `class-YYYY-MM-DD` (class session), `deck-NN-<slug>`, or
`reading-<slug>`. Open with the pointer to the file (`> **Full deck:** materials/...`),
then a slide map, then the argument in a few lines.

**c. Concept pages — `wiki-style: concepts`.** For each concept, create or update
`wiki/concepts/<specific-kebab-name>.md` from `wiki/concepts/_TEMPLATE.md`.
- Concept pages **accumulate** across lectures. Integrate new material into the existing
  page with the smallest edit that works; preserve what's there.
- Filenames must be unique across the whole repo — `social-norm.md`, not `norm.md`.

**c. Glossary — `wiki-style: glossary`.** Append one section to `wiki/glossary.md`
(create it if missing): every term from the chapter, the author's own wording where the
book defines it, one concrete example each. Make a concept page only for an idea that
recurs across chapters and already has material from more than one.

**d. Cross-reference.** Add `[[wikilinks]]` between related pages in both directions —
**within this course only**. Each course folder is its own Obsidian vault, so a link to
another course's page is dead there. If new material **contradicts** an existing page,
don't overwrite — add a `> [!warning] Contradiction` callout naming both sources.

**e. Assignments.** If the material maps to a graded item, update that page in
`wiki/assignments/` — add newly-covered concepts to its "Concepts I need" list. Flip a
concept page from `status: planned` to `status: active` once a lecture covers it. Skip
requirements for a section the student isn't in (see `course.md`).

**f. Index + log.** Update `wiki/index.md` with each new page and its one-line summary.
Append one entry to `wiki/log.md`:
`## [YYYY-MM-DD] ingest | <source file> → N pages created, M updated`

## 3. Report

Keep it short — overview level. Files ingested, pages created vs updated, any
contradictions, and real gaps (unfinished sentences, "???", a scheduled class day with
no notes per `course.md`). No page-by-page tour.

## Hard rules

- **Never modify `lectures/`, `materials/`, or `assignments/`.** Gaps and corrections go
  in the wiki, never back into the raw notes. (Creating `<book>-full.txt` and its index
  in `materials/` is the one allowed addition — it's an extraction, not an edit.)
- **Never overwrite a `## Pins` section.** Those are the student's own corrections.
- Cite sources on every claim: `[[lecture-2026-08-27]]`.
- Mark outside knowledge `> [!note] Outside the notes`.
- `.pptx` cannot be read as text — convert to PDF or ask the student to export it.
