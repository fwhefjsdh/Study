"""30024 Financial Statement Analysis: source intake, deck units and the questions that fill the gaps.

Same rules as c30178.py / c30257.py: real questions first, word for word; keys official where printed, otherwise
solved twice; generated Hard questions only for gaps; every source item in the ledger.

Exam format (syllabus 2026-27, section 6): "a mix of open essay questions (with and without calculations), and multiple
choices". The bank therefore carries three shapes: concept MCQs, quantitative essay parts and qualitative essay parts,
each with its own harder-rule thresholds (MCQ_SHAPE, QUAL_SHAPE below; the quantitative shape is in build_banks.py).

Decks in the folder: Session 1 (intro and cases) plus the Session 1 accounting-refresh handout, Session 2 (accounting
basics and the statements), Sessions 3-4 (reclassification). Everything taught later (ratio analysis, earnings quality,
forecasting, going concern, valuation) waits for its deck.
"""
from build_banks import mcq, written, question, cite, f, r, near, CREATED, L

C = "30024"
F_S1 = "Slides/30024 - AM - Session 1 - Intro.pdf"
F_S1T = "Session 1 - Accounting Refresh - TEXT.pdf"
F_S2 = "Slides/30024 - AM - Session 2.pdf"
F_S34 = "Slides/30024 - AM - Session 3 - 4 Reclassification.pdf"
F_SYL = "30024 - 2026-27 Syllabus FSA - Final.pdf"
F_M23 = "Exam Material/[studocu.com] - 30024 FINANCIAL STATEMENT ANALYSIS MOCK EXAM PART A & B 2023.pdf"
F_M23C = "Exam Material/Clean/[studocu.com] - 30024 FINANCIAL STATEMENT ANALYSIS MOCK EXAM PART A & B 2023.pdf"
F_P17 = "Exam Material/[studocu.com] - Soluzioni Prova Generale 30024 - 30 Maggio 2017.pdf"
F_P17C = "Exam Material/Clean/[studocu.com] - Soluzioni Prova Generale 30024 - 30 Maggio 2017.pdf"
NEG = None  # not known yet: the exam direction sheet (late November) will say
TEXTCHK = "text checked word for word against the PDF text layer on 2026-09-24"
ANNOT = "; the uploader's page notes in the Studocu copy (e.g. 'PAG 7', 'FEBRUARY 2') are left out"

MCQ, QUANT, QUAL, MULTI = "concept MCQ", "quantitative open essay (written parts)", "qualitative open essay (written)", "short answer (select all that apply)"


def s_mcq(n, prompt, options, letter, status="double-solved", marks=1):
    assert letter in L[:len(options)]
    return ({"n": n, "prompt": prompt, "options": options, "marks": marks}, {"n": n, "answer": letter, "answer_status": status}, [])


def s_written(n, prompt, answer, marks="UNKNOWN", status="double-solved"):
    return ({"n": n, "prompt": prompt, "options": [], "marks": marks}, {"n": n, "answer": answer, "answer_status": status}, [])


def realq(**kw):
    parts = kw.pop("parts")
    marks = [p[0]["marks"] for p in parts]
    q = {"id": kw["id"], "course": C, "deck": kw["deck"], "topic": kw["topic"], "syllabus_objective": kw["objective"],
         "shape": kw["shape"], "stem": kw["stem"], "data": kw.get("data"), "difficulty": "exam",
         "source": {"type": kw.get("type", "real"), "file": kw["file"], "location": kw["location"], "label": "SUPPORTING",
                    "verbatim_verified": kw.get("verbatim", True), "transcribed_from_image": False, "page_snapshot_asset": None},
         "subquestions": [p[0] for p in parts], "answer_key": [p[1] for p in parts], "error_tags": [],
         "marks": round(sum(marks), 2) if all(isinstance(m, (int, float)) for m in marks) else "UNKNOWN",
         "mark_scheme": kw["scheme"], "citations": kw["cites"], "slides": [], "slide_groups": kw["groups"],
         "units": kw["units"], "est_minutes": kw["minutes"], "created_at": CREATED, "negative_marking": NEG}
    if kw.get("check"):
        q["source"]["check"] = kw["check"]
    if q["data"] is None:
        del q["data"]
    return q


REAL, HARD = [], []

# ================================================================================================
# REAL: Session 1 accounting-refresh handout (instructor exercise; no key printed, so every key is solved twice)
# ================================================================================================
REF_STEM = ("On January 01st, 2021, Outstanding Inc – an online fashion company – owned by 3 friends, starts its tenth year of operations. "
            "During the year, they complete the following business-related activities that need to be recorded.")
REF_LOC = "Session 1 accounting-refresh handout (instructor exercise for the in-class check), question {}; " + TEXTCHK


def refq(id, n, topic, obj, prompt, parts, scheme, units, cites, minutes=2, shape=MCQ, check=None):
    REAL.append(realq(id=id, deck="S1", topic=topic, objective=obj, shape=shape, file=F_S1T, location=REF_LOC.format(n),
                      stem=REF_STEM + "\n\n" + prompt, parts=parts, scheme=scheme, cites=cites, groups=["S1C"], units=units,
                      minutes=minutes, check=check))


# Q1: 3,000 old shares; the new friend gets 25% of the votes -> 1,000 new shares at par 50
new_sh = 3000 * 0.25 / 0.75
near(new_sh, 1000)
cs_q1, pic_q1 = new_sh * 50, 85000 - new_sh * 50
near(cs_q1, 50000); near(pic_q1, 35000); near(45000 + 40000, cs_q1 + pic_q1)
q1 = ("1. On January 1st they issue new shares to let one more friend (Marc) join the company. Existing shares are as follows: 3,000 shares with a par value of $50 each "
      "(each shareholder owns 1,000 shares). They have agreed on the following: the new shareholder will have 25% of the voting rights, and the total consideration "
      "agreed for the new share issue is $85,000. Marc will give 45,000 in cash and a small building portion (a warehouse) that will be used by the firm to store "
      "products whose value has been estimated to be $40,000. Which of the following recordings is wrong? (There may be more than one correct answer)\n\n"
      "a. Debit Cash for 45.000 and Debit Building for 40.000\nb. Credit Common Stock for 35.000\nc. Credit Paid in Capital for 50.000\nd. Credit Paid in Capital for 35.000")
refq("30024-S1-10", 1, "Share issue for cash and a building", "Accounting refresh: recording a share issue (par value, paid-in capital, contribution in kind)", q1,
     [s_written("1", "Write the letter(s) of every wrong recording.", "b and c")],
     ["Answer: b and c (no key in the handout; solved twice).",
      "Route 1: 25% of the votes after the issue → new shares = 3,000 × 25/75 = 1,000; Common Stock = 1,000 × $50 = $50,000; Paid-in Capital = 85,000 − 50,000 = $35,000. So a and d are right and b and c are wrong.",
      "Route 2: debits 45,000 + 40,000 = 85,000 must equal the credits 50,000 + 35,000: the only split that balances with 1,000 shares at par is CS 50,000 / PIC 35,000.",
      "Trap: 25% of the existing 3,000 shares (750 shares) — 25% of the votes means 25% of the shares after the issue."],
     ["S1-U10"], [cite("S2", "Statement of shareholders’ equity", "Ending equity = Beginning equity + Profit or loss + Other comprehensive income + Owner contributions − Distributions to owners")],
     minutes=3, shape=MULTI)

# Q2: bond issued at par 1 Jan 2022, 5%, paid each 1 Jan from 2023
near(150000 * 0.05, 7500)
q2 = ("2. On January 1st 2022, Outstanding Inc issues a 5-year bond at par value for a total of $150,000. The interest rate is 5% annual and payments are made once a "
      "year each January 1st starting from the next period (January 1st, 2023). Select the correct recording (There may be more than one correct answer).\n\n"
      "a. Register cash outflow on the 1st of January 2022\nb. Register Interest Payable on the 31st of December 2022\nc. Register Interest Payable on the 1st of January 2022\n"
      "d. Register Interest Expense on the 31st of December 2022")
refq("30024-S1-11", 2, "Bond issue and accrued interest", "Accounting refresh: accrued expenses (interest incurred, paid next period)", q2,
     [s_written("1", "Write the letter(s) of every correct recording.", "b and d")],
     ["Answer: b and d (no key in the handout; solved twice).",
      "Route 1: issuing a bond brings cash in (a is wrong: it is an inflow). By 31 Dec 2022 one year of interest ($150,000 × 5% = $7,500) has been incurred but is paid on 1 Jan 2023: Dr Interest Expense 7,500 / Cr Interest Payable 7,500 (b and d).",
      "Route 2: on 1 Jan 2022 no interest has accrued yet, so c is wrong. The accrued-expense slide: expense incurred now, cash paid next period → expense and a payable."],
     ["S1-U11"], [cite("S2", "Accounting distortions: accrued and deferred revenues and expenses", "The company has incurred an expense but the cash will be paid in the next period.")],
     minutes=2, shape=MULTI)

q3 = ("3. On January 1st they paid rent for their main office for a total amount of 20.000 for the entire\n\nyear 2021. Select the correct recording (There may be more than one correct answer).\n\n"
      "a. Debit Rent Expense for 20.000 and Credit Bank for 20.000\nb. Debit Pre-Paid Rent for 20.000 and Credit Rent Payable for 20.000\n"
      "c. Debit Rent Expense for 20.000 and Credit Rent Payable for 20.000\nd. Debit Pre-Paid Rent for 20.000 and Credit Bank for 20.000")
refq("30024-S1-12", 3, "Rent paid in advance", "Accounting refresh: pre-paid expenses", q3,
     [s_written("1", "Write the letter(s) of every correct recording.", "a and d")],
     ["Answer: a and d (no key in the handout; solved twice).",
      "Route 1 (pre-paid expense, the slide's treatment): cash is paid before the expense is incurred → Dr Pre-Paid Rent 20,000 / Cr Bank 20,000 (d); the asset is then expensed month by month during 2021.",
      "Route 2: the whole prepayment is used up within the same financial year (2021), so booking it straight to Rent Expense against Bank (a) gives the same 2021 statements. b and c credit a payable, but the rent was paid in cash.",
      "The handout says more than one answer may be correct; a and d are the two that credit Bank."],
     ["S1-U12"], [cite("S2", "Accounting distortions: accrued and deferred revenues and expenses", "The payment is initially recorded as an asset, which is reduced as the related goods or services are consumed")],
     minutes=2, shape=MULTI,
     check="Key a and d: d is the textbook pre-paid entry; a is accepted because the rent covers exactly the 2021 financial year. If the in-class answer was d only, change it.")

nbv = 400000 - 175000
near(200000 - nbv, -25000)
refq("30024-S1-13", 4, "Sale of a shop below book value", "Accounting refresh: disposal of a non-current asset (gain or loss)",
     "4. On January 1st the company sells a shop in south Philly it owned. The shop’s selling price (accounted as Building) is $200,000 and is collected in cash on the same day. "
     "The gross value and the cumulated depreciation of the shop on January 1st were $400,000 and 175,000 respectively. Which of the following items has to be recorded in the Income Statement?",
     [s_mcq("1", "Which of the following items has to be recorded in the Income Statement?",
            ["Increase in Revenues for 200.000", "Gain on Sale for 25.000", "Increase in Cash for 200.000", "Loss on Sale for 25.000"], "D")],
     ["Answer: D (no key in the handout; solved twice).", "Route 1: net book value = 400,000 − 175,000 = 225,000; price 200,000 → loss of 25,000 in the income statement.",
      "Route 2: Dr Cash 200,000, Dr Accumulated depreciation 175,000, Dr Loss 25,000 / Cr Building 400,000. A treats a disposal as revenue; C is a balance-sheet item; B reverses the sign."],
     ["S1-U13"], [cite("S2", "The Balance Sheet: Non - Current Assets (optional)", "tangible assets are carried at cost less accumulated depreciation and accumulated impairment losses")])

