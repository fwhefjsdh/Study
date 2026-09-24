"""30178 International Banking: source intake, deck units and the questions that fill the gaps.

Everything here follows the rule agreed on 2026-09-24:
  1. Real questions (past papers, problem sets, instructor samples) come first, copied word for word
     from the PDF text layer. Keys are the official ones where the source prints them; where it does not,
     the key is solved twice and marked "double-solved", and the mark scheme says the source has no key.
  2. Generated questions only fill gaps: a deck unit with no question, or a deck section with no Hard
     question. Every generated question is Hard and passes the harder rule (banks/review.js).
  3. Every source item gets a ledger decision; every deck unit is examinable (and then needs a question)
     or not (with the reason). banks/review.js refuses to pass while a gap remains.
"""
from build_banks import mcq, written, question, cite, f, r, near, CREATED, L

F_INTRO = "Slides/Introductory concepts to banking_30178_2026-27.pdf"
F_SVB = "Slides/The SVB case_in class discussion.pdf"
F_IRR = "Slides/Managing Interest Rate Risk_2026-27_PART I and 2_classroom.pdf"
F_STERN = "Slides/SVB and Beyond_Stern Position Paper_2023.pdf"
F_PS1 = "Reference Material/Clean/Problem Set 1.pdf"
F_PS1S = "Reference Material/Clean/Part1_.pdf"
F_P1 = "Reference Material/Clean/P1 1st part.pdf"
F_PAMB = "Reference Material/Clean/MCQ/Partial1.pdf"
STUDOCU = "third-party copy via Studocu; text checked word for word against the PDF text layer on 2026-09-24"


# ------------------------------------------------------------------------------------------------
# helpers for real questions (options keep the source order and letters; nothing is shuffled)
# ------------------------------------------------------------------------------------------------
def src_mcq(n, prompt, options, letter, status="official", marks=0.8):
    assert letter in L[:len(options)]
    return ({"n": n, "prompt": prompt, "options": options, "marks": marks},
            {"n": n, "answer": letter, "answer_status": status}, [])


def src_tf(n, prompt, truth, marks=0.8, status="official"):
    return src_mcq(n, prompt, ["True", "False"], "A" if truth else "B", status, marks)


def src_written(n, prompt, answer, marks="UNKNOWN", status="official"):
    return ({"n": n, "prompt": prompt, "options": [], "marks": marks},
            {"n": n, "answer": answer, "answer_status": status}, [])


def realq(**kw):
    parts = kw.pop("parts")
    marks = [p[0]["marks"] for p in parts]
    q = {
        "id": kw["id"], "course": "30178", "deck": kw["deck"], "topic": kw["topic"],
        "syllabus_objective": kw["objective"], "shape": kw["shape"], "stem": kw["stem"],
        "data": kw.get("data"), "difficulty": "exam",
        "source": {"type": kw.get("type", "real"), "file": kw["file"], "location": kw["location"], "label": "SUPPORTING",
                   "verbatim_verified": kw.get("verbatim", True), "transcribed_from_image": False, "page_snapshot_asset": None},
        "subquestions": [p[0] for p in parts], "answer_key": [p[1] for p in parts],
        "error_tags": kw.get("tags", []),
        "marks": round(sum(marks), 2) if all(isinstance(m, (int, float)) for m in marks) else "UNKNOWN",
        "mark_scheme": kw["scheme"], "citations": kw["cites"], "slides": kw.get("slides", []),
        "slide_groups": kw["groups"], "units": kw["units"], "est_minutes": kw["minutes"], "created_at": CREATED,
        "negative_marking": kw.get("neg"),
    }
    if kw.get("check"):
        q["source"]["check"] = kw["check"]
    if q["data"] is None:
        del q["data"]
    return q


NEG = {"correct": 0.8, "wrong": -0.1, "blank": 0}  # partial exam scoring (exam structure guide 2025-26)
REAL, HARD = [], []

# ================================================================================================
# REAL QUESTIONS
# ================================================================================================
PS1_LOC = "Problem Set 1 – TEXT (a.y. 2025-26 problem set, International Banking 30178), {}; official solution in Reference Material/Clean/Part1_.pdf (Problem set 1 with solutions), " + STUDOCU

# ---- PS1 Exercise 2: firm commitment underwriting ----------------------------------------------
REAL.append(realq(
    id="30178-INTRO-03", deck="INTRO", topic="Underwriting on a firm commitment basis",
    objective="What banks do: investment banking services (underwriting)",
    shape="numerical exercise (written)", file=F_PS1, location=PS1_LOC.format("Exercise 2"),
    stem="An investment bank pays $23.50 per share for 4 million shares of ABC Company (underwriting on a firm commitment basis). It then sells those shares to the public for $25 per share.",
    parts=[src_written("1", "How much money does ABC receive?", "ABC receives $23.50 x 4,000,000 shares = $94,000,000."),
           src_written("2", "What is the profit to the investment bank?", "The profit to the investment bank is ($25.00 - $23.50) x 4,000,000 shares = $6,000,000."),
           src_written("3", "What is the stock price of ABC?", "The stock price of ABC is $25.00 since that is what the public must pay.")],
    scheme=["Official solution: ABC receives $94,000,000; the investment bank earns $6,000,000; the stock price is $25.00.",
            "From the perspective of ABC, the $6,000,000 represents the commission that it must pay to issue the stock (official solution).",
            "Deck link: investment banks help issuers raise funds and 'may purchase them before reselling them to investors' — that purchase-and-resale is the firm commitment."],
    cites=[cite("INTRO", "What Do Banks Do? Investment banks", "The investment bank structures, prices and markets the securities—and may purchase them before reselling them to investors.")],
    groups=["I1"], units=["INTRO-U3"], minutes=3))

# ---- PS1 Exercise 3: best-efforts underwriting --------------------------------------------------
REAL.append(realq(
    id="30178-INTRO-04", deck="INTRO", topic="Underwriting on a best-efforts basis",
    objective="What banks do: investment banking services (underwriting)",
    shape="numerical exercise (written)", file=F_PS1, location=PS1_LOC.format("Exercise 3"),
    stem="XYZ, Inc. has issued 10 million new shares of stock. An investment bank agrees to underwrite these shares on a best-efforts basis. The investment bank is able to sell 8.4 million shares for $27 per share, and it charges XYZ $0.675 per share sold.",
    parts=[src_written("1", "How much money does XYZ receive?", "XYZ receives ($27.00 - $0.675) x 8,400,000 shares = $221,130,000."),
           src_written("2", "What is the profit to the investment bank?", "The investment bank’s profit is $0.675 x 8,400,000 shares = $5,670,000."),
           src_written("3", "What is the stock price of XYZ?", "The stock price is $27 per share since that is what the public pays.")],
    scheme=["Official solution: XYZ receives $221,130,000; the investment bank earns $5,670,000; the stock price is $27.",
            "Check: 26.325 × 8.4m = 221.13m; 0.675 × 8.4m = 5.67m. Only the 8.4 million shares sold count: under best efforts the unsold 1.6 million stay with XYZ.",
            "Where marks are lost: using 10 million shares; subtracting the fee from the bank's profit instead of from XYZ's proceeds."],
    cites=[cite("INTRO", "What Do Banks Do? Investment banks", "Help companies and governments raise funds by issuing shares or bonds.")],
    groups=["I1"], units=["INTRO-U3"], minutes=3))

# ---- PS1 Exercise 4: net income, loan losses and funding cost -----------------------------------
ni = 0.06 * 9e6 - 0.005 * 9e6 - 0.01 * 6e6 - 0.04 * 2e6
near(ni, 355000)
REAL.append(realq(
    id="30178-INTRO-05", deck="INTRO", topic="Net income from interest, loan losses and funding costs",
    objective="What banks do: sources of income and cost (interest income, interest expense, loan loss provisions)",
    shape="numerical exercise (written)", file=F_PS1, location=PS1_LOC.format("Exercise 4"),
    stem="A FI has assets of $10 million consisting of $1 million in cash and $9 million in loans with an interest rate of 6%. On the loans the FI expect loan losses for 0.5% (N.B. assume no reserves for loan losses are recorded on b/s). The FI has core deposits of $6 million, on which the FI pays on average 1% of interest rates and subordinated debt of $2 million on which it pays an interest rate of 4% and equity of $2 million.",
    parts=[src_written("a", "Compute the NI (net income)", "NI=0.06(9m.) - 0.005(9m.)-0.01(6m.)-0.04(2m.) = 495,000-60,000-80,000 = $355,000"),
           src_written("b", "Suppose that the interest rates on loans fall to 5%: compute the change in NI", "Change in NI= - 0.01(9m.) = - $90,000"),
           src_written("c", "How does the NI changes if following a recession the loan losses increase to 1.75%?", "Change in NI= - (0.0175-0.005)(9m.) = -(0.0125)(9m.) = - $112,500"),
           src_written("d", "Calculate the change in NI if depositors were expected to withdraw $1 million of deposits and the FI had to raise the same amount in subordinated debt.", "Change in NI= - (0.04-0.01)(1m.)= - $30,000")],
    scheme=["Official answers: (a) $355,000; (b) −$90,000; (c) −$112,500; (d) −$30,000.",
            "(a) interest on loans 540,000 − expected loan losses 45,000 − deposit interest 60,000 − sub-debt interest 80,000 = 355,000. Cash earns nothing; there are no taxes or operating costs in the data.",
            "Where marks are lost: charging the loss rate on total assets; forgetting the cash earns nothing; in (d) using the full 4% instead of the 3-point cost difference."],
    cites=[cite("INTRO", "How Banking Activities Generate Revenues", "Interest income − Interest expense = Net interest income"),
           cite("INTRO", "How Banking Activities Generate Revenues and Expenses", "Loan Loss Provisions: amounts recognised to cover expected losses when borrowers may not fully repay their loans")],
    groups=["I2"], units=["INTRO-U6", "INTRO-U7"], minutes=5,
    check="The source solution prints '- $90.000' for (b); the key writes $90,000 (a thousands separator, not a decimal)."))

# ---- PS1 MCQs 2–5 (the source prints no key: each key is solved twice) --------------------------
PS1_MCQ_NOTE = "The problem set's solution file repeats these MCQs without marking an answer, so this key is Claude's, checked two ways against the deck; it is not official."
REAL.append(realq(
    id="30178-INTRO-06", deck="INTRO", topic="Firm commitment versus best-efforts underwriting",
    objective="What banks do: investment banking services (underwriting)", shape="concept MCQ",
    file=F_PS1, location=PS1_LOC.format("Multiple choice question 2"),
    stem="Which of the following statement is true?",
    parts=[src_mcq("1", "Which of the following statement is true?",
                   ["In a firm commitment underwriting, the investment bank acts as an agent of the company issuing the security and receives a fee based on the number of securities sold.",
                    "In a best effort underwriting, the investment bank purchases the securities from the company at a negotiated price and sells them to the investing public at what it hopes will be a higher price.",
                    "The investment bank bears more risk with the firm commitment underwriting.",
                    "The investment bank bears more risk with the best-effort underwriting."], "C", "double-solved")],
    scheme=["Answer C. Route 1: A and B swap the two definitions (A describes best efforts, B describes firm commitment). Route 2: under firm commitment the bank buys the issue first, so it carries any shortfall in the resale price; under best efforts it only sells as an agent. So the firm commitment is riskier (C), not D.",
            PS1_MCQ_NOTE],
    cites=[cite("INTRO", "What Do Banks Do? Investment banks", "The investment bank structures, prices and markets the securities—and may purchase them before reselling them to investors.")],
    groups=["I1"], units=["INTRO-U3"], minutes=1.5, neg=NEG))
REAL.append(realq(
    id="30178-INTRO-07", deck="INTRO", topic="Asset side of a commercial bank's balance sheet",
    objective="What banks do: reading a simplified bank balance sheet", shape="concept MCQ",
    file=F_PS1, location=PS1_LOC.format("Multiple choice question 3"),
    stem="Which of the following appears on the asset side of a balance sheet for a commercial bank?",
    parts=[src_mcq("1", "Which of the following appears on the asset side of a balance sheet for a commercial bank?",
                   ["Interbank market borrowing.", "Loans.", "Sovereign bonds.", "B and C."], "D", "double-solved")],
    scheme=["Answer D. Route 1: loans and government bonds are both listed among the assets on the deck's simplified balance sheet. Route 2: interbank borrowing is money the bank owes, so it is funding (a liability), which rules out A and leaves B and C together.",
            PS1_MCQ_NOTE],
    cites=[cite("INTRO", "Commercial banks: Simplified Balance sheet (b/s)", "Government and corporate bonds, etc.")],
    groups=["I2"], units=["INTRO-U5"], minutes=1, neg=NEG))
REAL.append(realq(
    id="30178-INTRO-08", deck="INTRO", topic="What a commercial bank does not typically do",
    objective="What banks do: commercial versus investment banking", shape="concept MCQ",
    file=F_PS1, location=PS1_LOC.format("Multiple choice question 4"),
    stem="What is not a typical function of a commercial bank?",
    parts=[src_mcq("1", "What is not a typical function of a commercial bank?",
                   ["Granting corporate loans.", "Buying government bonds.", "Trading securities.", "Granting mortgages."], "C", "double-solved")],
    scheme=["Answer C. Route 1: the deck's commercial bank 'accepts deposits and transforms funding into loans and securities' and lends to households (mortgages) and firms, which covers A, B and D. Route 2: the deck lists trading securities for a speculative profit among the investment-bank activities of a universal bank.",
            PS1_MCQ_NOTE],
    cites=[cite("INTRO", "Not All Banks Do the Same Things", "Commercial banking: accepts deposits and transforms funding into loans and securities"),
           cite("INTRO", "What Do Banks Do? Universal banks", "trade securities for a speculative profit, offer brokerage services (Inv. Bank)")],
    groups=["I1"], units=["INTRO-U1", "INTRO-U2"], minutes=1, neg=NEG))
REAL.append(realq(
    id="30178-INTRO-09", deck="INTRO", topic="Definition of market risk",
    objective="What banks do: the main risks banking activities generate", shape="concept MCQ",
    file=F_PS1, location=PS1_LOC.format("Multiple choice question 5"),
    stem="What is the definition of market risk?",
    parts=[src_mcq("1", "What is the definition of market risk?",
                   ["It is the risk of not having funds to start new investments.", "It is a risk that borrowers will default on their debt.",
                    "It is the risk connected with the uncertainty of a bank’s earnings on its trading book due to changes in market conditions.",
                    "It is the risk of not having enough equity to offset a decline in the asset value."], "C", "double-solved")],
    scheme=["Answer C. Route 1: the deck defines market risk as 'security prices may move adversely', which is earnings uncertainty on the trading book from market moves. Route 2: B is credit risk and A is close to liquidity risk, so both are other risks on the deck's list; D is about capital (solvency), not a risk type.",
            PS1_MCQ_NOTE],
    cites=[cite("INTRO", "Banking Activities Generate Risks", "Market risk: security prices may move adversely")],
    groups=["I3"], units=["INTRO-U9"], minutes=1, neg=NEG))

