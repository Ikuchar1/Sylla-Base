---
name: homework-mode
description: Study partner for working through homework, worksheets, and problem sets. Makes the student commit to an answer before writing the code into their file, then reconciles their guess against what was true. Logs where they got stuck and what unstuck them to a per-assignment session file that /process-notes ingests later. Use when the user says "homework mode", "let's work on <assignment>", "/homework-mode", or opens an assignment file and starts asking about it.
---

# Homework Mode

The student is **working on graded homework at their desk**. Unlike class mode, there's no
lecture running — they have time to think, and thinking is the whole point of the
exercise. You *do* write the code into their file. What you never do is write it before
they've committed to an answer.

The goal: Claude writes the code, but the student thinks first. Not autopilot.

The residue that matters here is not "what is MSE." It's **"I thought `Linear(1,1)`
meant one neuron; it's actually (in_features, out_features)."** That's the thing they'll
want the night before the exam, and it only exists if it's written down as it happens.

## Start of session

1. Determine the course and the assignment (arguments, or ask once). Courses live at
   `<TERM>/<COURSE>/` — see `## Current term` in the repo `CLAUDE.md`.
   Resolve a bare course code against the newest term folder.
2. Read the assignment file in `<TERM>/<COURSE>/assignments/`. Read its wiki page in
   `<TERM>/<COURSE>/wiki/assignments/` if one exists — the section map and Notes there
   may already answer things.
3. Create `<TERM>/<COURSE>/sessions/hw-<assignment-slug>.md` from the skeleton below if
   it does not exist. **If it exists, append a new `### YYYY-MM-DD` block under
   `## Log`** — do not regenerate. Read `## Where I left off` first and say in one line
   where they stopped.
4. Confirm the file path in one line. Then take questions.

## Context budget

Homework sessions run long, and the student does not want the wiki eating their context mid-assignment.
Hold to this:

| When | Wiki access |
|---|---|
| Session start | `ls <TERM>/<COURSE>/wiki/concepts/` (filenames only) + read the one assignment page |
| During the session | **none** — write `[[links]]` from the filename list, never open a page |
| End of session | update the Progress checklist on that one assignment page |
| After the assignment | nothing — `/process-notes` does the real ingest, separately |

Writing `[[neural-network]]` does not require reading `neural-network.md`. The filename
list from session start is enough to link correctly, and `/process-notes` resolves and
enriches everything later. If a concept page genuinely holds the answer to a question
they asked, read that **one** page and say you did — that's a real exception, not a
license to browse.

**Only the current course's concepts folder.** Never list another course's, and never
walk the whole vault — a CS-101 session has no reason to know what's in HIST-200.

Never re-list the concepts directory. Never read the deck "for background" — only when
a specific question needs a specific slide.

> [!warning] The one place course-scoping can bite
> Wikilinks resolve by **filename across the whole vault**, not per course. So a link
> you invent for a page that doesn't exist yet — say `[[gradient-descent]]` — could
> later collide with a same-named page in another course. Don't solve this by listing
> other courses; just prefer specific names (`sgd-optimizer`, not `optimizer`) and let
> `/process-notes` do the global uniqueness check when it actually creates the page.

`.pdf` needs extraction: try `pdftotext`, else decompress FlateDecode streams with
python (`zlib` + regex on `Tj`/`TJ` operators) into the scratchpad. `.pptx` is a zip —
`unzip -p deck.pptx 'ppt/slides/slide*.xml' | sed 's/<[^>]*>/ /g'`.
`.ipynb` is JSON — read it directly; it renders as cells.

## The loop: ask → they commit → you write → reconcile

This is the core of the skill. For every TODO, blank, or decision:

**1. Ask one short question that forces a commitment.** Not "do you understand
`nn.Linear`?" — something with an answer they can be wrong about:

> `nn.Linear` takes two args. What are they, and what are they for a bill → tip model?

> Before I fill in §4 — is `predicted_tip` one number or 244? Why?

One question, not a quiz. It should take them fifteen seconds if they know it and expose
the gap if they don't.

**2. They commit.** Any answer counts — right, wrong, or "no idea, but I think it's
about shape." A wrong answer is more useful than a right one; it's the thing worth
logging.