near(150000 * 0.4, 60000); near(150000 * 0.6, 90000)
refq("30024-S1-14", 5, "Inventory bought partly on a note", "Accounting refresh: purchase of inventory (asset, not expense)",
     "5. On March 1st Outstanding Inc purchases inventory for a total amount of $150.000 (they buy 5.000 shirts at a standard price of $30 each). "
     "They pay 40% on the same day through cash and issue a 12-month note payable for the remaining 60%. Select the correct recording.",
     [s_mcq("1", "Select the correct recording.",
            ["Debit Inventory for 150.000. Credit Bank for 60.000 and Note Payables for 90.000", "Debit Cost of Goods Sold for 150.000. Credit Bank for 60.000 and Note Payables for 90.000",
             "Debit Bank for 60.000 and Note Payables for 90.000. Credit Inventory for 150.000", "Debit Bank for 60.000 and Note Payables for 90.000. Credit Sales Revenue for 150.000"], "A")],
     ["Answer: A (no key in the handout; solved twice).", "Route 1: buying goods creates an asset (inventory), expensed as COGS only when sold; cash 40% = 60,000, note 60% = 90,000.",
      "Route 2: debits must be the asset received; C and D reverse the entry; B expenses unsold goods."],
     ["S1-U14"], [cite("S2", "The Balance Sheet: Current Assets (optional)", "Under IAS 2, inventories are measured at the lower of cost and net realisable value.")])

refq("30024-S1-15", 6, "Cash collected before delivery", "Accounting refresh: unearned revenue (contract liability)",
     "6. On October 1st, Outstanding Inc signs a contract to supply 200 shirts during the period February to April 2022. The total amount for the 200 shirts is $25,000 "
     "and is all collected in advance on Oct 1st, 2021. Which of the following items must be credited in this transaction?",
     [s_mcq("1", "Which of the following items must be credited in this transaction?",
            ["Credit Cash for 25.000", "Credit Unearned Revenue for 25.000", "Credit Sales Revenue for 25.000", "Credit Other Revenue for 25.000"], "B")],
     ["Answer: B (no key in the handout; solved twice).", "Route 1: cash received before the performance obligation is satisfied → Dr Cash / Cr Unearned Revenue (a liability).",
      "Route 2: revenue is recognised when control of the goods passes (February–April 2022), so C and D are premature; cash is debited, not credited (A)."],
     ["S1-U15"], [cite("S2", "Accounting distortions: accrued and deferred revenues and expenses", "Cash is received before the related revenue is earned; therefore, a liability is initially recognised.")])

near(300000 * 0.2, 60000)
refq("30024-S1-16", 7, "Receivables from credit sales", "Accounting refresh: revenue on credit and accounts receivable",
     "7. Total sales – for the entire year – for Outstanding Inc are $300,000 and they sold 3,000 shirts at an average price of $100 (80% of the sale price is collected in "
     "cash at the sale date, and the remaining 20% will be collected in 2022). On the 31st of December, which would be the total amount of Accounts Receivable?",
     [s_mcq("1", "On the 31st of December, which would be the total amount of Accounts Receivable?", ["30.000", "300.000", "60.000", "90.000"], "C")],
     ["Answer: C (no key in the handout; solved twice).", "Route 1: 20% × 300,000 = 60,000 still to be collected.", "Route 2: 300,000 − cash collected 240,000 = 60,000."],
     ["S1-U16"], [cite("S2", "Accounting distortions: accrued and deferred revenues and expenses", "The company has earned revenue but the cash will be received in the next period.")], minutes=1)

# ================================================================================================
# REAL: 2023 mock exam, Part A (attending) and Part B (non-attending) — Studocu copy, no answers printed
# ================================================================================================
M23_LOC = "30024 mock exam 2023 (Studocu copy), {}; " + TEXTCHK


def m23(id, where, deck, topic, obj, prompt, options, letter, groups, units, cites, scheme, minutes=2):
    REAL.append(realq(id=id, deck=deck, topic=topic, objective=obj, shape=MCQ, file=F_M23, location=M23_LOC.format(where) + ANNOT,
                      stem=prompt, parts=[s_mcq("1", prompt, options, letter)], scheme=scheme, cites=cites, groups=groups, units=units, minutes=minutes))


m23("30024-S2-10", "Part A, MC4", "S2", "US GAAP and IFRS", "Accounting standards: purpose, convergence, IFRS vs US GAAP",
    "MC4. Which of the following statements about the differences between US GAAP and IFRS is true?",
    ["US GAAP are principle based, while IFRS are rule based", "US GAAP prohibit LIFO, while IFRS do not",
     "US GAAP are used only in North America, while IFRS in more than 166 countries (as of 2020)", "IFRS require a higher level of professional judgement than US GAAP"], "D",
    ["S2A"], ["S2-U5", "S2-U12"],
    [cite("S2", "Reasons for accounting standards’ alignment", "The two most commonly used accounting standards all over the world are US GAAP and IFRS."),
     cite("S2", "The Balance Sheet: Current Assets (optional)", "FIFO and weighted-average cost are permitted; LIFO is prohibited under IFRS Accounting Standards.")],
    ["Answer: D (no key in the source; solved twice).",
     "Route 1: A is reversed (IFRS are principles-based, US GAAP rules-based); B is reversed (IFRS prohibit LIFO, per the Session 2 slide; US GAAP allow it); C is false (US GAAP is not used 'only' in North America as a matter of rule and is the standard for SEC filers worldwide).",
     "Route 2: principles-based standards leave more to the preparer, so IFRS need more professional judgement — D."])
m23("30024-S2-11", "Part A, MC6", "S2", "What must be disclosed", "The role of financial information: cost constraint, materiality, relevance",
    "MC6. Which of the following statements about disclosure is false?",
    ["A firm must disclose all information that is material, even if the costs of providing such information are higher than the benefits",
     "One benefit of voluntary disclosure is the possible decrease of cost of capital", "The Management, Discussion & Analysis is a “narrative form” of financial statements",
     "If the information is old, its relevance is lost"], "A",
    ["S2A"], ["S2-U4", "S2-U5"],
    [cite("S2", "The role of financial information", "The benefits of providing financial reporting information should justify the costs of providing and using that information.")],
    ["Answer: A (no key in the source; solved twice).",
     "Route 1: the Session 2 slide calls cost 'a pervasive constraint': benefits should justify the costs, so 'even if the costs are higher than the benefits' is false.",
     "Route 2: B matches the slide on comparability/transparency lowering the cost of capital; C and D describe the MD&A and timeliness, both standard."])
m23("30024-S2-12", "Part A, MC9", "S2", "Financial vs managerial accounting", "Financial vs managerial accounting",
    "MC9. Which of the following statements about the differences between financial accounting and managerial accounting is false?\n\n"
    "I. Evaluating the company and its management are primary objectives of financial accounting; running the company is a primary objective of managerial accounting\n"
    "II. Financial accounting relates to period disclosure about financial information; management accounting relates to performance reports",
    ["I", "I and II", "II", "None of the statements is false (i.e., I, II, and III are true)"], "D",
    ["S2A"], ["S2-U3"],
    [cite("S2", "Financial vs Managerial Accounting: a different perspective", "Objectives Evaluating the company - Running the company")],
    ["Answer: D (no key in the source; solved twice). The option text says 'I, II, and III' although there are only two statements; kept as printed.",
     "Route 1: the Session 2 table gives financial accounting the objective 'evaluating the company / its management' and managerial accounting 'running the company' — I is true.",
     "Route 2: the same table: financial accounting = periodic financial statements and disclosures; managerial = budgets, cost analyses, performance reports — II is true. Nothing is false."])
m23("30024-S2-13", "Part A, MC13", "S2", "Investor styles", "Users of financial information: investment styles",
    "MC13. Which of the following statements about investors’ investment principles is false?",
    ["The intuitive investor bases his/her investment decision on his/her own intuition.", "The intuitive investor bases his/her investment decision on his/her own gut feeling.",
     "The passive investor typically holds a diversified portfolio.", "Intuitive investors are largely long term oriented"], "D",
    ["S2B"], ["S2-U7"],
    [cite("S2", "Users of financial information: investment style", "Investment decision based on gut feeling. Simple approach.")],
    ["Answer: D (no key in the source; solved twice).",
     "Route 1: the slide's table: intuitive investor = own intuition, gut feeling (A, B true); passive investor holds a diversified portfolio (C true).",
     "Route 2: nothing on the slide ties intuitive investors to a long-term horizon; the long-term, value-driven style is the fundamental investor's. D is the false one."])

# ---- Part A open essay (quantitative): Covid-19 and profitability of three Italian listed companies -----------------------
fs19 = {"A": (5599, 826, 203, 226, 936, 5291), "B": (1025, 255, 101, 45, 1081, 2005), "C": (72, 54, 30, 21, 161, 881)}
fs20 = {"A": (2348, 159, -512, -504, 731, 4108), "B": (847, 80, 36, -73, 1007, 2065), "C": (109, 81, 39, 32, 207, 944)}
roe = lambda d: {k: v[3] / v[4] * 100 for k, v in d.items()}
roa = lambda d: {k: v[3] / v[5] * 100 for k, v in d.items()}
roe19, roa19, roe20, roa20 = roe(fs19), roa(fs19), roe(fs20), roa(fs20)
droa = {k: (roa20[k] - roa19[k]) / roa19[k] * 100 for k in "ABC"}
# second route: ROA = ROE × equity / assets
for k in "ABC":
    near(roa19[k], roe19[k] * fs19[k][4] / fs19[k][5]); near(roa20[k], roe20[k] * fs20[k][4] / fs20[k][5])
near(round(roe19["A"], 2), 24.15); near(round(roa20["A"], 2), -12.27); near(round(droa["C"], 2), 42.21)
rev_chg = {k: fs20[k][0] / fs19[k][0] - 1 for k in "ABC"}
assert rev_chg["A"] < -0.5 and -0.25 < rev_chg["B"] < -0.1 and rev_chg["C"] > 0.4
pct = lambda x: f(x, 2) + "%"
ans_a = ("2019 — ROE: A " + pct(roe19["A"]) + ", B " + pct(roe19["B"]) + ", C " + pct(roe19["C"]) + "; ROA: A " + pct(roa19["A"]) + ", B " + pct(roa19["B"]) + ", C " + pct(roa19["C"]) +
         ". 2020 — ROE: A " + pct(roe20["A"]) + ", B " + pct(roe20["B"]) + ", C " + pct(roe20["C"]) + "; ROA: A " + pct(roa20["A"]) + ", B " + pct(roa20["B"]) + ", C " + pct(roa20["C"]) + ".")