# ---- Pambianco sample MCQ [1]: loan loss provisions in the P&L ----------------------------------
REAL.append(realq(
    id="30178-INTRO-12", deck="INTRO", topic="Where loan loss provisions are reported",
    objective="What banks do: reading a simplified bank income statement (loan loss provisions)", shape="concept MCQ",
    file=F_PAMB, location="Sample Questions and Exercise, Financial Statements Overview and Asset Quality (R. Pambianco), question [1]; official solution printed below the question; " + STUDOCU,
    stem="In relation to banks’ asset quality and to “loan loss provisions”, which of the following statements is correct?",
    parts=[src_mcq("1", "In relation to banks’ asset quality and to “loan loss provisions”, which of the following statements is correct?",
                   ["Evidence of the loan loss provisions booked by a bank in a certain year can be found in the bank’s P&L for that particular year.",
                    "Loan loss provisions are usually reported on the liability side of a bank’s balance sheet.",
                    "Loan loss provisions are generally a positive line item reported in the P&L of a bank below the net income line.",
                    "None of the above."], "A")],
    scheme=["Official solution: a).",
            "Deck link: the example income statement books loan loss provisions as an expense line (D. Loan Loss Provisions −5,000) above profit before tax, so they are in that year's P&L, negative, and above net income.",
            "Source note: this sample set belongs to Part II (R. Pambianco); only this question is kept for midterm 1 because the INTRO deck covers the same point. Its other items wait for the Part II decks."],
    cites=[cite("INTRO", "How Banking Activities Generate Revenues and Expenses", "Loan Loss Provisions: amounts recognised to cover expected losses when borrowers may not fully repay their loans")],
    groups=["I2"], units=["INTRO-U7"], minutes=1, neg=NEG))

# ---- PS1 Exercise 6: refinancing risk in MCQ form (official answers) -----------------------------
nii1, nii2 = 10000 * (0.10 - 0.06), 10000 * (0.10 - 0.07)
y = 0.10 + (nii1 + nii2) / 10000
near(y, 0.17)
REAL.append(realq(
    id="30178-IRR-33", deck="IRR", topic="Refinancing risk over three years, solved backwards",
    objective="Interest-rate risk: refinancing risk and the income (NII) perspective",
    shape="numerical exercise with 3 MCQ sub-questions", file=F_PS1, location=PS1_LOC.format("Exercise 6"),
    stem="A financial institution has the following market value balance sheet structure:\n\nA bond has a 3-year maturity, a fixed-rate coupon of 10 percent paid at the end of each year, and a par value of $10,000. The certificate of deposit has a 1-year maturity and a 6 percent fixed rate of interest. The FI expects no additional asset growth.",
    data="| Assets | | Liabilities and Equity | |\n|---|---|---|---|\n| Cash | $ 1,000 | Certificate of deposit | $ 10,000 |\n| Bond | 10,000 | Equity | 1,000 |\n| Total assets | $ 11,000 | Total liabilities and equity | $ 11,000 |",
    parts=[src_mcq("1", "What will be the net interest income at the end of the first year?", ["$400", "$440", "$340", "$1000"], "A"),
           src_mcq("2", "If at the beginning of the second year market interest rates have increased 100 basis points (1 percent), what will be the net interest income for the second year?", ["$400", "$440", "$300", "$1100"], "C"),
           src_mcq("3", "In the third year, the interest rates have increased so much that the FI makes zero total net interest income over the three years. How much should the interest rate increase in the third year (compared to the second one) for this to be true, if the interest rate on the bond has remained at 10 percent?",
                   ["Such situation is not possible", "1000 bps increase", "1100 bps increase", "1400 bps increase"], "B")],
    scheme=["Official: (1) $400=10,000*(10%-6%); (2) $300=10,000*(10%-7%); (3) $400 + $300 - $X=0, -$700=10,000 * (10%-Y%), Y=17%, change=10% (1000 bps).",
            "Why: the CD reprices every year and the bond does not, so rising rates widen the funding cost only: refinancing risk.",
            "Where marks are lost in (3): quoting the year-3 CD rate (17%) as the change; measuring the change from the original 6% (1100 bps); counting the cash as earning interest."],
    cites=[cite("IRR", 14, "Refinancing risk: maturing liabilities may need to be replaced at higher rates"),
           cite("IRR", 15, "It occurs when the bank is holding assets with maturities greater than the maturities of its liabilities")],
    groups=["S2"], units=["IRR-U5"], slides=[14, 15, 16], minutes=6, neg=NEG))

# ---- PS1 True/False 1 and 3 (official T, F) ------------------------------------------------------
REAL.append(realq(
    id="30178-IRR-34", deck="IRR", topic="Refinancing risk and cross-country differences in IRR exposure",
    objective="Interest-rate risk: refinancing risk; why repricing (and deposit betas) differ across banks",
    shape="true/false", file=F_PS1, location=PS1_LOC.format("True/false questions 1 and 3"),
    stem="True/false questions",
    parts=[src_tf("1", "A bank is subject to refinancing risk when its liabilities have shorter maturity than its assets.", True),
           src_tf("3", "In the Euro area economy, banks are equally exposed to interest rate risk across countries.", False)],
    scheme=["Official answers: 1) T; 3) F.",
            "3 is false: the deck's deposit betas differ across countries (Bank Italy β = 0.11 versus Bank France β = 0.35), and asset and funding mixes are bank-specific, so the same rate move hits banks differently.",
            "Numbering follows the source; items 2 and 4–7 are held back (off-balance-sheet, FX and operational risk have no deck yet)."],
    cites=[cite("IRR", 15, "It occurs when the bank is holding assets with maturities greater than the maturities of its liabilities"),
           cite("IRR", 52, "Imagine two banks, each holding €300m of retail deposits at 2%, and each experiencing the same +1% rise in market rates")],
    groups=["S2", "S6"], units=["IRR-U5", "IRR-U15"], slides=[15, 51, 52], minutes=1.5, neg=NEG))

# ---- P1 1st part, section D: SVB MCQ and two true/false (official) ------------------------------
P1_LOC = "Samples of Questions and Exercises on IRR & Securitisation with solutions (B. Bruno, a.y. 2025-26), section D, {}; " + STUDOCU
REAL.append(realq(
    id="30178-SVB-03", deck="SVB", topic="SVB's response to the post-COVID stimulus",
    objective="Interest-rate risk in practice: the SVB case (balance-sheet growth and funding)", shape="concept MCQ",
    file=F_P1, location=P1_LOC.format("multiple choice question"),
    stem="How did Silicon Valley Bank (SVB) respond to the macroeconomic stimulus initiated by the US monetary policy authorities since the COVID pandemic? Consider the following options and select the correct one:",
    parts=[src_mcq("1", "Select the correct option.",
                   ["By shrinking its balance sheet.", "By expanding assets, mainly through mortgages financed by new bond issuances.",
                    "By more than doubling the size of its balance sheet, primarily thanks to the issuance of new customer deposits.",
                    "By changing its funding structure, shifting from short-term to long-term customer deposits."], "C")],
    scheme=["Official answer: C.",
            "Deck: SVB's balance sheet 'has tripled since 2019', financed with deposits (typically wholesale or uninsured). SVB's assets grew mainly in securities, not mortgages funded by bonds, and time deposits stayed tiny, so there was no shift to long-term deposits."],
    cites=[cite("SVB", "Effects: Massive growth in bank balance in SVB sheets", "Balance sheet size has tripled since 2019"),
           cite("SVB", "Effects: Massive growth in bank balance sheets during the ZLB and QE years", "Bank balance sheets expand, financed with deposits (typically wholesale or uninsured)")],
    groups=["V2"], units=["SVB-U3", "SVB-U4"], minutes=1, neg=NEG))
REAL.append(realq(
    id="30178-SVB-04", deck="SVB", topic="SVB's deposit concentration and funding structure",
    objective="Interest-rate risk in practice: the SVB case (liability side)", shape="true/false",
    file=F_P1, location=P1_LOC.format("true/false questions"),
    stem="True/False question",
    parts=[src_tf("1", "Silicon Valley Bank's funding structure was highly concentrated: the 10 largest depositors held nearly 8% of the bank's total deposits", True),
           src_tf("2", "To fund its assets, SVB relied almost exclusively on long-term deposits, which constituted (approx.) 90% of its total deposits.", False)],
    scheme=["Official answers: 1 TRUE; 2 FALSE.",
            "2 is false because the ≈90% figure is the uninsured share of deposits; SVB's time deposits were tiny (below 1% of deposits until 2021, 4% in 2022 on the slide)."],
    cites=[cite("SVB", "Liability side: The Achilles’ heel", "Large corporate depositors: the largest 10 depositors accounted for 8% of SVB deposits, for an average of $ 1.3 bill each"),
           cite("SVB", "Liability side: The Achilles’ heel", "≈ 90% of Dep were uninsured")],
    groups=["V4"], units=["SVB-U8"], minutes=1.5, neg=NEG))

# ---- P1 1st part, section A: standardized (beta) GAP solution (adapted: table rebuilt) -----------
beta_a = [("On-demand credit lines", 460, 0.95), ("Interbank 1 m deposits", 80, 1.10), ("3 m-gov't. securities", 60, 1.05),
          ("5yr variable-rate cons. credit (repricing in 6 m.)", 120, 0.90), ("10yr variable-rate mortgages (Euribor+100 bp, repricing in 1 yr)", 280, 1.00)]
beta_l = [("Customer deposits", 380, 0.80), ("1m interbank deposits", 140, 1.10), ("Variable-rate CDs (next repricing in 3 m)", 120, 0.95),
          ("10 yr variable-rate bonds (euribor+50 bp, repricing in 6 m)", 160, 1.00), ("1 yr fx-rate CDs", 80, 0.90)]
rsa, rsl = sum(a for _, a, _ in beta_a), sum(a for _, a, _ in beta_l)
sa, sl = sum(a * b for _, a, b in beta_a), sum(a * b for _, a, b in beta_l)
assert (rsa, rsl) == (1000, 880) and (round(sa), round(sl)) == (976, 804) and rsl + 120 == 1000
REAL.append(realq(
    id="30178-IRR-35", deck="IRR", type="adapted", verbatim=False, topic="Maturity GAP versus standardized (beta) GAP",
    objective="Interest-rate risk: repricing GAP versus standardised (beta) GAP", shape="numerical exercise (written)",
    file=F_P1, location="Samples of Questions and Exercises on IRR & Securitisation with solutions (B. Bruno, a.y. 2025-26), section A 'Solutions to exercises presented in class', Standardized (Beta) GAP; official solution table and NOTE on the same page; " + "third-party copy via Studocu",
    stem="Standardized (Beta) GAP. Using the balance sheet below (Eur m, with the beta of each item), calculate the Maturity GAP and the Standardized GAP, the weighted average beta of assets and of liabilities, and say what they show about the bank's exposure.",
    data="| Assets | Eur m | Beta | Liabilities | Eur m | Beta |\n|---|---|---|---|---|---|\n" + "\n".join(
        f"| {a[0]} | {a[1]} | {a[2]:g} | {l[0]} | {l[1]} | {l[2]:g} |" for a, l in zip(beta_a, beta_l)) + "\n| | | | Equity | 120 | |\n| Total | 1000 | | Total | 1000 | |",
    parts=[src_written("1", "Maturity GAP: RSA, RSL and GAP.", "RSA 1000, RSL 880, Maturity GAP 120"),
           src_written("2", "Standardized GAP: beta-weighted RSA, RSL and GAP.", "RSA 976, RSL 804, Standardized GAP 172"),
           src_written("3", "Weighted average beta of assets and of liabilities.", "0.98 (assets) and 0.91 (liabilities)"),
           src_written("4", "What do the two GAPs show about the bank's exposure?", "The bank is asset sensitive. The exposure is larger if calculated with the standardized (or Beta) GAP model. Comparing the average (weighted beta) conveys the same information as for the sign of the exposure, although it is uninformative in terms of magnitude of the exposure.")],
    scheme=["Official solution table: Maturity GAP 1000 − 880 = 120; Standardized GAP 976 − 804 = 172; weighted betas 0.98 and 0.91.",
            f"Check: assets 460×0.95 + 80×1.1 + 60×1.05 + 120×0.9 + 280×1 = {sa:.0f}; liabilities 380×0.8 + 140×1.1 + 120×0.95 + 160×1 + 80×0.9 = {sl:.0f}.",
            "Where marks are lost: counting equity as a rate-sensitive liability; treating the 10-year variable-rate bonds as an asset (they are issued bonds, a liability)."],
    cites=[cite("IRR", 53, "The Beta GAP is derived from multiplying the amount of RSAs by the associated beta factors and summing across all rate-sensitive assets")],
    groups=["S6"], units=["IRR-U16"], slides=[53, 54, 55], minutes=6,
    check="Adapted, not verbatim: the source prints only the solution tables (no question wording), and its text layer runs the asset and liability columns together. The table was rebuilt so that it reproduces the printed totals exactly (assets 1000, RSL 880, beta-weighted 976 and 804), which puts the 10-yr variable-rate bonds on the liability side. Please check the table against page 2 of the PDF."))

# ================================================================================================
# GENERATED HARD QUESTIONS (fill unit gaps; one Hard per deck section)
# ================================================================================================
EP, CM = "numerical exercise with 2 MCQ sub-questions", "concept MCQ (statements)"


def hq(**kw):
    units, groups = kw.pop("units"), kw["groups"]
    q = question(course="30178", **kw)
    q["units"] = units
    q["negative_marking"] = NEG
    return q


def statements_mcq(n, intro, stmts, options, correct):
    """stmts: list of (text, truth). options: list of (text, trap) where text lists roman numerals."""
    roman = ["I", "II", "III", "IV", "V", "VI"]
    true_set = [roman[i] for i, (_, t) in enumerate(stmts) if t]
    assert correct == fmt_set(true_set), (correct, true_set)
    body = intro + "\n\n" + "\n".join(f"{roman[i]}. {s}" for i, (s, _) in enumerate(stmts)) + "\n\nWhich of the statements are correct?"
    return mcq(n, body, options, correct, 0.8)


def fmt_set(xs):
    xs = list(xs)
    if len(xs) == 1:
        return f"{xs[0]} only"
    return ", ".join(xs[:-1]) + f" and {xs[-1]} only"


# ---- IRR S1: repricing maturity, transmission lags and the mix effect -------------------------------
dp = 0.015
liq, var_m, fix_m, cur, term, ib = 100.0, 400.0, 300.0, 500.0, 200.0, 100.0
d_ii = liq * dp * 1 + var_m * dp * 0.5
d_ie = cur * 0.20 * dp + ib * dp * 0.75
d1 = d_ii - d_ie
near(d1, 1.875)
t_contract = liq * dp - d_ie                                  # variable mortgages treated as not repricing (20-yr maturity)
t_fullyear = liq * dp + var_m * dp - (cur * 0.2 * dp + ib * dp)  # timing ignored
t_passall = d_ii - (cur * dp + ib * dp * 0.75)                  # deposits pass-through taken as 100%
p1 = mcq("1.1", "The policy rate rises by 1.5 percentage points today and stays there. Compared with no change, by how much does Bank Lambda's net interest income over the next 12 months change, in € million?",
         [(f"+{f(d1, 3)}", None), (f(t_contract, 3), "contractual_maturity_used_for_variable_mortgages"),
          (f"+{f(t_fullyear, 3)}", "repricing_dates_ignored"), (f(t_passall, 3), "full_pass_through_on_current_accounts")], f"+{f(d1, 3)}", 0.8)