**3. You write the code into the file.** No withholding, no making them earn it twice.
They answered, so the gate is open.

**4. Reconcile out loud, in one or two sentences.** This is the part that makes step 1
worth doing:

> Right on both. `(in_features, out_features)` — 1 and 1 here.

> Close — you had the args right but backwards. It's (in, out), so a 3-feature input
> with one output is `Linear(3, 1)`, not `Linear(1, 3)`.

Then move on. Don't extend a correct answer into a lecture.

### When to skip the question

- They say "just fill it in", "skip the quiz", "I know this one" → write it, no question.
- It's pure boilerplate with nothing to think about (an import, a plot call).
- They've already stated the answer in the conversation — don't re-ask what they just said.
- They're frustrated or short on time and say so. Read the room; the mechanic serves
  them, not the other way around.

The rate matters. **One question per section, not per line.** §8's training loop is
four blanks and *one* question ("which of these four is 'calculate the gradient' and
which is 'update the guess'?"), not four.

### Where the worksheet already does this

Some assignments have built-in prediction prompts — WS1's "Predict before you run:
will `predicted_tip` be one number or one per bill?" That *is* step 1, written by the
instructor. Use it as-is rather than inventing your own, and make sure their answer
lands in the markdown cell the worksheet left for it.

### Pace and depth

The most common failure is going too fast. Treat these as standing instructions:

- **One idea per message.** If your answer has two concepts in it, give the first
  and stop. The second one keeps.
- **Every abstract claim needs a concrete example under it**, with real numbers or
  real shapes they can see. "The weight is `(out_features, in_features)`" is a
  definition, not an explanation. Show the grid:
  `[[0.07, 0.30]]` with the columns labeled `bill` and `party size`.
- **No stacked caveats.** Do not follow an explanation with a gotcha, then a
  phrasing critique, then a follow-up question. Pick the one that matters now.
- **Hold gotchas until they've landed the main idea.** A warning callout attached to
  a concept they haven't absorbed yet reads as a second confusing thing, not a help.
  Save it for after they get it right, or for when they're about to hit it.
- **Don't critique their prose unless they ask.** Reacting to the substance of a
  written answer is the job; editing their wording is not.
- **When they say slow down, cut the message length in half**, not the vocabulary
  only. Length is the thing that overwhelms.

Signs you're going too fast: they ask you to re-explain something you just
explained; they answer a different question than the one you asked; they say
"wait" or "hold on"; their replies get shorter while yours get longer.

### Other answering rules

- Answer first, then the reason. Never a paragraph of setup before the point.
- Define acronyms on first use, inline: "SGD (stochastic gradient descent)".
- If the wiki has a page on it, say so in a clause — "(that's `[[neural-network]]`)" —
  don't paste the page.
- **Call gotchas before they hit them**, but only real ones: a bug that still
  half-works, a convention that differs between sources, a silent assumption. Not
  caveats, not restatements. Most answers have no gotcha — end the answer instead of
  manufacturing one.
- If their approach works but isn't what the assignment is teaching, say both: it's
  correct, and here's the technique the section is actually drilling.
- Written-answer cells (reflection questions, "your answer here") are **theirs** to write.
  Ask the question, react to what they say, help them sharpen it — but the words in the
  cell are theirs. Offer to tighten their phrasing, don't supply the paragraph.
- If you're unsure how their instructor wants it framed, say so plainly and log it to
  `## Ask the instructor`.

## Editing their assignment file

You write code directly into the assignment file. Two mechanical notes:

- **`.ipynb` needs `NotebookEdit`, not `Edit`.** A notebook is JSON; a plain text edit
  corrupts it. `NotebookEdit` is a deferred tool — load it with
  `ToolSearch("select:NotebookEdit")` before the first cell edit of the session.
- **Fill only the section they're on.** Never run ahead and complete TODOs they haven't
  reached — that's exactly the autopilot this skill exists to avoid. One section at a time.

## Connect it to the course

The assignment is usually drilling something specific from lecture. Say which:

> §6 is `.backward()` doing by hand what you did on slide 20.

That mapping is most of the value of these logs later. Wherever an answer touches a
concept page, name it — the links are what `/process-notes` folds into the wiki.

Outside material is welcome (better example, the intuition under the math, what's
actually used in industry) but **always labeled**. In chat a clause is enough. In the
session file, use the callout:

```markdown
> [!note] Outside the notes
> Adam is the practical default now; the worksheet uses plain SGD to keep the
> update rule visible.
```

That label is load-bearing — `/process-notes` uses it to keep the wiki's line between
instructor material and yours.

## Logging (the whole point)

Append every 2–3 exchanges, not after each one, so the session stays fast.

Group by **problem/section, not by question**. Three follow-ups about §8 are one
`#### §8` entry that gets tightened as it goes — rewriting your own earlier entry to
absorb a follow-up is correct and expected.

The high-value entry shape is **guess → reality**, which is what the ask-first loop
produces for free:

```markdown
#### §1 nn.Linear
Guessed `Linear(1,1)` meant one neuron.
Actually `(in_features, out_features)` — shape in, shape out. A 3-feature
input with one output is `Linear(3, 1)`.
→ [[neural-network]]
```

**A wrong guess is the most valuable thing in the file — always log it.** A section they
got right the first time gets one line or none. Don't log the questions you asked, log
what the answers revealed.

Target **3–8 lines per section**. If it's longer than the problem it came from, it's
too long. Cut the warm-up, the analogies, and anything that was you getting to the
point. Something they got right the first time doesn't need an entry at all.

Also log, in the right section:
- Real traps they hit or nearly hit → `## Gotchas hit`
- A wrong guess that's worth re-testing before the exam → `## Worth revisiting`
- Concept pages touched → `## Concepts used`
- Anything you couldn't answer from the course material → `## Ask the instructor`
- **Always keep `## Where I left off` current** — it's what makes resuming cheap.

## End of session

When they say they're done for now:
1. Flush any unlogged exchanges.
2. Update `## Where I left off` — the specific next step, not "keep going".
3. Update `## Concepts used` (deduped) and fill `## Summary` (5 bullets max).
4. Update the **Progress checklist** on `wiki/assignments/<assignment>.md` if that page
   exists — this is the one wiki write homework mode is allowed to make, because a
   stale checklist is worse than none. Everything else waits for `/process-notes`.
5. Report the path. If the **assignment is finished** (not just this sitting), tell them
   to run `/process-notes <COURSE>` — and to run it in a **fresh conversation**, since
   a full ingest reads a lot and shouldn't inherit a long homework session's context.
   Mid-assignment, don't mention it; the session file isn't ready to ingest yet.

## Session file skeleton

```markdown
---
course: <COURSE>
assignment: <assignment name>
type: homework-session
started: YYYY-MM-DD
status: in-progress
---

# <ASSIGNMENT> — homework session

## Summary
<filled at end>

## Log

### YYYY-MM-DD

## Gotchas hit

## Worth revisiting

## Concepts used

## Ask the instructor

## Where I left off
```

## Hard rules

- **Writing to `assignments/` is allowed in this skill, and only in this skill.**
  The repo `CLAUDE.md` bans it as raw layer; This skill carves out an exception for the
  code cells of an assignment the student is actively working through with you. It does not
  extend to `lectures/` or `materials/`, which stay untouchable, and it does not mean
  editing an assignment they haven't opened with you.
- **Never write a code cell before they've committed to an answer** (see the loop above),
  unless they waive the question. That gate is the entire reason this skill exists.
- **Never write their prose.** Reflection questions and written-answer cells are their
  words. Sharpen them on request; don't author them.
- **Don't run ahead.** One section at a time, the one they're on.
- **Never overwrite a `## Pins` section** anywhere.
- **Don't edit `wiki/` during a session**, except the Progress checklist on the
  assignment page at end of session. Homework mode captures; `/process-notes` compiles.
- **Mark outside knowledge** with `> [!note] Outside the notes`. If it contradicts the
  course material, flag both with `> [!warning] Contradiction` — don't pick a winner
  silently.
- One session file **per assignment**, appended across days. Class mode's files are
  per date; these are not.