ans_b = "%ΔROA: A " + pct(droa["A"]) + ", B " + pct(droa["B"]) + ", C " + pct(droa["C"]) + " (computed on unrounded ROAs)."
REAL.append(realq(
    id="30024-S2-14", deck="S2", topic="Covid-19 and the profitability of three listed companies", objective="Why financial statement analysis matters: the pandemic's effect on Italian listed companies (ROE, ROA, industries)",
    shape=QUANT, file=F_M23, type="adapted", verbatim=False,
    location=M23_LOC.format("Part A, Open Essay (Quantitative), 10 points") + "; the four company descriptions are split across the text layer and were put back in one list",
    stem="Below you find selected financial information for the 2019 and 2020 Financial Statements for three Italian public companies.\n\n"
         "Your objective is to evaluate the impact of Covid-19 on their profitability, answering to the following questions Please round your values at the second decimal (e.g., 8,45% or 1,23)",
    data="| FS 2019 (EUR thousand) | A | B | C |\n|---|---|---|---|\n| Revenues | 5.599 | 1.025 | 72 |\n| EBITDA | 826 | 255 | 54 |\n| EBIT | 203 | 101 | 30 |\n| Net income | 226 | 45 | 21 |\n| Total Equity | 936 | 1.081 | 161 |\n| Total Assets | 5.291 | 2.005 | 881 |\n\n"
         "| FS 2020 (EUR thousand) | A | B | C |\n|---|---|---|---|\n| Revenues | 2.348 | 847 | 109 |\n| EBITDA | 159 | 80 | 81 |\n| EBIT | -512 | 36 | 39 |\n| Net income | -504 | -73 | 32 |\n| Total Equity | 731 | 1.007 | 207 |\n| Total Assets | 4.108 | 2.065 | 944 |",
    parts=[s_written("A", "(4p.) Calculate ROE and ROA for the three companies and complete the tables below: (2019 and 2020: ROE, ROA for A, B, C)", ans_a, 4),
           s_written("B", "(2p.) Calculate the percentage change in ROA from 2019 to 2020.", ans_b, 2),
           s_written("C", "(2p.) Are below you find a brief description of 4 companies, 3 of which are related to the companies above.\n\n"
                          "- A company specialized in electricity production from renewable sources, particularly in the wind power and solar sector, recently founded\n"
                          "- An Italian retailer operating in the luxury fashion industry\n- The Italian leading provider of food & beverage services for travelers\n"
                          "- The Italian market leader in the automatic data capture\n\n"
                          "Based on the above information (we know it is an incomplete information set) and your inference on the expected impact of Covid-19, assign each company to one of the following industries. "
                          "Complete the table below as follows:\n- 1 for “Fashion and Luxury” - 2 for “Transportations” - 3 for “Technology” - 4 for “Renewable Energy”.",
                     "A = 2 (Transportations: food & beverage for travelers), B = 1 (Fashion and Luxury), C = 4 (Renewable Energy); code 3 (Technology) is the description not used.", 2),
           s_written("D", "(2p.) Justify your answer",
                     f"A: revenues fell {f(-rev_chg['A'] * 100, 1)}% and EBIT turned deeply negative — travel stopped in 2020, the hardest-hit industry on the Session 2 slide. "
                     f"B: revenues fell {f(-rev_chg['B'] * 100, 1)}% and net income turned negative, a sharp but smaller hit — luxury retail closed stores. "
                     f"C: revenues grew {f(rev_chg['C'] * 100, 1)}% with a 75% EBITDA margin in 2019 — a young, capital-heavy renewable producer (large assets relative to revenues), unaffected by lockdowns. "
                     "Technology would also be resilient, but a market leader in data capture would not have revenues of 72 against assets of 881 and a 75% EBITDA margin.", 2)],
    scheme=["No key in the source; solved twice. ROE = net income / total equity; ROA = net income / total assets (end-of-year figures, the only ones given).",
            "Second route for A: ROA = ROE × equity/assets (asserted for all six pairs in build_banks).",
            "%ΔROA = (ROA2020 − ROA2019) / ROA2019; with rounded ROAs the second decimal can differ slightly.",
            "ROA definition: this key uses net income over total assets, consistent with the DuPont chain (ROE = ROA × assets/equity) in the same exam's Part B. Some courses use EBIT over total assets; say which one you use.",
            "Industry: the Session 2 slide shows transport and fashion with the sharpest falls in revenues and EBITDA, and technology/medical as resilient."],
    cites=[cite("S2", "Is Accounting interesting?", "what has been the impact of Covid-19 on Italian listed companies?"),
           cite("S2", "Pandemic’s Effect by Industry", "technology and medical companies proved more resilient, while transportation and fashion suffered sharp declines.")],
    groups=["S2A"], units=["S2-U1"], minutes=20,
    check="(1) The four descriptions are split across the Studocu text layer; the order was restored as a single list. (2) The mock does not define ROA; the key uses net income / total assets. If your class uses EBIT / total assets, the ROA figures change."))

# ---- Part B open essay 2 (qualitative): operating vs financial liabilities, Nissim and Penman (2003) --------------------------
REAL.append(realq(
    id="30024-S34-10", deck="S34", topic="Operating vs financial liabilities and why leverage must be split", objective="Reclassification: operating vs financial items; the Net Financial Position",
    shape=QUAL, file=F_M23, location=M23_LOC.format("Part B (non-attending students), Open Essay 2, 11 points") + ANNOT,
    stem="Open Essay 2 (11 points) Explain the difference between financial and operating liabilities, providing examples for both types. Then, discuss the importance of disentangling the overall leverage in operating and financial with reference to the Nissim and Penman (2003) paper. (max 250 words)",
    parts=[s_written("1", "Answer in at most 250 words.",
                     "Financial liabilities are interest-bearing obligations that finance the firm: short-term and long-term bank debt, bonds, the current portion of long-term debt, lease liabilities; they enter the Net Financial Position. "
                     "Operating liabilities arise from day-to-day operations and carry no explicit interest: trade payables, accrued operating expenses, customer prepayments (contract liabilities); they reduce Operating NWC and so Net Invested Capital. "
                     "Borderline items are classified by substance (a security deposit received is financing; a customer deposit in current liabilities is operating; income tax payable and pensions stay outside both). "
                     "Nissim and Penman (2003): total leverage mixes two things with different effects. Financing leverage raises ROE when the return on net operating assets exceeds the net borrowing cost; operating-liability leverage "
                     "(credit from suppliers, customers, employees) is typically cheaper because its cost is implicit in prices, so it levers operating profitability more favourably and is priced differently (price-to-book). "
                     "Lumping them together misstates both profitability and risk, so the analyst must split them before computing returns.", 11)],
    scheme=["Model answer (no key in the source; built from the Sessions 3-4 slides and the paper).",
            "Points: (1) definition of each type with examples; (2) where each goes in the reclassified balance sheet (NFP vs ONWC/NIC); (3) borderline items by substance; "
            "(4) Nissim-Penman: ROE decomposes into operating profitability plus a financing-leverage effect; operating-liability leverage has its own effect; (5) the two have different costs and valuation implications, so aggregate leverage misleads."],
    cites=[cite("S34", "Focus on the ONWC", "trade payables, contract liabilities and accrued operating expenses on the liability side."),
           cite("S34", "Focus on the NFP", "NFP = (short-term debt + current portion long-term debt + long-term debt + lease liabilities)"),
           cite("S34", "Focus on the ONWC: borderline cases", "if it is a financing deposit (security deposit) consider excluding.")],
    groups=["S34A"], units=["S34-U4", "S34-U6"], minutes=20,
    check="The Nissim and Penman (2003) part relies on the paper (Blackboard reading), which is not in the folder; the summary in the key is from the paper's well-known findings. This is a Part B (non-attending) essay."))

# ================================================================================================
# ADAPTED: 30 May 2017 'prova generale' (official solutions printed; Italian, translated)
# ================================================================================================
cur_t1, cur_t = 3700, 2500
pc_t1, pc_t = 1200, 1470
dccn = (cur_t1 - pc_t1) - (cur_t - pc_t)   # release of working capital
near(dccn, 1470)
fcgc = 10100 + dccn - 846
near(fcgc, 10724)
disp_nbv = 32000 - 5100 - 24200   # fixed assets sold at book value, no capex (ACI fell by more than depreciation)
capex_net = disp_nbv + 230
near(capex_net, 2930)
fcf = fcgc + capex_net
near(fcf, 13654)
dcap = 21610 - 15200 - 1974
near(dcap, 4436)
cf_all = fcf + (4500 - 4000) - 2410 + dcap - 0
near(cf_all, 16180); near(cf_all, 23800 - 7620)            # route 2: change in NFP
dliq = cf_all + (10600 - 25000)
near(dliq, 1780); near(dliq, 2980 - 1200)                  # route 2: change in liquidity
REAL.append(realq(
    id="30024-S2-15", deck="S2", topic="From EBITDA to the change in net debt and in cash", objective="Cash flow statement: operating, investing and financing flows; reconciliation of cash and of the Net Financial Position",
    shape=QUANT, file=F_P17, type="adapted", verbatim=False,
    location="30024 'Prova generale' of 30 May 2017 with official solutions (Studocu copy), Esercizio 4 (2 points); translated from Italian by Claude on 2026-09-24",
    stem="Based on the information below, compute the period's cash-flow dynamics, showing the change in liquidity.",
    data="| Balance sheet | Year t-1 | Year t |\n|---|---|---|\n| Current assets | 3.700 | 2.500 |\n| Non-current operating assets (ACI) | 32.000 | 24.200 |\n| Operating assets (current + ACI) | 35.700 | 26.700 |\n| Non-operating (accessory) assets | 4.500 | 4.000 |\n| Total assets | 40.200 | 30.700 |\n"
         "| Current liabilities | 1.200 | 1.470 |\n| Net financial position (NFP) | 23.800 | 7.620 |\n|   of which liquidity (cash, shown negative) | -1.200 | -2.980 |\n|   of which bonds | 25.000 | 10.600 |\n| Book value of equity | 15.200 | 21.610 |\n| Total liabilities and equity | 40.200 | 30.700 |\n\n"
         "| Income statement | Year t |\n|---|---|\n| EBITDA | 10.100 |\n| Depreciation | -5.100 |\n| Gain on disposal of non-current operating assets | 230 |\n| Net financial charges | -2.410 |\n| EBT | 2.820 |\n| Taxes for the year (t = 30%) | -846 |\n| Net income | 1.974 |",
    parts=[s_written("a", "Compute the free cash flow (FCF) from operations.", f"FCF = {f(fcf, 0)}: EBITDA 10.100 + release of working capital 1.470 − taxes 846 = 10.724; + net disposals 2.930 (book value sold 2.700 + gain 230).", 1, "official"),
           s_written("b", "Compute the total cash flow and the change in the Net Financial Position.", f"Cash flow {f(cf_all, 0)} = FCF 13.654 + accessory assets 500 − net financial charges 2.410 − dividends 0 + capital increase 4.436; ΔNFP = −16.180.", 0.5, "official"),
           s_written("c", "Compute the change in liquidity.", f"Δ liquidity = +{f(dliq, 0)}: 16.180 − bond repayment 14.400.", 0.5, "official")],
    scheme=["Official solution (printed in the source). Working capital: (3.700 − 1.200) − (2.500 − 1.470) = 1.470 released. Taxes: the year's tax charge (no tax payable shown). "
            "Non-current assets: 32.000 − 5.100 depreciation − 24.200 = 2.700 of book value sold, plus the gain of 230 = 2.930 of proceeds. Capital increase: 21.610 − 15.200 − 1.974 = 4.436.",
            "Second route: ΔNFP = 7.620 − 23.800 = −16.180 and Δ liquidity = 2.980 − 1.200 = +1.780, both from the balance sheets (asserted in build_banks).",
            "Where marks are lost: treating the gain as cash from operations and again in disposals, forgetting the accessory assets' 500, missing the capital increase."],
    cites=[cite("S2", "The Cash Flow Statement: Reconciliation of Cash", "If the CFI (typically negative) exceeds the CFO, the deficit can be covered by either borrowing (through CFF) or using existing cash at hand"),
           cite("S2", "Statement of shareholders’ equity", "Ending equity = Beginning equity + Profit or loss + Other comprehensive income + Owner contributions − Distributions to owners")],
    groups=["S2C"], units=["S2-U17", "S2-U18", "S2-U16"], minutes=10,
    check="Translated from Italian (the 2017 paper is in Italian; the 2026-27 exam is in English). Labels: CCN = working capital, ACI = non-current operating assets, SA = accessory (non-operating) assets, PFN = NFP. Numbers and the official answer unchanged."))

