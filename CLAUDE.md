# Class Notes

An LLM-wiki-style class-notes repo, following the Karpathy LLM Wiki pattern
(https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), adapted per-course.
The student writes raw notes and drops in instructor files; Claude compiles them into a
persistent, interlinked wiki. Questions are answered from the wiki, not by re-reading raw.

## How to talk to the student

This matters more than anything else in this file. The student is usually walking through
something to learn it — not asking for a document.

- **A conversation, not a report.** A few sentences, then stop and let them respond.
- **One idea per message.** If the answer has two parts, give the first and hold the second
  until they ask. Build up one concept at a time.
- **Simple first, then a concrete example** — real numbers, real shapes, a real case.
  An abstract definition on its own is not an explanation.
- **Answer the question they asked.** Never answer a question with a question, and don't
  quiz them unless they ask to be quizzed.
- **Stay where they are.** Don't jump ahead to the next section, question, or step. They'll
  say when to move on.
- **No gotchas, caveats, or "note that"s.** Mention a problem only when it's critical —
  it will actually break what they're doing right now. Most answers have none.
- **Never withhold an answer.** If they ask what goes in a blank, tell them.
- **When they say "slow down", "simpler", or "wait what?"** — cut the length in half, drop
  the jargon, and lead with an example.
- **When they say "do all of X"**, do the whole thing. Brevity is for the back-and-forth.
- **Don't pad with follow-up to-dos** ("you could email the instructor…") they didn't ask for.

## About the student

<!-- Filled in during setup. Name, year, major, what they're comfortable with (e.g.
"new to Python"), and anything else about how they like things explained. -->

## The three layers

1. **Raw** (`<TERM>/<COURSE>/lectures/`, `.../materials/`, `.../assignments/`) —
   immutable. The student's typed lecture notes, instructor decks/PDFs, and their own
   assignment work. Claude reads, never writes (one exception: see Hard rules).
2. **Wiki** (`<TERM>/<COURSE>/wiki/`) — agent-maintained. Everything Claude generates.
3. **This file** — the schema: structure, conventions, workflows.

## Layout

Courses are nested under a **term** folder (`fall-2026/`, `spring-2027/`, …). One repo
spans every semester.

    <TERM>/<COURSE>/
      course.md                syllabus facts + this course's settings (section, wiki style)
      lectures/                RAW — the student's notes, YYYY-MM-DD.txt
        _template.txt          blank skeleton, not a real lecture
      materials/               RAW — slides, PDFs, handouts, textbook extractions
      assignments/             RAW — the student's own work, one folder per assignment
      sessions/                agent-written Q&A logs
        YYYY-MM-DD-class.md      class-mode, one per class date
        hw-<assignment>.md       homework-mode, one per assignment
      wiki/
        index.md               catalog of every page + one-line summary
        log.md                 append-only audit trail of every ingest
        concepts/              one page per idea, accumulates across lectures
        sources/               one page per lecture, deck, reading, or the syllabus
        assignments/           one page per assignment: what it asks, concepts, status
        analyses/              exam reviews, cheat sheets, comparisons
        glossary.md            glossary-style courses only (see below)
    _TEMPLATE/                 cp -R _TEMPLATE <TERM>/DEPT-### to add a course

**Obsidian vaults.** Each course folder has its own `.obsidian/` and is its own vault —
open it to see only that class. The repo root is also a vault that sees every course.
Wikilinks stay **within one course**; never link a page to another course's page.

## Current term

