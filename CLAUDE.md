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
   | 30285 Empirical Methods | calc MCQ | 5 | 3 | steps ≥ 6, concepts ≥ 2 | ≤ 5 |
   | 30024 Financial Statement Analysis | quantitative essay part | 2 | 2 | steps ≥ 4, concepts ≥ 2 | ≤ 8 |
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

**Review before creating.** Build banks with `banks/build_banks.py` (every number computed and solved a second way with an assert;
scenario sanity asserts such as "the run is not covered by liquid assets"), then run `node banks/review.js`. It applies the site's
validator and harder-rule check with each course's fingerprint and must print "20/20 pass" (or all N) before anything is written to
the Answer Grid database. Then read every key and option set yourself: check the key is not always the same letter, that distractors
come from named mistakes, and that the scheme text uses the computed numbers.

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