# ================================================================================================
# HARD: gap-filling generated questions (one or more per section)
# ================================================================================================
def hq(**kw):
    units = kw.pop("units")
    q = question(course=C, **kw)
    q["units"] = units
    return q


def fmt_set(xs):
    xs = list(xs)
    return f"{xs[0]} only" if len(xs) == 1 else ", ".join(xs[:-1]) + f" and {xs[-1]} only"


def statements_mcq(n, intro, stmts, options, correct):
    roman = ["I", "II", "III", "IV", "V"]
    assert correct == fmt_set([roman[i] for i, (_, tt) in enumerate(stmts) if tt]), correct
    body = intro + "\n\n" + "\n".join(f"{roman[i]}. {s}" for i, (s, _) in enumerate(stmts)) + "\n\nWhich of the statements are correct?"
    return mcq(n, body, options, correct, 1)


CMS, QE, QL = "concept MCQ (statements)", "quantitative open essay (written parts)", "qualitative open essay (written parts)"

# ---- S1 A: accounting, FSA and value -------------------------------------------------------------------------------------
ev_avg, ev_med = 398 * 11.1, 398 * 9.7
assert 3700 <= ev_med < ev_avg <= 6200
st = [("The course frames three complementary tools: financial statement analysis (what the numbers reveal), measurement of accounting quality (can they be trusted) and valuation (expected future performance).", True),
      ("Applying the sector's average EV/EBITDA of 11.1x to Armani's 2024 EBITDA of €398m gives about €4.4bn, inside the €3.7–6.2bn range the slide obtains from sector multiples.", True),
      ("Prada paid an enterprise value of €1.25bn for Versace, so Versace's investment value to Prada is €1.25bn.", False),
      ("The lecture concludes that financial statements speak for themselves once accounting standards are applied correctly.", False),
      ("Accounting may create incentives for opportunistic reporting, which is why it requires effective controls, governance and professional judgement.", True)]
p = statements_mcq("1", "Consider the following statements about the Session 1 framework and cases.", st,
                   [("I, II and V only", None), ("I, II, III and V only", "price_taken_as_value"), ("I and V only", "multiple_applied_to_ebit"), ("I, II, IV and V only", "statements_speak_for_themselves")],
                   "I, II and V only")
HARD.append(hq(id="30024-S1-02", deck="S1", topic="Why accounting matters: the three tools, price vs value, incentives", objective="Role of accounting in decisions; FSA, accounting quality and valuation; price vs value",
    shape=CMS, shape_class="concept MCQ", stem="Session 1: statements.", parts=[p],
    scheme=["[1] Steps: (1) I true (slide 'From financial information to investment decisions'); (2) II: 398 × 11.1 = 4,417.8 ≈ €4.4bn; median 9.7x gives 3,860.6 — both inside €3.7–6.2bn, true; "
            "(3) III false: 'The transaction price tells us what Prada paid, not whether Prada made a good investment' (price is a fact, value an expectation); "
            "(4) IV false: 'Financial statements do not speak for themselves'; (5) V true ('May create incentives for opportunistic reporting'); (6) I, II and V.",
            "Second route: III and IV each quote a slide fact and draw the conclusion the slide rejects."],
    cites=[cite("S1", "From financial information to investment decisions", "Measurement of accounting quality: can the information be trusted?"),
           cite("S1", "Versace: price does not necessarily equal value", "The transaction price tells us what Prada paid, not whether Prada made a good investment."),
           cite("S1", "A CONCLUSION", "Financial statements do not speak for themselves.")],
    location="Session 1 slides: mission, the three tools, Armani, Prada–Versace, conclusion", file=F_S1, groups=["S1A"], minutes=3,
    notches=["near_true_statements", "extra_step"], hc_parts=[{"n": "1", "steps": 6, "concepts": 3}], units=["S1-U1", "S1-U2", "S1-U7", "S1-U8"]))

# ---- S1 B: the cases -------------------------------------------------------------------------------------------------------
st = [("Credit Suisse: PwC found that the financial statements were presented fairly in all material respects, yet issued an adverse opinion on internal control over financial reporting.", True),
      ("A material weakness in internal control means that a material misstatement has already occurred in the financial statements.", False),
      ("Macy's: the falsified accruals understated about $151m of delivery expenses, immaterial in every period, but the control failure itself was material.", True),
      ("Apple: the lecture uses Luca Maestri's transition to show that the CFO's role reaches strategy, resource allocation and the link with shareholders, beyond preparing the statements.", True),
      ("Carillion impaired Eaga's goodwill steadily during Eaga's five consecutive loss-making years, so the 2017 collapse was not an accounting surprise.", False)]
p = statements_mcq("1", "Consider the following statements about the Session 1 cases.", st,
                   [("I, III and IV only", None), ("I, II, III and IV only", "weakness_read_as_misstatement"), ("III and IV only", "adverse_opinion_on_statements"), ("I, III, IV and V only", "carillion_impaired")],
                   "I, III and IV only")
HARD.append(hq(id="30024-S1-03", deck="S1", topic="Controls, impairment and the CFO: what the cases teach", objective="Material misstatement vs material weakness; adverse ICFR opinion; delayed impairment; role of the CFO",
    shape=CMS, shape_class="concept MCQ", stem="Session 1 cases: statements.", parts=[p],
    scheme=["[1] Steps: (1) I true: two different conclusions — fair statements, adverse ICFR opinion; (2) II false: 'A material weakness does not necessarily mean that a material misstatement has already occurred'; "
            "(3) III true (Macy's: immaterial errors, material control failure); (4) IV true (Apple: CFO as a strategic business partner); "
            "(5) V false: Carillion recognised no goodwill impairment in the five years before 2017; (6) I, III and IV.",
            "Second route: separate what the auditor opines on (statements vs controls) from what happened (misstatement vs weakness); the trap options each merge the two."],
    cites=[cite("S1", "The Credit Suisse Case: an adverse opinion on internal controls", "Internal control over financial reporting: PwC issued an adverse opinion, because the controls were not effective."),
           cite("S1", "The SEC review on the effectiveness of Credit Suisse’s reporting controls (2/2)", "A material weakness does not necessarily mean that a material misstatement has already occurred."),
           cite("S1", "Another accounting scandal: when Carillion’s aggressive accounting concealed a failing business", "Carillion recognized no goodwill impairment in the five years before 2017")],
    location="Session 1 slides: Apple, GE, Carillion, Credit Suisse, Macy's", file=F_S1, groups=["S1B"], minutes=3,
    notches=["near_true_statements", "extra_classification"], hc_parts=[{"n": "1", "steps": 6, "concepts": 3}], units=["S1-U4", "S1-U5", "S1-U6"]))

# ---- S1 C: accounting refresh (harder than the handout) --------------------------------------------------------------------
old_sh, par, pic0, re0 = 4000, 10.0, 60000.0, 30000.0
target, consid, cash_in, wh = 0.20, 70000.0, 25000.0, 45000.0
n_new = old_sh * target / (1 - target)
near(n_new, 1000)
cs_new, pic_new = n_new * par, consid - n_new * par
eq0 = old_sh * par + pic0 + re0
eq1 = eq0 + consid
near(eq1, eq0 + cs_new + pic_new)          # route 2: by components
near(cash_in + wh, consid)
pa = written("a", "Northwind issues new shares so that the new investor holds 20% of the voting rights after the issue, for a total consideration of €70,000: €25,000 in cash and a warehouse valued at €45,000. "
                  "Compute the number of new shares, the credits to Common Stock and to Paid-in Capital, the debits, and total equity after the issue.",
             f"{f(n_new, 0)} new shares; Common Stock +{f(cs_new, 0)}; Paid-in Capital +{f(pic_new, 0)}; Dr Cash 25,000 and Dr Building 45,000; equity {f(eq1, 0)}.", 2.5,
             [("twenty_percent_of_old_shares", "800 new shares (20% of the old 4,000)"), ("whole_consideration_to_common_stock", "€70,000 credited to Common Stock"), ("warehouse_as_revenue", "the warehouse recorded as income")])
gross, accdep, price = 300000.0, 140000.0, 150000.0
loss = price - (gross - accdep)
rent_paid, rent_exp = 24000.0, 24000.0 * 3 / 12
prepaid = rent_paid - rent_exp
unearned = 18000.0
bond, rate = 100000.0, 0.06
int_exp = bond * rate * 6 / 12
effect = loss - rent_exp - int_exp
near(loss, -10000); near(prepaid, 18000); near(int_exp, 3000); near(effect, -19000)
near(effect, -(gross - accdep - price) - rent_paid * 0.25 - bond * 0.03)   # route 2
pb = written("b", "During 2021 Northwind also: (1) sells a shop on 1 January for €150,000 cash (gross value €300,000, accumulated depreciation €140,000); (2) pays €24,000 on 1 October for 12 months of office rent; "
                  "(3) collects €18,000 on 1 November for goods to be delivered in February 2022; (4) issues a €100,000 bond at par on 1 July at 6%, interest paid each 1 July. "
                  "Compute the effect of these four items on 2021 profit before tax, and the 31 December balances of pre-paid rent, unearned revenue and interest payable.",
             f"Loss on sale {f(loss, 0)}; rent expense {f(-rent_exp, 0)}; interest expense {f(-int_exp, 0)}; effect on profit {f(effect, 0)}. Pre-paid rent {f(prepaid, 0)}; unearned revenue {f(unearned, 0)}; interest payable {f(int_exp, 0)}.", 2.5,
             [("disposal_as_revenue", "€150,000 recorded as revenue"), ("rent_fully_expensed", "all €24,000 expensed in 2021"), ("advance_as_revenue", "€18,000 recognised as 2021 revenue"),
              ("full_year_interest", "a full year of interest (6,000) accrued")])