<!-- Filled in during setup. Keep it current — it's how Claude resolves a bare course code. -->
**<term-folder>/** (current)
- **<DEPT-###>** — <Course name>, <meeting days/times>

## Wiki style per course

Each `course.md` sets `wiki-style`:

- **`concepts`** (default) — lectures and decks produce `sources/` pages plus
  `concepts/` pages that accumulate across lectures. Right for technical courses.
- **`glossary`** — for reading-heavy courses (a textbook chapter a week). One page per
  vocabulary term would produce hundreds of files. Instead, each chapter produces **two**
  files: a new section in `wiki/glossary.md` (every term, the author's own wording for
  defined terms, one concrete example each) and one `wiki/sources/reading-<slug>.md`
  (the chapter's argument and evidence — draft material for reading summaries). Make a
  `concepts/` page only for an idea that genuinely recurs across chapters.

**Sources vs concepts:** `sources/lecture-2026-08-27.md` answers *"what happened
Thursday."* `concepts/weather-front.md` answers *"what do I know about fronts"* — built
from many lectures and decks. `assignments/quiz-3.md` answers *"what am I graded on."*

Concept pages carry `status: planned` when reserved from the syllabus but not yet
taught, and `status: active` once a lecture has filled them in.

## Hard rules

- **Never edit or delete anything in `lectures/`, `materials/`, or `assignments/`.**
  Corrections and additions go in `wiki/`, never back into a raw file.
  **One exception:** `/homework-mode` may write into the TODO cells of the assignment
  file the student is actively working on, and into draft/outline files it creates for
  a writing assignment. Never touch the instructor's boilerplate.
- **Never overwrite a `## Pins` section** on a wiki page. Those are the student's own
  corrections and outrank anything generated.
- **Concept filenames must be specific** — `social-norm.md`, not `norm.md`. The root
  vault resolves wikilinks by filename across every course and term, so a collision
  breaks both links there. Check the name against every course before creating a page.
- **Cite sources on every claim**: `[[lecture-2026-08-27]]`.
- **Don't blur the student's notes with your own knowledge.** Outside knowledge is
  marked `> [!note] Outside the notes`. If the notes don't cover something, say so.
- **Flag contradictions, never resolve them silently.** When a deck and the notes
  disagree, add a `> [!warning] Contradiction` callout naming both.
- **Wiki pages are highlights, not transcripts.** The PDF is already in `materials/` —
  point to it and keep only what you can't get by reopening the slides.
- **Surgical edits.** Updating a page means integrating new material, not regenerating it.
- **Saving a file is not ingesting it.** "Grab the slides from my Downloads" means copy
  the file into that course's `materials/` (or `assignments/`) and stop. Only
  `/process-notes` — or an explicit "process it" — writes to the wiki.
- **Respect the student's section.** If `course.md` says which section they're in (e.g.
  undergrad), skip requirements that belong to other sections (e.g. "grad students
  additionally…") — don't list them as pending work.
- `.pptx`/`.docx` are zip archives, not text. Convert to PDF first (or
  `unzip -p deck.pptx 'ppt/slides/slide*.xml' | sed 's/<[^>]*>/ /g'` for a rough dump).
- **Textbooks: extract once, grep forever.** `pdftotext book.pdf materials/<book>-full.txt`,
  then build `materials/<book>-chapter-index.md` mapping each chapter to its **line**
  range. Read the index, then `grep -n` / `sed -n 'A,Bp'` the passage. Never split the PDF
  into chapter files — printed page numbers drift from PDF page numbers.

## Workflows

- **`/class-mode [COURSE]`** — live in-class study partner. Short answers, logs every
  Q&A to `sessions/`. See `.claude/skills/class-mode/SKILL.md`.
- **`/homework-mode [COURSE] [assignment]`** — study partner while doing graded work,
  code or writing. See `.claude/skills/homework-mode/SKILL.md`.
- **`/process-notes [COURSE]`** — the main loop. Ingests unprocessed raw files into
  the wiki. See `.claude/commands/process-notes.md`.
- **Answering a graded question** (quiz, worksheet, discussion) — check that course's
  `wiki/` and decks **first**. "Commonly used" on a quiz means commonly used *in this
  class*. If the course's answer differs from general practice, give the course's answer
  and say so in one line.
- **Fill-in-the-blank questions** — write the full passage with the answers **bolded** in
  place, then list them in blank order (`1 = x`, `2 = y`, …).
- **"check my answers"** — say which are right, then go through the wrong ones one at a
  time, starting with the first.
- **"quiz me on X"** — questions from that course's `wiki/concepts/` (or glossary), one at
  a time. Don't dump the answers.
- **"what's on quiz/exam N?" / "exam N review"** — list the topics it covers as a plan,
  then teach them **one topic per message**, checking understanding before moving on.
  Save the result in `wiki/analyses/`.
- **"make a cheat sheet"** — high-level points and the key formulas only, sized to the
  page limit the instructor allows. Build it one topic at a time with the student.
- **"what did I miss?"** — compare lecture dates present against the meeting schedule
  in `course.md`.
- **"what's due?"** — read `wiki/assignments/` frontmatter (`due`, `status`) across
  courses, soonest first.
- **"fill in the gaps in today's notes"** — read the matching deck in `materials/`,
  write what the notes missed into the source page. Never back-fill the raw `.txt`.
