# Sylla-Base

**A knowledge base that builds itself from your class notes.**

A [Karpathy-style LLM wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
for coursework, built for [Claude Code](https://code.claude.com/docs/en/overview) and
[Obsidian](https://obsidian.md). You type rough notes in class and download the
instructor's slides; Claude turns them into an interlinked wiki you can study from, quiz
yourself on, and ask questions against.

## What you need

- [Claude Code](https://code.claude.com/docs/en/overview) — needs a paid Claude plan or an API key
- Git and a GitHub account
- [Obsidian](https://obsidian.md) — optional, for browsing the wiki
- `pdftotext` — optional, makes reading PDFs faster: `brew install poppler`

## Setup

1. **Make your own private copy.** Click **Use this template** → **Create a new
   repository**, and set it to **Private** — it'll hold your coursework. Then clone it:

       git clone https://github.com/<you>/<repo-name>.git
       cd <repo-name>

   Or do both in one step with the [GitHub CLI](https://cli.github.com):

       gh repo create my-notes --template Ikuchar1/Sylla-Base --private --clone
       cd my-notes

2. **Run `claude`, then type `/get-started`.** It asks your name and classes, makes a
   folder per class, and walks you through downloading each syllabus and the slides
   posted so far. You download from Canvas (or whatever your school uses); Claude pulls
   the files in from your Downloads folder. Each step is checked off in `SETUP.md`, so
   you can stop and pick up later.

Run `/get-started` again at the start of each semester, or to add a class.

<details>
<summary>Setting up by hand instead</summary>

    mkdir fall-2026
    cp -R _TEMPLATE fall-2026/CS-101      # one per class

Put each syllabus in `<class>/materials/`, fill in `course.md` (`wiki-style`: `concepts`
for technical classes, `glossary` for reading-heavy ones, `sources` for seminars with
nothing to study), and fill `## About the student` and `## Current term` in `CLAUDE.md`.
Then run `/process-notes all`.
</details>

## Day to day

Always start `claude` from the repo root — that's where the commands live.

1. **In class** — run `/class-mode CS-101` and ask questions as they come up (logged to
   `sessions/`), or type notes into `lectures/YYYY-MM-DD.txt` (copy `_template.txt`).
2. **New slides posted** — download them (PDF if offered) and tell Claude "grab the new
   CS-101 slides from my Downloads". It copies them into `materials/`.
3. **After class** — `/process-notes CS-101`. Claude reads what's new, writes and links
   the wiki pages, and updates the index and log.

## Commands

| Command | What it does |
|---|---|
| `/get-started` | Setup: your name, your classes, each syllabus and the slides so far. Rerun for a new semester or to add a class. |
| `/process-notes [COURSE]` | Turns new notes, slides, and session logs into wiki pages. No argument = every class this term. |
| `/class-mode [COURSE]` | Live study partner during lecture. Short answers, logged to `sessions/`. |
| `/homework-mode [COURSE] [assignment]` | Works through an assignment with you one section at a time — explains, reviews your code, or outlines and proofreads writing. Logs where your guesses went wrong. |

Or just ask:

    grab the chapter 3 slides from my Downloads
    what's on quiz 2? teach me one topic at a time
    make a 2-page cheat sheet for exam 1
    check my answers
    quiz me on unit 1
    what did I miss?
    what's due?

## Layout

    fall-2026/
      CS-101/          one folder per class — also its own Obsidian vault
        course.md      syllabus facts: meeting times, grading, key dates
        lectures/      ← your notes (YYYY-MM-DD.txt)
        materials/     ← instructor files: syllabus, slides, readings
        assignments/   ← your own homework and drafts
        sessions/      ← class-mode and homework-mode logs
        wiki/          ← Claude writes here
          index.md  log.md  concepts/  sources/  assignments/  analyses/
    _TEMPLATE/         a blank class folder — /get-started copies it
    SETUP.md           your setup checklist
    CLAUDE.md          the rules Claude follows
    .claude/           slash commands and skills

`lectures/`, `materials/`, and `assignments/` are yours — Claude reads them but never
edits them. Everything Claude writes goes in `wiki/` or `sessions/`.

## Tips

- **PDF over PowerPoint.** Claude reads PDFs directly; a `.pptx` loses its figures when
  converted to text.
- **Files over 100 MB won't push to GitHub.** `/get-started` checks for them; add any
  later ones to `.gitignore`.
- **`## Pins`** on any wiki page is for your own corrections. Claude never overwrites them.
- **Too long? Too fast?** Say "simpler" or "slow down". How Claude talks to you is set at
  the top of `CLAUDE.md` — edit it to taste.
- **Obsidian:** open a class folder as a vault to see just that class, or the repo root
  to see everything.
- `.claude/settings.json` keeps background Claude sessions working on `main` instead of
  a separate worktree branch. Delete it if you'd rather they isolate.

## Credits and license

- Pattern: Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
- The Obsidian skills in `.claude/skills/` (`defuddle`, `json-canvas`, `obsidian-bases`,
  `obsidian-cli`, `obsidian-markdown`) are by Steph Ango
  ([kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)), MIT — see
  `.claude/skills/LICENSE-kepano-obsidian-skills`.
- Everything else: MIT — see `LICENSE`.