base_ii = liq * 0.01 + var_m * 0.04 + fix_m * 0.035
new_ii = (liq - 50) * (0.01 + dp) + var_m * (0.04 * 0.5 + (0.04 + dp) * 0.5) + fix_m * 0.035 + 50 * 0.045
d2 = new_ii - base_ii - d_ie
near(d2, d1 + 50 * (0.045 - (0.01 + dp)))
t_preshock = d1 + 50 * (0.045 - 0.01)
t_nomix = d1
p2 = mcq("1.2", "At the same moment Bank Lambda moves €50 million from liquid assets into new fixed-rate mortgages at 4.5%. Compared with no rate change and no move, by how much does its net interest income over the next 12 months change, in € million?",
         [(f"+{f(d2, 3)}", None), (f"+{f(t_preshock, 3)}", "mix_effect_valued_at_the_pre_shock_liquid_yield"),
          (f"+{f(t_nomix, 3)}", "mix_change_ignored"), (f"+{f(d2 + 50 * (0.01 + dp), 3)}", "liquid_assets_not_reduced_by_the_move")], f"+{f(d2, 3)}", 0.8)
assert len({o for o in p2[0]["options"]}) == 4
HARD.append(hq(
    id="30178-IRR-36", deck="IRR", topic="Repricing maturity, transmission lags and the mix effect",
    objective="Interest-rate risk: why IRR matters; contractual versus repricing maturity; drivers of NII (mix, size, rates)",
    shape=EP, shape_class="exercise part",
    stem="Bank Lambda's balance sheet is below (€ million). Liquid assets reset immediately and one for one with the policy rate. The variable-rate mortgages reset one for one at their next reset date, in 6 months. The 3-month interbank funding resets one for one in 3 months. Current-account rates are administered: the bank passes on 20% of any policy-rate change, immediately. Fixed-rate items do not reprice within the year. Ignore compounding.",
    data="| Assets | € m | Rate | Liabilities and equity | € m | Rate |\n|---|---|---|---|---|---|\n| Liquid assets | 100 | 1.0% | Current-account deposits | 500 | 0.5% |\n| Variable-rate mortgages (20-yr, reset every 6 months, next in 6 months) | 400 | 4.0% | Term deposits (fixed, 3 years left) | 200 | 2.0% |\n| Fixed-rate mortgages (15-yr) | 300 | 3.5% | Interbank funding (3-month, next reset in 3 months) | 100 | 3.0% |\n| Branches and other non-earning assets | 50 | — | Equity | 50 | — |\n| **Total** | **850** | | **Total** | **850** | |",
    parts=[p1, p2],
    scheme=[f"[1.1] Steps: (1) classify by repricing, not contractual, maturity: liquid assets (now), variable mortgages (in 6 months), interbank (in 3 months), current accounts (now, 20%); fixed items never; (2) months at the new rate: 12, 6, 9, 12; (3) ΔII = 100 × 1.5% + 400 × 1.5% × 6/12 = {f(d_ii, 3)}; (4) ΔIE = 500 × 20% × 1.5% + 100 × 1.5% × 9/12 = {f(d_ie, 3)}; (5) ΔNII = {f(d_ii, 3)} − {f(d_ie, 3)} = +{f(d1, 3)}.",
            f"[1.2] Steps: (1) the moved €50m would otherwise have earned the post-shock liquid rate 1% + 1.5% = 2.5%; (2) it now earns 4.5%, a mix gain of 50 × 2.0% = {f(50 * 0.02, 3)}; (3) the rate effect from 1.1 is unchanged on the other items; (4) total = {f(d1, 3)} + {f(50 * 0.02, 3)} = +{f(d2, 3)}.",
            f"Second route for 1.2: interest income without the rise and move = {f(base_ii, 3)}; with both = {f(new_ii, 3)}; ΔII = {f(new_ii - base_ii, 3)}; minus ΔIE {f(d_ie, 3)} gives {f(d2, 3)}.",
            f"Where marks are lost: treating the 20-year variable mortgages as non-sensitive ({f(t_contract, 3)}); ignoring reset dates (+{f(t_fullyear, 3)}); passing the whole rise to current accounts ({f(t_passall, 3)}); valuing the mix gain at the old 1% liquid yield (+{f(t_preshock, 3)}).",
            "Not needed: the branches, equity and the term deposits' rate (extraneous)."],
    cites=[cite("IRR", 7, "Contractual maturity: when an instrument expires or must be repaid. Repricing maturity: when its interest rate can change."),
           cite("IRR", 12, "Transmission occurs with delays and varies according to loan maturity, fixed versus variable rates, credit risk, competition and banks’ funding structures."),
           cite("IRR", 9, "Effect: NII increases by €0.4 because the bank holds more higher- yielding loans.")],
    location="IRR deck slides 3–13 (why IRR matters; contractual vs repricing maturity; NII drivers; monetary transmission)",
    file=F_IRR, slides=[3, 7, 8, 9, 10, 12], groups=["S1", "S6"], minutes=9,
    notches=["extra_classification", "chain", "cross_section", "extraneous_data"],
    hc_parts=[{"n": "1.1", "steps": 5, "concepts": 3}, {"n": "1.2", "steps": 4, "concepts": 2}],
    units=["IRR-U2", "IRR-U3", "IRR-U4"]))

# ---- IRR S2: refinancing vs reinvestment, NII vs EVE, ALM/ALCO, why IRR matters (statements) ---------
st = [("A bank that funds a 5-year fixed-rate car loan with 1-year CDs is exposed to refinancing risk: if rates rise, its spread may drop when the CDs roll over.", True),
      ("A bank that funds a 3-year fixed-rate commercial loan with a 5-year fixed-rate time deposit is exposed to refinancing risk, because its liability must be replaced before its asset matures.", False),
      ("Under the economic-value perspective, a rate rise lowers the market value of both fixed-rate assets and fixed-rate liabilities, so the economic value of equity is unchanged whenever both fall.", False),
      ("The ALCO oversees the bank's ALM framework: it sets limits and coordinates balance-sheet, funding and hedging decisions, looking at the effect of rates on both current earnings and EVE.", True),
      ("Interest-earning assets and interest-bearing liabilities dominate bank balance sheets and banks are highly levered, which is why net interest income is a major component of bank profitability.", True)]
p1 = statements_mcq("1", "Consider the following statements about interest-rate risk.", st,
                    [("I, IV and V only", None), ("I, II, IV and V only", "refinancing_and_reinvestment_swapped"),
                     ("I, III, IV and V only", "eve_change_is_the_difference_not_the_sign"), ("IV and V only", "car_loan_example_misread")], "I, IV and V only")
HARD.append(hq(
    id="30178-IRR-37", deck="IRR", topic="Refinancing versus reinvestment risk, NII versus EVE, and the ALCO",
    objective="Interest-rate risk: definition, refinancing and reinvestment risk, income vs economic-value perspective, ALM",
    shape=CM, shape_class="concept MCQ",
    stem="Interest-rate risk: statements.", parts=[p1],
    scheme=["[1] Steps: (1) I is true: assets longer than liabilities means refinancing risk (slides 15–16); (2) II is false: the liability (5 years) outlives the asset (3 years), which is reinvestment risk (slides 17–18); (3) III is false: ΔEVE = ΔMVA − ΔMVL, so both falling says nothing about EVE unless the falls are equal (slides 14, 20, 76); (4) IV is true (slide 21); (5) V is true (slides 4–6); (6) so I, IV and V.",
            "Second route: II and III both contain a correct first half and a wrong conclusion (near-true statements); striking the conclusion leaves only I, IV and V standing.",
            "Where marks are lost: swapping refinancing and reinvestment risk; reading 'both fall' as 'no change'."],
    cites=[cite("IRR", 15, "It occurs when the bank is holding assets with maturities greater than the maturities of its liabilities"),
           cite("IRR", 17, "This risk occurs when the bank is holding assets with maturities lower than the maturities of its liabilities"),
           cite("IRR", 21, "Sets limits and coordinates balance-sheet, funding and hedging decisions."),
           cite("IRR", 3, "Interest-earning assets and interest-bearing liabilities dominate bank balance sheets.")],
    location="IRR deck slides 3–21 (why IRR matters; definition; refinancing and reinvestment risk; two perspectives; ALM and ALCO)",
    file=F_IRR, slides=[3, 4, 5, 14, 15, 16, 17, 18, 20, 21], groups=["S2", "S1"], minutes=3.5,
    notches=["near_true_statements", "cross_section"],
    hc_parts=[{"n": "1", "steps": 6, "concepts": 3}],
    units=["IRR-U1", "IRR-U5", "IRR-U6", "IRR-U7"]))

# ---- IRR S3: classify, GAP, ΔNII; then the CD switch that meets a GAP/NW limit ----------------------
A3 = [("Overnight interbank loans", 60, True), ("6-month Treasury bills", 90, True), ("Fixed-rate business loans maturing in 9 months", 110, True),
      ("10-year variable-rate mortgages, next reset in 18 months", 150, False), ("3-year fixed-rate consumer loans", 200, False),
      ("5-year fixed-rate government bonds", 140, False), ("Cash in vault, branches and other non-earning assets", 50, False)]
L3 = [("Non-interest-bearing demand deposits", 120, False), ("Savings accounts (rate adjusted at the bank's discretion; treat as rate-sensitive)", 180, True),
      ("3-month CDs", 150, True), ("2-year fixed-rate term deposits", 170, False), ("Variable-rate bonds issued, reset every 6 months", 80, True),
      ("7-year fixed-rate subordinated bonds", 40, False), ("Equity", 60, False)]
assert sum(a for _, a, _ in A3) == sum(a for _, a, _ in L3) == 800
RSA3 = sum(a for _, a, s in A3 if s); RSL3 = sum(a for _, a, s in L3 if s); G3 = RSA3 - RSL3
di3 = 0.008
dn3 = G3 * di3
near(dn3, -1.2)
p1 = mcq("1.1", "Using a one-year gapping period, what change in net interest income does the repricing GAP model predict if all rates rise by 0.8 percentage points, in € million?",
         [(f(dn3, 2), None), (f((RSA3 + 150 - RSL3) * di3, 2), "variable_mortgages_counted_by_reset_frequency_not_next_reset"),
          (f((RSA3 - RSL3 - 120) * di3, 2), "non_interest_bearing_deposits_counted_as_rsl"), (f((RSA3 - 110 - RSL3) * di3, 2), "maturing_fixed_rate_loan_left_out")], f(dn3, 2), 0.8)
band = 0.15 * 60
switch = RSL3 - (RSA3 + band)
near(switch, 141)
assert switch <= 150
p2 = mcq("1.2", "The ALCO limits the one-year GAP to between −15% and +15% of equity (net worth). The bank will replace some 3-month CDs with 2-year fixed-rate term deposits. What is the smallest amount of CDs, in € million, it must switch?",
         [(f(switch, 0), None), (f(RSL3 - RSA3 - 0.15 * 800, 0), "limit_applied_to_total_assets"),
          (f(-G3, 0), "gap_closed_to_zero"), (f(RSL3 - RSA3 - 0.15 * 750, 1), "limit_applied_to_earning_assets")], f(switch, 0), 0.8)
HARD.append(hq(
    id="30178-IRR-38", deck="IRR", topic="Classify, measure the GAP, then meet an ALCO limit by lengthening funding",
    objective="Interest-rate risk: repricing (static) GAP, rate sensitivity by maturity or repricing, managing the GAP",
    shape=EP, shape_class="exercise part",
    stem="Bank Mu's balance sheet is below (€ million). Treat an item as rate-sensitive within the gapping period if it matures or reprices in that period.",
    data="| Assets | € m | Liabilities and equity | € m |\n|---|---|---|---|\n" + "\n".join(f"| {a[0]} | {a[1]} | {l[0]} | {l[1]} |" for a, l in zip(A3, L3)) + "\n| **Total** | **800** | **Total** | **800** |",
    parts=[p1, p2],
    scheme=[f"[1.1] Steps: (1) classify: RSA = overnight loans 60 + T-bills 90 + business loans maturing in 9 months 110 (matures) = {RSA3}; the mortgages' next reset is in 18 months, so not sensitive; (2) RSL = savings 180 + 3-month CDs 150 + variable-rate bonds 80 = {RSL3}; non-interest-bearing deposits are not RSL; (3) GAP = {RSA3} − {RSL3} = {G3}; (4) ΔNII = GAP × Δi = {G3} × 0.8% = {f(dn3, 2)}; (5) liability-sensitive, so the rise hurts.",
            f"[1.2] Steps: (1) band = ±15% × equity 60 = ±{f(band, 0)}; (2) the GAP must rise from {G3} to at least −{f(band, 0)}; (3) switching CDs to 2-year deposits removes them from RSL one for one, so RSL must fall to {RSA3} + {f(band, 0)} = {f(RSA3 + band, 0)}; (4) switch = {RSL3} − {f(RSA3 + band, 0)} = {f(switch, 0)} (≤ the 150 of CDs available).",
            f"Second route for 1.2: new GAP = {RSA3} − ({RSL3} − {f(switch, 0)}) = {f(RSA3 - RSL3 + switch, 0)} = −15% × 60.",
            "Where marks are lost: counting the variable mortgages as sensitive; treating demand deposits that pay no interest as RSL; leaving out the fixed-rate loan that matures within the year; applying the ±15% to total or earning assets instead of equity."],
    cites=[cite("IRR", 29, "Maturity: If any asset or liability matures within a given time interval"),
           cite("IRR", 26, "∆NIIEXP = GAP x ∆iEXP"),
           cite("IRR", 38, "Match fund re-priceable assets with similar re-priceable liabilities so that periodic GAPs approach zero"),
           cite("IRR", 69, "ALCO policies often set a target range, e.g. one-year cumulative GAP between –15% and +15% of net worth.")],
    location="IRR deck slides 22–39 (repricing GAP, rate sensitivity, managing the GAP) and slide 69 (GAP/NW limit)",
    file=F_IRR, slides=[22, 25, 26, 28, 29, 30, 38, 69], groups=["S3", "S4", "S7"], minutes=9,
    notches=["extra_classification", "working_backwards", "cross_section"],
    hc_parts=[{"n": "1.1", "steps": 5, "concepts": 2}, {"n": "1.2", "steps": 4, "concepts": 2}],
    units=["IRR-U8", "IRR-U9", "IRR-U10", "IRR-U12", "IRR-U20"]))

# ---- IRR S5: maturity buckets with behavioural deposits, then the timed ΔNII ----------------------
dd_share = 0.25
b03 = (40 + 100) - (dd_share * 400 + 120)
b36 = 220 - 0
b612 = 130 - 80
cum6 = b03 + b36
near(cum6, 140)
p1 = mcq("1.1", "Build the 0–3 month and >3–6 month buckets. What is Bank Nu's cumulative GAP at 6 months, in € million?",
         [(f"+{f(cum6, 0)}", None), (f(40 + 100 - (400 + 120) + b36, 0), "all_demand_deposits_treated_as_rate_sensitive"),
          (f"+{f(b36, 0)}", "periodic_gap_quoted_as_cumulative"), (f"+{f(40 + 100 - dd_share * 400 + b36, 0)}", "wholesale_funding_left_out")], f"+{f(cum6, 0)}", 0.8)
