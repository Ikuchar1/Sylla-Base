# Getting started

Open a terminal in this folder, run `claude`, and type `/get-started`. Claude asks one
thing at a time and checks it off here. Stop whenever you like — `/get-started` picks
up where you left off.

You'll download files from Canvas yourself (syllabus, slides). Just tell Claude when
they're in your **Downloads** folder and it pulls them in from there.

## About you
- [ ] Your name, year, and major
- [ ] What you already know, and what's new to you (optional)

## This semester
- [ ] Semester folder
- [ ] Your classes
<!-- Claude adds a section per class below: syllabus, class details, slides so far -->

## Build your wiki
- [ ] First `/process-notes` — turns each syllabus into pages for every graded item
- [ ] Open a class in Obsidian (optional)
- [ ] Save to GitHub

## Day to day

Once everything above is checked:
- **In class** — `/class-mode <CLASS>`, or type notes in `lectures/YYYY-MM-DD.txt`
- **New slides posted** — download them, then tell Claude "grab the new slides from my Downloads"
- **After class** — `/process-notes <CLASS>`
- **Homework** — `/homework-mode <CLASS> <assignment>`
- **Before an exam** — `/lint-wiki <CLASS>`
- **Anytime** — "what's due?", "quiz me on …", "what's on exam 1?"

New semester, or adding a class? Run `/get-started` again.