HARD.append(hq(id="30024-S1-04", deck="S1", topic="Share issue in kind, a disposal and three period-end accruals", objective="Accounting refresh: share issue, disposals, pre-paid expenses, unearned revenue, accrued interest",
    shape=QE, shape_class="quantitative essay part", stem="Northwind Ltd has 4,000 shares of €10 par, €60,000 of paid-in capital and €30,000 of retained earnings at 1 January 2021. Its financial year is the calendar year.",
    parts=[pa, pb],
    scheme=["[a] Steps: (1) the investor's 20% is of the shares after the issue: n/(4,000 + n) = 0.20 → n = 1,000; (2) Common Stock = 1,000 × €10 = 10,000; (3) Paid-in Capital = 70,000 − 10,000 = 60,000; "
            "(4) debits: Cash 25,000 and Building 45,000 (the warehouse is an asset contributed by an owner, not income); (5) equity = 40,000 + 60,000 + 30,000 + 70,000 = 200,000.",
            "[b] Steps: (1) net book value 300,000 − 140,000 = 160,000 → loss 10,000; (2) rent: 3 of 12 months used in 2021 → expense 6,000; (3) pre-paid rent 18,000; "
            "(4) advance for February goods: no revenue, unearned revenue 18,000; (5) interest: 100,000 × 6% × 6/12 = 3,000 expense and payable; (6) profit effect = −10,000 − 6,000 − 3,000 = −19,000.",
            "Where marks are lost: taking 20% of the old shares, crediting the whole consideration to Common Stock, expensing all the rent, booking the advance as revenue, accruing a full year of interest.",
            "Harder than the handout: the share count has to be worked back from the post-issue percentage, and part b chains four period-end judgements into one profit figure."],
    cites=[cite("S2", "Accounting distortions: accrued and deferred revenues and expenses", "Cash is paid before the related expense is recognised. The payment is initially recorded as an asset"),
           cite("S2", "Accounting distortions: accrued and deferred revenues and expenses", "Cash is received before the related revenue is earned; therefore, a liability is initially recognised."),
           cite("S2", "Statement of shareholders’ equity", "Ending equity = Beginning equity + Profit or loss + Other comprehensive income + Owner contributions − Distributions to owners")],
    location="Session 1 accounting-refresh handout (questions 1-7), harder version; rules from the Session 2 slides", file=F_S1T, groups=["S1C"], minutes=16,
    notches=["working_backwards", "chain", "extra_classification"], hc_parts=[{"n": "a", "steps": 5, "concepts": 2}, {"n": "b", "steps": 6, "concepts": 4}],
    units=["S1-U10", "S1-U11", "S1-U12", "S1-U13", "S1-U15"]))

# ---- S2 A: accounting information, standards, the Covid example ------------------------------------------------------------
roa_drop = (2.84 - 4.80) / 4.80
near(round(roa_drop * 100, 1), -40.8)
st = [("Financial accounting is highly regulated and serves external decision makers; managerial accounting is governed primarily by internal policies and decision needs.", True),
      ("Materiality is a second general constraint on financial reporting, alongside cost.", False),
      ("On the Session 2 slide, the sample's median ROA fell from 4.80% in 2019 to 2.84% in 2020, a relative fall of about 41%.", True),
      ("Higher comparability from accounting standards can lower firms' cost of equity by reducing the corporate governance risk premium.", True),
      ("One aim of the convergence between accounting standards is to decrease the costs of preparing financial statements, information risk and the cost of capital.", True)]
p = statements_mcq("1", "Consider the following statements about accounting information and standards.", st,
                   [("I, III, IV and V only", None), ("I, II, III, IV and V", "materiality_as_constraint"), ("I, IV and V only", "roa_change_in_points"), ("III, IV and V only", "managerial_is_regulated")],
                   "I, III, IV and V only")
HARD.append(hq(id="30024-S2-03", deck="S2", topic="Accounting information, standards and the pandemic example", objective="Financial vs managerial accounting; cost constraint and materiality; purpose and convergence of standards; the Covid example",
    shape=CMS, shape_class="concept MCQ", stem="Session 2: statements.", parts=[p],
    scheme=["[1] Steps: (1) I true (regulation and users row of the table); (2) II false: 'Materiality is not a second general constraint. It is an entity-specific aspect of relevance'; "
            "(3) III: (2.84 − 4.80)/4.80 = −40.8% ≈ −41% — true (a fall of 1.96 points is the absolute change); (4) IV true; (5) V true; (6) I, III, IV and V.",
            "Second route: only II contradicts a slide sentence word for word; III checks by 4.80 × 0.59 = 2.83."],
    cites=[cite("S2", "The role of financial information", "Materiality is not a second general constraint. It is an entity-specific aspect of relevance."),
           cite("S2", "Accounting standards’ purpose", "might also reduce firms’ cost of equity capital (transparency implied by comparability decreases the Corporate Governance Risk Premium)."),
           cite("S2", "Reasons for accounting standards’ alignment", "Decrease costs of preparing financial statements, information risk, and cost of capital.")],
    location="Session 2 slides: pandemic example, accounting information, financial vs managerial, role of financial information, standards", file=F_S2, groups=["S2A"], minutes=3,
    notches=["near_true_statements", "extra_step"], hc_parts=[{"n": "1", "steps": 6, "concepts": 3}], units=["S2-U1", "S2-U2", "S2-U3", "S2-U4", "S2-U5"]))

# ---- S2 B: FSA, investors, price and value, efficiency -----------------------------------------------------------------------
iv, px = 42.0, 35.0
near(iv / px - 1, 0.20)
st = [("A fundamental investor estimates intrinsic value at €42 per share while the price is €35: the value estimate is 20% above the price, so the share is an attractive investment under the fundamental rule.", True),
      ("Under the semi-strong form of market efficiency, prices reflect all public and private information, so no investor holds an informational advantage.", False),
      ("The passive investor relies on the information reflected in market prices under the efficient-market hypothesis and holds a diversified portfolio to reduce risk.", True),
      ("Investment value is the value of an asset to a particular owner given their objectives, whereas market value is the amount at which willing, knowledgeable participants should exchange it.", True),
      ("Because intrinsic value is estimated with precision by fundamental analysis, a price 20% below it proves the market is inefficient.", False)]
p = statements_mcq("1", "Consider the following statements about investors, value and market efficiency.", st,
                   [("I, III and IV only", None), ("I, II, III and IV only", "semi_strong_includes_private"), ("I, III, IV and V only", "estimate_taken_as_precise"), ("III and IV only", "mispricing_direction")],
                   "I, III and IV only")
HARD.append(hq(id="30024-S2-04", deck="S2", topic="Price, value, investor styles and market efficiency", objective="Fundamental analysis; investor styles; price vs value (market, investment, intrinsic); semi-strong efficiency",
    shape=CMS, shape_class="concept MCQ", stem="Session 2: statements.", parts=[p],
    scheme=["[1] Steps: (1) I: 42/35 − 1 = 20%, price below value → attractive, true; (2) II false: semi-strong = publicly available information; private information may still give an advantage; "
            "(3) III true; (4) IV true (definitions on the price-vs-value slide); (5) V false: 'this does not imply precision', and markets are 'not perfectly efficient'; (6) I, III and IV.",
            "Second route: II and V both overstate — one what prices contain, the other what an intrinsic value estimate can prove."],
    cites=[cite("S2", "Fundamental Investor Approach", "A company is an attractive investment if the price is lower than the intrinsic value."),
           cite("S2", "Semi-strong form of efficient markets", "Market prices reflect publicly available information; investors possessing private information may nevertheless have an informational advantage."),
           cite("S2", "Users of financial information: investment style", "Relies on a fundamental analysis which strives at identifying the intrinsic value. However, this does not imply precision.")],
    location="Session 2 slides: FSA and fundamental analysis, investment styles, price vs value, market efficiency", file=F_S2, groups=["S2B"], minutes=3,
    notches=["near_true_statements", "extra_step"], hc_parts=[{"n": "1", "steps": 6, "concepts": 3}], units=["S2-U6", "S2-U7", "S2-U8", "S2-U9"]))

# ---- S2 C: the statements — measurement and formats -----------------------------------------------------------------------------
inv_cost, nrv = 120.0, 105.0
ca, viu, fvlcd = 500.0, 430.0, 460.0
imp = ca - max(viu, fvlcd)
near(min(inv_cost, nrv), 105); near(imp, 40)
st = [("Inventory that cost €120k with a net realisable value of €105k is carried at €105k under IAS 2.", True),
      ("A machine with a carrying amount of €500k, value in use of €430k and fair value less costs of disposal of €460k is impaired by €40k.", True),
      ("In consolidated statements, the profit on goods a parent sold to its subsidiary that are still in the subsidiary's inventory is eliminated in full.", True),
      ("In the functional income statement, EBIT equals gross profit minus SG&A expenses minus depreciation and amortisation.", True),
      ("Under accrual accounting, revenue on a sale on credit is recognised when the customer pays.", False)]
p = statements_mcq("1", "Consider the following statements about measurement and the statements' formats.", st,
                   [("I, II, III and IV only", None), ("I, III and IV only", "recoverable_amount_from_value_in_use"), ("I, II and IV only", "intragroup_profit_kept"), ("II, III and IV only", "inventory_at_cost")],
                   "I, II, III and IV only")
HARD.append(hq(id="30024-S2-05", deck="S2", topic="Measurement rules, consolidation and the functional income statement", objective="Balance sheet measurement (IAS 2, impairment), consolidated statements, income statement format, accrual principle",
    shape=CMS, shape_class="concept MCQ", stem="Session 2: statements.", parts=[p],
    scheme=["[1] Steps: (1) I: lower of cost and NRV = min(120, 105) = 105, true; (2) II: recoverable amount = higher of 430 and 460 = 460; impairment = 500 − 460 = 40, true (using value in use gives 70); "
            "(3) III true: intragroup transactions and income are eliminated in full; (4) IV true: gross profit − SG&A = EBITDA, − D − A = EBIT; (5) V false: revenue follows the transfer of control, not the cash; (6) I, II, III and IV.",
            "Second route: II is the only numerical trap — the recoverable amount is the higher of the two measures."],
    cites=[cite("S2", "The Balance Sheet: Non - Current Assets (optional)", "defined as the higher of value in use and fair value less costs of disposal."),
           cite("S2", "Which Financial Statements?", "intragroup balances, transactions, income, expenses and cash flows are eliminated in full."),
           cite("S2", "The Income Statement: accounting principles", "rather than only when cash is received or paid.")],
    location="Session 2 slides: which statements, balance sheet formats and items, income statement format and principles", file=F_S2, groups=["S2C"], minutes=4,
    notches=["extra_step", "near_true_statements", "extra_classification"], hc_parts=[{"n": "1", "steps": 7, "concepts": 4}], units=["S2-U10", "S2-U11", "S2-U12", "S2-U14", "S2-U15"]))

# ---- S2 D: accounting distortions (qualitative essay) -----------------------------------------------------------------------------
gift_sold, gift_red = 500.0, 0.0
contract, months_done = 240.0, 6
rev_c = contract * months_done / 24
near(rev_c, 60); near(contract - rev_c, 180)
pa = written("a", "An analyst reviewing Sigma SpA notes four things: (1) capitalised development costs have tripled while revenue is flat; (2) the allowance for doubtful receivables fell from 6% to 3% of receivables "
                  "although sales to weaker customers grew; (3) a downsizing plan was approved and announced in November but no provision was booked; (4) three-year equipment leases are treated as short-term leases and kept off the balance sheet. "
                  "For each, name the statement item distorted, the direction of the effect on earnings, and whether it proves earnings management.",
             "(1) Assets (intangibles): capitalising more development spend defers expense → earnings overstated if the IAS 38 criteria are not met. "
             "(2) Assets (receivables allowance): a lower estimate understates the expense → earnings overstated. "
             "(3) Liabilities (provisions, IAS 37): an announced plan creates an obligation → expense and liability understated, earnings overstated. "
             "(4) Assets and liabilities (IFRS 16): the short-term exemption does not cover three-year leases → right-of-use asset and lease liability missing (debt understated). "
             "None of the four proves earnings management by itself: estimates and judgement are required by accrual accounting; it is earnings management only if discretion is used opportunistically — the analyst reverses the distortion and asks why.", 2.5)
