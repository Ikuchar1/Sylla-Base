# Class Notes Template

A [Karpathy-style LLM wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
for coursework, built for [Claude Code](https://claude.com/claude-code) and
[Obsidian](https://obsidian.md). You type raw notes and drop in the instructor's slides;
Claude compiles them into an interlinked wiki of concept pages you can study from,
quiz yourself on, and ask questions against.

## What you need

- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)
- [Obsidian](https://obsidian.md) (optional, but it's how you browse the wiki)
- `pdftotext` (optional, makes reading PDFs faster): `brew install poppler`

## Setup

1. **Get a copy.** Click **Use this template** on GitHub to make your own repo
   (keep it private — it'll hold your coursework), then clone it:

       git clone https://github.com/<you>/<your-notes-repo>.git Notes
       cd Notes

2. **Add a term and your courses.** One folder per term, one per course:

       mkdir fall-2026
       cp -R _TEMPLATE fall-2026/CS-101
       cp -R _TEMPLATE fall-2026/HIST-200

3. **Fill in each `course.md`** — meeting days, grading, exam dates ("what did I miss?"
   checks against them), plus two settings: `section` (so Claude skips requirements for
   other sections, like grad-only work) and `wiki-style` — `concepts` for technical
   courses, `glossary` for reading-heavy ones where one page per term would mean
   hundreds of files.

4. **Edit `CLAUDE.md`** — fill in `## Current term` with your course list and
   `## About the student` with how you like things explained.

5. **Open in Obsidian.** Each course folder is its own vault (**Open folder as vault** →
   `fall-2026/CS-101`) showing only that class. The repo root is also a vault if you
   want to see everything at once.

## Daily workflow

1. **In class** — type notes into `<TERM>/<COURSE>/lectures/YYYY-MM-DD.txt`
   (copy `_template.txt` to start), or run `/class-mode CS-101` and ask questions live.
   That logs to `<TERM>/<COURSE>/sessions/`.
2. **After class** — drop the slide deck into `<TERM>/<COURSE>/materials/`, ideally as PDF.
3. **Process** — run `claude` **from the repo root** (the skills live there), then:

       /process-notes CS-101

   Claude reads what's new, writes concept pages, links them, and updates the index and log.

## Commands

| Command | What it does |
|---|---|
| `/process-notes [COURSE]` | Ingest new lectures, decks, and session logs into the wiki. No argument = every course this term. |
| `/class-mode [COURSE]` | Live study partner during lecture. Short answers, logged to `sessions/`. |
| `/homework-mode [COURSE] [assignment]` | Works through an assignment with you, one section at a time. Explains and reviews your code, or writes TODO cells when you ask. For writing: outlines with word counts, reference drafts, minimal proofreading. Logs where your guess was wrong. |

Then just ask:

    grab the chapter 3 slides from my Downloads
    what's on quiz 2? teach me one topic at a time
    make a 2-page cheat sheet for exam 1
    check my answers
    quiz me on unit 1
    what did I miss?
    what's due?

## Layout

    fall-2026/
      CS-101/
        .obsidian/     this course's vault
        course.md      syllabus facts
        lectures/      ← you write here (raw .txt)
        materials/     ← instructor files go here
        assignments/   ← your own drafts and submitted work
        sessions/      ← Claude's class-mode / homework-mode logs
        wiki/          ← Claude writes here
          index.md  log.md  concepts/  sources/  assignments/  analyses/
    _TEMPLATE/         copy this to add a course
    CLAUDE.md          the rules Claude follows
    .claude/           slash commands and skills

`lectures/`, `materials/`, and `assignments/` are the raw layer — Claude reads them but
never edits them. Everything Claude writes goes in `wiki/` or `sessions/`.

## Tips

- **Export PowerPoints to PDF.** Claude reads PDFs directly; `.pptx` is a zip archive
  that loses figures and slide order when converted to text. Files over 100 MB won't
  push to GitHub — add them to `.gitignore`.
- **Name lecture files `YYYY-MM-DD`** — the only date format that sorts as text.
- **`## Pins`** on any wiki page is for your own corrections. Claude never overwrites them.
- **Too long? Too fast?** Say "simpler", "slow down", or "one step at a time" — the
  skills are built to cut length and lead with an example. How Claude talks to you is set
  at the top of `CLAUDE.md`; edit it to taste.
- `.claude/settings.json` keeps background Claude sessions editing on `main` instead of a
  separate worktree branch. Delete it if you'd rather they isolate.
- **Wikilinks stay within one course.** Concept filenames still need to be unique across
  the whole repo (`social-norm.md`, not `norm.md`) so they don't collide in the root vault.

## Credits

- Pattern: Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
- Obsidian skills in `.claude/skills/` (`defuddle`, `json-canvas`, `obsidian-bases`,
  `obsidian-cli`, `obsidian-markdown`) are by Steph Ango
  ([@kepano](https://github.com/kepano/obsidian-skills)), MIT — see
  `.claude/skills/LICENSE-kepano-obsidian-skills`.