months = {"cash": (40, 12), "ib": (100, 9), "var": (220, 8), "fix": (130, 2)}
lmon = {"dd": (dd_share * 400, 12), "wh": (120, 10), "cd": (80, 3)}
dii = sum(a * m / 12 for a, m in months.values()) * 0.01
die = sum(a * m / 12 for a, m in lmon.values()) * 0.01
dt = dii - die
static = (40 + 100 + 220 + 130 - (100 + 120 + 80)) * 0.01
near(static, 1.90)
p2 = mcq("1.2", "Rates rise by 1 percentage point today, once. Each rate-sensitive item reprices on its own date (given in the table) and keeps the new rate to the year end. By how much does net interest income over the next 12 months change, in € million?",
         [(f"+{f(dt, 2)}", None), (f"+{f(static, 2)}", "static_one_year_gap_ignores_timing"),
          (f(dii - (400 * 12 / 12 + 120 * 10 / 12 + 80 * 3 / 12) * 0.01, 2), "all_demand_deposits_treated_as_rate_sensitive"),
          (f"+{f(dt - 0.4, 2)}", "cash_and_reserves_left_out")], f"+{f(dt, 2)}", 0.8)
HARD.append(hq(
    id="30178-IRR-39", deck="IRR", topic="Maturity buckets with behavioural deposits, then the timing of the NII effect",
    objective="Interest-rate risk: maturity-bucket approach, periodic and cumulative GAP, timing of income effects",
    shape=EP, shape_class="exercise part",
    stem="Bank Nu's balance sheet is below (€ million). Use the buckets 0–3 months, >3–6 months, >6–12 months and >1 year. The bank estimates that 25% of its demand deposits are behaviourally rate-sensitive and reprice immediately; the rest are core funding that does not reprice within the year.",
    data="| Assets | € m | Reprices | Liabilities and equity | € m | Reprices |\n|---|---|---|---|---|---|\n| Cash and reserves | 40 | now | Demand deposits | 400 | 25% now; 75% not within the year |\n| 3-month interbank loans | 100 | in 3 months | Wholesale funding (reprices quarterly, next in 2 months) | 120 | in 2 months |\n| Variable-rate corporate loans (reset every 6 months, next in 4 months) | 220 | in 4 months | 9-month CDs | 80 | in 9 months |\n| Fixed-rate loans maturing in 10 months | 130 | in 10 months | 3-year fixed-rate bonds issued | 150 | not within the year |\n| 20-year fixed-rate mortgages | 310 | not within the year | Equity | 100 | — |\n| Non-earning assets | 50 | — | | | |\n| **Total** | **850** | | **Total** | **850** | |",
    parts=[p1, p2],
    scheme=[f"[1.1] Steps: (1) sensitive demand deposits = 25% × 400 = {f(dd_share * 400, 0)}; (2) 0–3m: RSA 40 + 100 = 140, RSL 100 + 120 = 220, periodic {f(b03, 0)}; (3) >3–6m: RSA 220 (next reset in 4 months), RSL 0, periodic +{f(b36, 0)}; (4) cumulative at 6 months = {f(b03, 0)} + {f(b36, 0)} = +{f(cum6, 0)}; (5) the 0–3m bucket is liability-sensitive even though the 6-month total is asset-sensitive. (>6–12m would add +{f(b612, 0)}, cumulative +{f(cum6 + b612, 0)}.)",
            f"[1.2] Steps: (1) months at the new rate: cash 12, interbank 9, corporate loans 8, maturing fixed loans 2; deposits 12, wholesale 10, CDs 3; (2) ΔII = 1% × (40 + 100×9/12 + 220×8/12 + 130×2/12) = {f(dii, 4)}; (3) ΔIE = 1% × (100 + 120×10/12 + 80×3/12) = {f(die, 4)}; (4) ΔNII = +{f(dt, 4)}, so +{f(dt, 2)}; (5) compare the static one-year GAP estimate: (490 − 300) × 1% = +{f(static, 2)}: timing cuts the gain by two-thirds because the liabilities reprice first.",
            f"Second route for 1.2: bucket by bucket with each item's months: 0–3m items give 1% × (40×12 + 100×9 − 100×12 − 120×10)/12 = {f((40 * 12 + 100 * 9 - 100 * 12 - 120 * 10) / 12 * 0.01, 4)}; later items give 1% × (220×8 + 130×2 − 80×3)/12 = {f((220 * 8 + 130 * 2 - 80 * 3) / 12 * 0.01, 4)}; sum {f(dt, 4)}.",
            "Where marks are lost: making all 400 of demand deposits sensitive; quoting a periodic GAP as cumulative; using the static one-year GAP (+1.90), which ignores when items reprice; leaving out the cash."],
    cites=[cite("IRR", 45, "The Gap for each time bucket and measures the timing of potential income effects from interest rate changes"),
           cite("IRR", 45, "The sum of periodic GAP's and measures aggregate interest rate risk over the entire period"),
           cite("IRR", 42, "Demand deposits 300 30% “behaviorally” rate-sensitive")],
    location="IRR deck slides 42–49 (Bank Alpha; maturity-bucket approach; periodic and cumulative GAP)",
    file=F_IRR, slides=[42, 44, 45, 46, 47], groups=["S5", "S3"], minutes=9,
    notches=["extra_classification", "extra_step", "what_if_followon", "chain"],
    hc_parts=[{"n": "1.1", "steps": 5, "concepts": 2}, {"n": "1.2", "steps": 5, "concepts": 3}],
    units=["IRR-U14", "IRR-U9"]))

# ---- IRR S6: asymmetric pass-through; beta GAP up and down ----------------------------------------
items6 = {"loans": (500, 0.95, 0.60, "A"), "ib": (100, 1.00, 1.00, "A"), "dep": (600, 0.25, 0.40, "L"), "wh": (150, 0.95, 0.95, "L")}
gup = sum(a * u * (1 if s == "A" else -1) for a, u, d, s in items6.values())
gdn = sum(a * d * (1 if s == "A" else -1) for a, u, d, s in items6.values())
near(gup, 282.5); near(gdn, 17.5)
up, dn = 0.0125, -0.02
e1 = gup * up
p1 = mcq("1.1", "Euribor 3m rises by 1.25 percentage points. Using the beta GAP, by how much does Bank Xi's annual net interest income change, in € million?",
         [(f"+{f(e1, 2)}", None), (f(-150 * up, 2), "static_gap_used"), (f"+{f(gdn * up, 2)}", "downward_betas_used_for_a_rise"),
          (f((575 - 750) * up, 2), "betas_applied_to_assets_only")], f"+{f(e1, 2)}", 0.8)
e2 = gup * up + gdn * dn
per_item = sum(a * (u * up + d * dn) * (1 if s == "A" else -1) for a, u, d, s in items6.values())
near(e2, per_item)
p2 = mcq("1.2", "Euribor then falls by 2.0 percentage points from its new level, so it ends 0.75 points below where it started. Compared with the start, by how much has annual net interest income changed after both moves, in € million?",
         [(f"+{f(e2, 2)}", None), (f(gup * (up + dn), 2), "upward_betas_used_for_the_fall"),
          (f"+{f(-150 * (up + dn), 2)}", "static_gap_used"), (f(gdn * (up + dn), 2), "downward_betas_used_for_both_moves")], f"+{f(e2, 2)}", 0.8)
HARD.append(hq(
    id="30178-IRR-40", deck="IRR", topic="Asymmetric pass-through: beta GAP when rates rise, then fall",
    objective="Interest-rate risk: spread effect, deposit betas and the standardised (beta) GAP",
    shape=EP, shape_class="exercise part",
    stem="Bank Xi's rate-sensitive items over a one-year gapping period are below (€ million), with the estimated betas to Euribor 3m. Following the deck, loan rates follow rises faster than falls and higher rates reach depositors only slowly, so each item has one estimated beta for rises and one for falls (given below). The bank also holds €900 million of fixed-rate assets and €850 million of fixed-rate liabilities and equity that do not reprice within the year.",
    data="| Item | Side | € m | Beta when Euribor rises | Beta when Euribor falls |\n|---|---|---|---|---|\n| Variable-rate loans | asset | 500 | 0.95 | 0.60 |\n| Interbank deposits | asset | 100 | 1.00 | 1.00 |\n| Retail sight deposits (rate administered) | liability | 600 | 0.25 | 0.40 |\n| Wholesale funding | liability | 150 | 0.95 | 0.95 |",
    parts=[p1, p2],
    scheme=[f"[1.1] Steps: (1) static GAP = 600 − 750 = −150 (would predict a loss); (2) beta-weighted RSA = 500×0.95 + 100 = 575; (3) beta-weighted RSL = 600×0.25 + 150×0.95 = 292.5; (4) beta GAP = +{f(gup, 1)}; (5) ΔNII = {f(gup, 1)} × 1.25% = +{f(e1, 4)}.",
            f"[1.2] Steps: (1) choose the falling betas for the second move; (2) falling beta GAP = 500×0.60 + 100 − (600×0.40 + 150×0.95) = {f(gdn, 1)}; (3) effect of the fall = {f(gdn, 1)} × (−2%) = {f(gdn * dn, 3)}; (4) total = {f(e1, 4)} {f(gdn * dn, 3)} = {f(e2, 4)}; (5) NII ends higher although Euribor ends lower: the spread effect from asymmetric pass-through.",
            f"Second route for 1.2: net rate change per item: loans 0.95×1.25 − 0.60×2 = −0.0125 pts (−0.0625), interbank −0.75 pts (−0.75), deposits 0.25×1.25 − 0.40×2 = −0.4875 pts (expense −2.925), wholesale 0.95×(−0.75) = −0.7125 pts (expense −1.069); ΔNII = −0.0625 − 0.75 + 2.925 + 1.069 = {f(per_item, 4)}.",
            "Where marks are lost: using the static GAP; applying the rising betas to the fall (the model assumes symmetry, the deck says it fails); weighting only the assets.",
            "Not needed: the fixed-rate balances (extraneous)."],
    cites=[cite("IRR", 50, "Banks tend to raise loan rates quickly when rates rise, but lower them slowly when rates fall"),
           cite("IRR", 50, "Banks are similarly slow to pass higher rates through to depositors"),
           cite("IRR", 53, "The Beta GAP is derived from multiplying the amount of RSAs by the associated beta factors and summing across all rate-sensitive assets"),
           cite("IRR", 57, "Spread effect: RSA and RSL don't move by equal amounts even when the general rate level changes")],
    location="IRR deck slides 50–60 (spread effect, deposit betas, beta GAP, level vs spread effect)",
    file=F_IRR, slides=[50, 51, 52, 53, 54, 57], groups=["S6"], minutes=9,
    notches=["what_if_followon", "chain", "extra_classification", "extraneous_data"],
    hc_parts=[{"n": "1.1", "steps": 5, "concepts": 2}, {"n": "1.2", "steps": 5, "concepts": 3}],
    units=["IRR-U15", "IRR-U16", "IRR-U17"]))

# ---- IRR S7: caps and floors ------------------------------------------------------------------------
eur0 = 0.03
mort, whs, ret = 400.0, 200.0, 300.0


def rates(e, mort_floor=None):
    m = min(e + 0.02, 0.06)
    if mort_floor is not None:
        m = max(m, mort_floor)
    w = min(e + 0.005, 0.045)
    d = max(e - 0.015, 0.005)
    return m, w, d


def nii_change(e, mort_floor=None, cap=True, dep_floor=True, wh=True):
    m0, w0, d0 = rates(eur0)
    m, w, d = rates(e, mort_floor)
    if not cap:
        m, w = e + 0.02, e + 0.005
    if not dep_floor:
        d = e - 0.015
    return mort * (m - m0) - (whs * (w - w0) if wh else 0) - ret * (d - d0)


a1 = nii_change(0.055)
near(a1, -5.5)
p1 = mcq("1.1", "Euribor rises by 2.5 percentage points, to 5.5%, for the whole year. What is the change in Bank Omicron's annual net interest income, in € million?",
         [(f(a1, 1), None), (f(nii_change(0.055, cap=False), 1), "caps_ignored"),
          (f(mort * 0.025 - whs * 0.01 - ret * 0.025, 1), "mortgage_cap_ignored"), (f(mort * 0.01 - whs * 0.025 - ret * 0.025, 1), "wholesale_cap_ignored")], f(a1, 1), 0.8)
b0 = nii_change(0.005)
near(b0, -2.0)
need_fall = (whs * 0.025 + ret * 0.01) / mort       # largest mortgage-rate fall that keeps ΔNII ≥ 0
floor = rates(eur0)[0] - need_fall
near(nii_change(0.005, mort_floor=floor), 0)
near(floor, 0.03)
t_nowh = rates(eur0)[0] - (ret * 0.01) / mort
p2 = mcq("1.2", "Now suppose instead that Euribor falls by 2.5 percentage points, to 0.5%, for the whole year. What floor on the mortgage rate would keep annual net interest income from falling at all?",
         [(f(floor * 100, 2) + "%", None), (f(t_nowh * 100, 2) + "%", "wholesale_funding_saving_ignored"),
          (f(2.5, 2) + "%", "deposit_floor_ignored_so_no_floor_seems_needed"), (f(5.0, 2) + "%", "floor_set_at_todays_rate")], f(floor * 100, 2) + "%", 0.8)
HARD.append(hq(
    id="30178-IRR-41", deck="IRR", topic="Caps and floors: when embedded limits bind",
    objective="Interest-rate risk: embedded options (caps and floors) and their effect on NII",
    shape=EP, shape_class="exercise part",
    stem="Bank Omicron (€ million). Euribor is 3.0% today. Variable-rate mortgages of 400 pay Euribor + 2.0% with a cap of 6.0% (today 5.0%). Wholesale funding of 200 costs Euribor + 0.5% with a cap of 4.5% (today 3.5%). Retail deposits of 300 pay Euribor − 1.5% with a floor of 0.5% (today 1.5%). Term deposits of 250 pay a fixed 2.0% until maturity in 3 years. All variable items reset immediately.",
    parts=[p1, p2],
    scheme=[f"[1.1] Steps: (1) mortgages: 5.5% + 2.0% = 7.5% > cap, so 6.0% (+1.0 pt); (2) wholesale: 6.0% > cap, so 4.5% (+1.0 pt); (3) deposits: 4.0%, above the floor (+2.5 pts); (4) ΔII = 400 × 1.0% = 4.0; (5) ΔIE = 200 × 1.0% + 300 × 2.5% = 9.5; (6) ΔNII = {f(a1, 1)}. The asset cap hurts the bank, the liability cap helps it.",
            f"[1.2] Steps: (1) without a mortgage floor: mortgages 2.5% (−2.5 pts, −10.0); wholesale 1.0% (−2.5 pts, saves 5.0); deposits −1.0% hits the 0.5% floor, so only −1.0 pt (saves 3.0); ΔNII = {f(b0, 1)}; (2) savings available = 5.0 + 3.0 = 8.0, so the mortgage rate may fall at most 8.0 / 400 = {f(need_fall * 100, 1)} pts; (3) floor = 5.0% − {f(need_fall * 100, 1)}% = {f(floor * 100, 2)}%; (4) check: with the floor ΔNII = −8.0 + 5.0 + 3.0 = 0.",
            "Second route for 1.2: set 400 × (5.0% − F) = 200 × 2.5% + 300 × 1.0% and solve F = 3.0%.",
            f"Where marks are lost: ignoring the caps ({f(nii_change(0.055, cap=False), 1)}); letting deposits fall below their floor, which makes the fall look harmless; forgetting the wholesale saving ({f(t_nowh * 100, 2)}%).",
            "Not needed: the fixed-rate term deposits (extraneous)."],
    cites=[cite("IRR", 64, "6% cap on €250m variable mortgages: Euribor pushes the mortgage rate to 7%, bank stuck earning 6%."),
           cite("IRR", 64, "5% cap on €150m wholesale funding: market rates hit 7%, bank still only pays 5%."),
           cite("IRR", 64, "2% floor on term deposits: rates fall to 0%, bank must still pay 2%."),
           cite("IRR", 62, "Caps on loan or deposit rates")],
    location="IRR deck slides 61–64 (embedded options; caps and floors)",
    file=F_IRR, slides=[61, 62, 63, 64], groups=["S7"], minutes=9,
    notches=["extra_classification", "working_backwards", "what_if_followon", "extraneous_data"],
    hc_parts=[{"n": "1.1", "steps": 6, "concepts": 2}, {"n": "1.2", "steps": 4, "concepts": 2}],
    units=["IRR-U18", "IRR-U18b"]))

