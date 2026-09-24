# Answer Grid: rules for creating questions

This repo holds **Answer Grid**, a static exam-practice website (`index.html`, `js/`, `css/`, `data/`).
Questions come from Claude (in Cowork or here) as bank files that the site imports.

## The harder rule (guardrail: review this before creating any question)

Will's instruction (24 Sep 2026): **the exam is harder than the slide material, so every question Claude writes must be harder than the slides.**
Course 30178 stores it in `courses/30178.fingerprint.hard_target`:

> harder than the slides: steps above the slide maximum AND above the exam-level median for the shape,
> at least two distinct notches, never via ambiguity or out-of-syllabus content

Before writing a generated question, and again before handing it over, check every point below.
If any point fails, fix the question or drop it. Do not relabel it or lower the bar.

1. **Label.** `difficulty: "hard"`. `exam` and `exam+1` are not enough for generated questions.
2. **Steps, per answer part.** Count the steps a student must take for each sub-question.
   The count must be **above** the slide maximum and **above** the exam median for its shape, and at least the hard target:
   | Shape class | Slide max | Exam median | Each answer needs |
   |---|---|---|---|
   | exercise part (any `shape` containing "exercise") | 3 | 3 | steps ≥ 4, concepts ≥ 2 |
   | concept MCQ (everything else) | — | 1.5 | steps ≥ 2.5, concepts ≥ 2 |
   (30178 values.) The other subjects' thresholds (PROXY, scored on 2026-09-24 from each course's own mock/practice exam and slide examples):
   | Course | Shape class | Slide max | Exam median | Each answer needs | Minutes per answer |
   |---|---|---|---|---|---|
   | 30257 Corporate Valuation | short problem (written) | 6 | 5.5 | steps ≥ 7, concepts ≥ 2 | ≤ 10 |
   | 30257 Corporate Valuation | concept MCQ | — | 1.5 | steps ≥ 3, concepts ≥ 2 | ≤ 10 |
   | 30285 Empirical Methods | calc MCQ | 5 | 3 | steps ≥ 6, concepts ≥ 2 | ≤ 5 |
   | 30024 Financial Statement Analysis | quantitative essay part | 2 | 2 | steps ≥ 4, concepts ≥ 2 | ≤ 8 |
   | 30024 Financial Statement Analysis | concept MCQ | — | 3 | steps ≥ 4, concepts ≥ 2 | ≤ 8 |
   | 30024 Financial Statement Analysis | qualitative essay part | 3 | 3 | steps ≥ 5, concepts ≥ 2 | ≤ 8 |
   Always read the course's own `fingerprint` in the Answer Grid database first: it wins over this table.
3. **Notches.** Use at least **2 distinct** ones from this list: `extra_step`, `extra_classification`, `working_backwards`,
   `cross_section`, `what_if_followon`, `extraneous_data`, `chain`, `near_true_statements`.
4. **Time.** `est_minutes ÷ number of answer parts ≤ 4.5` (the course's `minutes_per_answer_cap`).
5. **No ambiguity.** Each part has exactly one defensible answer. Solve the key twice (`answer_status: "double-solved"`); never ship `unverified`.
6. **In syllabus.** Everything needed is in the slides or syllabus. Cite at least one slide in `citations` (quotes ≤ 25 words).
7. **Record the review** on the question so the site can check it:
   ```json
   "hard_check": {
     "shape_class": "exercise part",
     "parts": [{"n": "3.1", "steps": 5, "concepts": 2}, {"n": "3.2", "steps": 4, "concepts": 2}],
     "notches": ["extra_classification", "working_backwards", "chain"],
     "no_ambiguity": true,
     "in_syllabus": true
   }
   ```

**Source rule (agreed 2026-09-24).** Every real past-paper, problem-set or instructor-sample question that fits the current
syllabus goes in, copied word for word from the PDF text layer (`source.type: "real"`, `verbatim_verified: true`). Keys are
official where the source prints one; otherwise solve twice and mark `double-solved`, and say in the mark scheme that the source
has no key. If the text layer is garbled and the item has to be rebuilt, it is `adapted`, not verified, and carries a
`source.check` note for Will. Claude-written mocks and RemNote decks are never evidence. Generated questions only fill gaps.

**Coverage rule.** Each deck is split into sections and units (`banks/c30178.py`: `SECTIONS`, `UNITS`). Every examinable unit
needs at least one question (`q.units`); non-examinable units state why. Every section needs a Hard question whose first
`slide_group` is that section. Every source file and item has a ledger decision (`LEDGER`: included, held, duplicate, excluded…,
with a reason). The site shows this as the **Coverage** panel in each deck folder.

**Review before creating.** Run `python3 banks/build_banks.py` (every number computed and solved a second way with an assert),
then `node banks/review.js`. It checks every bank question (validator, key self-check, harder rule for generated questions,
verbatim for real ones) and then the coverage rule for each course with a coverage block. It exits non-zero on any gap, and
nothing is written to the Answer Grid database until it passes. Then read every key and option set yourself.

The site applies the same rule (`reviewHarder` in `js/logic.js`). **Imports block** any generated question that fails it or
has no `hard_check`. Real and adapted course questions are exempt, because they are the evidence the rule is measured against.

## Bank file format

A JSON array of questions, or `{"courses": [...], "questions": [...]}`. Each question needs:
`id` (`<course>-<deck>-NN`), `course`, `deck`, `topic`, `syllabus_objective`, `shape`, `stem`, optional `data` (Markdown table),
`source {type: real|adapted|generated, file, location, label, verbatim_verified, transcribed_from_image, page_snapshot_asset}`,
`marks`, `subquestions [{n, prompt, options[], marks}]`, `answer_key [{n, answer (letter or text), answer_status}]`,
`mark_scheme [string]`, `error_tags [{tag, trap: "<n>:<letter> …"}]`, `citations [{deck, slide, quote}]`, `slides [int]`,
`slide_groups [section id]`, `est_minutes`, `difficulty (exam|exam+1|hard)`, `created_at`, and `hard_check` for generated questions.

## Working on the code

- No build step. Open `index.html` directly or serve the folder (`python3 -m http.server`).
- Pure logic lives in `js/logic.js` and is tested with `node --test tests/logic.test.js`. Run the tests before committing.
- `data/seed.js` is the bundled 30178 bank and progress, exported from the original Answer Grid artifact.
