---
name: get-started
description: Sets up this notes repo for a new student, or a new semester for a returning one. Asks their name, year, and classes, makes the folders, then walks them through downloading each syllabus and the slides posted so far and pulls those files in from their Downloads folder. Checks each step off in SETUP.md so it can pick up where it left off. Use when the user says "get started", "set me up", "/get-started", "new semester", "add a class", or has a fresh copy of the template.
---

# Get Started

Get a student from a fresh copy of the template to a working wiki in about 15 minutes,
without them needing to know how the repo works.

**One step at a time.** Ask one thing, wait, do it, check it off in `SETUP.md`, then say
what's next. Every message ends with exactly one thing for them to do. Never show the
whole plan up front — `SETUP.md` already shows it.

## Where are we?

- **Nothing checked yet** → first-time setup. One line of hello — *"I'll get your notes
  set up one step at a time; you can stop anytime."* — then step 1.
- **`SETUP.md` has some items checked** → resume at the first unchecked one. One line on
  what's done and what's next, then that step.
- **`SETUP.md` is all checked, or missing, and `## About the student` in `CLAUDE.md` is
  filled in** → returning student. Ask: new semester, or add a class to this one?
  - New semester → append a `## <Semester>` section to `SETUP.md` (create the file if
    missing) with the steps from "Semester" onward, and move the `(current)` marker in
    `CLAUDE.md` to the new term.
  - Add a class → append just that class's three items.

When you check an item off, write what was decided next to it:
`- [x] Your classes — CSCE-480H, METR-100`. `SETUP.md` doubles as a record.

## 1. About you

Ask: *"What's your name, what year are you in, and what's your major?"* Then, as its own
question: *"Anything you already know well, or anything brand new? (e.g. 'know Java, never
used Python') — skip it if you like."*

Replace the comment under `## About the student` in `CLAUDE.md` with 2–4 plain lines.
This is what every future session reads, so write it for Claude: what to assume, what
to explain from scratch.

## 2. Semester

Work it out from today's date — Jan–May `spring-YYYY`, Jun–Jul `summer-YYYY`, Aug–Dec
`fall-YYYY`. Don't ask; say it in the same message as the next question:
*"This semester goes in `fall-2026/`. What classes are you taking? Just the codes is
fine — like CSCE 480, METR 100."*

## 3. Classes

For each class:
- Folder name: uppercase, hyphen, keep letter suffixes — `CSCE 480H` → `CSCE-480H`.
- `mkdir -p <term> && cp -R _TEMPLATE <term>/<CODE>`, then set `course:` in its
  `course.md`.
- Add it to `## Current term` in `CLAUDE.md` (replacing the `<placeholder>` lines). Name and
  meeting times come from the syllabus in step 5 — leave them out until then.
- Add its section to `SETUP.md` under the semester:

      ### CSCE-480H
      - [ ] Syllabus
      - [ ] Class details from the syllabus
      - [ ] Slides and readings posted so far

Then go through the classes **one at a time**, doing steps 4–6 for each before moving on.

## 4. Syllabus — pull it from Downloads

Say:
> Let's get the **CSCE 480H** syllabus. Download it from Canvas — usually under
> **Syllabus** or **Files** — and tell me when it's done. I'll pull it straight from your
> Downloads folder.
>
> If the syllabus is a Canvas page instead of a file, press **Cmd+P** (Ctrl+P on
> Windows) and choose **Save as PDF**.

The first time only, add: *"If your Mac asks whether the terminal can access your
Downloads folder, click **Allow**."*

When they say it's there, see [Pulling from Downloads](#pulling-from-downloads). Save it
as `materials/syllabus.<ext>`, keeping its extension. If it turns out to be a lab or
recitation syllabus, save it as `lab-syllabus.<ext>` and ask if there's a lecture one too.

## 5. Class details from the syllabus

If the syllabus shows a different code than they typed — a suffix like `480H`, or a
cross-listing — rename the folder now and fix its `course:`, its `CLAUDE.md` line, and
its `SETUP.md` heading. It's still empty, so nothing breaks.

Read the syllabus and fill in `course.md`: term, meeting times, instructor, textbook,
grading table, key dates. Add the name and meeting times to `## Current term` in
`CLAUDE.md`.