pb = written("b", "Sigma also sold €500k of gift cards in December (none redeemed by 31 December; ignore breakage) and on 1 July received €240k for a two-year maintenance contract starting that day. "
                  "Explain how each is recognised in the year's income statement and balance sheet, and what the analyst should do if Sigma booked both as revenue on receipt.",
             f"Gift cards: a contract liability of 500; revenue 0 until redemption. Maintenance: revenue {f(rev_c, 0)} (6 of 24 months) and unearned revenue {f(contract - rev_c, 0)}. "
             f"If both were booked as revenue on receipt, revenue is overstated by {f(gift_sold + contract - rev_c, 0)}: the analyst moves it back to liabilities (contract liabilities are operating liabilities, not financial debt).", 2.5)
HARD.append(hq(id="30024-S2-06", deck="S2", topic="Reading accounting distortions: judgement or earnings management?", objective="Accounting distortions in assets, liabilities and revenue; accrual accounting vs earnings management",
    shape="qualitative open essay (written parts)", shape_class="qualitative essay part", stem="Answer each part in about 120 words.", parts=[pa, pb],
    scheme=["[a] Steps: (1) development costs → asset recognition (IAS 38), earnings up; (2) allowance → asset measurement, earnings up; (3) announced downsizing → existence of an obligation (IAS 37), earnings up; "
            "(4) three-year leases → IFRS 16 recognition, liability understated; (5) judgement ≠ earnings management: only opportunistic discretion is; (6) the analyst's response: reverse the distortion.",
            "[b] Steps: (1) gift cards → contract liability until redemption; (2) maintenance → recognised over time: 240 × 6/24 = 60; (3) unearned revenue 180; (4) booking both on receipt overstates revenue by 500 + 180 = 680; "
            "(5) correction: back to contract liabilities, which are operating (ONWC), not NFP.",
            "Where marks are lost: calling every estimate earnings management, treating the lease exemption as available, recognising the whole maintenance fee, treating contract liabilities as debt."],
    cites=[cite("S2", "Reverse accounting distortions", "managerial discretion should not automatically be interpreted as earnings management."),
           cite("S2", "Accounting distortions: Liabilities and equity", "planned downsizing, long-term service provision with upfront payment"),
           cite("S2", "Accounting distortions: Income Statement", "When a gift card is sold, the consideration received is generally recognised as a contract liability.")],
    location="Session 2 slides: reverse accounting distortions; distortions in assets, liabilities and income", file=F_S2, groups=["S2D"], minutes=16,
    notches=["extra_classification", "chain", "near_true_statements"], hc_parts=[{"n": "a", "steps": 6, "concepts": 4}, {"n": "b", "steps": 5, "concepts": 3}],
    units=["S2-U20", "S2-U21", "S2-U22", "S2-U23"]))

# ---- S34 A: operating vs financial by substance (qualitative essay) ------------------------------------------------------------
pa = written("a", "Classify each item of Lambda SpA as part of Operating NWC, the Net Financial Position, non-current operating assets, or outside NIC and NFP, and justify each in one line: "
                  "(1) a €2m deposit received from a tenant renting part of a warehouse; (2) €3m of customer prepayments for orders to ship next month; (3) a €1.5m loan to a sister company; "
                  "(4) a €0.8m warranty provision for products sold this year, expected to be used within twelve months; (5) €1.2m of income tax payable; (6) €6m of lease liabilities on stores.",
             "(1) NFP (financing deposit, a security deposit — excluded from ONWC). (2) ONWC (operating: a customer deposit in current liabilities from the operating cycle). "
             "(3) NFP as a financial asset (short-term financial receivable from a related party — excluded from ONWC). (4) ONWC (short-term and directly related to sales). "
             "(5) Outside both (income taxes are modelled separately; not trade-related). (6) NFP (lease liabilities are financial debt).", 2.5)
pb = written("b", "Half of Lambda's head-office building is used by its own staff and half is leased to a third party. Explain how the analyst treats it in NIC, what information that needs, "
                  "why the rent earned must not stay in the EBIT used for ROIC, and why reclassification does not change reported profit.",
             "Split by substance: the half used in operations is a non-current operating asset in NIC; the leased half is a non-operating asset excluded from NIC (it is held for investment return). "
             "The split needs the notes (floor area, carrying amounts) and analytical judgement — there is no prescribed IFRS/US GAAP format. "
             "Consistency: NIC is compared only with operating earnings (EBIT or NOPAT), so the rent from the excluded half comes out of EBIT; otherwise the ratio mixes a non-operating return into an operating base. "
             "Reclassification reorganises items into analytical categories; it does not modify the underlying accounting information, so reported profit and total equity do not change.", 2.5)
HARD.append(hq(id="30024-S34-03", deck="S34", topic="Classify by substance: borderline items and a mixed-purpose building", objective="Management account method: operating vs financial vs non-operating items, borderline cases, consistency with ROIC",
    shape="qualitative open essay (written parts)", shape_class="qualitative essay part", stem="Answer each part in about 120 words.", parts=[pa, pb],
    scheme=["[a] Steps: six classifications, each tied to a slide rule: (1) security deposit → financing; (2) customer deposit → operating; (3) related-party loan → financial; (4) short-term, sales-related warranty → ONWC; "
            "(5) income tax payable → outside NWC; (6) lease liabilities → NFP.",
            "[b] Steps: (1) split the building by use; (2) operating half in NIC, leased half non-operating and excluded; (3) needs notes and judgement, no standard format; "
            "(4) remove the rent from EBIT so NOPAT and NIC match; (5) reclassification does not change reported figures.",
            "Where marks are lost: following the balance-sheet caption instead of substance (deposits, loans), putting tax payable in ONWC, leaving leases out of NFP, keeping non-operating rent in EBIT."],
    cites=[cite("S34", "Focus on the ONWC: borderline cases", "if it is a financing deposit (security deposit) consider excluding."),
           cite("S34", "Some items require attention", "In practice, many balance sheets contain mixed-purpose assets. An accurate reclassification requires: analytical judgment; access to notes disclosures."),
           cite("S34", "Reclassification of the Balance Sheet: an Introduction", "Reclassification does not modify the underlying accounting information")],
    location="Lectures 3-4 slides: management account method, when it becomes difficult, NFP and ONWC items, borderline cases", file=F_S34, groups=["S34A"], minutes=16,
    notches=["extra_classification", "near_true_statements"], hc_parts=[{"n": "a", "steps": 6, "concepts": 3}, {"n": "b", "steps": 5, "concepts": 3}],
    units=["S34-U1", "S34-U4", "S34-U5", "S34-U6"]))

# ---- S34 B: liquidity-based balance sheet (MCQ) -----------------------------------------------------------------------------------
sta = {"cash": 25, "securities": 15, "receivables": 210, "inventories": 190, "prepayments": 10}
stl = {"payables": 220, "bank": 80, "accrued": 40, "cpltd": 60, "tax": 20}
fnwc = sum(sta.values()) - sum(stl.values())
tm = sum(sta.values()) - sta["inventories"] - sum(stl.values())
onwc = sta["receivables"] + sta["inventories"] + sta["prepayments"] - stl["payables"] - stl["accrued"]
near(fnwc, 30); near(tm, -160); near(onwc, 150)
st = [(f"Financial NWC is €{fnwc}k.", True),
      (f"The treasury margin is −€{-tm}k: cash, securities, receivables and prepayments do not cover short-term liabilities, so the company relies on future sales or bank credit.", True),
      (f"Operating NWC is also €{fnwc}k, because both measures take every current asset and liability.", False),
      ("A negative treasury margin is a milder signal than a negative Net Working Capital, because it ignores inventories.", False),
      ("For a retailer paid at the till and paying suppliers on credit, a negative Net Working Capital can be a strategic advantage rather than distress.", True)]
p = statements_mcq("1", "Omega SpA (€k). Short-term assets: cash 25, marketable securities 15, trade receivables 210, inventories 190, operating prepayments 10. "
                        "Short-term liabilities: trade payables 220, short-term bank debt 80, accrued operating expenses 40, current portion of long-term debt 60, income tax payable 20. Consider the following statements.", st,
                   [("I, II and V only", None), ("I, II, III and V only", "onwc_equals_financial_nwc"), ("I, II, IV and V only", "treasury_margin_milder"), ("II and V only", "financial_nwc_sign")],
                   "I, II and V only")
HARD.append(hq(id="30024-S34-04", deck="S34", topic="Financial NWC, treasury margin and Operating NWC from one balance sheet", objective="Liquidity-based balance sheet: Financial NWC, treasury margin; contrast with Operating NWC",
    shape=CMS, shape_class="concept MCQ", stem="Omega SpA: liquidity view.", parts=[p],
    scheme=[f"[1] Steps: (1) short-term assets = {sum(sta.values())}, short-term liabilities = {sum(stl.values())}, Financial NWC = {fnwc}; (2) treasury margin = {sum(sta.values())} − 190 − {sum(stl.values())} = {tm}; "
            f"(3) ONWC = 210 + 190 + 10 − 220 − 40 = {onwc} (cash, securities, bank debt, current LTD and tax payable excluded) — III false; (4) IV false: a negative treasury margin is more severe; (5) V true; (6) I, II and V.",
            "Second route: ONWC − Financial NWC = (bank 80 + current LTD 60 + tax 20) − (cash 25 + securities 15) = 120 = 150 − 30."],
    cites=[cite("S34", "Liquidity-based Balance Sheet", "Treasury margin = short-term assets – inventories – short-term liabilities"),
           cite("S34", "Liquidity-based Balance Sheet: how do we interpret the values?", "This situation looks more severe than a negative Net Working Capital (NWC)"),
           cite("S34", "Liquidity-based Balance Sheet", "Operating NWC (used in the Management Account Method) is a narrower operational measure that excludes financial items.")],
    location="Lectures 3-4 slides: liquidity-based balance sheet and its interpretation; ONWC items", file=F_S34, groups=["S34B"], minutes=4,
    notches=["extra_step", "cross_section", "near_true_statements"], hc_parts=[{"n": "1", "steps": 6, "concepts": 3}], units=["S34-U7", "S34-U8", "S34-U2"]))

# ---- S34 C: the three income-statement reclassifications ---------------------------------------------------------------------------
rev, dfg, capw = 5000.0, 150.0, 50.0
rm_purch, drm = 2100.0, -100.0   # raw-material inventory fell by 100 -> consumption = purchases + 100
serv, rents, other, pers, da = 600.0, 150.0, 50.0, 1100.0, 300.0
cons = rm_purch - drm
vop = rev + dfg + capw
ext = cons + serv + rents + other
va = vop - ext
ebitda = va - pers
ebit_na = ebitda - da
near(cons, 2200); near(vop, 5200); near(va, 2200); near(ebit_na, 800)
ind = {"pers": 0.6, "da": 0.7, "serv": 0.5, "rents": 0.4}
cogs = cons + pers * ind["pers"] + da * ind["da"] + serv * ind["serv"] + rents * ind["rents"] - dfg - capw
gm = rev - cogs
sga = pers * (1 - ind["pers"]) + da * (1 - ind["da"]) + serv * (1 - ind["serv"]) + rents * (1 - ind["rents"]) + other
near(cogs, 3230); near(gm, 1770); near(gm - sga, ebit_na)     # route 2: both formats reach the same EBIT
pa = written("a", "Reclassify by nature: compute the Value of Production, Value Added, the Value Added ratio, EBITDA and EBIT.",
             f"VoP {f(vop, 0)}; external costs {f(ext, 0)}; VA {f(va, 0)}; VA ratio {f(va / vop * 100, 2)}%; EBITDA {f(ebitda, 0)}; EBIT {f(ebit_na, 0)}.", 2.5,
             [("purchases_not_consumption", "purchases (2,100) used instead of consumption (2,200)"), ("revenues_as_vop", "VA ratio over revenues"), ("personnel_external", "personnel deducted before VA")])
