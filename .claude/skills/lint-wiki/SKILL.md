---
name: lint-wiki
description: Health-checks one course's wiki — broken or cross-course links, orphan pages, index gaps, filename collisions, stale planned stubs, overdue work, raw files not yet ingested, contradictions, stale claims, answered open questions, concepts with no page. Reports numbered findings and stops; fixes only the ones the student picks. Use when the user says "lint", "/lint-wiki", "health-check the wiki", "clean up the wiki", or is getting ready for an exam.
---

# Lint Wiki

The wiki drifts: a lecture corrects an old claim, a planned stub never gets filled, a
link points at a page that was renamed. Run this before each exam so the pages the
student studies from are right.

**Report first, then stop.** Nothing is edited until the student picks findings by
number.

## Scope

- One course. A bare code resolves against the term marked `(current)` in `CLAUDE.md`;
  `<TERM>/<COURSE>` targets an older one.
- Read only that course's `wiki/` and `course.md` (for key dates). **Never open raw
  files** — a file that needs ingesting is a `/process-notes` job, not a lint fix.
- Other courses matter only as filenames (collisions, stray links). Never read or edit
  their pages.

## 1. Mechanical pass — the script

    python3 .claude/skills/lint-wiki/lint.py <TERM>/<COURSE>

It checks links (every form: `[[a|alias]]`, `[[a#heading]]`, `![[embed]]`, `\|` in
tables), the index, orphans, missing back-links, names and course suffixes, planned
stubs, overdue items, and raw files against `log.md` — the same new/changed rule as
`/process-notes` step 1. **Its output is final.** Don't re-verify it by hand, and don't
add mechanical findings of your own.

## 2. Judgment pass — read selectively

Read `wiki/index.md` first. Under ~30 pages, read them all. Otherwise read the **next
graded item** (soonest `due` ≥ today in `wiki/assignments/`, else `course.md` key
dates), its "Concepts I need" pages, the sources those cite, and any page the script
flagged.

Look for:
- **Contradictions** — two pages disagree on a fact, number, or definition. Skip ones
  already inside a `> [!warning] Contradiction` callout.
- **Stale claims** — a page still says what a later lecture corrected.
- **Answered open questions** — an entry under `## Open questions` in `index.md` that a
  later page answers.
- **Concepts with no page** — a term named on 3+ pages (count with Grep) with no page of
  its own. Not one the script already reported as a broken link.

Report only what you can quote from both sides. No style nits, no "could be expanded".

## 3. Report, then stop

One numbered list: the script's findings first with its numbers, then yours continuing
the count. Keep its groups; add **Contradictions**, **Stale claims**, **Answered open
questions**, **Concepts with no page**. One line each — what, where, the fix in a few
words. Ten of one kind (e.g. every page missing its suffix) is one finding.

End with: *"Which should I fix? (e.g. 1, 3, 5 — or all)"* — and stop.

## 4. Fix what they pick

Use Edit, never rewrite a page. Per finding:

- **Broken link / index entry with no page** — repoint to the right page, or unlink. An
  index name with no page is often a crashed ingest: say to rerun `/process-notes`.
- **Link into another course** — unlink, or point at this course's page on it.
- **Missing from index** — add it under its section with a one-line summary.
- **Orphan** — link it from the pages that discuss it.
- **Missing cross-reference** — add the source to the concept's `## Sources` and fold in
  what that source page says about it, cited.
- **Collision / missing suffix** — rename this course's file (never the other course's)
  and update every link to it, including `index.md`.
- **Planned but taught** — fill it from the wiki pages that cover it; set
  `status: active`.
- **Planned but already tested** — no wiki fix; the lecture is missing. Say so
  ("what did I miss?" checks the schedule).
- **Overdue, still not-started** — ask what happened, then set the status they give.
- **Raw file to process** — no fix here; tell them to run `/process-notes <COURSE>`.
- **Contradiction** — a `> [!warning] Contradiction` callout on each page, naming both
  sources. Never pick a winner.
- **Stale claim** — update it, cite the later source, keep one line of what it said
  before: "(was X before [[lecture-…]])".
- **Answered open question** — remove it from `index.md` and link the answer's page.
- **Concept with no page** — create it from `wiki/concepts/_TEMPLATE.md` using only what
  the wiki already says, cited; `status: active` if a lecture covers it. Link it where
  it's named, add it to `index.md`, and check the name against every course first.

Then rerun the script to confirm, append one line to `wiki/log.md` — also when they
pick none — and report one line per fix, then what's still open:

    ## [YYYY-MM-DD] lint | N findings, M fixed

## Hard rules

- **Never edit `lectures/`, `materials/`, `assignments/`, or another course.** Fixes use
  only what's already in this wiki.
- **Never touch a `## Pins` section.** If a Pin disagrees with a page, the Pin wins —
  fix the page, not the Pin.
- **Never resolve a contradiction silently.** Flag both sides.
- Links stay within the course. Cite a source on every line you add.