Two settings to decide:
- **`section`** — only if the syllabus has different requirements per section (grad vs
  undergrad, honors). Ask which they're in. Otherwise delete the line.
- **`wiki-style`** — pick from the syllabus and say which in one line:
  `glossary` for reading-heavy classes (a textbook chapter a week), `sources` for
  pass/no-pass seminars with nothing to study, `concepts` for everything else.

Show a 3-line summary — *"TR 11:00–12:15 · project 36%, three quizzes · no final."* —
and ask if anything's off. Don't build wiki pages yet; that's step 7.

## 6. Slides and readings posted so far

Say:
> Now download anything already posted for **CSCE 480H** — slides, readings, handouts.
> PDF if Canvas gives you a choice. Tell me when they're in Downloads. Nothing posted
> yet? Just say so.

Pull them in — see below. Slides, readings, and the textbook go in `materials/`; a
homework notebook or starter file goes in `assignments/<name>/`. Keep the instructor's
filenames. Check the item off with a count: `— 4 decks, textbook`.

## 7. Build the wiki

Once every class is done:
> Want me to build your wiki now? I'll read each syllabus and make a page for every
> graded item with its due date — so "what's due?" works from today.

On yes, follow `.claude/commands/process-notes.md` for every class. Report in two or three lines: pages per class, and the
next thing due.

## 8. Obsidian (optional)

> To browse your notes, install Obsidian (obsidian.md), click **Open folder as vault**,
> and pick a class folder — like `fall-2026/CSCE-480H`. Or skip this; everything works
> without it.

## 9. Save to GitHub

1. Files over 100 MB can't go to GitHub (a big textbook PDF can be). Check with
   `find . -size +95M -not -path './.git/*'`; add any hits to `.gitignore` and tell them.
2. If `gh` is installed, check the repo is private (`gh repo view --json visibility`).
   If it's public, say so once — homework in a public repo can be an academic-integrity
   problem — and give the fix: `gh repo edit --visibility private --accept-visibility-change-consequences`.
3. Ask, then commit and push: `git add -A && git commit -m "Set up <term>" && git push`.
   No remote (`git remote` prints nothing) means they downloaded instead of cloning —
   commit, then offer `gh repo create <name> --private --source . --push`.

## 10. Done

Check the last item, then give them the day-to-day in four lines — it's also at the
bottom of `SETUP.md`:
- **In class** — `/class-mode CSCE-480H`, or type notes in `lectures/YYYY-MM-DD.txt`
- **New slides posted** — download them and say "grab the new slides from my Downloads"
- **After class** — `/process-notes CSCE-480H`
- **Homework** — `/homework-mode CSCE-480H <assignment>`

## Pulling from Downloads

1. List the newest files: `ls -lt ~/Downloads | head -15`. "Operation not permitted"
   means macOS blocked it: System Settings → Privacy & Security → Files and Folders →
   turn on Downloads for their terminal app, then try again.
2. Match by name — class code, "syllabus", the deck title. A generic name
   (`Syllabus(1).pdf`, `download.pdf`)? Peek inside: `pdftotext -l 1 <file> - | head`
   for a PDF, the `unzip -p` dump from `CLAUDE.md` for `.docx`/`.pptx`. Two copies
   with `(1)` on one: take the newest.
3. If you're unsure which file goes where, list your guesses in one message and let them
   correct it. Never guess silently.
4. **Copy** into the class folder — don't move, and never read a file for the wiki
   straight out of Downloads. The copy in `materials/` is the permanent one.
5. A `.zip`: `unzip -oj <zip> -d <class>/materials/` — `-j` flattens the folder Canvas
   wraps around the files, which `/process-notes` wouldn't look inside. Then show what
   came out.
6. Nothing new there? Say so plainly and ask them to check the download finished.

## Hard rules

- Never skip ahead of the student. One step, then wait.
- Never overwrite a filled-in `## About the student` or `## Current term` — add to them.
- Only touch `lectures/`, `materials/`, and `assignments/` to **add** the files the
  student downloaded. Never edit or delete what's already there.
- Wiki pages come from `/process-notes`, not from this skill.
