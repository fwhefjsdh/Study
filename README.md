# Answer Grid

Spaced-repetition practice for exam questions, as a website you can open in any browser.
It is built from the Answer Grid Claude artifact and comes with the 30178 International Banking bank (30 questions and your progress so far).

**Use it:** the site runs as your private Answer Grid artifact on claude.ai, at https://claude.ai/artifact/Y7qKUys3BN7prnBe6q2gXL.
There, data lives in the artifact's database (the one Cowork writes to), so it works on any device, and Claude marking uses your claude.ai account.
`python3 tools/build-artifact.py` builds the single-file page (`dist/answer-grid-artifact.html`) that is published there.

Opening `index.html` directly also works as a standalone, offline copy. Its data stays in that one browser, and it starts from the bundled bank.

## What it does

- **Queue.** Due cards ranked by exam proximity, priority and overdue days. Press <kbd>Enter</kbd> to start.
- **Answering.** Choose options with <kbd>A</kbd>–<kbd>D</kbd> (it moves to the next part automatically), write your reasoning, sketch working, then submit with <kbd>Enter</kbd>.
  Unsubmitted answers are kept as drafts. After you submit, the key, mark scheme, traps you hit and sources are shown. Rate yourself with <kbd>1</kbd>–<kbd>4</kbd> and press <kbd>Enter</kbd> for the next card.
- **Marking.** Multiple-choice parts are marked from the key. For written reasoning, add an Anthropic API key in Settings and Claude marks it (Claude Opus 5 by default); without a key you mark yourself.
- **Scheduling.** Three counted corrects archive a card (3 then 7 days, or 4 then 10 with Easy). Reviews are capped two days before the exam, and a final review brings archived cards back.
- **Harder rule.** Every generated question is checked against the course's rule: *harder than the slides, with more steps than the slide maximum and the exam median, at least two notches, and never harder through ambiguity or out-of-syllabus content.*
  Imports block questions that fail. The Courses screen shows the thresholds, Browse filters by status, and each question has a review form. See `CLAUDE.md`.
- **Exports** of attempted questions:
  - **One question:** *Export* on the answer screen (<kbd>E</kbd>) or in Browse.
  - **A group:** tick questions in Browse, then *Export…* in the bar at the bottom.
  - **A whole folder:** *Export folder…* in a deck folder, or *Export subject…*.
  - **Today's session:** from the Queue.

  Formats: Markdown, a print view (save as PDF), a zipped folder with one file per question plus sketches, CSV, and re-importable JSON.
  You choose attempted-only or everything; all, latest, today's or no attempts; and whether to include the key and sources.

## Development

```
python3 -m http.server   # then open http://localhost:8000
node --test tests/logic.test.js
```
