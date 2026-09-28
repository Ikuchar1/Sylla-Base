# Class Notes

An LLM-wiki-style class-notes repo, following the Karpathy LLM Wiki pattern
(https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), adapted per-course.
The student writes raw notes and drops in instructor files; Claude compiles them into a
persistent, interlinked wiki. Questions are answered from the wiki, not by re-reading raw.

## The three layers

1. **Raw** (`<TERM>/<COURSE>/lectures/`, `.../materials/`, `.../assignments/`) —
   immutable. The student's typed lecture notes, instructor decks/PDFs, and their own
   assignment drafts. Claude reads, never writes.
2. **Wiki** (`<TERM>/<COURSE>/wiki/`) — agent-maintained. Everything Claude generates.
3. **This file** — the schema: structure, conventions, workflows.

## Layout

Courses are nested under a **term** folder (`fall-2026/`, `spring-2027/`, …). One repo
spans every semester so concept pages accumulate across terms.

    <TERM>/<COURSE>/
      course.md                syllabus: meeting days, grading, key dates
      lectures/                RAW — the student's notes, YYYY-MM-DD.txt
        _template.txt          blank skeleton, not a real lecture
      materials/               RAW — slides, PDFs, handouts, study guides
      assignments/             RAW — the student's own drafts and submitted work
      sessions/                agent-written Q&A logs
        YYYY-MM-DD-class.md      class-mode, one per class date
        hw-<assignment>.md       homework-mode, one per assignment
      wiki/
        index.md               catalog of every page + one-line summary
        log.md                 append-only audit trail of every ingest
        concepts/              one page per idea, accumulates across lectures
        sources/               one page per lecture, handout, or the syllabus
        assignments/           one page per assignment: what it asks, concepts, status
        analyses/              exam reviews, comparisons, syntheses
    _TEMPLATE/                 cp -R _TEMPLATE <TERM>/DEPT-### to add a course

Terms live at the repo root; `_TEMPLATE/` stays at the root and is shared by all of them.

**Obsidian vaults.** Each course folder has its own `.obsidian/` and is its own vault —
open it to see only that class. The repo root is also a vault that sees every course.
Wikilinks stay **within one course**; never link a page to another course's page. A new
course gets its vault from `_TEMPLATE/.obsidian/`.

## Current term

<!-- Keep this list current — it's how Claude resolves a bare course code. -->
**<term-folder>/** (current)
- **<DEPT-###>** — <Course name>, <meeting days/times>

<!-- Per-course exceptions go here. Example: a reading-heavy course where one concept
page per vocabulary term would produce hundreds of files can be "glossary-first" —
each ingested chapter appends to `wiki/glossary.md` plus one `wiki/sources/` page,
and concept pages are made only for ideas that recur across chapters. -->

**Sources vs concepts** — the distinction that makes this work:
`sources/lecture-2026-08-27.md` answers *"what happened Thursday."*
`concepts/weather-front.md` answers *"what do I know about fronts"* — built from
many lectures, decks, and the student's own questions. `assignments/quiz-3.md` answers
*"what am I graded on and which concepts does it need."* Dated pages are how notes get
taken; concept pages are how the student studies; assignment pages are how they plan.

Concept pages carry `status: planned` when reserved from the syllabus but not yet
taught, and `status: active` once a lecture has filled them in.

## Hard rules

- **Never edit or delete anything in `lectures/`, `materials/`, or `assignments/`.**
  That's the raw layer — the student's own words and the instructor's files.
  Corrections, gap-fills, and additions go in `wiki/`, never back into a raw file.
  **One exception:** `/homework-mode` may write code cells into the specific
  `assignments/` file the student is actively working through, under that skill's
  ask-before-you-write rule. `lectures/` and `materials/` have no exception, and the
  student's written-answer prose is their own everywhere.
- **Never overwrite a `## Pins` section** on a wiki page. Those are the student's own
  corrections and outrank anything generated.
- **Concept filenames must be globally unique and specific** — `social-norm.md`, not
  `norm.md`. In the root vault, wikilinks resolve by filename across every course and
  *term* — so a collision silently breaks both links there, even if each course vault
  looks fine. Before creating a page, check the name against every term, not only the
  current one.
- **Cite sources on every claim**: `[[lecture-2026-08-27]]`.
- **Don't blur the student's notes with your own knowledge.** Outside knowledge is
  marked `> [!note] Outside the notes`. If the notes don't cover something, say so plainly.
- **Flag contradictions, never resolve them silently.** When a deck and the notes
  disagree, add a `> [!warning] Contradiction` callout naming both. That gap is
  usually the thing worth studying.
- **Surgical edits.** Updating a concept page means integrating new material into it,
  not regenerating it. Preserve what's there.
- **Wiki pages are highlights, not transcripts.** Keep pages short and point to the
  deck PDF for the full treatment; keep the contradictions and gotchas.
- `.pptx`/`.docx` are zip archives, not text. Convert to PDF first (or
  `unzip -p deck.pptx 'ppt/slides/slide*.xml' | sed 's/<[^>]*>/ /g'` for a rough dump).

## Workflows

- **`/class-mode [COURSE]`** — live in-class study partner. Short answers, logs every
  Q&A to `<TERM>/<COURSE>/sessions/`. See `.claude/skills/class-mode/SKILL.md`.
- **`/homework-mode [COURSE] [assignment]`** — study partner while doing graded work.
  Asks a question that forces a commitment, *then* writes the code into the assignment
  file, then reconciles the guess against reality. Logs guess-vs-reality to
  `<TERM>/<COURSE>/sessions/hw-<slug>.md`, one file per assignment, appended across
  days. See `.claude/skills/homework-mode/SKILL.md`.
- **`/process-notes [COURSE]`** — the main loop. Ingests unprocessed raw files into
  the wiki. See `.claude/commands/process-notes.md`.
- **"quiz me on X"** — generate questions from that course's `wiki/concepts/`. Ask one
  at a time. Don't dump the answers.
- **"what did I miss?"** — compare lecture dates present against the meeting schedule
  in `course.md`.
- **"exam N review"** / **"quiz N review"** — merge the concepts listed on that
  assignment page into `wiki/analyses/`.
- **"what's due?"** — read `wiki/assignments/` frontmatter (`due`, `status`) across
  courses, newest deadline first.
- **"fill in the gaps in today's notes"** — read the matching deck in `materials/`,
  write what the notes missed into the source page. Never back-fill the raw `.txt`.

## About the student

<!-- Edit this section: your major, what you're preparing for, how you like things
explained. Claude reads it every session. -->

Keep explanations short, define terms on first use, lead with the answer.

**Talk, don't report.** Default to a few sentences and a stop, one idea per message —
the student is usually walking through something to learn it, not asking for a
document. When they explicitly ask for the whole thing ("do all of X", "process every
chapter"), do the whole thing; the brevity default is for the back-and-forth.

**Warn only about a trap they'd actually hit** — a bug that still half-works, a
convention that differs between sources, an assumption a slide makes silently. Not
caveats, not "note that"s. Most answers have none; end the answer instead of
manufacturing one.

**On graded work, check the course deck before answering.** The instructor's framing
beats the textbook-general answer.

**Never withhold an answer.** If they ask what something is or what goes in a blank,
tell them. The homework-mode gate is a question *before* you write code, not a refusal
to answer — see `.claude/skills/homework-mode/SKILL.md`.