# ---- INTRO I1: classify three banks by business model; then a universal-bank target ---------------
banks = {"P": (6000, 1800, 600, 100, 3400), "Q": (4100, 2300, 1700, 100, 4264), "R": (3200, 2900, 1700, 200, 5600)}
share = {k: v[0] / sum(v[:4]) for k, v in banks.items()}
ci = {k: v[4] / sum(v[:4]) for k, v in banks.items()}
near(share["P"], 6000 / 8500); near(share["Q"], 0.5); near(share["R"], 0.4); near(ci["Q"], 0.52); near(ci["R"], 0.70); near(ci["P"], 0.4)
ok = "P commercial/retail; Q universal; R investment-banking-heavy"
p1 = mcq("1.1", "Using the deck's benchmarks for the three business models, how would you classify the three banks?",
         [(ok, None), ("P commercial/retail; Q commercial/retail; R universal", "trading_income_left_out_of_operating_income"),
          ("P universal; Q investment-banking-heavy; R investment-banking-heavy", "classified_by_cost_to_income_over_nii_not_total_income"),
          ("P commercial/retail; Q investment-banking-heavy; R universal", "nii_share_and_cost_to_income_read_the_wrong_way")], ok, 0.8)
tot_p = sum(banks["P"][:4])
need = 2 * 6000 - tot_p
new_ci = (3400 + 0.7 * need) / (tot_p + need)
near(need, 3500); near(new_ci, 5850 / 12000)
t55 = 6000 / 0.55 - tot_p
p2 = mcq("1.2", "Bank P wants to look like a universal bank, with NII exactly 50% of total operating income. NII and other income stay the same; the extra fee and trading income comes with extra operating expenses equal to 70% of it. What would P's cost-to-income ratio be?",
         [(f(new_ci * 100, 1) + "%", None), (f(3400 / 12000 * 100, 1) + "%", "extra_costs_ignored"),
          ("70.0%", "marginal_cost_ratio_quoted"), (f((3400 + 0.7 * t55) / (tot_p + t55) * 100, 1) + "%", "fifty_five_percent_target_used")], f(new_ci * 100, 1) + "%", 0.8)
HARD.append(hq(
    id="30178-INTRO-10", deck="INTRO", topic="Classifying banks by business model, then re-engineering one",
    objective="What banks do: business models (commercial, investment, universal) and their income and cost structure",
    shape=EP, shape_class="exercise part",
    stem="Three banks report (€ million). The deck's benchmarks: commercial/retail banks have NII above 55–75% of revenues and cost-to-income of about 38–43%; investment-banking-heavy banks earn 57–60% from non-interest income with cost-to-income of 62–76%; universal banks split about 50/50 with cost-to-income around 52%. Bank R also reports total assets of €610 billion and 1,900 branches.",
    data="| € m | Bank P | Bank Q | Bank R |\n|---|---|---|---|\n| Net interest income | 6,000 | 4,100 | 3,200 |\n| Net fee and commission income | 1,800 | 2,300 | 2,900 |\n| Net trading and investment income | 600 | 1,700 | 1,700 |\n| Other operating income | 100 | 100 | 200 |\n| Operating expenses | 3,400 | 4,264 | 5,600 |",
    parts=[p1, p2],
    scheme=[f"[1.1] Steps: (1) total operating income: P 8,500, Q 8,200, R 8,000; (2) NII share: P {f(share['P'] * 100)}%, Q 50.0%, R 40.0% (non-interest 60%); (3) cost-to-income: P 40.0%, Q 52.0%, R 70.0%; (4) match both benchmarks: P commercial, Q universal, R investment-banking-heavy.",
            f"[1.2] Steps: (1) NII 6,000 must be 50%, so total income = 12,000; (2) extra fee/trading income = 12,000 − 8,500 = {need:,.0f}; (3) extra costs = 70% × {need:,.0f} = {0.7 * need:,.0f}; (4) new opex = 3,400 + {0.7 * need:,.0f} = {3400 + 0.7 * need:,.0f}; (5) cost-to-income = {3400 + 0.7 * need:,.0f} / 12,000 = {f(new_ci * 100, 2)}%, so {f(new_ci * 100, 1)}%.",
            f"Second route for 1.2: the new ratio is a revenue-weighted average: (8,500 × 40% + {need:,.0f} × 70%) / 12,000 = {f(new_ci * 100, 2)}%.",
            "Where marks are lost: leaving trading income out of revenue; dividing costs by NII; forgetting the costs that come with the new revenue (28.3%).",
            "Not needed: Bank R's total assets and branch count (extraneous)."],
    cites=[cite("INTRO", "Main Takeaways – Business Models", "Revenues dominated by net interest income (NII > 55–75%)"),
           cite("INTRO", "Main Takeaways – Business Models", "High cost-to-income (62-76%), weaker efficiency vs peers"),
           cite("INTRO", "Main Takeaways – Business Models", "More balanced model between NII and non-interest (≈50/50 split)")],
    location="INTRO deck: business models, universal banks and 'Main Takeaways – Business Models'",
    file=F_INTRO, groups=["I1", "I2"], minutes=9,
    notches=["extra_classification", "working_backwards", "chain", "extraneous_data"],
    hc_parts=[{"n": "1.1", "steps": 4, "concepts": 2}, {"n": "1.2", "steps": 5, "concepts": 2}],
    units=["INTRO-U1", "INTRO-U4", "INTRO-U8", "INTRO-U6"]))

# ---- INTRO I3: size classes, provisions vs capital, transformation, regulation (statements) ---------
st = [("Smaller commercial banks collect relatively more retail deposits, while larger banks use relatively more wholesale funding and tend to be listed.", True),
      ("Banks recognise provisions for expected losses and hold capital to absorb unexpected losses.", True),
      ("Because maturity, liquidity and risk transformation create fragility, they cannot justify loan rates above deposit rates.", False),
      ("Regulation and supervision are needed because banks combine high leverage, liquid liabilities, less-liquid risky assets and strong interconnections, so one failure can spread instability.", True),
      ("A universal bank earns mostly fee income, so its main risks are operational rather than credit or interest-rate risk.", False)]
p1 = statements_mcq("1", "Consider the following statements about what banks do.", st,
                    [("I, II and IV only", None), ("I, II, III and IV only", "transformation_seen_only_as_a_cost"),
                     ("II and IV only", "size_classes_reversed"), ("I, II, IV and V only", "universal_bank_risks_misread")], "I, II and IV only")
HARD.append(hq(
    id="30178-INTRO-11", deck="INTRO", topic="Size, provisions versus capital, transformation and why banks are regulated",
    objective="What banks do: business models, risks and risk management, transformation and fragility, why regulation is needed",
    shape=CM, shape_class="concept MCQ", stem="What banks do: statements.", parts=[p1],
    scheme=["[1] Steps: (1) I true (commercial banks by size); (2) II true (risk management: provisions for expected, capital for unexpected losses); (3) III false: the deck says the transformations 'provide the rationale for an interest spread' and also create fragility; (4) IV true (why regulation and supervision are needed); (5) V false: universal banks earn a mix (≈50/50) and face credit, liquidity, interest-rate, market and operational risk; (6) I, II and IV.",
            "Second route: III and V each take a true premise (fragility; fee income matters) and draw a conclusion the deck contradicts.",
            "Where marks are lost: reading transformation only as a source of fragility; reversing which banks rely on wholesale funding."],
    cites=[cite("INTRO", "What Do Banks Do? Commercial banks", "Smaller banks collect deposits (retail customers) while large banks use (relatively more) wholesale sources of funding"),
           cite("INTRO", "Banking Activities Generate Risks", "Hold sufficient capital to absorb unexpected losses"),
           cite("INTRO", "The concepts of maturity, liquidity and risk transformation", "Provide the rationale for an interest spread (loan interest rates being higher than deposit interest rates)"),
           cite("INTRO", "Why regulation and supervision are needed", "Bank failure can therefore affect depositors, disrupt lending and payments, and spread instability through the financial system.")],
    location="INTRO deck: commercial banks by size, universal banks, risks and risk management, fragility, transformation and regulation",
    file=F_INTRO, groups=["I3", "I1"], minutes=3.5,
    notches=["near_true_statements", "cross_section"],
    hc_parts=[{"n": "1", "steps": 6, "concepts": 3}],
    units=["INTRO-U2", "INTRO-U4", "INTRO-U9", "INTRO-U11", "INTRO-U12"]))

# ---- SVB V2: deposit insurance and the macro story (statements) --------------------------------------
st = [("Deposit insurance is part of the financial safety net, alongside central bank lender-of-last-resort facilities and bank resolution mechanisms.", True),
      ("Insured deposits are less stable than uninsured deposits, because insured depositors have no reason to monitor their bank.", False),
      ("Deposit insurance typically covers retail deposits up to a limit ($250,000 in the US, €100,000 in the EU), while large corporate and interbank deposits are often excluded to keep market discipline.", True),
      ("Banks flush with uninsured deposits read the Fed's 'low for long' forward guidance as a commitment, which encouraged them to take interest-rate risk and to avoid paying for hedges.", True),
      ("US bank balance sheets grew in the zero-lower-bound and QE years mainly through insured retail deposits.", False)]
p1 = statements_mcq("1", "Consider the following statements about the macro background to the SVB case.", st,
                    [("I, III and IV only", None), ("I, II, III and IV only", "insured_deposits_thought_less_stable"),
                     ("I, III, IV and V only", "growth_attributed_to_insured_deposits"), ("III and IV only", "safety_net_components_misread")], "I, III and IV only")
HARD.append(hq(
    id="30178-SVB-05", deck="SVB", topic="Deposit insurance, forward guidance and the growth of uninsured deposits",
    objective="Interest-rate risk in practice: the SVB case (macro scenario, deposit insurance, uninsured deposits)",
    shape=CM, shape_class="concept MCQ", stem="The SVB case: statements.", parts=[p1],
    scheme=["[1] Steps: (1) I true (deposit insurance as part of the safety net); (2) II false: insured deposits are more stable, because insured depositors know they will be repaid; (3) III true (coverage and rationale); (4) IV true ('low for long' read as a commitment; hedging would eat into carry); (5) V false: growth was fuelled by over $3.5 trillion of uninsured deposits; (6) I, III and IV.",
            "Second route: II and V each reverse the deck's point about insured versus uninsured deposits; with those struck, I, III and IV remain.",
            "Where marks are lost: thinking insurance makes deposits less stable (it removes the reason to run); attributing the deposit boom to insured deposits."],
    cites=[cite("SVB", "Why deposit insurance is important in this context?", "Deposit insurance is one of several tools—alongside central bank lender-of-last-resort facilities and bank resolution mechanisms—that form the “financial safety net.”"),
           cite("SVB", "Why deposit insurance is important in this context?", "More stable. Because insured depositors have confidence that their money will be repaid even if the bank fails"),
           cite("SVB", "Period of Fed tightening", "Banks flush with uninsured deposits read the Fed's \"low for long\" forward guidance as a commitment, not a forecast"),
           cite("SVB", "Effects: Massive growth in bank balance sheets during the ZLB and QE years", "Not just SVB. Balance sheet growth fulled by over $3.5 trillion increase in US uninsured deposits")],
    location="SVB slides on the macro scenario, balance-sheet growth, deposit insurance and 'Phase 1: balance sheet growth and the carry trade'",
    file=F_SVB, groups=["V2"], minutes=3.5,
    notches=["near_true_statements", "cross_section"],
    hc_parts=[{"n": "1", "steps": 6, "concepts": 3}],
    units=["SVB-U3", "SVB-U4", "SVB-U5", "SVB-U9"]))

# ---- SVB V4: concentration, then the run arithmetic ---------------------------------------------------
top10 = 10 * 1.3
dep_total = top10 / 0.08
unins = 0.90 * dep_total
others = unins - top10
near(dep_total, 162.5); near(others, 133.25)
p1 = mcq("2.1", "Using only the slide figures, and assuming the ten largest depositors are fully uninsured, how much uninsured deposit money sits outside the top ten, in $ billion?",
         [(f(others, 2), None), (f(0.9 * 173 - top10, 2), "reading_total_used_instead_of_the_slide_implied_total"),
          (f(unins, 2), "top_ten_not_removed"), (f(0.9 * (1.3 / 0.08) * 10 - 1.3, 2), "one_depositor_removed_instead_of_ten")], f(others, 2), 0.8)
cash_a, afs_fv = 14.0, 26.0
wd = top10 + 0.25 * others
need = wd - cash_a - afs_fv
assert need > 0
ratio = 76 / 91
book = need / ratio
loss = book - need
near(loss, need * 15 / 76)
p2 = mcq("2.2", "Suppose the top ten withdraw everything and the other uninsured depositors withdraw 25%. The bank pays with $14bn of cash (an assumed figure), then sells all its AFS securities at their $26bn fair value, then sells HTM securities at the slides' end-2022 ratio of market to book value ($76bn to $91bn). What loss does it realise on the HTM sales, in $ billion?",
         [(f(loss, 2), None), ("15.00", "whole_unrealised_htm_loss_recognised"), (f(need * 15 / 91, 2), "loss_not_grossed_up_to_book_value_sold"),
          (f(max(0.0, 0.25 * unins - cash_a - afs_fv) * 15 / 76, 2), "top_ten_treated_like_other_depositors")], f(loss, 2), 0.8)