pb = written("b", "Reclassify by destination: compute COGS, the gross margin and gross margin %, and SG&A, and show that EBIT is the same as in (a).",
             f"COGS {f(cogs, 0)}; gross margin {f(gm, 0)} ({f(gm / rev * 100, 2)}%); SG&A {f(sga, 0)}; EBIT {f(gm - sga, 0)}, as in (a).", 2.5,
             [("inventory_change_not_deducted", "increase in finished goods not deducted from COGS"), ("all_costs_industrial", "all personnel and D&A put in COGS")])
out_p, out_fee = 200.0, 230.0
va2, ebitda2 = va - out_fee, ebitda - out_fee + out_p
near(va2, 1970); near(ebitda2, 1070); near(ebitda2 - da, 770)
pc = written("c", "Kappa outsources maintenance now done by in-house staff costing €200k, for a fee of €230k a year. Recompute Value Added, the VA ratio, EBITDA and EBIT, and say what the VA ratio change means.",
             f"VA {f(va2, 0)}; VA ratio {f(va2 / vop * 100, 2)}%; EBITDA {f(ebitda2, 0)}; EBIT {f(ebitda2 - da, 0)}. The lower VA ratio shows less vertical integration (a shift in outsourcing posture), and EBIT falls by 30 because the fee exceeds the staff cost.", 2.5,
             [("va_unchanged", "VA unchanged (fee treated as personnel)"), ("ratio_read_as_efficiency", "a lower VA ratio read as lower efficiency by itself")])
HARD.append(hq(id="30024-S34-05", deck="S34", topic="One income statement, three reclassifications and an outsourcing decision", objective="Income statement reclassification: value added (by nature), cost of sales (by destination); VA ratio and outsourcing",
    shape=QE, shape_class="quantitative essay part",
    stem="Kappa SpA, 2026 (€k): revenues 5,000; increase in finished goods and WIP inventory 150; internal work capitalised 50; raw-material purchases 2,100 (raw-material inventory fell by 100); services 600; rents 150; "
         "other operating expenses 50; personnel 1,100; depreciation 300. The cost accounts assign to the industrial function 60% of personnel, 70% of depreciation, 50% of services and 40% of rents; raw materials are all industrial; "
         "other operating expenses are administrative.",
    parts=[pa, pb, pc],
    scheme=[f"[a] Steps: (1) consumption = 2,100 + 100 = 2,200; (2) VoP = 5,000 + 150 + 50 = 5,200; (3) external costs = 2,200 + 600 + 150 + 50 = 3,000; (4) VA = 2,200; (5) VA ratio = 2,200/5,200 = {f(va / vop * 100, 2)}%; "
            "(6) EBITDA = 2,200 − 1,100 = 1,100; (7) EBIT = 800.",
            "[b] Steps: (1) industrial costs = 2,200 + 660 + 210 + 300 + 60 = 3,430; (2) less the increase in finished goods/WIP 150 and capitalised work 50 → COGS 3,230; (3) gross margin = 1,770; "
            f"(4) gross margin % = {f(gm / rev * 100, 2)}%; (5) SG&A = 440 + 90 + 300 + 90 + 50 = 970; (6) EBIT = 800, identical to (a) — reclassification does not change EBIT.",
            f"[c] Steps: (1) the fee is an external cost: VA = 2,200 − 230 = 1,970; (2) VA ratio {f(va2 / vop * 100, 2)}%; (3) personnel falls to 900: EBITDA = 1,970 − 900 = 1,070; (4) EBIT = 770; "
            "(5) interpretation: less vertical integration; the decision costs 30 a year of EBIT unless it buys flexibility or quality.",
            "Where marks are lost: using purchases instead of consumption, dividing VA by revenues, deducting personnel before VA, forgetting to take the inventory increase out of COGS."],
    cites=[cite("S34", "Value Added Income Statement: Definitions", "Value of Production represents the total value generated by the company’s operating activity during the period"),
           cite("S34", "A Metric of Vertical Integration", "Value Added Ratio = Value Added / Value of Production"),
           cite("S34", "The Cost of Sales Method: Gross Margin", "Gross Margin % = (Net Sales Revenues − COGS) / Net Sales Revenues × 100")],
    location="Lectures 3-4 slides: three methods, cost of sales, value added, VA ratio and outsourcing posture", file=F_S34, groups=["S34C"], minutes=24,
    notches=["cross_section", "what_if_followon", "extra_classification", "chain"],
    hc_parts=[{"n": "a", "steps": 7, "concepts": 2}, {"n": "b", "steps": 6, "concepts": 3}, {"n": "c", "steps": 5, "concepts": 2}],
    units=["S34-U9", "S34-U10", "S34-U11"]))

# ---- S34 C: contribution margin and the choice of method (MCQ) ----------------------------------------------------------------------
sales, varc, fixc = 2000.0, 1200.0, 600.0
cm = sales - varc
be = fixc / (cm / sales)
near(cm, 800); near(cm - fixc, 200); near(be, 1500); near(be - be * varc / sales, fixc)
st = [("With sales of €2,000k, variable costs of €1,200k and fixed costs of €600k, the contribution margin of €800k covers fixed costs and leaves an EBIT of €200k.", True),
      ("For the same company, sales of €1,500k are needed to cover fixed operating costs.", True),
      ("The cost of sales format reports EBITDA explicitly, because depreciation is shown on its own line.", False),
      ("The value added income statement classifies costs by nature and is usually prepared by external analysts, who lack the data to classify costs by destination.", True),
      ("Because they classify costs differently, the three reclassification methods lead to different EBIT figures for the same year.", False)]
p = statements_mcq("1", "Consider the following statements about the three income-statement reclassifications.", st,
                   [("I, II and IV only", None), ("I, II, IV and V only", "methods_change_ebit"), ("I and IV only", "break_even_from_sales_ratio"), ("I, II, III and IV only", "ebitda_in_cost_of_sales")],
                   "I, II and IV only")
HARD.append(hq(id="30024-S34-06", deck="S34", topic="Contribution margin, break-even sales and what each method shows", objective="Contribution margin income statement; comparing cost of sales, value added and contribution margin formats",
    shape=CMS, shape_class="concept MCQ", stem="Income statement reclassification: statements.", parts=[p],
    scheme=["[1] Steps: (1) CM = 2,000 − 1,200 = 800; EBIT = 800 − 600 = 200 — I true; (2) CM ratio = 40%; sales to cover fixed costs = 600/0.40 = 1,500 — II true; "
            "(3) III false: 'EBITDA is not explicitly reported because depreciation and amortization are incorporated into the Cost of Sales calculation'; (4) IV true; "
            "(5) V false: all three methods identify the same EBIT and do not modify reported earnings; (6) I, II and IV.",
            "Second route for II: at 1,500 of sales, variable costs = 1,500 × 0.6 = 900 and CM = 600 = fixed costs."],
    cites=[cite("S34", "Reclassification by Cost of Sales: some Points of Interest", "EBITDA is not explicitly reported because depreciation and amortization are incorporated into the Cost of Sales calculation;"),
           cite("S34", "The Contribution Margin Income Statement: Definitions", "estimate the level of sales required to cover fixed operating costs."),
           cite("S34", "The three Methods: an Introduction", "they all ultimately identify Operating Profit (EBIT or Earnings Before Interest and Taxes).")],
    location="Lectures 3-4 slides: the three methods, cost of sales, value added, contribution margin", file=F_S34, groups=["S34C"], minutes=4,
    notches=["extra_step", "near_true_statements", "working_backwards"], hc_parts=[{"n": "1", "steps": 7, "concepts": 3}], units=["S34-U9", "S34-U10", "S34-U11", "S34-U12"]))

# ================================================================================================
# Deck sections and units
# ================================================================================================
SECTIONS = {
    "S1": [{"id": "S1A", "title": "Why accounting matters: from financial information to decisions"}, {"id": "S1B", "title": "The cases (Juventus, Apple, GE, Carillion, Credit Suisse, Macy's, Armani, Prada–Versace)"},
           {"id": "S1C", "title": "Accounting refresh (Session 1 handout)"}],
    "S2": [{"id": "S2A", "title": "Accounting information, users and standards (with the Covid example)"}, {"id": "S2B", "title": "Financial statement analysis, investors, price and value, market efficiency"},
           {"id": "S2C", "title": "The financial statements and how they connect"}, {"id": "S2D", "title": "Accounting distortions"}],
    "S34": [{"id": "S34A", "title": "Balance sheet: the management account method (ONWC, NIC, NFP)"}, {"id": "S34B", "title": "Balance sheet: the liquidity-based view"},
            {"id": "S34C", "title": "Income statement: cost of sales, value added, contribution margin"}],
}


def U(id, section, title, where, examinable=True, reason=None):
    u = {"id": id, "section": section, "title": title, "where": where, "examinable": examinable}
    if reason:
        u["reason"] = reason
    return u