HARD.append(hq(
    id="30178-SVB-06", deck="SVB", topic="Deposit concentration and the run arithmetic",
    objective="Interest-rate risk in practice: the SVB case (liability side, uninsured and concentrated deposits, forced sales)",
    shape=EP, shape_class="exercise part",
    stem="The SVB slides report that the largest 10 depositors accounted for 8% of SVB's deposits, for an average of $1.3 billion each, and that about 90% of deposits were uninsured. The average duration of the HTM portfolio was 6.2 years (not needed here).",
    parts=[p1, p2],
    scheme=[f"[2.1] Steps: (1) top-ten deposits = 10 × 1.3 = {f(top10)}; (2) implied total = {f(top10)} / 8% = {f(dep_total)}; (3) uninsured = 90% × {f(dep_total)} = {f(unins, 2)}; (4) outside the top ten = {f(unins, 2)} − {f(top10)} = {f(others, 2)}. (The reading gives $173bn total and $13bn for the top ten at end-2022, i.e. 7.5%: close to the slide's 'about 8%'.)",
            f"[2.2] Steps: (1) withdrawals = 13 + 25% × {f(others, 2)} = {f(wd, 4)}; (2) after cash and AFS: {f(wd, 4)} − 14 − 26 = {f(need, 4)}; (3) HTM sells at 76/91 = {f(ratio, 4)} of book; (4) book value sold = {f(book, 4)}; (5) realised loss = {f(book, 4)} − {f(need, 4)} = {f(loss, 4)}, so {f(loss, 2)}.",
            f"Second route for 2.2: each $ raised from HTM costs 15/76 of equity; {f(need, 4)} × 15/76 = {f(loss, 4)}.",
            "Where marks are lost: using the reading's $173bn in 2.1 when the question says slide figures only; recognising the whole $15bn HTM loss; taking the loss per $ of book (15/91) instead of per $ raised (15/76).",
            "Not needed: the HTM duration (extraneous)."],
    cites=[cite("SVB", "Liability side: The Achilles’ heel", "Large corporate depositors: the largest 10 depositors accounted for 8% of SVB deposits, for an average of $ 1.3 bill each"),
           cite("SVB", "Liability side: The Achilles’ heel", "≈ 90% of Dep were uninsured"),
           cite("SVB", "Asset side – the HTM portfolio", "At the end of 2022, the market value of the HTM portfolio would have been $76bn vs. $91 ($15 bn of unrealized losses)"),
           cite("SVB", "Asset side – the AFS portfolio", "Over $26 bn of AFS assets: these are carried at the fair value, i.e., marked to market")],
    location="SVB slides on the liability side, the HTM and AFS portfolios and the deposit drawdown",
    file=F_SVB, groups=["V4", "V3"], minutes=9,
    notches=["working_backwards", "chain", "cross_section", "extraneous_data"],
    hc_parts=[{"n": "2.1", "steps": 4, "concepts": 2}, {"n": "2.2", "steps": 5, "concepts": 3}],
    units=["SVB-U8", "SVB-U10", "SVB-U6"]))

# ---- SVB V5: what went wrong (statements) -------------------------------------------------------------
st = [("To compensate for lower profits, SVB unwound most of its interest rate swaps by July 2022, leaving its AFS portfolio with no shock absorber.", True),
      ("Like most historical bank failures, SVB failed mainly because of credit losses on its loans.", False),
      ("SVB's depositors were connected: their venture capital backers advised them to withdraw, and they communicated with each other during the run.", True),
      ("The case shows the law of large numbers and the benefits of diversification being neglected on the funding side.", True),
      ("SVB, a regional lender with $210 billion in assets, collapsed over roughly two weeks of steady outflows.", False)]
p1 = statements_mcq("1", "Consider the following statements about why SVB failed.", st,
                    [("I, III and IV only", None), ("I, III, IV and V only", "speed_of_the_run_misread"),
                     ("I, II, III and IV only", "failure_attributed_to_credit_risk"), ("III and IV only", "hedging_story_misread")], "I, III and IV only")
HARD.append(hq(
    id="30178-SVB-07", deck="SVB", topic="What went wrong: hedges, credit versus duration, connected depositors",
    objective="Interest-rate risk in practice: the SVB case (causes, the role of technology and social media, lessons)",
    shape=CM, shape_class="concept MCQ", stem="The SVB case: statements.", parts=[p1],
    scheme=["[1] Steps: (1) I true ('Here be dragons': swaps unwound by July 2022); (2) II false: the slide's quote says SVB is the first major failure where the primary issue was a duration mismatch, not credit risk; (3) III true (connected depositors, VC advice); (4) IV true ('Law of large numbers and benefits of diversification neglected!'); (5) V false: it collapsed in two days; (6) I, III and IV.",
            "Second route: II and V contradict two of the deck's headline facts (duration, not credit; two days, not two weeks).",
            "Where marks are lost: treating SVB as a credit-risk failure; missing that the run took two days."],
    cites=[cite("SVB", "What happened in March 2023", "served the tech and life science industry for 40 years. It collapsed in two days."),
           cite("SVB", "Asset side – the AFS portfolio", "to compensate for lower profits, SVB has unwound the largest part of IRS (interest rate swaps) by July 2022"),
           cite("SVB", "Deposit drawdown: what was different this time?", "SVB depositors received advice from their venture capital backers to withdraw funds and communicated with each other during the run"),
           cite("SVB", "What was wrong, in the end? Ipse dixit", "This is the first major one I recall where the primary issue was a duration mismatch between high quality assets and deposit liabilities.")],
    location="SVB slides 'What happened', the AFS hedging strategy, 'What was different this time?' and 'What was wrong, in the end?'",
    file=F_SVB, groups=["V5", "V1", "V4"], minutes=3.5,
    notches=["near_true_statements", "cross_section"],
    hc_parts=[{"n": "1", "steps": 6, "concepts": 3}],
    units=["SVB-U1", "SVB-U7", "SVB-U11", "SVB-U12"]))

# ---- Reading (required for the exam): SVB's frailties and accounting (statements) -------------------
st = [("SVB held 43% of its total assets in the held-to-maturity bucket, which is not marked to market unless a security from that bucket is sold.", True),
      ("Under the 2019 revision of the AOCI filter, SVB opted out of reflecting unrealised losses on available-for-sale securities in regulatory capital.", True),
      ("From 2011 to 2022 time deposits made up about 10% of SVB's deposits, which made its funding relatively sticky.", False),
      ("As the Fed hiked in 2022, SVB let the duration of its fixed-income securities rise by nearly two years, to 5.6 years, while unwinding its hedges.", True),
      ("Adjusted for unrealised losses, SVB's CET1 ratio at end-2022 was about 0.9% of risk-weighted assets.", True)]
p1 = statements_mcq("1", "Consider the following statements from the required reading (Acharya, Cecchetti and Schoenholtz, 'Overview of recent banking stress').", st,
                    [("I, II, IV and V only", None), ("I, II, III, IV and V", "time_deposit_share_misread"),
                     ("I, II and IV only", "adjusted_capital_ratio_misread"), ("II, IV and V only", "htm_share_misread")], "I, II, IV and V only")
assert fmt_set(["I", "II", "IV", "V"]) == "I, II, IV and V only"
HARD.append(hq(
    id="30178-SVB-08", deck="SVB", topic="Reading: SVB's accounting choices, duration and adjusted capital",
    objective="Interest-rate risk in practice: the SVB case (required reading: frailties, accounting, adjusted capital)",
    shape=CM, shape_class="concept MCQ", stem="SVB and Beyond, chapter 1: statements.", parts=[p1],
    scheme=["[1] Steps: (1) I true (43% of total assets in HTM); (2) II true (AOCI opt-out); (3) III false: time deposits were less than 1% of deposits from 2011 through 2022; (4) IV true (duration up nearly two years to 5.6, hedges unwound); (5) V true (SVB 0.9% adjusted); (6) I, II, IV and V.",
            "Second route: the reading's own list of banks with adjusted ratios below 5% includes SVB at 0.9%, which confirms V; III contradicts the reading's point that SVB 'did little to extend the duration of their deposits'.",
            "Watch the numbers: the slides say the HTM portfolio's duration was 6.2 years and HTM was 76% of the securities portfolio; the reading says 5.6 years for all fixed-income securities and 43% of total assets. Both are right; they measure different things."],
    cites=[cite("READING", 4, "the bank opted to hold 43% of its total assets in the held-to-maturity (HTM) bucket that is not required to be marked to market"),
           cite("READING", 4, "SVB chose to “opt out” of the GAAP obligation to reflect unrealized losses in regulatory capital"),
           cite("READING", 4, "time deposits (which tend to be less run-prone than demand and savings deposits) remained less than 1% of SVB’s total deposits"),
           cite("READING", 4, "by nearly two full years to 5.6 years"),
           cite("READING", 10, "SVB (0.9%)")],
    location="Acharya, Cecchetti and Schoenholtz (2023), 'Overview of recent banking stress', SVB and Beyond, NYU Stern, pp. 2–10",
    file=F_STERN, groups=["R"], minutes=3.5,
    notches=["near_true_statements", "cross_section"],
    hc_parts=[{"n": "1", "steps": 6, "concepts": 3}],
    units=["READ-U1", "READ-U2", "READ-U5"]))

# ---- Reading: the trigger, the system-wide picture and the policy response (statements) --------------
st = [("Total US uninsured deposits rose from about $5.5 trillion at the end of 2019 to over $8 trillion by the first quarter of 2022.", True),
      ("Unrealised losses on banks' securities approached $700 billion by the third quarter of 2022, about eight times their peak in the 2017–19 tightening.", True),
      ("The run was triggered by SVB's March 8 announcement of securities sold at a loss and a capital raise that soon failed; SVB was closed on March 10.", True),
      ("By invoking the systemic risk exception to protect all depositors at SVB and Signature, policymakers removed moral hazard, since banks now know uninsured deposits are safe.", False),
      ("First Republic's fragility came from losses on mortgage loans, whereas SVB's insolvency came entirely from losses on its securities portfolio.", True)]
p1 = statements_mcq("1", "Consider the following statements from the required reading (Acharya, Cecchetti and Schoenholtz, 'Overview of recent banking stress').", st,
                    [("I, II, III and V only", None), ("I, II, III, IV and V", "moral_hazard_direction_reversed"),
                     ("I, III and V only", "size_of_unrealised_losses_misread"), ("II, III and V only", "uninsured_deposit_growth_misread")], "I, II, III and V only")
HARD.append(hq(
    id="30178-SVB-09", deck="SVB", topic="Reading: the trigger, system-wide fragility and the moral hazard trade-off",
    objective="Interest-rate risk in practice: the SVB case (required reading: system-wide vulnerability, trigger, resolution, moral hazard)",
    shape=CM, shape_class="concept MCQ", stem="SVB and Beyond, chapter 1: statements.", parts=[p1],
    scheme=["[1] Steps: (1) I true; (2) II true (less than $85bn peak in 2017–19, about eight times larger by 2022Q3); (3) III true (March 8 announcement; closed Friday March 10); (4) IV false: the reading says these emergency measures 'seem sure to encourage further risky behavior' — they create moral hazard, not remove it; (5) V true; (6) I, II, III and V.",
            "Second route: IV is the only statement whose conclusion runs against the reading's conclusion (the trade-off between crisis mitigation and crisis prevention).",
            "Where marks are lost: reading the blanket protection as solving moral hazard; confusing First Republic's (mortgages) and SVB's (securities) losses."],
    cites=[cite("READING", 7, "total uninsured deposits had surged from about $5.5 trillion at the end of 2019 to over $8 trillion by the first quarter of 2022"),
           cite("READING", 8, "By the third quarter of 2022, these losses were about eight times larger, approaching $700 billion."),
           cite("READING", 5, "The trigger for the run on SVB was the March 8 announcement in which the bank’s management reported the sale of securities at a loss"),
           cite("READING", 13, "these emergency measures seem sure to encourage further risky behavior by banks in the future"),
           cite("READING", 10, "SVB’s insolvency resulted entirely from losses on its securities portfolio. By contrast, First Republic’s fragility arose from losses on mortgage loans.")],
    location="Acharya, Cecchetti and Schoenholtz (2023), 'Overview of recent banking stress', SVB and Beyond, NYU Stern, pp. 5–13",
    file=F_STERN, groups=["R"], minutes=3.5,
    notches=["near_true_statements", "cross_section"],
    hc_parts=[{"n": "1", "steps": 6, "concepts": 3}],
    units=["READ-U3", "READ-U4", "READ-U5", "READ-U6"]))

# ================================================================================================
# DECK SECTIONS AND UNITS  (examinable units need at least one question; the rest say why not)
# ================================================================================================
def U(id, section, title, where, examinable=True, reason=None):
    u = {"id": id, "section": section, "title": title, "where": where, "examinable": examinable}
    if reason:
        u["reason"] = reason
    return u


SECTIONS = {
    "INTRO": [{"id": "I1", "title": "Bank business models: commercial, investment, universal"},
              {"id": "I2", "title": "Balance sheet, revenues, costs and the income statement"},
              {"id": "I3", "title": "Risks, fragility, transformation and why banks are regulated"}],
    "SVB": [{"id": "V1", "title": "What happened; AFS and HTM accounting"},
            {"id": "V2", "title": "Macro scenario, balance-sheet growth, deposit insurance, the carry trade"},
            {"id": "V3", "title": "Asset side: HTM and AFS portfolios, duration, hedging"},
            {"id": "V4", "title": "Liability side, the deposit drawdown and the role of tech and social media"},
            {"id": "V5", "title": "What was wrong, in the end"},
            {"id": "R", "title": "Required reading: Acharya et al. (2023), 'Overview of recent banking stress' (NYU Stern)"}],
}
UNITS = {
    "INTRO": [
        U("INTRO-U0", "I1", "Learning goals, agenda and glossary slides", "opening slides", False, "Course navigation only: no content beyond the units below."),
        U("INTRO-U1", "I1", "How we define a bank: commercial vs investment, wholesale vs retail, private and universal banking", "'How Do We Define a Bank?', 'Not All Banks Do the Same Things'"),
        U("INTRO-U2", "I1", "The traditional core of commercial banking; commercial banks by size (retail vs wholesale funding, listing)", "'The Traditional Core of Banking', 'What Do Banks Do? Commercial banks'"),
        U("INTRO-U3", "I1", "Investment banks: underwriting, advisory, asset management, risk-management products; large vs advisory-focused platforms", "'What Do Banks Do? Investment banks' (2 slides)"),
        U("INTRO-U4", "I1", "Universal banks: activities, revenue sources and risks", "'What Do Banks Do? Universal banks'"),
        U("INTRO-U5", "I2", "The simplified commercial-bank balance sheet", "'Commercial banks: Simplified Balance sheet (b/s)' (2 slides)"),
        U("INTRO-U6", "I2", "Revenues: net interest income and (net) non-interest income", "'How Banking Activities Generate Revenues' (2 slides)"),
        U("INTRO-U7", "I2", "Costs and the income statement: operating expenses, loan loss provisions, cost-to-income, profit", "'How Banking Activities Generate Revenues and Expenses'; example income statement"),
        U("INTRO-U8", "I1", "Comparing banks by business model: NII share and cost-to-income benchmarks", "'Compare the following banks…', 'Main Takeaways – Business Models'"),
        U("INTRO-U9", "I3", "Main risks (credit, liquidity, interest-rate, market, operational) and how banks manage them", "'Banking Activities Generate Risks'"),
        U("INTRO-U10", "I3", "Why banks are inherently fragile: leverage and maturity/liquidity mismatch", "'Why Are Banks Inherently Fragile?' (2 slides)"),
        U("INTRO-U11", "I3", "Maturity, liquidity and risk transformation: the rationale for the spread and the source of fragility", "'The concepts of maturity, liquidity and risk transformation'"),
        U("INTRO-U12", "I3", "Why banking is regulated and supervised", "'Why regulation and supervision are needed', 'Why banking is highly regulated'"),
        U("INTRO-U13", "I3", "Who sets the rules and who supervises banks", "'Who sets the rules—and who supervises banks?'", False,
          "The slide's content is an image with no text layer; nothing can be quoted without guessing. Covered in Part II C (Troiano) — check the PDF if you want a question on it now."),
    ],
    "IRR": [
        U("IRR-U0", "S1", "Agenda and learning goals", "slides 1–3", False, "Navigation only."),
        U("IRR-U1", "S1", "Why interest-rate risk matters: earning assets and paying liabilities dominate; NII is a major profit component; leverage", "slides 3–5"),
        U("IRR-U2", "S1", "Contractual versus repricing maturity; fixed versus variable rates by balance-sheet item", "slides 6–7"),
        U("IRR-U3", "S1", "Drivers of NII: asset/liability mix and balance-sheet size", "slides 8–11"),
        U("IRR-U4", "S1", "Monetary-policy transmission through bank rates (delays, pass-through)", "slides 12–13"),
        U("IRR-U5", "S2", "IRR definition; refinancing and reinvestment risk", "slides 14–19"),
        U("IRR-U6", "S2", "Two perspectives: NII (income) and EVE (economic value); models for each", "slides 19–20"),
        U("IRR-U7", "S2", "Asset–liability management and the ALCO", "slide 21"),
        U("IRR-U8", "S3", "The GAP: RSA and RSL; what makes an item rate-sensitive (maturity, repricing)", "slides 22–24, 29"),
        U("IRR-U9", "S3", "Sign and size of the GAP; ΔNII = GAP × Δi; asset- vs liability-sensitive", "slides 25–28, 31–34"),
        U("IRR-U10", "S3", "Steps of static GAP analysis", "slide 30"),
        U("IRR-U11", "S3", "In-class static GAP exercise: a zero GAP immunises NII", "slides 35–36"),
        U("IRR-U12", "S4", "Managing the GAP: immunisation versus active management; hedging", "slides 37–39"),
        U("IRR-U13", "S4", "Assumptions, strengths and weaknesses of static GAP; which model fixes each", "slides 40–41"),
        U("IRR-U14", "S5", "Maturity-bucket approach: periodic and cumulative GAP; infra-annual rate paths (Bank Alpha)", "slides 42–49"),
        U("IRR-U15", "S6", "Spread effect and deposit betas (Italy vs France)", "slides 50–52"),
        U("IRR-U16", "S6", "Beta (standardised) GAP: steps and Bank Alpha", "slides 53–56"),
        U("IRR-U17", "S6", "Level versus spread effect; NIM evidence for European banks", "slides 57–60"),
        U("IRR-U18", "S7", "Embedded options: prepayment, calls, early withdrawal; when they are exercised", "slides 61–63"),
        U("IRR-U18b", "S7", "Caps and floors on loan and deposit rates", "slide 64"),
        U("IRR-U19", "S7", "Option-adjusted GAP (Bank Alpha)", "slides 65–68"),
        U("IRR-U20", "S7", "Alternative GAP measures: GAP ratio, GAP/IEA, GAP/NW and ALCO limits", "slides 69–70"),
        U("IRR-U21", "S8", "Bond prices and rates; Macaulay and modified duration", "slides 71–75"),
        U("IRR-U22", "S8", "ΔEVE, the duration GAP formula and its steps", "slides 76–79"),
        U("IRR-U23", "S8", "Reading the duration GAP: sign, immunisation, link to SVB", "slides 80–83"),
    ],
    "SVB": [
        U("SVB-U0", "V1", "Points to address and list of readings", "opening slides", False, "Navigation only; the required reading has its own units (READ-U1…U6)."),
        U("SVB-U1", "V1", "What happened in March 2023 (size, clients, two-day collapse)", "'What happened in March 2023'"),
        U("SVB-U2", "V1", "AFS versus HTM securities; OCI", "'What are AFS and HTM securities?', timeline"),
        U("SVB-U3", "V2", "Macro scenario: ZLB, forward guidance and QE, then Fed tightening", "'Macro scenario' slides"),
        U("SVB-U4", "V2", "Balance-sheet growth financed by (uninsured) deposits; SVB tripled", "'Effects: Massive growth…' slides"),
        U("SVB-U5", "V2", "Deposit insurance: role, safety net, which deposits, stability", "'Why deposit insurance is important' (3 slides)"),
        U("SVB-U6", "V3", "HTM portfolio: share, duration, MBS, unrealised losses", "'Asset side – the HTM portfolio'"),
        U("SVB-U7", "V3", "AFS portfolio and the hedging strategy (swaps unwound)", "'Asset side – the AFS portfolio', 'The AFS portfolio hedging strategy'"),
        U("SVB-U8", "V4", "Liability side: uninsured share, concentration, deposit mix changes", "'Liability side: The Achilles’ heel'"),
        U("SVB-U9", "V2", "Macro causes: carry trade, uninsured deposit growth, reluctance to hedge", "'INVESTIGATING THE CAUSES', 'Phase 1'"),
        U("SVB-U10", "V4", "Phase 2: deposit drawdown; unrealised losses and capital; forced sales", "'Phase 2: Deposits drawdown', 'How unrealized losses affect bank capital'"),
        U("SVB-U11", "V4", "What was different: speed, social media, connected depositors", "'What was different this time?' slides"),
        U("SVB-U12", "V5", "What was wrong in the end: asset risk plus volatile funding; ALM failure; 'Ipse dixit'", "'What was wrong, in the end?' (2 slides)"),
        U("READ-U1", "R", "SVB's liability frailties: uninsured share, concentration, time deposits, deposit surge", "reading pp. 2–3"),
        U("READ-U2", "R", "SVB's asset side and accounting: securities share, duration, hedges, HTM 43%, AOCI opt-out", "reading pp. 3–5"),
        U("READ-U3", "R", "The trigger (March 8), closure, the systemic risk exception and First Republic", "reading pp. 5–7"),
        U("READ-U4", "R", "System-wide fragility: uninsured deposit surge and unrealised losses", "reading pp. 7–9"),
        U("READ-U5", "R", "Spotting the weak banks: adjusted capital ratios and SRISK", "reading pp. 9–12"),
        U("READ-U6", "R", "Conclusion: why supervisors missed it; moral hazard versus crisis mitigation", "reading pp. 12–13"),
    ],
}

# Existing questions (already in the artifact database): their sections are their slide_groups; units below.
EXISTING_UNITS = {
    "30178-IRR-01": ["IRR-U22"], "30178-IRR-02": ["IRR-U16"], "30178-IRR-03": ["IRR-U22", "IRR-U23"],
    "30178-IRR-04": ["IRR-U8", "IRR-U14"], "30178-IRR-05": ["IRR-U9"], "30178-IRR-06": ["IRR-U8", "IRR-U2"],
    "30178-IRR-07": ["IRR-U12"], "30178-IRR-08": ["IRR-U22", "IRR-U6"], "30178-IRR-09": ["IRR-U6"],
    "30178-IRR-10": ["IRR-U23", "IRR-U9", "IRR-U20"], "30178-IRR-11": ["IRR-U16"], "30178-IRR-12": ["IRR-U9"],
    "30178-IRR-13": ["IRR-U11", "IRR-U10"], "30178-IRR-14": ["IRR-U14"], "30178-IRR-15": ["IRR-U14"],
    "30178-IRR-16": ["IRR-U16"], "30178-IRR-17": ["IRR-U18", "IRR-U19"], "30178-IRR-18": ["IRR-U20"],
    "30178-IRR-19": ["IRR-U22"], "30178-IRR-20": ["IRR-U5"], "30178-IRR-21": ["IRR-U5"],
    "30178-IRR-22": ["IRR-U5", "IRR-U6", "IRR-U21"], "30178-IRR-23": ["IRR-U5"], "30178-IRR-24": ["IRR-U3"],
    "30178-IRR-26": ["IRR-U13"], "30178-IRR-27": ["IRR-U15", "IRR-U17"], "30178-IRR-28": ["IRR-U11", "IRR-U23"],
    "30178-IRR-30": ["IRR-U22", "IRR-U21"], "30178-IRR-31": ["IRR-U13", "IRR-U23"], "30178-IRR-32": ["IRR-U19", "IRR-U20"],
    "30178-INTRO-01": ["INTRO-U10", "INTRO-U5"], "30178-INTRO-02": ["INTRO-U6", "INTRO-U7"],
    "30178-SVB-01": ["SVB-U2", "SVB-U6", "SVB-U10"], "30178-SVB-02": ["SVB-U6", "IRR-U22", "SVB-U12"],
}
EXISTING_GROUPS = {"30178-INTRO-01": ["I3", "I2"], "30178-INTRO-02": ["I2"], "30178-SVB-01": ["V1", "V3", "V4"], "30178-SVB-02": ["V3", "V5"]}

# ================================================================================================
# SOURCE LEDGER: every file, every item, one decision
# ================================================================================================
def D(file, item, decision, ids=None, reason=""):
    return {"file": file, "item": item, "decision": decision, "ids": ids or [], "reason": reason}


HELD_CAP = "Bank capital / Basel III: 'The role of bank capital and capital management' is on the Part I syllabus but its deck is not in the folder yet. Held until the deck arrives."
HELD_LIQ = "Liquidity risk management is Part II (Pambianco); not in the midterm-1 decks. Held for Part II."
HELD_FX = "FX, country, off-balance-sheet and operational risk have no deck in the folder; the INTRO deck only lists the main risks. Held until a deck covers them."
LEDGER = [
    D(F_P1, "A. Maturity-bucket solution (Jan 2023 data)", "key_source", ["30178-IRR-14"], "Official solution to the slide exercise; used as the official method for IRR-14 part 2. Its data differ slightly from the 2026-27 slide, so IRR-14 keeps the slide's data."),
    D(F_P1, "A. Standardized (Beta) GAP solution", "included_adapted", ["30178-IRR-35"], "Only the solution is printed (no question wording) and the text layer merges the columns; table rebuilt to match the printed totals. Flagged for a check."),
    D(F_P1, "B. MCQ 1–6", "included", ["30178-IRR-04", "30178-IRR-05", "30178-IRR-06", "30178-IRR-07", "30178-IRR-08", "30178-IRR-09"]),
    D(F_P1, "B. True/False (4 items)", "included", ["30178-IRR-10"]),
    D(F_P1, "C. Exercise A (Alpha Bank 2005)", "included", ["30178-IRR-11"]),
    D(F_P1, "C. Exercise B (6-month GAP, NII)", "included", ["30178-IRR-12"], "Now checked word for word against the PDF text layer (it was previously transcribed from the page image)."),
    D(F_P1, "C. Exercise C (duration GAP, ΔEVE)", "included", ["30178-IRR-01"]),
    D(F_P1, "D. SVB MCQ", "included", ["30178-SVB-03"]),
    D(F_P1, "D. SVB True/False (2 items)", "included", ["30178-SVB-04"]),
    D(F_P1, "E. Securitisation MCQ and 2 True/False", "held", [], "Securitisation is on the Part I syllabus but its deck is not in the folder yet. Held until the deck arrives."),
    D("Reference Material/Clean/exam structure guide.pdf", "Sample MCQ 1–3 and Exercise A", "duplicate", ["30178-IRR-04", "30178-IRR-05", "30178-IRR-06", "30178-IRR-01"], "Word for word the same as P1 1st part B.1–3 and C. Exercise C; kept once."),
    D("Reference Material/Clean/exam structure guide.pdf", "Exam rules and scoring", "used", [], "Sets the format (16 MCQs + 2 exercises × 2 MCQ parts, +0.8/−0.1) already in the course fingerprint."),
    D("Reference Material/Clean/Additional Q.pdf", "Extra exercises 1–4 (IRR)", "included", ["30178-IRR-20", "30178-IRR-21", "30178-IRR-22", "30178-IRR-23"]),
    D("Reference Material/Clean/Additional Q.pdf", "Extra exercise 5 (FX risk, London assets)", "held", [], HELD_FX),
    D("Reference Material/Clean/Additional Q.pdf", "Extra exercises 6–7 (stored/purchased liquidity, deposit drain)", "held", [], HELD_LIQ),
    D("Reference Material/Clean/Additional Q.pdf", "Extra exercise 8 (bank run equilibrium)", "held", [], "Bank runs / Diamond–Dybvig are not in the midterm-1 decks (the SVB case discusses runs only qualitatively). Held for the liquidity deck."),
    D("Reference Material/Clean/Additional Q.pdf", "Extra exercises on capital regulation 1–4", "held", [], HELD_CAP),
    D("Reference Material/P111.pdf", "Whole file", "duplicate", [], "Same document as Additional Q.pdf."),
    D("Reference Material/international-banking-additional-exercises-and-solutions.pdf", "Whole file", "duplicate", [], "Same document as Additional Q.pdf."),
    D(F_PS1, "Exercise 1 (Megalopolis: ROE, ROA, NIM, loan loss reserves, liquidity ratios)", "held", [], "Performance ratios (ROE, ROA, NIM, reserve and liquidity ratios) are Part II 'Measuring bank performance'; the INTRO deck only covers cost-to-income. Held for Part II."),
    D(F_PS1, "Exercise 2 (firm commitment)", "included", ["30178-INTRO-03"]),
    D(F_PS1, "Exercise 3 (best efforts)", "included", ["30178-INTRO-04"]),
    D(F_PS1, "Exercise 4 (net income)", "included", ["30178-INTRO-05"]),
    D(F_PS1, "Exercise 5 (deposit drain: shrink loans or borrow)", "held", [], HELD_LIQ + " Same exercise as Additional Q extra exercise 7."),
    D(F_PS1, "Exercise 6 (3-year bond, CD, NII)", "included", ["30178-IRR-33"]),
    D(F_PS1, "MCQ 1 (off-balance-sheet activities)", "held", [], HELD_FX),
    D(F_PS1, "MCQ 2 (underwriting)", "included", ["30178-INTRO-06"], "No key in the source; solved twice."),
    D(F_PS1, "MCQ 3 (asset side)", "included", ["30178-INTRO-07"], "No key in the source; solved twice."),
    D(F_PS1, "MCQ 4 (commercial bank functions)", "included", ["30178-INTRO-08"], "No key in the source; solved twice."),
    D(F_PS1, "MCQ 5 (market risk)", "included", ["30178-INTRO-09"], "No key in the source; solved twice."),
    D(F_PS1, "MCQ 6 (characterise risk exposures)", "held", [], HELD_FX),
    D(F_PS1, "True/false 1 and 3", "included", ["30178-IRR-34"]),
    D(F_PS1, "True/false 2 (loan commitment fee)", "held", [], HELD_FX),
    D(F_PS1, "True/false 4–5 (FX positions)", "held", [], HELD_FX),
    D(F_PS1, "True/false 6–7 (operational risk)", "held", [], HELD_FX),
    D(F_PS1S, "Whole file", "key_source", ["30178-INTRO-03", "30178-INTRO-04", "30178-INTRO-05", "30178-IRR-33", "30178-IRR-34"], "Problem Set 1 with solutions: the official keys."),
    D("Reference Material/PS1 financial analysis.pdf", "Whole file", "duplicate", [], "Same text as Problem Set 1.pdf (no solutions)."),
    D("Reference Material/Clean/PS2.pdf", "Exercises 1–4 and MCQ 1–4 (liquidity, bank runs, contagion)", "held", [], HELD_LIQ),
    D("Reference Material/Clean/More P1_.pdf", "Whole file", "duplicate", [], "Problem set 2 with solutions (same as PS2); held with it."),
    D("Reference Material/problem-set-2-…-solutions.pdf", "Whole file", "duplicate", [], "Same as PS2."),
    D("Reference Material/Clean/PS3.pdf", "Exercises 1–4 and MCQ 1–6 (Basel III)", "held", [], HELD_CAP),
    D("Reference Material/Clean/PS4.pdf", "Extended solutions to the Basel III set", "held", [], HELD_CAP),
    D("Reference Material/…problem-set-4-solutions-and-ratios.pdf", "Whole file", "duplicate", [], "Same as PS4."),
    D("Reference Material/Clean/final exam review notes.pdf", "MCQ 1–5, T/F 1–5, Exercises 1–2 (Basel, resolution, deposit insurance, lender of last resort)", "held", [], "Final review from an earlier syllabus (E. Carletti): capital regulation and resolution. " + HELD_CAP),
    D(F_PAMB, "[1] Loan loss provisions", "included", ["30178-INTRO-12"], "Part II sample, but the INTRO deck covers the point."),
    D(F_PAMB, "[2] Total assets as scale variable; [A.1]–[A.2] NPE ratio and coverage", "held", [], "Part II (Pambianco): financial-statement analysis and asset quality. Held for Part II."),
    D("Reference Material/Clean/Partial 2 Qs but not like exam.pdf", "Liquidity and bank valuation questions 1–11", "excluded", [], "Your note says 'not like exam'; open definitional Q&A on Part II topics. Not exam-shaped; excluded."),
    D("Reference Material/Clean/final exam review notes.pdf", "Answer grid template", "not_a_question", [], ""),
    D("Mock Exams/Mock Partial 1 - Interest Rate Risk (PAPER, MARK SCHEME)", "Whole file", "excluded", [], "Written by Claude in an earlier chat: not evidence of what is examined."),
    D("Mock Exams/Mock Partial - SVB case (PAPER, MARK SCHEME, question bank)", "Whole file", "excluded", [], "Written by Claude in an earlier chat: not evidence of what is examined."),
    D("Mock Exams/International Banking L2 Mock.pdf", "Whole file", "excluded", [], "Written by Claude in an earlier chat: not evidence of what is examined."),
    D(F_INTRO, "Deck", "units", [], "14 units; 12 examinable."),
    D(F_IRR, "Deck (in-class exercises included as IRR-13…19)", "units", [], "25 units; 24 examinable."),
    D(F_SVB, "Deck", "units", [], "13 units; 12 examinable (plus the reading's 6)."),
    D(F_STERN, "Required reading, chapter 1", "units", [], "6 units, all examinable ('required for the exam')."),
    D("Slides/Course Introduction_30178_2026-27.pdf", "Deck", "not_examinable", [], "Syllabus, exam rules and dates only. Used for the exam date (28 Oct 2026) and scope (midterm 1 = Part I)."),
]