UNITS = {
    "S1": [U("S1-U1", "S1A", "Mission: FSA, accounting quality and valuation as complementary tools", "slides 2–3"),
           U("S1-U2", "S1A", "Accounting is everywhere: decisions, incentives, controls, judgement", "slide 4"),
           U("S1-U3", "S1B", "Juventus–Aston Villa: connected transactions across two reporting periods", "Juventus slides"),
           U("S1-U4", "S1B", "Apple: the CFO as a strategic business partner", "Apple slide"),
           U("S1-U5", "S1B", "General Electric and Carillion: delayed impairment and aggressive estimates", "GE and Carillion slides"),
           U("S1-U6", "S1B", "Credit Suisse and Macy's: material misstatement vs material weakness; adverse ICFR opinion", "Credit Suisse and Macy's slides"),
           U("S1-U7", "S1B", "Armani and Prada–Versace: multiples, price vs value", "Armani and Versace slides"),
           U("S1-U8", "S1A", "Conclusion: what financial statements really tell us", "cases summary and conclusion"),
           U("S1-U9", "S1A", "Course organisation: materials, attending status, assessment", "last slides", False, "Course administration, not examinable content."),
           U("S1-U10", "S1C", "Share issue: par value, paid-in capital, contribution in kind", "handout Q1"),
           U("S1-U11", "S1C", "Bond issue and accrued interest", "handout Q2"),
           U("S1-U12", "S1C", "Rent paid in advance (pre-paid expense)", "handout Q3"),
           U("S1-U13", "S1C", "Disposal of a non-current asset: gain or loss", "handout Q4"),
           U("S1-U14", "S1C", "Inventory purchase with a note payable", "handout Q5"),
           U("S1-U15", "S1C", "Cash collected in advance (unearned revenue)", "handout Q6"),
           U("S1-U16", "S1C", "Credit sales and accounts receivable", "handout Q7")],
    "S2": [U("S2-U1", "S2A", "The pandemic's effect on Italian listed companies (ROA, ROE, industries)", "slides 2–5"),
           U("S2-U2", "S2A", "Accounting as valuable information: benefits of accounting quality", "slide 8"),
           U("S2-U3", "S2A", "Financial vs managerial accounting", "slide 9"),
           U("S2-U4", "S2A", "Purpose of financial statements, users, cost constraint and materiality", "slides 10–13"),
           U("S2-U5", "S2A", "Accounting standards: purpose, convergence, IFRS and US GAAP", "slides 14–15"),
           U("S2-U6", "S2B", "What FSA enables; fundamental analysis", "slide 16"),
           U("S2-U7", "S2B", "Investment styles: intuitive, passive, fundamental", "slide 17"),
           U("S2-U8", "S2B", "Price vs value (market, investment, intrinsic) and mispricing", "slides 18–19"),
           U("S2-U9", "S2B", "Efficient markets, the semi-strong form and reporting", "slides 20–23"),
           U("S2-U10", "S2C", "Which financial statements: consolidated statements", "slide 24"),
           U("S2-U11", "S2C", "Balance sheet views and formats (IFRS, US practice), the accounting identity", "slides 25–28"),
           U("S2-U12", "S2C", "Balance sheet items and measurement (cash, receivables, inventories, PP&E, financial assets, intangibles, liabilities)", "slides 29–33 (optional)"),
           U("S2-U13", "S2C", "Equity: book vs market value, market premium", "slide 34"),
           U("S2-U14", "S2C", "Income statement: definitions and the functional format", "slides 35–36"),
           U("S2-U15", "S2C", "Income statement principles: revenue recognition, accruals, recognition uncertainty", "slide 37"),
           U("S2-U16", "S2C", "Statement of shareholders' equity and retained earnings", "slide 38"),
           U("S2-U17", "S2C", "Cash flow statement: CFO, CFI, CFF; direct and indirect methods", "slides 39–41"),
           U("S2-U18", "S2C", "Reconciliation of cash and the interrelation of the statements", "slides 42–43"),
           U("S2-U19", "S2C", "Fiat Chrysler: the statements of a real company", "slides 44–48", False, "Illustration: the statements are shown as images with no figures in the text; the lesson (read the notes, connect the statements) is examined through S2-U18."),
           U("S2-U20", "S2D", "Reverse accounting distortions: judgement vs earnings management", "slide 49"),
           U("S2-U21", "S2D", "Distortions in assets (leases, R&D, fair values, depreciation, allowances)", "slides 50–51"),
           U("S2-U22", "S2D", "Distortions in liabilities and equity (provisions, leases, employment benefits, share-based payments)", "slide 52"),
           U("S2-U23", "S2D", "Distortions in the income statement (revenue recognition, gift cards, deferred expenses)", "slide 53"),
           U("S2-U24", "S2D", "Accrued and deferred revenues and expenses", "slides 54–55")],
    "S34": [U("S34-U1", "S34A", "Why reclassify; objectives; no prescribed format", "slides 3–8"),
            U("S34-U2", "S34A", "Operating NWC: definition and interpretation (negative ONWC)", "slides 9–10"),
            U("S34-U3", "S34A", "Net Invested Capital: asset side and financing side", "slides 11–13"),
            U("S34-U4", "S34A", "Net Financial Position: items included and excluded", "slides 13, 20–23"),
            U("S34-U5", "S34A", "Operating vs non-operating assets; non-operating fixed assets excluded from NIC; ROIC consistency", "slides 15–16"),
            U("S34-U6", "S34A", "ONWC items included and excluded; borderline cases", "slides 24–28"),
            U("S34-U7", "S34B", "Liquidity-based balance sheet: classification by liquidity and maturity", "slides 17–18"),
            U("S34-U8", "S34B", "Financial NWC and treasury margin; interpretation", "slides 19–20"),
            U("S34-U9", "S34C", "Income statement reclassification: the three methods and EBIT", "slides 29–32"),
            U("S34-U10", "S34C", "Cost of sales (destination): COGS, cost drivers, gross margin %", "slides 33–37"),
            U("S34-U11", "S34C", "Value added (nature): value of production, external/internal costs, distribution, VA ratio, outsourcing", "slides 38–46"),
            U("S34-U12", "S34C", "Contribution margin (behaviour): variable/fixed costs, CVP uses", "slides 47–50")],
}

EXISTING_UNITS = {"30024-S1-01": ["S1-U3", "S1-U7"], "30024-S2-01": ["S2-U16", "S2-U17", "S2-U18"], "30024-S2-02": ["S2-U24", "S2-U23", "S2-U13"],
                  "30024-S34-01": ["S34-U2", "S34-U3", "S34-U4", "S34-U5", "S34-U6"], "30024-S34-02": ["S34-U7", "S34-U8", "S34-U11"]}
EXISTING_GROUPS = {"30024-S1-01": ["S1B"], "30024-S2-01": ["S2C"], "30024-S2-02": ["S2D", "S2C"], "30024-S34-01": ["S34A"], "30024-S34-02": ["S34B", "S34C"]}

# Extra shapes (PROXY, scored 2026-09-24).
# concept MCQ: 2023 mock Part A, 15 MCQs: single-fact items 1 step (MC3, 4, 6, 13, 14), two statements 2 (MC9),
#   three statements or a small computation 3 (MC1, 2, 5, 8, 10, 11, 12, 15), four statements 4 (MC7) -> median 3, range 1-4.
# qualitative essay: 2023 Part B essays (4 points each) and the 2017 short essays (2-3 points) -> median 3, range 2-4;
#   slide baseline: the decks' interpretive lists (ONWC and treasury-margin interpretation, reclassification objectives) make 2-3 points.
MCQ_SHAPE = {"exam": {"n": 15, "steps": {"median": 3, "range": [1, 4]}, "concepts_combined": {"median": 1, "range": [1, 2]}},
             "target": {"steps_min": 4, "concepts_min": 2}}
QUAL_SHAPE = {"exam": {"n": 9, "steps": {"median": 3, "range": [2, 4]}, "concepts_combined": {"median": 2, "range": [1, 2]}},
              "slide": {"n": 3, "steps": {"median": 3, "range": [2, 3]}},
              "target": {"steps_min": 5, "concepts_min": 2}}


def D(file, item, decision, ids=None, reason=""):
    return {"file": file, "item": item, "decision": decision, "ids": ids or [], "reason": reason}


LATER = "Taught after Session 5 ({}); that deck is not in the folder yet. Held until it arrives."
H_RATIO = LATER.format("ratio analysis: profitability, liquidity and solvency, sessions 6-9")
H_EQ = LATER.format("earnings quality and its determinants")
H_VAL = LATER.format("accounting and valuation, sessions 18-21")
H_FC = LATER.format("forecasting, sessions 10-13")
LEDGER = [
    D(F_SYL, "Syllabus 2026-27", "used", [], "Exam: 'a mix of open essay questions (with and without calculations), and multiple choices'; direction sheet in late November. Sets the three shapes."),
    D(F_S1, "Session 1 deck", "units", [], "Sections S1A-S1B."),
    D(F_S1T, "Session 1 accounting-refresh handout", "units", [], "Section S1C."),
    D(F_S1T, "Questions 1-7", "included", ["30024-S1-10", "30024-S1-11", "30024-S1-12", "30024-S1-13", "30024-S1-14", "30024-S1-15", "30024-S1-16"]),
    D(F_S2, "Session 2 deck", "units", [], "Sections S2A-S2D."),
    D(F_S34, "Sessions 3-4 deck", "units", [], "Sections S34A-S34C."),
    D(F_S2, "Fiat Chrysler statements (slides 44-48)", "not_examinable", [], "Images only; see unit S2-U19."),
    D(F_M23, "Part A MC4, MC6, MC9, MC13", "included", ["30024-S2-10", "30024-S2-11", "30024-S2-12", "30024-S2-13"]),
    D(F_M23, "Part A MC1, MC5 (accounting-quality studies)", "held", [], H_EQ),
    D(F_M23, "Part A MC12", "duplicate", [], "Same question as MC5 (repeated in the source)."),
    D(F_M23, "Part A MC2 (multi-business valuation)", "held", [], H_VAL + " The table is also scrambled in the text layer."),
    D(F_M23, "Part A MC3, MC7 (guest speakers)", "excluded", [], "About the 2023 guest speakers' talks; the 2026-27 guest sessions are different."),
    D(F_M23, "Part A MC8, MC10, MC11 (P/E, recommendations, price-to-sales)", "held", [], H_VAL),
    D(F_M23, "Part A MC14 (ROCE)", "held", [], H_RATIO),
    D(F_M23, "Part A MC15 (qualities of financial information)", "held", [], "Primary/secondary qualities are not in the 2026-27 decks so far, and the key depends on which framework is used; recheck when the book chapter or a deck covers it."),
    D(F_M23, "Part A Open Essay (ROE/ROA and Covid-19)", "included_adapted", ["30024-S2-14"]),
    D(F_M23, "Part B MC1 (Basu), MC2 (CapEx ratio)", "held", [], H_EQ + " MC2's formula is also garbled in the text layer."),
    D(F_M23, "Part B MC3-MC5 (FIFO/LIFO ratios, DuPont, vertical analysis)", "held", [], H_RATIO),
    D(F_M23, "Part B Open Essay 1 (Leuz, Nanda and Wysocki)", "held", [], H_EQ),
    D(F_M23, "Part B Open Essay 2 (operating vs financial liabilities)", "included", ["30024-S34-10"]),
    D(F_M23C, "Whole file", "duplicate", [], "Byte-identical copy of the 2023 mock (same size) in Exam Material/Clean."),
    D(F_P17, "Esercizio 4 (cash-flow dynamics)", "included_adapted", ["30024-S2-15"], ""),
    D(F_P17, "Questions 1, 2, 5, 6, 8, 9 (AEG, earnings growth, DDM, value creation, RIM, IRR)", "held", [], H_VAL),
    D(F_P17, "Question 3 and Esercizi 1, 5 (ROE leverage, ROIC decomposition)", "held", [], H_RATIO + " Esercizio 1 also reclassifies a balance sheet; it comes in with the ratio deck."),
    D(F_P17, "Esercizio 2 (Residual Income Model)", "held", [], H_VAL),
    D(F_P17, "Esercizio 3 (forecast financial statements)", "held", [], H_FC),
    D(F_P17, "Question 4 (margin of safety)", "held", [], "Needs the degree of operating leverage, which the Sessions 3-4 contribution-margin slides do not cover; recheck with the forecasting or ratio decks."),
    D(F_P17, "Question 7 (US analyst's adjustment for development costs)", "held", [], "Needs the US GAAP treatment of development costs, which is not in the 2026-27 slides so far."),
    D(F_P17, "Question 10 (inflation revaluation of plant)", "held", [], "Not in the 2026-27 decks so far."),
    D(F_P17C, "Whole file", "duplicate", [], "Same text as the Exam Material copy (checked 2026-09-24)."),
    D("Mock Exam/30024 Mock Exam - Lecture 1, PART A Lecture 1, Lecture 2, Lectures 3-4 (paper, mark scheme, question bank)", "All items", "excluded", [], "Claude-written mocks are not evidence."),
    D("Claude outputs/ (RemNote decks: lectures 3-4; COGS and Value Added)", "All items", "excluded", [], "Claude-written study decks are not evidence."),
]