# ================================================================================================
# Seed questions (the original Answer Grid bank, data/seed.js) brought under the harder rule on 2026-09-24.
# Nine generated IRR questions pre-dated the rule: six were labelled exam+1 and none recorded a hard_check.
# Seven meet the 30178 thresholds on an honest step count and get their review recorded; IRR-24 (a two-step
# mix/size shortcut) and IRR-26 (two one-step true/false items) did not, so they are rewritten harder, same ids.
# ================================================================================================
SEED_HARD_CHECKS = {
    "30178-IRR-02": ("exercise part", [{"n": "1.1", "steps": 4, "concepts": 2}, {"n": "1.2", "steps": 5, "concepts": 2}], ["extra_classification", "cross_section", "chain"]),
    "30178-IRR-03": ("exercise part", [{"n": "2.1", "steps": 4, "concepts": 2}, {"n": "2.2", "steps": 4, "concepts": 2}], ["working_backwards", "extraneous_data", "what_if_followon"]),
    "30178-IRR-27": ("concept MCQ", [{"n": "1.1", "steps": 5, "concepts": 2}, {"n": "1.2", "steps": 4, "concepts": 2}], ["extra_step", "cross_section"]),
    "30178-IRR-28": ("concept MCQ", [{"n": "1", "steps": 3, "concepts": 2}], ["near_true_statements", "cross_section"]),
    "30178-IRR-30": ("exercise part", [{"n": "2.1", "steps": 6, "concepts": 3}, {"n": "2.2", "steps": 4, "concepts": 2}], ["working_backwards", "what_if_followon", "extra_step"]),
    "30178-IRR-31": ("concept MCQ", [{"n": "1", "steps": 5, "concepts": 4}], ["near_true_statements", "cross_section"]),
    "30178-IRR-32": ("exercise part", [{"n": "3.1", "steps": 7, "concepts": 2}, {"n": "3.2", "steps": 4, "concepts": 2}], ["chain", "working_backwards", "extra_classification"]),
}
SEED_REVIEW_NOTE = ("Step counts recorded on 2026-09-24 when the seed bank was checked against the harder rule: "
                    "{}.")
SEED_STEP_NOTES = {
    "30178-IRR-02": "1.1 classify earning/bearing items, Σ amount×beta for assets, for liabilities, subtract; 1.2 static RSA, RSL, GAP, both ΔNII, difference",
    "30178-IRR-03": "2.1 DA, DL, L/A, DGAP; 2.2 immunisation ⇔ DGAP = 0, hold L/A and DL, DA* = (L/A)·DL, evaluate",
    "30178-IRR-27": "1.1 income change, two funding lines at their betas, total expense, ΔNII; 1.2 GAP = 0, level effect 0, spread effect = ΔNII, reason",
    "30178-IRR-28": "zero GAP protects NII over the period; positive DGAP lowers EVE when rates rise; reject the distractors that merge the two perspectives",
    "30178-IRR-30": "2.1 DA, DL, ΔMVA and ΔMVL each with its own modified duration and Δi, ΔEVE; 2.2 set ΔMVL = ΔMVA, solve for Δi_L",
    "30178-IRR-31": "four statements, each tested against its model assumption, then the combination",
    "30178-IRR-32": "3.1 static RSA, RSL, three option adjustments, GAP, ÷ net worth; 3.2 limit in €, GAP as a function of p, solve",
}

# ---- IRR-24 rewritten: a mix change at a lower marginal loan rate plus a size change funded at a higher marginal rate ----
L0, LQ0, D0, E0, FA = 120.0, 40.0, 150.0, 20.0, 10.0
rl, rq, rd, rl_new, rd_new = 0.045, 0.012, 0.016, 0.039, 0.020
nii0 = L0 * rl + LQ0 * rq - D0 * rd
nii1 = L0 * rl + 25 * rl_new + (LQ0 - 15) * rq - D0 * rd - 10 * rd_new
d_nii = nii1 - nii0
near(nii0, 3.48); near(nii1, 4.075); near(d_nii, 0.595)
near(d_nii, 15 * (rl_new - rq) + 10 * (rl_new - rd_new))            # route 2: mix effect + size effect
assert abs((L0 + 25 + LQ0 - 15 + FA) - (D0 + 10 + E0)) < 1e-9          # the balance sheet still balances (180)
ea1 = L0 + 25 + LQ0 - 15
nim1 = nii1 / ea1
nii2 = nii1 * 1.08
near(ea1, 170); near(nii2 / (ea1 * 1.08), nim1)                      # route 2: NIM unchanged by a pure size change
o11 = [(f"{f(d_nii, 3)}", None), (f"{f(15 * (rl - rq), 3)}", "old_loan_rate_and_new_deposits_ignored"),
       (f"{f(25 * rl - 15 * rq - 10 * rd_new, 3)}", "new_loans_at_the_old_rate"), (f"{f(25 * rl_new - 15 * rq, 3)}", "new_deposit_cost_ignored")]
assert all(len(o[0].split(".")[1]) == 3 for o in o11)            # exact to 3 decimals: no rounding ambiguity (0.595, 0.495, 0.745, 0.795)
p11 = mcq("1.1", "What is the change in Bank Kappa's annual net interest income, in € million?", o11, o11[0][0], 0.8)
o12 = [(f"NIM {f(nim1 * 100, 2)}%; after growth NII {f(nii2, 2)} and NIM {f(nim1 * 100, 2)}%", None),
       (f"NIM {f(nii1 / 180 * 100, 2)}%; after growth NII {f(nii2, 2)} and NIM {f(nii1 / 180 * 100, 2)}%", "nim_over_total_assets"),
       (f"NIM {f(nim1 * 100, 2)}%; after growth NII {f(nii2, 2)} and NIM {f(nim1 * 108, 2)}%", "size_effect_read_as_margin_effect"),
       (f"NIM {f(nim1 * 100, 2)}%; after growth NII {f(nii0 * 1.08, 2)} and NIM {f(nim1 * 100, 2)}%", "growth_applied_before_the_changes")]
p12 = mcq("1.2", "After the changes in 1.1, what is Bank Kappa's net interest margin (NII / total earning assets)? If every item on its balance sheet then grows by 8%, "
                 "with rates and composition unchanged, what are its NII (€ million) and NIM?", o12, o12[0][0], 0.8)
IRR24 = question(
    id="30178-IRR-24", course="30178", deck="IRR", topic="Mix and size effects at marginal rates, and the net interest margin",
    objective="Interest-rate risk: measurement and management using maturity-gap and duration-gap models",
    shape="numerical exercise with 2 MCQ sub-questions", shape_class="exercise part",
    stem="Bank Kappa's balance sheet is shown below (€ million, annual rates). During the year it moves €15 million from liquid assets into new loans, and it also grants "
         "€10 million of further new loans funded by €10 million of new deposits. New loans can only be placed at 3.9% and new deposits cost 2.0%; existing loans, "
         "liquid assets and deposits keep their rates. Rates then stay unchanged.",
    data="| **Assets** | € million | Rate |\n|---|---|---|\n| Loans | 120 | 4.5% |\n| Liquid assets | 40 | 1.2% |\n| Fixed assets | 10 | — |\n"
         "| **Liabilities and equity** |  |  |\n| Deposits | 150 | 1.6% |\n| Equity | 20 | — |",
    parts=[p11, p12],
    scheme=[f"[1.1] Steps: (1) NII before = 120×4.5% + 40×1.2% − 150×1.6% = {f(nii0, 3)}; (2) new loans 25 × 3.9% = 0.975 while liquid income falls to 25 × 1.2% = 0.30; "
            f"(3) extra deposit cost 10 × 2.0% = 0.20; (4) NII after = {f(nii1, 3)}; ΔNII = +{f(d_nii, 3)}.",
            f"Second route for 1.1: mix effect 15 × (3.9% − 1.2%) = 0.405 plus size effect 10 × (3.9% − 2.0%) = 0.19 → +{f(d_nii, 3)} (asserted).",
            f"[1.2] Steps: (1) earning assets = loans 145 + liquid 25 = 170 (fixed assets earn nothing); (2) NIM = {f(nii1, 3)}/170 = {f(nim1 * 100, 2)}%; "
            f"(3) a pure size change scales NII: {f(nii1, 3)} × 1.08 = {f(nii2, 3)}; (4) earning assets also grow 8%, so NIM is unchanged; (5) the slides' size example: NII rises, the margin does not.",
            "Where marks are lost: pricing the new loans at the old 4.5%, forgetting the cost of the new deposits, dividing NII by total assets (180) instead of earning assets, "
            "treating the size effect as a wider margin, growing the NII from before the changes.",
            "Harder than the slides' examples: the slide moves €10 at the existing loan rate; here the marginal rates differ from the average ones and a size change is mixed in."],
    cites=[cite("IRR", 9, "the bank shifts €10 from liquid assets to loans"),
           cite("IRR", 11, "loans and deposits both increase by 10%, while rates and composition remain unchanged"),
           cite("IRR", 23, "Net Interest Margin (NII / Total Earning Assets)")],
    groups=["S1", "S6"], location="slides 8-11, 23 (rewritten 2026-09-24 to meet the harder rule)", file="Slides/Managing Interest Rate Risk_2026-27_PART I and 2_classroom.pdf",
    minutes=6, notches=["extra_step", "chain", "extra_classification"],
    hc_parts=[{"n": "1.1", "steps": 4, "concepts": 2}, {"n": "1.2", "steps": 5, "concepts": 2}])
IRR24["created_at"] = "2026-09-24T13:00:00Z"
IRR24["units"] = ["IRR-U3", "IRR-U8"]

# ---- IRR-26 rewritten: static GAP assumptions matched to the model that relaxes each ------------------------------
st26 = [("Borrowers who prepay fixed-rate mortgages when rates fall change the bank's repricing within the year; option-adjusted analysis addresses this.", True),
        ("The maturity bucket approach addresses rate-sensitive assets and liabilities repricing by different amounts.", False),
        ("Static GAP captures refinancing and reinvestment risk but not the change in the market values of assets and liabilities; the duration GAP (EVE) addresses the latter.", True),
        ("If rates change twice within the one-year gapping period, ΔNII = GAP × Δi still holds exactly for the cumulative change, because the GAP is measured over the whole year.", False),
        ("Static GAP analysis works well for small changes in interest rates.", True)]
roman = ["I", "II", "III", "IV", "V"]
assert [roman[i] for i, (_, t) in enumerate(st26) if t] == ["I", "III", "V"]
body26 = ("Consider the following statements about the static repricing GAP model.\n\n" + "\n".join(f"{roman[i]}. {s}" for i, (s, _) in enumerate(st26))
          + "\n\nWhich of the statements are correct?")
o26 = [("I, III and V only", None), ("I, II, III and V only", "bucket_vs_beta_model_swap"), ("I, III, IV and V only", "multiple_rate_moves_ignored"),
       ("III and V only", "embedded_options_left_to_static_gap")]
p26 = mcq("1", body26, o26, "I, III and V only", 0.8)
IRR26 = question(
    id="30178-IRR-26", course="30178", deck="IRR", topic="Static GAP: what each weakness is fixed by",
    objective="Interest-rate risk: measurement and management using maturity-gap and duration-gap models",
    shape="statement-combination MCQ", shape_class="concept MCQ", stem="Static GAP: statements.", parts=[p26],
    scheme=["[1] Steps: (1) I true: embedded options (prepayment) → option-adjusted analysis (slide 41); (2) II false: different repricing speeds/amounts → beta (standardised) GAP; "
            "the maturity bucket approach handles several rate moves; (3) III true: static GAP focuses on profitability; the price effect needs duration GAP (EVE); "
            "(4) IV false: the model assumes one rate change; several moves inside the period can change NII even with the same cumulative GAP; (5) V true: a listed strength; (6) I, III and V.",
            "Second route: read each statement against the slide-41 table (assumption → what it ignores → model that addresses it); II and IV each attach a weakness to the wrong fix or deny it.",
            "Harder than the former true/false pair: five statements, two near-true, and the answer is a combination."],
    cites=[cite("IRR", 41, "Model that addresses it"), cite("IRR", 41, "Option-adjusted analysis"),
           cite("IRR", 40, "Only one change in interest rates over the gapping period")],
    groups=["S4"], location="slides 40-41 (rewritten 2026-09-24 to meet the harder rule)", file="Slides/Managing Interest Rate Risk_2026-27_PART I and 2_classroom.pdf",
    minutes=3, notches=["near_true_statements", "extra_classification"], hc_parts=[{"n": "1", "steps": 6, "concepts": 4}])
IRR26["created_at"] = "2026-09-24T13:00:00Z"
IRR26["units"] = ["IRR-U13"]
SEED_REWRITES = {"30178-IRR-24": IRR24, "30178-IRR-26": IRR26}
