"""30257 Corporate Valuation: source intake, deck units and the questions that fill the gaps.

Same rules as c30178.py (real first, word for word, official keys where printed; generated Hard questions only for
gaps; every source item in the ledger). Workbook chapters 1-4 wait for readable page images (Will is splitting the
PDF); only the six workbook problems printed as text on the L6 slides are taken in now.
"""
from build_banks import mcq, written, question, cite, f, r, near, CREATED, L

C = "30257"
F_L12 = "Slides/Corporate Valuation - AY 26-27 - Lectures 1-2 - Introduction - v3.pdf"
F_L3 = "Slides/Corporate Valuation - AY 26-27 - Lecture 3 - DCF Valuation - v6.pdf"
F_L4 = "Slides/Corporate Valuation - C31 - Lecture 4 - Cost of Capital - v3.pdf"
F_L5 = "Slides/Corporate Valuation - C31 - Lecture 5 - Reorganizing and CFs - v13.pdf"
F_L6 = "Slides/Corporate Valuation - C31 - Lecture 6 - DCF Exercises - v1.pdf"
F_M26 = "Reference/Past Exams and Mock Exams/30257 Corporate Valuation - AY 26-27 - Mock Exam - v1.pdf"
F_M24X = "Reference/Past Exams and Mock Exams/30257 Corporate Valuation AY 24-25 - Mock Exam Solutions v1.xlsx"
F_V2 = "Reference/Clean/valuation-mock-exam-v2-final-exam.pdf"
F_V2X = "Reference/Valuation - Mock Exam Solutions v1.xlsx"
F_J19 = "Reference/Clean/prova-desame-30257-corporate-valuation-gennaio-2019-domande-e-risposte.pdf"
F_J23 = "Reference/Clean/past paper.pdf"
F_OLD1 = "Reference/Clean/Old Exam 1.pdf"
F_BSC = "Reference/Clean/BSc.pdf"
NEG = {"correct": 1, "wrong": 0, "blank": 0}
M26_LOC = "AY 26-27 instructor mock exam (file labelled 'Academic Year 2025/2026 Mock Exam'), {}; official key from the AY 24-25 mock's solutions workbook (same question), " + F_M24X
TEXTCHK = "text checked word for word against the PDF text layer on 2026-09-24"
PHOTO = "transcribed from the screen photographs and checked against them on 2026-09-24"


def s_mcq(n, prompt, options, letter, status="official", marks=1):
    assert letter in L[:len(options)]
    return ({"n": n, "prompt": prompt, "options": options, "marks": marks}, {"n": n, "answer": letter, "answer_status": status}, [])


def s_written(n, prompt, answer, marks="UNKNOWN", status="official"):
    return ({"n": n, "prompt": prompt, "options": [], "marks": marks}, {"n": n, "answer": answer, "answer_status": status}, [])


def realq(**kw):
    parts = kw.pop("parts")
    marks = [p[0]["marks"] for p in parts]
    q = {"id": kw["id"], "course": C, "deck": kw["deck"], "topic": kw["topic"], "syllabus_objective": kw["objective"],
         "shape": kw["shape"], "stem": kw["stem"], "data": kw.get("data"), "difficulty": "exam",
         "source": {"type": kw.get("type", "real"), "file": kw["file"], "location": kw["location"], "label": "SUPPORTING",
                    "verbatim_verified": kw.get("verbatim", True), "transcribed_from_image": kw.get("image", False), "page_snapshot_asset": None},
         "subquestions": [p[0] for p in parts], "answer_key": [p[1] for p in parts], "error_tags": [],
         "marks": round(sum(marks), 2) if all(isinstance(m, (int, float)) for m in marks) else "UNKNOWN",
         "mark_scheme": kw["scheme"], "citations": kw["cites"], "slides": kw.get("slides", []), "slide_groups": kw["groups"],
         "units": kw["units"], "est_minutes": kw["minutes"], "created_at": CREATED, "negative_marking": NEG}
    if kw.get("check"):
        q["source"]["check"] = kw["check"]
    if q["data"] is None:
        del q["data"]
    return q


REAL, HARD = [], []
MCQ, ESSAY, PROB, SHORT = "concept MCQ", "short essay (written)", "short problem (written)", "short answer (MCQ in the exam; options not captured)"

# ================================================================================================
# REAL: AY 26-27 instructor mock (keys: AY 24-25 solutions workbook, marked with an x)
# ================================================================================================
def m26(id, n, deck, topic, obj, prompt, options, letter, groups, units, cites, scheme, minutes=1.5):
    REAL.append(realq(id=id, deck=deck, topic=topic, objective=obj, shape=MCQ, file=F_M26, location=M26_LOC.format(f"Part I, MCQ {n}") + "; " + TEXTCHK,
                      stem=prompt, parts=[s_mcq("1", prompt, options, letter)], scheme=scheme, cites=cites, groups=groups, units=units, minutes=minutes))


m26("30257-L5-10", 1, "L5", "What raises FCFO", "Cash flows for valuation: what enters FCFO",
    "Free cash flows from operations (FCFO), other things being equal, increase if:",
    ["Shareholders underwrite a capital increase", "Dividends decrease", "Accounts receivables decrease", "Trade liabilities decrease"], "C",
    ["L5C"], ["L5-U4"], [cite("L5", 24, "FCFO = NOPAT - increase in core capital employed during the year")],
    ["Official answer: C (x in the AY 24-25 solutions workbook).", "A fall in receivables lowers noncash working capital, releasing cash; A and B are equity flows below FCFO; D ties up cash."])
m26("30257-L5-11", 2, "L5", "What is not an investment in FCFO", "Cash flows for valuation: investments subtracted from gross cash flows",
    "In calculating free cash flows, which of the following is/are not NOT an investment that should be subtracted from gross cash flows?",
    ["Change in operating working capital", "Change in debt outstanding", "Net capital expenditures", "Investment in goodwill and acquired intangibles"], "B",
    ["L5C"], ["L5-U4"], [cite("L5", 22, "- ↑ or + ↓ in noncash WC")],
    ["Official answer: B. The question's 'not NOT' is in the source; it asks which item is not an investment: debt is a financing flow (it enters FCFE, not FCFO).",
     "Solutions workbook note: 'CAPEX = CAPITAL EXPENDITURES IS NET OF D&A'."])
m26("30257-L5-12", 3, "L5", "Depreciation and FCFO", "Cash flows for valuation: D&A, taxes and FCFO",
    "A company records a free cash flows from operations (FCFO) equal to 100 and depreciation expenses equal to 20 in 2016. If the depreciation expense were equal to 30, FCFO would be:",
    ["Unchanged, since depreciation expenses are a non-monetary cost", "Higher by 10, therefore equal to 110", "Lower by 10, therefore equal to 90", "The question cannot be answered with the given inputs only"], "D",
    ["L5C"], ["L5-U4"], [cite("L5", 22, "- Operational taxes")],
    ["Official answer: D.", "Higher depreciation lowers operating taxes by 10 × t, so FCFO rises by the tax saving; without the tax rate the change cannot be computed. A ignores the tax effect."])
m26("30257-L4-10", 4, "L4", "What weights the MRP", "Cost of equity: the CAPM",
    "In determining the levered cost of equity of a company, the market risk premium is weighted by its:",
    ["Variance", "Standard deviation", "Beta", "Alpha"], "C", ["L4A"], ["L4-U2"], [cite("L4", 7, "The expected return (cost) of equity capital is generally estimated using the capital asset pricing model")],
    ["Official answer: C: kEL = rF + β × (rM − rF)."], 1)
m26("30257-L4-11", 5, "L4", "Pre-tax cost of debt from a rating", "Cost of debt: rating-based model",
    "Island Inc is a publicly traded company that has 120 in bank loans on its books, with a stated interest rate of 3% and 165 in publicly traded bonds,, which were issues under par, with a coupon rate of 3,9%. The company currently has a bond rating of BBB, with a default spread of 1,75% over the risk free rate. If the current T-Bill rate is 1%, the ten-year T-Bond rates 4,5% and the marginal tax rate is 40%, what is the pre-tax cost of debt?",
    ["3,52%", "6,25%", "2,75%", "8,02%"], "B", ["L4C"], ["L4-U11"], [cite("L4", 36, "The spread associated to a rating")],
    ["Official answer: B. Solution (mock): kD = 4,5% + 1,75% = 6,25%.", "Use the long-term (10-year) risk-free rate plus the rating spread; the book coupons and the T-Bill rate are distractors; 'pre-tax' means no (1 − t)."], 2)
m26("30257-L12-10", 6, "L12", "Fundamental approaches to valuation", "General approaches and specific methods",
    "Which of the following is not one of the fundamental approaches of firm valuation?",
    ["An approach based on the present value of future cash flows or earnings", "An approach based on current market share with respect to other competing businesses",
     "An approach based on the relative value of other businesses with respect to a driver", "An approach based on current value of assets, net of the current value of outstanding liabilities"], "B",
    ["L12B"], ["L12-U4"], [cite("L12", 16, "Income approach Market approach Cost approach")],
    ["Official answer: B. A, C and D are the income, market and cost approaches."], 1)
m26("30257-L3-10", 7, "L3", "Discount rate for an equity-side DCF", "The three DCF models and their discount rates",
    "With an equity side discounted cash flows model, cash flows to shareholders should be discounted using:",
    ["the cost of debt", "the weighted average cost of capital", "the unlevered cost of equity", "the levered cost of equity"], "D",
    ["L3A"], ["L3-U4"], [cite("L3", 12, "We can compute equity value also considering the cash flows to shareholders directly, as a perpetuity")],
    ["Official answer: D."], 1)
m26("30257-L3-11", 8, "L3", "EV at a year-end valuation date", "Two-stage DCF and the valuation date",
    "A company generates FCFO of 100 in 2016, 110 in 2017 and 121 in 2018. WACC is 10% and perpetual growth is 0%. How much is enterprise value on 31/12/2016?",
    ["1.510,0", "1.410,0", "1.200,0", "1.300,0"], "C", ["L3B", "L6"], ["L3-U6", "L6-U4.1"], [cite("L6", 6, "What is the enterprise value as of 31/12/2016?")],
    ["Official answer: C. Solution (mock): PV of FCFO = 110/1,1 + 121/1,1^2 = 200; TV = 121/0,1 = 1210; PV of TV = 1210/1,1^2 = 1000; EV = 200 + 1000 = 1200.",
     "The 2016 FCFO has already happened at 31/12/2016, so it is not discounted. Same problem as Workbook 4.1 (L6), in € thousand there."], 2.5)

REAL.append(realq(
    id="30257-L3-12", deck="L3", topic="Tax shields in APV and asset-side DCF", objective="Where tax benefits enter the DCF models", shape=ESSAY,
    file=F_M26, location=M26_LOC.format("Part II, open question 1") + "; " + TEXTCHK,
    stem="Consider an asset-side discounted cash flows model and an adjusted present value model. Please discuss if and how they incorporate the value generated from the possibility to deduct interest payments from income taxes",
    parts=[s_written("1", "Discuss (maximum 200 words).",
                     "APV: yes, it values tax shields as a sepatate components of enterprise value. The value of the tax shields is equal to the PV of forecast TSs, discounted using either kEL or kD. DCF asset-side: yes, it values tax shields by adjusting (backwards) the discount rate. While in APV FCFO are discounted with the kEU, in an asset-side DCF the discount rate is the WACC, which is lower than kEU to incorporate the tax benefit.", 3)],
    scheme=["Official model answer (mock and AY 24-25 solutions workbook), quoted as the key.",
            "Note: the key says the tax shields are discounted 'using either kEL or kD'; the L3 deck discounts them at kTS, 'kD or kEU' — the key's 'kEL' looks like a slip for kEU.",
            "Points: both include the benefit; APV adds V(TS) separately to VU (FCFO at kEU); asset-side DCF puts it in the discount rate (WACC < kEU via kD × (1 − t))."],
    cites=[cite("L3", 3, "Where are tax benefits taken into account in the DCF models?"), cite("L3", 14, "will be lower than the kEU as it incorporates the tax benefits that was otherwise a separate item in APV")],
    groups=["L3A"], units=["L3-U3", "L3-U5"], minutes=6,
    check="The official key writes 'discounted using either kEL or kD'; the deck uses kD or kEU (kTS). Kept as printed; flagged."))
REAL.append(realq(
    id="30257-L5-13", deck="L5", topic="FCFO from two balance sheets and an income statement", objective="Reorganizing financials; building FCFO", shape=PROB,
    file=F_M26, location=M26_LOC.format("Part III, problem 1") + "; " + TEXTCHK,
    stem="Based on the company’s following balance sheets and income statements and assuming a marginal tax rateequal to 30%, compute its free cash flows from operations in the only possible year.",
    data="| Balance sheet (€m) | 2011 | 2012 | Balance sheet (€m) | 2011 | 2012 |\n|---|---|---|---|---|---|\n| Excess cash | 18,0 | 19,4 | Short-term debt | 40,0 | 30,0 |\n| Account receivable | 40,0 | 44,0 | Account payables | 108,0 | 180,0 |\n| Inventory | 80,0 | 40,0 | Tax payable | 40,0 | 36,0 |\n| | | | Dividend payable | 26,0 | 26,0 |\n| Total current Assets | 138,0 | 103,4 | Total current liabilities | 214,0 | 272,0 |\n| Net tangible fixed assets | 200,0 | 230,0 | Long-term debt | 40,0 | 20,0 |\n| Non-operating assets | 60,0 | 70,0 | Shareholder equity | 100,0 | 92,4 |\n| | | | Minority interests | 44,0 | 19,0 |\n| Total Assets | 398,0 | 403,4 | Total liabilities and equity | 398,0 | 403,4 |\n\n| Income statement (€m) | 2011 | 2012 |\n|---|---|---|\n| Sales | 100,0 | 120,0 |\n| Raw materials | (40,0) | (60,0) |\n| Depreciation | (6,0) | (3,0) |\n| Interest paid | (6,0) | (6,0) |\n| Interest received | 1,0 | 1,0 |\n| Income taxes | (7,6) | (6,8) |\n| Net profit | 41,4 | 45,2 |",
    parts=[s_written("1", "Compute FCFO for 2012.", "FCFO 2012 = 113,9: EBIT 57 − operating taxes 17,1 + D&A 3 + decrease in noncash WC 104 − CAPEX 33.", 3)],
    scheme=["Official solution: noncash working capital 2011 = 40+80−108−40 = −28; 2012 = 44+40−180−36 = −132; EBIT = 120−60−3 = 57; operating taxes = −57×0,3 = −17,1; +D&A 3; −increase in NWC = −[(−132) − (−28)] = +104; CAPEX = −(230−200) − 3 = −33; FCFO = 113,9.",
            "Only 2012 is possible because FCFO needs the change in balance-sheet items. Excess cash, non-operating assets, debt and dividends payable are not operating."],
    cites=[cite("L5", 24, "FCFO = NOPAT - increase in core capital employed during the year")],
    groups=["L5C", "L5A"], units=["L5-U2", "L5-U4"], minutes=8))

# ---- valuation mock v2 (Studocu): the two items that are not in the AY mocks and are in scope ----------------
V2_LOC = "Valuation - Mock Exam v2 (Studocu copy of an instructor mock), multiple choice question {}; " + TEXTCHK
REAL.append(realq(
    id="30257-L5-14", deck="L5", topic="Supermarkets and noncash working capital", objective="Reorganizing the balance sheet: noncash working capital", shape=MCQ,
    file=F_V2, location=V2_LOC.format(9), stem="A supermarket chain will most likely:",
    parts=[s_mcq("1", "A supermarket chain will most likely:", ["Have negative noncash working capital", "Not easily get a bank loan", "Have high fixed costs", "Never be a target of a leveraged buyout"], "A", "double-solved")],
    scheme=["Answer A (no key in the source; solved twice). Route 1: supermarkets sell for cash (almost no receivables), turn inventory fast and pay suppliers on 60–90 days, so trade payables exceed receivables + inventory. Route 2: B and D are unfounded generalisations and C is not the defining trait asked for."],
    cites=[cite("L5", 10, "only includes the assets and the liabilities with an operating nature generated by the ordinary execution of the business model")],
    groups=["L5A"], units=["L5-U2"], minutes=1))
REAL.append(realq(
    id="30257-L12-11", deck="L12", topic="Probability of success in a young business's DCF", objective="Value and uncertainty: modelling cash flows and discount rates", shape=MCQ,
    file=F_V2, location=V2_LOC.format(10),
    stem="You are valuing a young business in the hardware industry. Its 2023 forecast FCFO is equal to € 10 million, whose probability of success is equal to 70%. The weighted average cost of capital (WACC) based on similarly young businesses in the industry is equal to 18%, while based on more mature hardware companies it would be equal to 10%. In a DCF model, in 2023 you should consider:",
    parts=[s_mcq("1", "In a DCF model, in 2023 you should consider:", ["A FCFO of 7 and a WACC of 18%", "A FCFO of 10 and a WACC of 18%", "A FCFO of 10 and a WACC of 10%", "None of the above"], "D", "double-solved")],
    scheme=["Answer D (no key in the source; solved twice). Route 1: the risk of failure is taken once — either in the cash flow (expected FCFO = 70% × 10 = 7) discounted at the mature 10% WACC, or in a higher rate on the success-case flow — so the consistent pair (7; 10%) is not listed. Route 2: A counts the failure risk twice; B and C each mix one convention with the other's number.",
            "The deck's 'Alternative approaches to cash flow representation' slide makes this point in a table the text layer does not show; this key rests on the double-counting argument."],
    cites=[cite("L12", 53, "Alternative approaches to cash flow representation")],
    groups=["L12D"], units=["L12-U15"], minutes=2,
    check="No official key. The key (D) relies on the double-counting argument; please confirm against the L1-2 slide 53 table (its content is an image)."))

# ---- January 2019 exam (questions only; no answers in the source) -------------------------------------------
J19_LOC = "30257 exam, 11 January 2019 (Studocu copy; questions only), question {}; " + TEXTCHK
REAL.append(realq(
    id="30257-L4-12", deck="L4", topic="Methods to estimate the market risk premium", objective="Cost of equity: the market risk premium", shape=ESSAY,
    file=F_J19, location=J19_LOC.format(1), stem="Explain the methods to estimate the Market Risk Premium (2 points)",
    parts=[s_written("1", "Explain the methods to estimate the Market Risk Premium.",
                     "Four methods (L4): 1) historical: rM = historical return on a market index (choice of index, sample 6–24 months, arithmetic/geometric, daily/weekly), MRP = rM − rF; 2) implied: rM implied by the cash returned to shareholders of the index (dividends + buybacks) at consensus growth; 3) Damodaran's estimates (implied premium separating country risk); 4) Fernandez's survey of professionals.", 2, "double-solved")],
    scheme=["No official answer in the source; the key lists the four methods on L4 slides 11–12.", "Full marks: each method named with how rM is obtained; a comment on the choices (index, sample, averaging)."],
    cites=[cite("L4", 11, "Historical approach: rM equal to the historical return of a market index"), cite("L4", 12, "Implied risk premium approach")],
    groups=["L4A"], units=["L4-U3"], minutes=5))
# Q6: enterprise DCF with target leverage; method and data mirror Workbook 4.3 (official solution)
ebit2, t, kel, kd, g = 33.0, 0.30, 0.132, 0.075, 0.03
nd2, e2 = 111.0 - 48.0, 105.0
w = kel * e2 / (nd2 + e2) + kd * (1 - t) * nd2 / (nd2 + e2)
da2 = 37.0 - 33.0
fcfo2 = ebit2 * (1 - t) + da2 + 1.0 - ((130.0 - 125.0) + da2)
ev1 = fcfo2 / (w - g)
eqv1 = ev1 - (122.0 - 45.0)
near(fcfo2, 19.1)
REAL.append(realq(
    id="30257-L3-13", deck="L3", topic="Enterprise DCF at a target leverage", objective="Asset-side DCF: FCFO, WACC at target leverage, the bridge to equity", shape=PROB,
    file=F_J19, location=J19_LOC.format(6),
    stem="Based on below data compute the enterprise and equity value of Company Alpha at the end of year 1 using enterprise DCF, assuming a target leverage equal to year 2 leverage. (3 points)",
    data="| | 1 | 2 |\n|---|---|---|\n| EBIT | 29,5 | 33,0 |\n| Investent rate | 30,0% | 30,0% |\n| Operating Working Capital | 46,0 | 45,0 |\n| Variation in WC | 3,0 | (1,0) |\n| Net fixed assets | 125,0 | 130,0 |\n| Market cap. | 102,0 | 105,0 |\n| Excess cash | 45,0 | 48,0 |\n| Long term debt | 122,0 | 111,0 |\n| Account payables | 52,0 | 56,0 |\n| Tax rate | 30,0% | 30,0% |\n| Growth rate | | 3,0% |\n| EBITDA | 31,0 | 37,0 |\n| kEL | 13,2% | 13,2% |\n| kD | 7,5% | 7,5% |",
    parts=[s_written("1", "Enterprise value and equity value at the end of year 1.", f"WACC {f(w * 100, 2)}%; FCFO year 2 = {f(fcfo2)}; EV = {f(ev1)}; equity value = {f(eqv1)}.", 3, "double-solved")],
    scheme=[f"No official answer in the source. Method = official solution of Workbook 4.3 (same company data, different debt): net debt = long-term debt − excess cash (payables are operating); WACC at year-2 weights: ND 63, E 105 → D/V 37,5%; WACC = 62,5% × 13,2% + 37,5% × 7,5% × 70% = {f(w * 100, 2)}%.",
            f"FCFO year 2 = EBIT 33 × 70% + D&A (37 − 33 = 4) + decrease in WC 1 − CAPEX (130 − 125 + 4 = 9) = {f(fcfo2)}.",
            f"EV end of year 1 = {f(fcfo2)} / ({f(w * 100, 2)}% − 3%) = {f(ev1)}; equity = EV − net debt year 1 (122 − 45 = 77) = {f(eqv1)}.",
            "The 'Investent rate 30%' (spelled so in the source) and EBITDA 1 are not needed: the workbook version labels the same 30% as ROCE."],
    cites=[cite("L3", 18, "a second subsequent stage (the terminal value), with a constant growth assumption"), cite("L4", 30, "Medium/long-term target financial leverage")],
    groups=["L3B", "L4C", "L5D"], units=["L3-U6", "L4-U10", "L5-U6"], minutes=10,
    check="No official key. Solved with the method of Workbook 4.3's official solution (same data); please confirm the reading of 'investment rate' as extraneous."))
# Q8: cost of equity from peers (method = Workbook 3.5 official solution)
peers = [(17979.7, 4883.4, 1247.9, 767.9, 0.30, 0.85), (18614.1, 4682.7, 2703.9, 1253.5, 0.28, 1.26), (17965.5, 6756.0, 10373.7, 95.5, 0.30, 1.61)]
bus, des = [], []
for E, st, lt, cash, tx, bl in peers:
    de = (st + lt - cash) / E
    des.append(de)
    bus.append(bl / (1 + (1 - tx) * de))
bu = sum(bus) / 3
de_avg = sum(des) / 3
keu = 0.058 + bu * 0.063
blv = bu * (1 + (1 - 0.28) * de_avg)
kel_capm = 0.058 + blv * 0.063
kel_mm = keu + de_avg * (keu - 0.075) * (1 - 0.28)
near(round(keu * 100, 1), 11.4)
REAL.append(realq(
    id="30257-L4-13", deck="L4", topic="Levered and unlevered cost of equity from peers", objective="Cost of equity: bottom-up beta (Hamada), CAPM", shape=PROB,
    file=F_J19, location=J19_LOC.format(8),
    stem="With rF = 5,8%, a MRP = 6,3%, a kD = 7,5%, and a peer of comparable companies, determine the levered and unlevered cost of equity for Company Beta, which operates in the same country company 2 does and whose target leverage is aligned with market average. (3 points)",
    data="| Company | Average mkt cap. | Short term financial debt | Long term financial debt | Cash | Tax Rate | Lev. Beta |\n|---|---|---|---|---|---|---|\n| 1 | 17.979,7 | 4.883,4 | 1.247,9 | 767,9 | 30,0% | 0,850 |\n| 2 | 18.614,1 | 4.682,7 | 2.703,9 | 1.253,5 | 28,0% | 1,260 |\n| 3 | 17.965,5 | 6.756,0 | 10.373,7 | 95,5 | 30,0% | 1,610 |",
    parts=[s_written("1", "Unlevered and levered cost of equity of Company Beta.", f"βU (average) = {f(bu, 3)}; kEU = {f(keu * 100, 1)}%; relevered β = {f(blv, 3)} at D/E {f(de_avg * 100, 1)}% and t = 28%; kEL = {f(kel_capm * 100, 1)}% (CAPM). Via MM with kD: {f(kel_mm * 100, 1)}%.", 3, "double-solved")],
    scheme=["No official answer in the source. The same peer table is Workbook problem 3.5, whose official solution uses net debt, Hamada per peer, the average βU, then relevers at the average D/E and applies CAPM ('first way'), also showing the MM route ('second way').",
            f"Net-debt D/E: {', '.join(f(d * 100, 1) + '%' for d in des)}; βU: {', '.join(f(b, 3) for b in bus)}; average {f(bu, 3)}.",
            f"kEU = 5,8% + {f(bu, 3)} × 6,3% = {f(keu * 100, 2)}% (question 9 of the same exam gives kEU = 11,4%, which confirms it).",
            f"Relever at the market-average D/E {f(de_avg * 100, 1)}% with company 2's 28% tax: β = {f(blv, 3)}; kEL = {f(kel_capm * 100, 2)}%. The MM route gives {f(kel_mm * 100, 2)}%: the two agree only if kD = rF (L4 slide 39)."],
    cites=[cite("L4", 24, "Unlever each bL with the Hamada formula: obtain bU for each"), cite("L4", 39, "Option 1 = Option 2 when kD = rF !")],
    groups=["L4B"], units=["L4-U7", "L4-U8", "L4-U12"], minutes=10,
    check="No official key. Two defensible kEL routes exist (L4 slide 39); the key gives CAPM relevering as the main answer, as the workbook's official solution to the same table does."))
tvf = [(17.7, 10.2), (24.1, 12.6)]
k = 0.114
pv = sum((a + b) / (1 + k) ** (i + 1) for i, (a, b) in enumerate(tvf))
tv = (24.1 + 12.6) * 1.03 / (k - 0.03)
ev = pv + tv / (1 + k) ** 2
near(ev, (17.7 / 1.114 + 24.1 / 1.114 ** 2 + 24.1 * 1.03 / 0.084 / 1.114 ** 2) + (10.2 / 1.114 + 12.6 / 1.114 ** 2 + 12.6 * 1.03 / 0.084 / 1.114 ** 2))
REAL.append(realq(
    id="30257-L3-14", deck="L3", topic="APV with kTS = kEU", objective="Adjusted present value in a two-stage model", shape=PROB,
    file=F_J19, location=J19_LOC.format(9), stem="Based on data of the previous exercise Compute the EV of Company Beta at the end of year 0 with the APV methodology (assume kTS=kEU). (3 points)",
    data="| | 0 | 1 | 2 |\n|---|---|---|---|\n| FCF | | 17,7 | 24,1 |\n| Tax shields | | 10,2 | 12,6 |\n| Growth | | | 3,0% |\n| kEU | 11,4% | | |",
    parts=[s_written("1", "EV at the end of year 0 (APV).", f"EV ≈ {f(ev)} (VU {f(17.7 / 1.114 + 24.1 / 1.114 ** 2 + 24.1 * 1.03 / 0.084 / 1.114 ** 2)} + V(TS) {f(10.2 / 1.114 + 12.6 / 1.114 ** 2 + 12.6 * 1.03 / 0.084 / 1.114 ** 2)}).", 3, "double-solved")],
    scheme=[f"No official answer. VU = 17,7/1,114 + 24,1/1,114² + [24,1 × 1,03 / (11,4% − 3%)]/1,114²; V(TS) the same with 10,2 and 12,6 (kTS = kEU); EV = {f(ev)}.",
            f"Second route: because kTS = kEU, discount (FCF + TS) together: 27,9/1,114 + 36,7/1,114² + 36,7 × 1,03/0,084/1,114² = {f(ev)}."],
    cites=[cite("L3", 19, "and in the APV valuation")], groups=["L3A"], units=["L3-U3", "L3-U6"], minutes=8))
# Q10 Theta: FCFO, FCFE, total cash flow with an effective tax rate
te = 319.0 / 2483.0
ebit, da = 2623.0, 609.0
nwc10, nwc11 = 1066 + 765 + 204 - 870, 1205 + 834 + 174 - 745
capex = (5053.0 - 4133.0) + da
fo = ebit * (1 - te) + da - (nwc11 - nwc10) - capex
fe = fo - 180 + 40 + (180 - 40) * te - (671 - 401) + (533 - 633) + ((1676 + 4140) - (1039 + 2082))
tot = fe + ((3167 - 2543) - 2164)
near(tot, 2324 - 598)
REAL.append(realq(
    id="30257-L5-15", deck="L5", topic="FCFO, FCFE and total cash flow of the year", objective="Building cash flows for valuation (FCFO, FCFE, change in cash)", shape=PROB,
    file=F_J19, location=J19_LOC.format(10), stem="Compute 2011 FCFO, FCFE and the total cash flow of company Theta (consider an effective tax rate). (2 points)",
    data="| Balance sheet | 2010 | 2011 | Income statement | 2010 | 2011 |\n|---|---|---|---|---|---|\n| Excess cash | 598,0 | 2.324,0 | Sales | 9.011,0 | 9.255,0 |\n| Account receivable | 1.066,0 | 1.205,0 | Operating costs | (5.673,0) | (6.023,0) |\n| Inventory | 765,0 | 834,0 | EBITDA | 3.338,0 | 3.232,0 |\n| Other current assets | 204,0 | 174,0 | Depreciation | (491,0) | (609,0) |\n| Tangible fixed assets | 4.133,0 | 5.053,0 | EBIT | 2.847,0 | 2.623,0 |\n| Real estate assets | 401,0 | 671,0 | Interest paid | (146,0) | (180,0) |\n| Total Assets | 7.167,0 | 10.261,0 | Interest received | 37,0 | 40,0 |\n| Short-term debt | 1.039,0 | 1.676,0 | Profit before taxes | 2.738,0 | 2.483,0 |\n| Account payables | 870,0 | 745,0 | Taxation | (364,0) | (319,0) |\n| Long-term debt | 2.082,0 | 4.140,0 | Net profit | 2.374,0 | 2.164,0 |\n| Non-operating provisions | 633,0 | 533,0 | | | |\n| Shareholder equity | 2.543,0 | 3.167,0 | | | |\n| Total liabilities and equity | 7.167,0 | 10.261,0 | | | |",
    parts=[s_written("1", "2011 FCFO, FCFE and total cash flow.", f"Effective tax rate {f(te * 100, 2)}%; FCFO = {f(fo)}; FCFE = {f(fe)}; total cash flow = {f(tot)} (= change in excess cash 2.324 − 598).", 2, "double-solved")],
    scheme=[f"No official answer. EBIT 2.623 × (1 − {f(te * 100, 2)}%) + D&A 609 − ΔNWC ({nwc11:,} − {nwc10:,} = {nwc11 - nwc10}) − CAPEX (920 + 609 = {capex:,.0f}) = {f(fo)}.",
            f"FCFE = FCFO − net interest 140 + tax shield {f(140 * te)} − increase in real estate (surplus) 270 − decrease in non-operating provisions 100 + increase in gross debt 2.695 = {f(fe)}.",
            f"Total cash flow = FCFE + equity flows (Δequity 624 − net profit 2.164 = −1.540) = {f(tot)}, which equals the change in excess cash 2.324 − 598 = 1.726: the check closes."],
    cites=[cite("L5", 21, "A new CF can be built ad-hoc for valuation, highlighting the CFs for the 3 DCF valuation models"), cite("L4", 27, "Superficial and prone to mistakes (not directly associated with interest tax shields), but easily applicable")],
    groups=["L5C"], units=["L5-U4", "L5-U5"], minutes=8))

# ---- January 2023 exam (screen photographs; Blackboard's correct answers shown; MCQ options not captured) ---------------
J23_LOC = "30257 exam of 26 January 2023, Blackboard review screen photographed (question {}); " + PHOTO
def j23(id, n, deck, topic, obj, prompt, answer, groups, units, cites, scheme, status="official", minutes=1.5, shape=SHORT):
    REAL.append(realq(id=id, deck=deck, topic=topic, objective=obj, shape=shape, file=F_J23, location=J23_LOC.format(n), image=True,
                      stem=prompt, parts=[s_written("1", prompt, answer, 1, status)], scheme=scheme, cites=cites, groups=groups, units=units, minutes=minutes))


j23("30257-L12-12", 8, "L12", "Where a sum-of-the-parts DCF fits", "DCF: valuing a multi-business company", "A sum of the parts discounted cash flows valuation model is better suited to value:",
    "Holding companies", ["L12B"], ["L12-U7"], [cite("L12", 28, "The value of a company is the result of the sum of the business units’s value")],
    ["Blackboard's correct answer: Holding companies. The other options were not photographed, so this is asked as a short answer."])
j23("30257-L4-14", 11, "L4", "Unlevered beta from market data", "Beta: Hamada formula with market values",
    "A company finances itself on regulated financial markets. The main market inputs are: price per share = 30; total number of shares = 20; beta (levered) = 1,0; market value of financial debt = 300. Also, the yield on Government bonds is 3%. The company published the following balance sheet data: shareholders' equity = 350; book value of financial debt = 250; market value of financial debt = 300. The income tax rate is 30%. Derive the unlevered beta of the company",
    "0.741", ["L4B"], ["L4-U7", "L4-U10"], [cite("L4", 22, "Debt and equity should be measured at market values (more on this later)")],
    ["Blackboard's correct answer: 0.741.", "E = 30 × 20 = 600 (market), D = 300 (market); βU = 1,0 / (1 + 0,7 × 300/600) = 0,741. Book equity and book debt are distractors."], minutes=2)
j23("30257-L5-16", 12, "L5", "FCFO when bank loans and fixed assets rise", "Cash flows for valuation: FCFO",
    "A company's 2019 annual report shows: EBITDA = 350; D&A = 50; interest expenses = 50; effective tax rate =50%. Meanwhile, the book value of bank loans and of fixed assets (after D&A) increased by 20 each. How much is FCFO 2019?",
    "130.0", ["L5C"], ["L5-U4"], [cite("L5", 22, "- (FA Y2 – Y1) – D&A Y2")],
    ["Blackboard's correct answer: 130.0.", "EBIT 300 × 50% = 150 + D&A 50 − CAPEX (20 + 50 = 70) = 130. Bank loans and interest are financing items, not in FCFO."], minutes=2)
j23("30257-L3-15", 14, "L3", "Terminal value at the end of the explicit period", "Two-stage DCF: the terminal value",
    "It's Dec. 31, 2021. A company estimated its free cash flows from operations for the period 2022 - 2026 (included). In a DCF asset-side valuation, the terminal value (assuming some growth exists) on Dec. 31, 2026, will be equal to:",
    "FCFO in 2026 * (1 + long term growth rate) / (WACC - long term growth rate)", ["L3B"], ["L3-U6"], [cite("L3", 18, "a second subsequent stage (the terminal value), with a constant growth assumption")],
    ["Blackboard's correct answer: FCFO in 2026 × (1 + g) / (WACC − g)."])
j23("30257-L5-17", 17, "L5", "What does not affect FCFO", "Cash flows for valuation: FCFO versus equity flows",
    "Free cash from operations, defined for valuation purposes, won't be affected by:", "An increase in the dividend paid to shareholders",
    ["L5C"], ["L5-U5"], [cite("L5", 25, "Free cash flows to equity (FCFE) = cash that would be available to shareholders (after repaying debtholders)")],
    ["Blackboard's correct answer: an increase in the dividend paid to shareholders."])
REAL.append(realq(
    id="30257-L5-18", deck="L5", topic="FCFO from forecast statements (15% tax)", objective="Building FCFO from two balance sheets", shape=PROB,
    file=F_J23, location=J23_LOC.format("2, essay") + "; the essay's 'Correct answer' field is [None]", image=True,
    stem="Starting from the company's forecast 2011 and 2012 income statements and balance sheets, determine the appropriate cash flow to be discounted in a DCF asset-side valuation model. Apply a 15% income tax rate, if necessary.",
    data="| Balance sheet ($m) | 2011 | 2012 |\n|---|---|---|\n| Cash | 240 | 300 |\n| Account receivables | 600 | 700 |\n| Tangible assets | 3,000 | 3,600 |\n| Investments in subsidiaries | 900 | 1,000 |\n| Assets | 4,740 | 5,600 |\n| Taxes payable | 540 | 540 |\n| Bank loans | 580 | 300 |\n| Equity | 3,620 | 4,760 |\n| Liabilities and equity | 4,740 | 5,600 |\n\n| Income statement ($m) | 2011 | 2012 |\n|---|---|---|\n| Sales | 1,500 | 1,800 |\n| Raw materials | (600) | (900) |\n| Depreciation | (90) | (46) |\n| Interests | (30) | (30) |\n| Income taxes | (120) | (100) |\n| Net income | 660 | 724 |",
    parts=[s_written("1", "The appropriate cash flow (FCFO 2012).", "FCFO 2012 = 25,9: EBIT 854 − 15% operating taxes 128,1 + D&A 46 − ΔNWC 100 − CAPEX 646.", 3, "double-solved")],
    scheme=["No official answer (essay). The photographed student answer (25,9) matches this key: EBIT 2012 = 1.800 − 900 − 46 = 854; NWC = receivables − taxes payable: 60 → 160 (Δ +100); CAPEX = 3.600 − 3.000 + 46 = 646; FCFO = 854 × 0,85 + 46 − 100 − 646 = 25,9.",
            "Cash and investments in subsidiaries are not operating; the bank loans are financing. The BSc paper (Q3) has the same question with every figure halved: its answer, 12,95, is exactly half — a second check."],
    cites=[cite("L5", 24, "FCFO = NOPAT - increase in core capital employed during the year")], groups=["L5C"], units=["L5-U4", "L5-U2"], minutes=8))
REAL.append(realq(
    id="30257-L3-16", deck="L3", topic="Tax shields in APV, asset-side and equity-side DCF", objective="Where tax benefits enter the three DCF models", shape=ESSAY,
    file=F_J23, location=J23_LOC.format("5, essay") + "; the 'Correct answer' field is [None]", image=True,
    stem="Briefly describe how the (1) adjusted present value (APV) model, the (2) asset-side discounted cash flows (DCF) model and (3) the equity-side DCF model incorporate into the valuation process the benefits originating from the tax treatment of debt interest payments.",
    parts=[s_written("1", "Describe (maximum 200 words).", "(1) APV: EV = VU + V(TS); FCFO at kEU, tax shields D × kD × t discounted separately at kTS (kD or kEU). (2) Asset-side DCF: FCFO at the WACC, whose after-tax kD × (1 − t) builds the benefit into the rate (WACC < kEU). (3) Equity-side DCF: FCFE already includes each year's tax shield (FCFE = FCFO − interest + tax shield ± Δdebt), discounted at kEL.", 3, "double-solved")],
    scheme=["No official answer. Key from L3 slides 8–16 and 21: APV separates the tax shields; WACC embeds them in the rate; FCFE embeds them in the cash flow.",
            "The photographed student answer said no tax-shield benefit enters the equity-side DCF; that is wrong — FCFE adds the tax shield of the year (L3 slide 21)."],
    cites=[cite("L3", 21, "+ Tax shields"), cite("L3", 14, "will be lower than the kEU as it incorporates the tax benefits that was otherwise a separate item in APV")],
    groups=["L3A"], units=["L3-U3", "L3-U4", "L3-U5"], minutes=6))
REAL.append(realq(
    id="30257-L3-17", deck="L3", topic="Enterprise value from NOPAT, growth and return on new capital", objective="Growth and value: g = ROI × reinvestment", shape=SHORT,
    type="adapted", verbatim=False, file=F_OLD1, location="Old Exam 1.pdf (a typed index of the January 2023 exam), question 3; the matching screen photograph is not in the folder",
    stem="Consider the following inputs: NOPAT t+1 = $72.2m. NOPAT growth rate = 2%. Return on new invested capital = 11.21. WACC = 7.4%. Which of the following is closest to the enterprise value at the end of year t?",
    parts=[s_written("1", "Enterprise value at the end of year t.", "≈ $1.098,5m: 72,2 × (1 − 2%/11,21%) / (7,4% − 2%).", 1, "double-solved")],
    scheme=[f"Reinvestment = g / RONIC = 2% / 11,21% = {f(2 / 11.21 * 100, 2)}%; FCFO = 72,2 × {f(1 - 2 / 11.21, 4)} = {f(72.2 * (1 - 2 / 11.21), 2)}; EV = {f(72.2 * (1 - 2 / 11.21), 2)} / 5,4% = {f(72.2 * (1 - 2 / 11.21) / 0.054, 1)}.",
            "Second route: EV = NOPAT/WACC-type check — with RONIC > WACC, EV exceeds the no-growth value 72,2/7,4% = 975,7, as it should."],
    cites=[cite("L3", 26, "the growth rate in earnings (g) should be equal to the product of the reinvestments into the business (CRR) and the return")],
    groups=["L3C"], units=["L3-U10"], minutes=2,
    check="Adapted: taken from a typed index of the exam (not the photographs); the options are not recorded and '11.21' has lost its % sign. Please check against the original if you have it."))

# ---- BSc past exam (photographs; no answers recorded) ------------------------------------------------------------------
BSC_LOC = "BSc past exam (Blackboard online exam, 60 minutes; photographs in BSc.pdf = Old Exam 2.pdf), question {}; " + PHOTO
def bsc(id, n, deck, topic, obj, prompt, options, letter, groups, units, cites, scheme, status="double-solved", minutes=1.5):
    REAL.append(realq(id=id, deck=deck, topic=topic, objective=obj, shape=MCQ, file=F_BSC, location=BSC_LOC.format(n), image=True,
                      stem=prompt, parts=[s_mcq("1", prompt, options, letter, status)], scheme=scheme, cites=cites, groups=groups, units=units, minutes=minutes))


REAL.append(realq(
    id="30257-L5-19", deck="L5", topic="When FCFO equals NOPAT", objective="FCFO in a zero-growth, maintenance-investment scenario", shape=ESSAY,
    file=F_BSC, location=BSC_LOC.format(1), image=True,
    stem="Consider the estimation of the free cash flows from operations (FCFO) in a DCF asset-side model. Under which conditions will it be equivalent to the net operating profit after taxes (NOPAT)?",
    parts=[s_written("1", "Explain.", "When net investment is zero: no change in noncash working capital and CAPEX equal to D&A (maintenance investments only), i.e. the zero-growth steady state; then FCFO = EBIT × (1 − t) = NOPAT.", 3, "double-solved")],
    scheme=["No official answer. L3 slide 7 and slide 21: in a zero-growth scenario with 'Maintenance investments (no ∆WC and CAPEX = D&A)', FCFO = EBIT − operating taxes; FCFO = NOPAT − increase in core capital employed (L5 slide 24), so they coincide when capital employed does not grow."],
    cites=[cite("L3", 7, "Maintenance investments (no ∆WC and CAPEX = D&A)"), cite("L5", 24, "FCFO = NOPAT - increase in core capital employed during the year")],
    groups=["L5C", "L3B"], units=["L5-U5", "L3-U7"], minutes=5))
E_u, D_u = 25.0 * 28.0, 130.0
kel_u, kd_u = 0.01 + 0.7 * 0.065, 0.01 + 0.02
wacc_u = kel_u * E_u / (E_u + D_u) + kd_u * 0.7 * D_u / (E_u + D_u)
REAL.append(realq(
    id="30257-L4-15", deck="L4", topic="WACC from market data (Umbrella Inc)", objective="WACC: CAPM, rating spread, market weights", shape=PROB,
    file=F_BSC, location=BSC_LOC.format(4), image=True, stem="According to the following financials, estimate the weighted average cost of capital.",
    data="| Umbrella Inc ($m) | |\n|---|---|\n| Levered beta | 0,70 |\n| Spread on debt | 2,0% |\n| Tax rate | 30,0% |\n| Risk-free rate | 1,0% |\n| Market risk premium | 6,5% |\n| Share price (€) | 25,0 |\n| Number of shares | 28,0 |\n| Financial debt | 130,0 |",
    parts=[s_written("1", "WACC.", f"WACC ≈ {f(wacc_u * 100, 2)}%: kEL {f(kel_u * 100, 2)}%, kD 3,0% (after tax 2,1%), E 700, D 130.", 3, "double-solved")],
    scheme=[f"No official answer. kEL = 1% + 0,70 × 6,5% = {f(kel_u * 100, 2)}%; kD = 1% + 2% = 3%; E = 25 × 28 = 700; D = 130; WACC = {f(kel_u * 100, 2)}% × 700/830 + 3% × 0,7 × 130/830 = {f(wacc_u * 100, 2)}%.",
            "Workbook 3.15 is the same company with different figures (official WACC 5,0% there)."],
    cites=[cite("L4", 32, "For a listed company a good proxy is the market capitalization")], groups=["L4C"], units=["L4-U10", "L4-U11"], minutes=6))
bsc("30257-L12-13", 5, "L12", "When a sum-of-the-parts DCF can be built", "DCF: valuing a multi-business company", "A sum of the parts DCF model can be designed if:",
    ["Standalone value can be separated from the value of expected synergies", "A cash flow can be derived for each business unit", "The value of the growth opportunities can be separated from the value of the assets in place", "For each business unit at least revenues can be identified"], "B",
    ["L12B"], ["L12-U7"], [cite("L12", 28, "The value of a company is the result of the sum of the business units’s value")],
    ["Answer B (no key recorded; solved twice). Route 1: a SOTP DCF discounts each BU's own cash flows. Route 2: A and C describe the acquisition value and the NPVGO split (other items on the same slide); revenues alone (D) are not enough for a DCF."])
bsc("30257-L5-21", 6, "L5", "Classifying a drawn line of credit", "Reorganizing the balance sheet: net debt", "According to the reformulated Balance Sheet, how would you classify the drawn portion of a short-term line of credit?",
    ["As an increase of noncash WC", "As an increase of fixed assets", "As an increase of net debt", "As a decrease of net equity"], "C",
    ["L5A"], ["L5-U2"], [cite("L5", 11, "Net debt represents the net exposure to third-party investors (banks, bondholders…)")],
    ["Answer C (solved twice): a drawn credit line is interest-bearing bank financing, so net debt; it is not an operating liability (A)."])
bsc("30257-L5-22", 7, "L5", "FCFO when payables and fixed assets rise", "Cash flows for valuation: FCFO",
    "A company's 2019 annual report shows: EBITDA = 350; D&A = 50; interest expenses = 50; effective tax rate = 50%. Meanwhile, the book value of accounts payable and of fixed assets increased by 20 each. How much is FCFO 2019?",
    ["175,0", "200,0", "150,0", "225,0"], "C", ["L5C"], ["L5-U4"], [cite("L5", 22, "- ↑ or + ↓ in noncash WC")],
    ["Answer C (solved twice): EBIT 300 × 50% = 150 + D&A 50 + increase in payables 20 − CAPEX (20 + 50) = 150.",
     "Check against the January 2023 version (bank loans instead of payables): 130; the extra +20 here is the payables' release of working capital."], minutes=2)
bsc("30257-L3-18", 8, "L3", "Top-down revenue forecasting", "Business plans and cash-flow forecasts", "A top-down approach to forecast revenues for a company:",
    ["Forecasts future revenues of the company as the sum of the forecast revenues of each product class", "Forecasts future revenues of the company as the product of the company's forecast cost of goods sold and a mark-up factor to cost of goods sold",
     "Forecasts future revenues of the company as the product of the forecast industry revenues and the company's forecast market share", "None of the other answers is correct"], "C",
    ["L3B"], ["L3-U7"], [cite("L3", 20, "The FCFO forecasts in the first stage should be based on a detailed business plan")],
    ["Answer C (solved twice): top-down starts from the market (industry revenues × market share); A is bottom-up.",
     "Forecasting techniques are covered in the Workbook (Ch. 2, 'Forecasting Techniques and Business Planning'), which is exam material."])
bsc("30257-L3-19", 9, "L3", "Why APV uses the unlevered cost of equity", "APV: unlevered value", "In the APV method, why is the unlevered cost of equity used instead of the WACC?",
    ["To account for retained earnings risk", "To avoid measuring the impact of debt", "To determine a value as if it were all equity financed", "To incorporate the risk of newly issued shares"], "C",
    ["L3A"], ["L3-U3"], [cite("L3", 9, "Adjusted present value (APV) method")], ["Answer C (solved twice): VU is the value as if all-equity financed; debt's effect is added separately as V(TS), so B is wrong."])
bsc("30257-L4-16", 10, "L4", "What moves the unlevered beta", "Beta determinants: financial and operating leverage",
    "Is the unlevered beta of a listed company affected by a higher (a) financial leverage( And by (b) operating leverage?",
    ["(a) Yes, beta increases. (b) Yes, beta increases", "(a) No. (b) Yes, beta decreases", "(a) No. (b) Yes, beta increases", "(a) No. (b) No."], "C",
    ["L4B"], ["L4-U6"], [cite("L4", 21, "More operating leverage (fixed operating costs versus variable costs) increases beta")],
    ["Answer C (solved twice): financial leverage affects only the levered beta; operating leverage is a business factor in βU and raises it."])
bsc("30257-L4-17", 11, "L4", "Bounds on the WACC", "WACC and the after-tax cost of debt", "A company has cost of debt of 6%, a fixed required return of equity of 9% and a tax rate of 50%. WACC is:",
    ["Between 6% and 9%", "Between 3% and 9%", "Between 0% and 9%", "None of the above because some inputs are missing"], "B",
    ["L4C", "L3A"], ["L4-U12", "L3-U5"], [cite("L3", 14, "The \"one-shot\" discount rate, the weighted average cost of capital")],
    ["Official answer B: the same question (options not photographed) in the January 2023 exam shows Blackboard's correct answer 'Between 3% and 9%'.",
     "After-tax kD = 6% × 50% = 3%, so WACC lies between 3% and 9% whatever the weights."], status="official")

# ---- L6 deck: workbook problems printed as slide text ----------------------------------------------------------------
L6_LOC = "L6 slides (Workbook selection, 2nd ed.), problem {}; " + TEXTCHK + "; official key: Corporate Valuation Workbook II solutions, Ch. {}"
REAL.append(realq(
    id="30257-L6-10", deck="L6", topic="Workbook 2.3: reorganizing Omega's balance sheet", objective="Reorganizing the balance sheet by sources and uses", shape=PROB,
    file=F_L6, location=L6_LOC.format("2.3", 2), stem="Omega Inc. closed FY 2019 with the following balance sheet. Reorganize it according to its sources and uses.",
    data="| Omega Inc. - Balance sheet (€m) | 2019 | | 2019 |\n|---|---|---|---|\n| Operating cash | 185,0 | Short-term debt | 1.113,0 |\n| Excess cash | 2.324,0 | Account payables | 745,0 |\n| Account receivable | 1.205,0 | Tax payable | 392,0 |\n| Inventory | 834,0 | Dividend payable | 16,0 |\n| Other current assets | 174,0 | Other current liabilities | 644,0 |\n| Total current Assets | 4.722,0 | Total current liabilities | 2.910,0 |\n| Net tangible fixed assets | 5.053,0 | Long-term debt | 3.540,0 |\n| Non-operating financial assets | 707,0 | Other provisions | 133,0 |\n| | | Shareholder equity | 3.167,0 |\n| | | Minority interest | 732,0 |\n| Total Assets | 10.482,0 | Total liabilities and equity | 10.482,0 |",
    parts=[s_written("1", "Reorganized balance sheet.", "Noncash WC 617; core invested capital 5.670; surplus assets 707 − provisions 133; net invested capital 6.244 = net debt 2.345 (1.113 + 16 + 3.540 − 2.324) + equity 3.899 (3.167 + 732).", 3)],
    scheme=["Official solution: NWC = 185 + 1.205 + 834 + 174 − 745 − 392 − 644 = 617; + fixed assets 5.053 = core 5.670; + surplus 707 − provisions 133 = 6.244.",
            "Net debt = short-term debt 1.113 + dividend payable 16 + long-term debt 3.540 − excess cash 2.324 = 2.345; equity incl. minorities 3.899; total 6.244."],
    cites=[cite("L5", 9, "Items can be dragged within sides (= sign) and across sides (change sign)")], groups=["L6", "L5A"], units=["L6-U2.3", "L5-U2"], minutes=8))
REAL.append(realq(
    id="30257-L6-11", deck="L6", topic="Workbook 2.5: Square Pizza's FCFO", objective="FCFO for valuation", shape=PROB,
    file=F_L6, location=L6_LOC.format("2.5", 2),
    stem="Square Pizzas Srl, a restaurant, shows the following key financials in FYs 2018 and 2019. How much is the company’s FCFO for valuation purposes in 2019?",
    data="| Square Pizza Srl - Key financials (€m) | |\n|---|---|\n| EBITDA 2019 | 300,0 |\n| D&A 2019 | 50,0 |\n| New investments 2019 | 40,0 |\n| Disposals 2019 | 5,0 |\n| Noncash working capital in balance sheet 2019 | 60,0 |\n| Noncash working capital in balance sheet 2018 | 80,0 |\n| Tax rate | 30,0% |\n| Debt in balance sheet 2019 | 52,0 |\n| Debt in balance sheet 2018 | 68,0 |\n| Interests 2019 | 4,0 |",
    parts=[s_written("1", "FCFO 2019.", "FCFO 2019 = 210: EBIT 250 − taxes 75 + D&A 50 + decrease in NWC 20 − CAPEX 35.", 3)],
    scheme=["Official solution: EBIT = 300 − 50 = 250; operating taxes 75; D&A 50; change in NWC +20; CAPEX = 40 − 5 = 35; FCFO = 210. Debt and interest are not in FCFO."],
    cites=[cite("L5", 24, "FCFO = NOPAT - increase in core capital employed during the year")], groups=["L6", "L5C"], units=["L6-U2.5", "L5-U4"], minutes=5))
REAL.append(realq(
    id="30257-L6-12", deck="L6", topic="Workbook 2.6: Full House's FCFE", objective="FCFE", shape=PROB,
    file=F_L6, location=L6_LOC.format("2.6", 2),
    stem="Full House LLC, a real estate company, discloses its FY 2019 annual report, which shows an EBIT equal to $500 million; capital expenditures for $100 million and interest expenses for $50 million. Meanwhile, Full House raised a new loan for $130 million and paid a dividend of $30 million. The business has no noncash working capital, no D&A and no income taxation.",
    parts=[s_written("1", "How much is FCFE in 2019?", "FCFE = 480: FCFO 400 (500 − 100) − interest 50 + new debt 130. The dividend is a use of FCFE, not a deduction.", 3)],
    scheme=["Official solution: FCFO = 500 − 100 = 400; FCFE = 400 − 50 + 130 = 480."],
    cites=[cite("L5", 25, "Free cash flows to equity (FCFE) = cash that would be available to shareholders (after repaying debtholders)")], groups=["L6", "L5C"], units=["L6-U2.6", "L5-U5"], minutes=4))
REAL.append(realq(
    id="30257-L6-13", deck="L6", topic="Workbook 3.8: Champagne's WACC with a synthetic rating", objective="WACC: synthetic rating, bottom-up beta", shape=PROB,
    file=F_L6, location=L6_LOC.format("3.8", 3) + "; the comparables table is not in the slide's text layer and is taken from the official solutions workbook's inputs",
    stem="Estimate Champagne SA’s WACC considering that its 2019 book value of equity is €300 million and the debt to equity leverage 0,2x. On the income statement, 2019 EBIT is €1.000 million, interests are €700 million and the income tax rate is 30%. Riskless securities have a return of 3%, whereas equity risk premium is 6%.\n\nThe cost of debt is based on a synthetic rating, with a spread following the interest coverage ratio, as below. Market data on comparable companies is also collected. If relevant, adopt the CAPM model.",
    data="| Interest coverage | Credit spread |\n|---|---|\n| Interest coverage > 2 | - |\n| 1 < Interest coverage < 2 | 2,0% |\n| Interest coverage < 1 | 4,0% |\n\n| Comparables | Market capitalization | Minorities | Bonds | Trade payables | Cash | Levered beta |\n|---|---|---|---|---|---|---|\n| Prosecco SpA | 15.000,0 | 2.000,0 | 2.000,0 | 1.400,0 | 500,0 | 1,250 |\n| Franciacorta SpA | 17.500,0 | - | 1.000,0 | - | 1.000,0 | 0,900 |\n| Sekt AG | 20.000,0 | 500,0 | 5.000,0 | 900,0 | - | 1,150 |",
    parts=[s_written("1", "WACC.", "WACC ≈ 8,9%: coverage 1,4x → spread 2% → kD 5%; average βU 1,020 → relevered 1,163 → kEL 10,0%; ND/(ND+E) 16,7%.", 3)],
    scheme=["Official solution: EBIT/interests = 1,4x → spread 2,0% → kD = 5,0%; peers' net debt (bonds − cash; payables are operating, minorities are equity) → D/E 8,8%, 0, 24,4% → βU 1,177, 0,900, 0,982, average 1,020; kEU 9,1%; relevered β 1,163 at D/E 0,2 → kEL 10,0% (CAPM); weights 16,7%/83,3%; WACC 8,9%.",
            "Book equity (300) is a distractor for weights: the target D/E 0,2x is given."],
    cites=[cite("L4", 36, "A \"synthetic\" rating, such as using Damodan's model"), cite("L4", 24, "Unlever each bL with the Hamada formula: obtain bU for each")],
    groups=["L6", "L4C"], units=["L6-U3.8", "L4-U8", "L4-U11"], minutes=10,
    check="The comparables table comes from the official solutions workbook (its input block), because the slide shows it only as an image."))
REAL.append(realq(
    id="30257-L6-14", deck="L6", topic="Workbook 4.9: Solar Beam's equity-side DCF", objective="Equity-side DCF: FCFE, kEL, terminal value, implied ROE", shape=PROB,
    file=F_L6, location=L6_LOC.format("4.9", 4),
    stem="A renewable energy group, Solar Beam SA, is developing a solar field, which is expected to generate the following key performance indicators between 2020 and 2023:\n\nThe setup will be financed by bonds, whose principal payment is €450 million per year up to and including year 4.\n\nStarting year 5 debt will be constantly refinanced to maintain the same outstanding level. In addition, little extra reinvestment will be needed, estimated at 10% of net income; residual earnings will be available to shareholders.\n\nIn this mature state the business’ earnings will grow 0,5% per year. On stock and money markets, the risk-free rate is 1%, the solar industry beta is 0,5 (already levered according to Solar Beam’s gearing) and the MRP is 6,5%.",
    data="| Solar Beam SA (€m) | 2019 | 2020 | 2021 | 2022 | 2023 |\n|---|---|---|---|---|---|\n| Net income | | 3.200,0 | 4.800,0 | 3.500,0 | 1.150,0 |\n| Investments for new projects (CAPEX) | | 1.000,0 | 500,0 | 500,0 | 100,0 |\n| EOP solar fields book value (Fixed assets) | 9.500,0 | 10.000,0 | 9.900,0 | 9.600,0 | 9.000,0 |",
    parts=[s_written("a", "Estimate the company’s free cash flows to equity between 2020 and 2023.", "FCFE 2020–2023 = 2.250; 4.450; 3.350; 1.300 (NI + implied D&A − CAPEX − 450 principal; implied D&A 500, 600, 800, 700)."),
           s_written("b", "What is the appropriate discount rate?", "kEL = 1% + 0,5 × 6,5% = 4,25% (≈ 4,3%)."),
           s_written("c", "Value Solar Beam with an equity DCF model as of the end of 2019.", "Equity value ≈ €33.794m: PV of FCFE 2020–23 = 10.310 + PV of TV 23.484 (TV = 1.155,8 × 90% / (4,25% − 0,5%) = 27.738)."),
           s_written("d", "What is the return on equity implied into the model’s long-term assumptions? Knowing that mature solar businesses rarely beat the market by more than 1% in equity returns, is it a reasonable underlying return?", "Implied ROE = g / reinvestment = 0,5% / 10% = 5,0%; reasonable, as it is less than 1% above kEL (4,25%).")],
    scheme=["Official solution: implied D&A from fixed assets (FA1 = FA0 + CAPEX − D&A): 500, 600, 800, 700; FCFE = NI + D&A − CAPEX − 450.",
            "kEL 4,3%; TV at 2023: NI 2024 = 1.150 × 1,005 = 1.155,8; FCFE = 90% = 1.040,2; TV = 27.738,0; PV 23.483,9; equity value 33.794,2.",
            "Implied long-term ROE 5,0%."],
    cites=[cite("L3", 19, "Similarly, DCF equity side in a two-staged model will be")], groups=["L6", "L3B"], units=["L6-U4.9", "L3-U6", "L3-U10"], minutes=16))

# ================================================================================================
# GENERATED HARD QUESTIONS (units with no question; one Hard per deck section)
# ================================================================================================
def hq(**kw):
    units = kw.pop("units")
    q = question(course=C, **kw)
    q["units"] = units
    q["negative_marking"] = NEG
    return q


def fmt_set(xs):
    xs = list(xs)
    return f"{xs[0]} only" if len(xs) == 1 else ", ".join(xs[:-1]) + f" and {xs[-1]} only"


def statements_mcq(n, intro, stmts, options, correct):
    roman = ["I", "II", "III", "IV", "V"]
    assert correct == fmt_set([roman[i] for i, (_, tt) in enumerate(stmts) if tt]), correct
    body = intro + "\n\n" + "\n".join(f"{roman[i]}. {s}" for i, (s, _) in enumerate(stmts)) + "\n\nWhich of the statements are correct?"
    q = mcq(n, body, options, correct, 1)
    return q


CM, SP = "concept MCQ (statements)", "short problem (written)"

# ---- L12 A: users and uses, the Kellanova example, fundamental skills ---------------------------------------------------
prem = 83.5 / 63.0 - 1
near(round(prem * 100, 1), 32.5)
st = [("A fairness opinion is prepared by an independent, unbiased party to assess the fairness of an offered price, as Morgan Stanley did for Scania's board when Volkswagen bid.", True),
      ("An investment bank's equity research report on a listed firm ends with a target price the stock should reasonably reach in about a year, based on public information.", True),
      ("Mars's offer valued Kellanova about 32.5% above its 2 August 2024 market capitalization, and Kellanova's share price then rose all the way to the $83.5 offer price.", False),
      ("Because valuation is a 'collage' of business, finance and economics, mastering each discipline separately is enough to produce consistent valuations.", False),
      ("Private equity and venture capital investors value companies to acquire majority or minority stakes, to value startups and in leveraged buyouts.", True)]
p = statements_mcq("1", "Consider the following statements about who values companies and why.", st,
                   [("I, II and V only", None), ("I, II, III and V only", "price_moved_to_the_offer"), ("II and V only", "fairness_opinion_misread"),
                    ("I, II, IV and V only", "skills_taken_as_a_collage")], "I, II and V only")
HARD.append(hq(id="30257-L12-02", deck="L12", topic="Users and uses of valuation, the Kellanova bid and the 'glue'", objective="Users and uses of valuation; bases of the introductory example; fundamental skills",
    shape=CM, shape_class="concept MCQ", stem="Introduction to valuation: statements.", parts=[p],
    scheme=["[1] Steps: (1) I true (fairness opinion, Scania/Volkswagen); (2) II true (target price, ~1 year, public information); (3) III: premium = 83,5/63,0 − 1 = 32,5%, but the price rose to about $80, not to 83,5 — false; (4) IV false: the deck calls the real determinant the 'glue' that holds the fields together; (5) V true; (6) I, II and V.",
            "Second route: III and IV each start from a fact on the slides and end with a conclusion the slides reject ('Why not up to 83,5?'; 'more than a collage')."],
    cites=[cite("L12", 7, "Morgan Stanley prepared a fairness opinion for Scania's board of directors"), cite("L12", 10, "Why did the market price increase to about $ 80? Why not up to 83,5?"),
           cite("L12", 14, "valuation is more than a \"collage of knowledge\" and technique")],
    location="L1-2 slides 3–14 (users and uses, Kellanova example, fundamental skills)", file=F_L12, groups=["L12A"], minutes=3,
    notches=["near_true_statements", "extra_step"], hc_parts=[{"n": "1", "steps": 6, "concepts": 3}], units=["L12-U1", "L12-U2", "L12-U3"]))

# ---- L12 B: approaches and methods -----------------------------------------------------------------------------------------
st = [("The income approach values an asset as the present value of all future benefits, while the cost approach revalues each balance-sheet item at its current conditions.", True),
      ("Relative valuation is less exposed to market moods than DCF, which is why it is preferred when pricing an IPO.", False),
      ("Economic profit models value a business as the adjusted book value of its invested capital plus the present value of excess returns, which can be negative.", True),
      ("Asset-based methods and DCF can give the same value for a firm with no growth opportunities whose asset values reflect expected cash flows.", True),
      ("EVA is the equity-side version of the economic profit approach and the residual income method is its asset-side version.", False)]
p = statements_mcq("1", "Consider the following statements about valuation approaches and methods.", st,
                   [("I, III and IV only", None), ("I, II, III and IV only", "relative_valuation_moods_reversed"), ("I, III, IV and V only", "eva_and_residual_income_swapped"),
                    ("III and IV only", "income_and_cost_approach_misread")], "I, III and IV only")
HARD.append(hq(id="30257-L12-03", deck="L12", topic="Income, market and cost approaches; economic profit; asset-based methods", objective="General approaches and specific methods",
    shape=CM, shape_class="concept MCQ", stem="Valuation approaches: statements.", parts=[p],
    scheme=["[1] Steps: (1) I true; (2) II false: relative valuation is MORE likely to reflect market moods — that is an advantage for an IPO; (3) III true; (4) IV true; (5) V false: EVA is the asset-side, residual income the equity-side version; (6) I, III and IV.",
            "Second route: II keeps the right conclusion (IPO) with the reason reversed; V swaps two labels."],
    cites=[cite("L12", 33, "Relative valuation is much more likely to reflect market perceptions and moods than DCF"),
           cite("L12", 35, "as an asset-side method: the economic value added method"), cite("L12", 37, "Asset based methods and DCF may yield the same values if we have a firm that has no growth opportunities")],
    location="L1-2 slides 16–37 (approaches, methods, DCF, relative valuation, economic profit, asset-based)", file=F_L12, groups=["L12B"], minutes=3,
    notches=["near_true_statements", "cross_section"], hc_parts=[{"n": "1", "steps": 6, "concepts": 3}],
    units=["L12-U4", "L12-U5", "L12-U6", "L12-U8", "L12-U9", "L12-U10"]))

# ---- L12 D: value and uncertainty -----------------------------------------------------------------------------------------
st = [("The choice between a static and a dynamic valuation standpoint depends on the level of uncertainty and on managerial flexibility.", True),
      ("The value of a new venture can be seen as its base-case standalone value plus the value generated by new choices and opportunities.", True),
      ("Because firms and managers are exposed to uncertainty but cannot influence it, the process to deal with risk starts from the cash flow model.", False),
      ("For a young business whose €10m FCFO has a 70% chance of success, discounting the expected €7m at a young-business WACC of 18% counts the failure risk twice.", True),
      ("All industrial sectors have the same predictability of performance, so uncertainty matters only for startups.", False)]
p = statements_mcq("1", "Consider the following statements about value and uncertainty.", st,
                   [("I, II and IV only", None), ("I, II, III and IV only", "risk_process_order_reversed"), ("I and II only", "double_counting_missed"),
                    ("I, II, IV and V only", "sector_predictability_misread")], "I, II and IV only")
HARD.append(hq(id="30257-L12-04", deck="L12", topic="Uncertainty, flexibility and how to represent risk in a DCF", objective="Value and uncertainty",
    shape=CM, shape_class="concept MCQ", stem="Value and uncertainty: statements.", parts=[p],
    scheme=["[1] Steps: (1) I true; (2) II true (base-case value + value of new choices); (3) III false: firms and management 'influence and generate risk', and the process starts by assessing the business model; (4) IV: expected FCFO 0,7 × 10 = 7 already prices failure, so 18% (which embeds it again) double-counts — true; (5) V false; (6) I, II and IV.",
            "Second route: IV is the same logic as the valuation mock v2 question 10 (answer 'none of the above')."],
    cites=[cite("L12", 47, "Firms and management are subjected to change, but also influence and generate risk and uncertainty"),
           cite("L12", 49, "The level of uncertainty"), cite("L12", 52, "Value generated by new choices and opportunities")],
    location="L1-2 slides 47–53 (value and uncertainty)", file=F_L12, groups=["L12D"], minutes=3,
    notches=["near_true_statements", "extra_step"], hc_parts=[{"n": "1", "steps": 6, "concepts": 3}], units=["L12-U14", "L12-U15"]))

# ---- L3 A (extra): leverage and accounting returns; MM without taxes; growth strategies ---------------------------------------
roe = 0.08 + 1.5 * (0.08 - 0.05)
near(roe, 0.125)
st = [("With no taxes, financing part of the invested capital with 5% debt raises the average ROE when ROI averages 10%, and widens the gap between worst- and best-case ROE.", True),
      ("Under Modigliani & Miller without taxes, higher leverage raises enterprise value because it raises ROE.", False),
      ("With ROE = ROI + D/E × (ROI − interest rate), a company with ROI 8%, D/E 1,5 and a 5% interest rate earns an ROE of 12,5%.", True),
      ("Convincing existing customers to buy more of a product is a high-value-creating growth strategy with a low risk of retaliation, because all competitors benefit.", True),
      ("Any growth creates value as long as the return on new investments is positive.", False)]
p = statements_mcq("1", "Consider the following statements about leverage, returns and growth.", st,
                   [("I, III and IV only", None), ("I, II, III and IV only", "roe_taken_as_value"), ("I and III only", "growth_strategies_misread"),
                    ("I, III, IV and V only", "growth_valued_without_wacc")], "I, III and IV only")
HARD.append(hq(id="30257-L3-03", deck="L3", topic="Leverage and accounting returns, MM without taxes, growth strategies", objective="Capital structure recap; growth and value",
    shape=CM, shape_class="concept MCQ", stem="Leverage, returns and growth: statements.", parts=[p],
    scheme=[f"[1] Steps: (1) I true (L3 slide 4: ROE 10% → 13%, range 3–23%); (2) II false: without taxes EV does not change; (3) III: 8% + 1,5 × 3% = {f(roe * 100, 1)}% — true; (4) IV true; (5) V false: growth creates value only if ROI > WACC; (6) I, III and IV.",
            "Second route: II and V both confuse higher accounting returns with value creation."],
    cites=[cite("L3", 5, "Financial leverage magnifies the volatility of accounting profitability"), cite("L3", 6, "does not affect enterprise (asset) value"),
           cite("L3", 29, "If ROI < WACC, an increase in the growth rate decreases value")],
    location="L3 slides 4–6 and 29–30", file=F_L3, groups=["L3A", "L3C"], minutes=3,
    notches=["near_true_statements", "extra_step", "cross_section"], hc_parts=[{"n": "1", "steps": 6, "concepts": 3}], units=["L3-U1", "L3-U2", "L3-U11", "L3-U12"]))

# ---- L3 B: two-stage DCF with a value-driver terminal value ---------------------------------------------------------------------
fc = [80.0, 95.0, 105.0]
nopat4, g2, ronic, wacc, nd = 150.0, 0.02, 0.12, 0.09, 400.0
pv_exp = sum(x / (1 + wacc) ** (i + 1) for i, x in enumerate(fc))
tv1 = nopat4 * (1 - g2 / ronic) / (wacc - g2)
ev1 = pv_exp + tv1 / (1 + wacc) ** 3
eq1 = ev1 - nd
tv2 = nopat4 / wacc
near(tv2, nopat4 * (1 - g2 / wacc) / (wacc - g2))
ev2 = pv_exp + tv2 / (1 + wacc) ** 3
eq2 = ev2 - nd
share2 = (tv2 / (1 + wacc) ** 3) / ev2
p1 = written("1", "Value the equity at 31/12/2026 with a two-stage asset-side DCF.", f"Equity value ≈ €{f(eq1)}m (EV {f(ev1)}; TV {f(tv1)} at end-2029).", 3,
             [("tv_from_last_fcfo", f"TV = 105 × 1,02 / 7% = {f(105 * 1.02 / 0.07)} → equity {f(pv_exp + 105 * 1.02 / 0.07 / 1.09 ** 3 - nd)}"),
              ("reinvestment_ignored", f"TV = 150 / 7% → equity {f(pv_exp + 150 / 0.07 / 1.09 ** 3 - nd)}"), ("tv_discounted_4_years", f"equity {f(pv_exp + tv1 / 1.09 ** 4 - nd)}")])
p2 = written("2", "The board argues that in the long run the return on new capital will fall to the WACC. Recompute the equity value and the share of EV that comes from the terminal value.",
             f"Equity value ≈ €{f(eq2)}m; the TV is {f(share2 * 100, 1)}% of EV. With RONIC = WACC, TV = NOPAT/WACC = {f(tv2)} whatever g.", 3,
             [("growth_still_counted", "keeping the 2% reinvestment at 12% RONIC")])
HARD.append(hq(id="30257-L3-04", deck="L3", topic="Two-stage DCF with a value-driver terminal value, then RONIC = WACC", objective="Two-stage DCF; terminal value; growth and value",
    shape=SP, shape_class="short problem", stem="Delta Srl expects FCFO of €80m, €95m and €105m in 2027, 2028 and 2029 (end of year). From 2030 it enters a steady state: NOPAT 2030 = €150m, long-term growth 2% (nominal GDP is expected to grow 3%), return on new invested capital 12%. WACC is 9%; net debt at 31/12/2026 is €400m. The 2026 FCFO (€70m) has already been generated.",
    parts=[p1, p2],
    scheme=[f"[1] Steps: (1) reinvestment rate = g / RONIC = 2%/12% = 16,7%; (2) FCFO 2030 = 150 × 83,3% = 125; (3) TV 2029 = 125 / (9% − 2%) = {f(tv1)}; (4) discount 3 years: {f(tv1 / 1.09 ** 3)}; (5–7) PV of 80, 95, 105 = {f(80 / 1.09)}, {f(95 / 1.09 ** 2)}, {f(105 / 1.09 ** 3)}; (8) EV = {f(ev1)}; (9) equity = EV − 400 = {f(eq1)}. g = 2% ≤ GDP 3%, so admissible.",
            f"[2] Steps: (1) RONIC = WACC; (2) reinvestment = 2%/9% = 22,2%; (3) FCFO 2030 = {f(150 * (1 - 0.02 / 0.09))}; (4) TV = {f(150 * (1 - 0.02 / 0.09))}/7% = {f(tv2)} = 150/9%; (5) PV TV = {f(tv2 / 1.09 ** 3)}; (6) EV = {f(ev2)}; (7) equity = {f(eq2)}; (8) TV share of EV = {f(share2 * 100, 1)}%.",
            "Second route for 2: with RONIC = WACC growth adds no value, so the TV is the no-growth value NOPAT/WACC.",
            "Not needed: the 2026 FCFO (already generated at the valuation date) and nominal GDP except as a check."],
    cites=[cite("L3", 25, "The TV growth rate should not exceed the growth rate of the economy as a whole"),
           cite("L3", 27, "In the LT, ROI should converge to WACC. This has a powerful consequence: value no longer depends on long term growth!"),
           cite("L3", 18, "a first stage, where T cash flows will be individually forecast and discounted one-by-one")],
    location="L3 slides 18–29 (two-stage DCF, terminal value, growth and value)", file=F_L3, groups=["L3B", "L3C"], minutes=18,
    notches=["chain", "what_if_followon", "extraneous_data", "cross_section"],
    hc_parts=[{"n": "1", "steps": 9, "concepts": 3}, {"n": "2", "steps": 8, "concepts": 2}], units=["L3-U6", "L3-U9", "L3-U11"]))

# ---- L4 A: implied MRP, beta from volatilities, Blume -----------------------------------------------------------------------------
yld = 0.02 + 0.025
rm = yld * 1.03 + 0.03
mrp = rm - 0.035
braw = 0.75 * 0.30 / 0.18
badj = braw * 2 / 3 + 1 / 3
kel6 = 0.035 + badj * mrp
near(braw, 1.25)
p1 = written("1", "Estimate the company's levered cost of equity.", f"Implied rM = {f(rm * 100, 2)}%, MRP = {f(mrp * 100, 2)}%; raw β = 1,25, Blume β = {f(badj, 3)}; kEL ≈ {f(kel6 * 100, 2)}%.", 3,
             [("no_blume", f"kEL with raw beta: {f((0.035 + braw * mrp) * 100, 2)}%"), ("dividend_yield_only", "buybacks left out of the implied return"),
              ("growth_not_applied", "yield not grown to next year's cash flows")])
HARD.append(hq(id="30257-L4-02", deck="L4", topic="Implied market risk premium, beta from volatilities, Blume's adjustment", objective="CAPM inputs: risk-free rate, MRP, top-down beta",
    shape=SP, shape_class="short problem",
    stem="You estimate Kappa SpA's cost of equity. The market index trades at 4.000; over the last twelve months it paid a dividend yield of 2,0% and a buyback yield of 2,5%. Cash returned to shareholders is expected to grow 3% next year and at that rate forever. The 10-year government bond yields 3,5% and the 3-month T-Bill 2,1%. Over the last two years of weekly returns, Kappa's volatility was 30%, the index's 18%, and their correlation 0,75 (R² 0,56).",
    parts=[p1],
    scheme=[f"[1] Steps: (1) total cash yield = 2,0% + 2,5% = 4,5%; (2) next year's cash = 4,5% × 1,03 = {f(yld * 1.03 * 100, 3)}% of the index; (3) implied rM = {f(yld * 1.03 * 100, 3)}% + 3% = {f(rm * 100, 3)}%; (4) MRP = rM − 10-year rF 3,5% = {f(mrp * 100, 3)}%; (5) cov = 0,75 × 30% × 18%; (6) raw β = cov/σM² = 0,75 × 30/18 = 1,25; (7) Blume: 1,25 × 2/3 + 1/3 = {f(badj, 4)}; (8) kEL = 3,5% + {f(badj, 4)} × {f(mrp * 100, 3)}% = {f(kel6 * 100, 3)}%.",
            "Second route for β: β = ρ × σi/σM directly = 1,25.",
            "Not needed: the T-Bill rate (the deck uses a 5–10 year maturity for rF) and R²."],
    cites=[cite("L4", 12, "Implied risk premium approach: rM as implied in estimates of CF returned to all shareholders in the index (dividends and buybacks), at consensus growth"),
           cite("L4", 17, "the estimated levered (\"raw\") beta after a number of years tends to converge (\"adj\") toward 1"), cite("L4", 9, "Medium long term: 5-10 years")],
    location="L4 slides 7–19 (CAPM, risk-free rate, MRP, top-down beta, Blume)", file=F_L4, groups=["L4A", "L4B"], minutes=10,
    notches=["extra_step", "extraneous_data", "chain"], hc_parts=[{"n": "1", "steps": 8, "concepts": 3}], units=["L4-U1", "L4-U2", "L4-U3", "L4-U4", "L4-U5"]))

# ---- L4 C: the tax rate (IRES/IRAP), market-value weights, two paths to kEL ---------------------------------------------------------
t_it = 0.24
Dm = 500 * 0.92 + 150 - 50
Em = 900.0
de = Dm / Em
bl = 0.9 * (1 + (1 - t_it) * de)
kel7 = 0.03 + bl * 0.06
dv = Dm / (Dm + Em)
w1 = kel7 * (1 - dv) + 0.055 * (1 - t_it) * dv
keu7 = 0.03 + 0.9 * 0.06
kel7b = keu7 + de * (keu7 - 0.055) * (1 - t_it)
w2 = kel7b * (1 - dv) + 0.055 * (1 - t_it) * dv
p1 = written("1", "Estimate the WACC relevering the industry beta and using the CAPM (option 2 in the slides).", f"WACC ≈ {f(w1 * 100, 2)}%: t = 24%, D = {f(Dm)} (bonds at market), D/E {f(de, 3)}, βL {f(bl, 3)}, kEL {f(kel7 * 100, 2)}%, kD 5,5%.", 3,
             [("irap_included_in_t", "t = 27,9%"), ("bonds_at_face_value", "D = 600"), ("accounting_kD_used", f"kD = 34/650 = {f(34 / 650 * 100, 2)}%")])
p2 = written("2", "Recompute the WACC with option 1 (unlevered cost of equity from the CAPM, then Modigliani & Miller's second proposition) and explain the difference.",
             f"WACC ≈ {f(w2 * 100, 2)}%: kEU {f(keu7 * 100, 2)}%, kEL {f(kel7b * 100, 2)}%. The two agree only if kD = rF; here kD 5,5% > rF 3%.", 3)
HARD.append(hq(id="30257-L4-03", deck="L4", topic="IRES versus IRAP, market-value weights and the two paths to kEL", objective="WACC inputs: tax rate, leverage at market values, cost of debt, final choices",
    shape=SP, shape_class="short problem",
    stem="Gamma SpA (Italy) is listed with a market capitalization of €900m. It has bonds with a face value of €500m trading at 92% of par (yield to maturity 5,5%), bank loans of €150m (book value), and cash of €50m. Last year's interest expense was €34m. It pays IRES of 24% on pre-tax profit and IRAP of 3,9% on EBIT plus personnel costs. The industry unlevered beta is 0,9, the risk-free rate 3% and the MRP 6%. Use net debt and the market cost of debt.",
    parts=[p1, p2],
    scheme=[f"[1] Steps: (1) relevant t = 24% (IRAP is levied on EBIT + personnel, so interest gives no IRAP shield); (2) bonds at market = 460; (3) net debt = 460 + 150 − 50 = {f(Dm)}; (4) D/E = {f(de, 4)}; (5) βL = 0,9 × (1 + 0,76 × {f(de, 4)}) = {f(bl, 4)}; (6) kEL = 3% + {f(bl, 4)} × 6% = {f(kel7 * 100, 3)}%; (7) weights D/V {f(dv * 100, 2)}%; (8) WACC = {f(kel7 * 100, 3)}% × {f((1 - dv) * 100, 2)}% + 5,5% × 0,76 × {f(dv * 100, 2)}% = {f(w1 * 100, 3)}%.",
            f"[2] Steps: (1) kEU = 3% + 0,9 × 6% = {f(keu7 * 100, 2)}%; (2) MM2: kEL = kEU + D/E × (kEU − kD) × (1 − t) = {f(kel7b * 100, 3)}%; (3) same weights; (4) WACC = {f(w2 * 100, 3)}%; (5) difference {f((w1 - w2) * 100, 2)} points; (6) cause: option 2's CAPM relevering treats debt as riskless (implicitly kD = rF); (7) they coincide only if kD = rF.",
            "Not needed: book equity and last year's interest expense (the accounting kD), except as distractors."],
    cites=[cite("L4", 28, "Second portion of income taxes: ~ equal to 3,9% of (EBIT + personnel expenses)"),
           cite("L4", 32, "Debt and equity should be measured with their market values"), cite("L4", 39, "Option 1 = Option 2 when kD = rF !")],
    location="L4 slides 27–39 (tax rate, leverage, cost of debt, final choices)", file=F_L4, groups=["L4C"], minutes=18,
    notches=["extra_classification", "extraneous_data", "what_if_followon", "cross_section"],
    hc_parts=[{"n": "1", "steps": 8, "concepts": 3}, {"n": "2", "steps": 7, "concepts": 2}], units=["L4-U9", "L4-U10", "L4-U11", "L4-U12"]))

# ---- L5 A: reorganize a balance sheet with borderline items --------------------------------------------------------------------------
A5 = {"PP&E": 620, "Goodwill": 140, "Trade receivables": 210, "Inventory": 180, "VAT receivable": 25, "Investment in associates": 60,
      "Non-core building held for sale": 45, "Cash (of which operating cash 10)": 90, "Marketable securities": 30}
L5 = {"Trade payables": 240, "Income tax payable": 35, "Dividends payable": 20, "Employee severance (pensions)": 40, "Restructuring provision (one-off)": 25,
      "Bank loans": 300, "Bonds": 250, "Lease liabilities": 80, "Minorities": 30, "Group equity": 380}
assert sum(A5.values()) == sum(L5.values()) == 1400
nwc5 = 210 + 180 + 25 + 10 - 240 - 35
core5 = nwc5 + 620 + 140
sa5 = 60 + 45 - 40 - 25
nd5 = 300 + 250 + 80 + 20 - 80 - 30
eq5 = 380 + 30
assert core5 + sa5 == nd5 + eq5
p1 = written("1", "Reorganize the balance sheet: noncash working capital, core capital employed, surplus assets net of other liabilities, net debt and equity.",
             f"NWC {nwc5}; core CE {core5}; surplus assets − other liabilities {sa5}; net capital employed {core5 + sa5} = net debt {nd5} + equity {eq5}.", 3,
             [("all_cash_as_excess", "operating cash left out of NWC"), ("dividends_payable_in_nwc", "dividends payable as operating"), ("leases_left_out", "lease liabilities not in net debt")])
HARD.append(hq(id="30257-L5-02", deck="L5", topic="Reorganizing a balance sheet with borderline items", objective="Reorganizing the balance sheet for valuation",
    shape=SP, shape_class="short problem", stem="Epsilon SpA's balance sheet is below (€m). €10m of the cash is needed for daily operations. The building is held for sale and not used in operations.",
    data="| Assets | €m | Liabilities and equity | €m |\n|---|---|---|---|\n" + "\n".join(f"| {a} | {av} | {l} | {lv} |" for (a, av), (l, lv) in zip(list(A5.items()) + [("", "")], L5.items())) + "\n| **Total** | **1.400** | **Total** | **1.400** |",
    parts=[p1],
    scheme=[f"[1] Steps: (1) NWC = receivables 210 + inventory 180 + VAT 25 + operating cash 10 − payables 240 − income tax payable 35 = {nwc5}; (2) fixed assets = 620 + 140 = 760; (3) core CE = {core5}; (4) surplus assets = associates 60 + building 45; (5) other liabilities = severance 40 + restructuring provision 25 → net {sa5}; (6) gross debt = 300 + 250 + 80 + dividends payable 20 = 650; (7) excess cash and securities = 80 + 30; (8) net debt = {nd5}; (9) equity incl. minorities = {eq5}; check {core5 + sa5} = {nd5 + eq5}.",
            "Second route: sources − uses must balance: 540 + 410 = 950 = 910 + 40."],
    cites=[cite("L5", 12, "Associates: non- consolidated equity investments"), cite("L5", 12, "\"Pensions\": employee termination indemnities"),
           cite("L5", 10, "There are tricky exceptions which should be assessed on a case by case basis")],
    location="L5 slides 7–13 (reorganizing the balance sheet)", file=F_L5, groups=["L5A", "L5D"], minutes=10,
    notches=["extra_classification", "extraneous_data", "chain"], hc_parts=[{"n": "1", "steps": 9, "concepts": 3}], units=["L5-U1", "L5-U2"]))

# ---- L5 B: reorganize an income statement ------------------------------------------------------------------------------------------------
ebitda = 1200 - (620 - 40) - (300 - 20 - 25) + (15 - 12)
ebit9 = ebitda - 60
ebt = 1200 - 620 - 300 + 15 + 8 - 30 + 4
near(ebit9 + (-25 + 12) + 8 - 26, ebt)
p1 = written("1", "Recurring EBITDA and its margin, recurring EBIT and NOPAT (24% tax).",
             f"Recurring EBITDA {ebitda} ({f(ebitda / 1200 * 100, 1)}% of sales); EBIT {ebit9}; NOPAT {f(ebit9 * 0.76)}.", 3,
             [("exceptionals_kept", "restructuring charge and building gain left in EBITDA"), ("da_not_added_back", "D&A inside COGS and SG&A left in")])
p2 = written("2", "Rebuild EBT from recurring EBIT in the reorganized layout, showing the exceptional items, associates and net interest.",
             f"EBT {ebt} = EBIT {ebit9} − exceptional items 13 (−25 + 12) + associates 8 − net interest 26.", 3)
HARD.append(hq(id="30257-L5-03", deck="L5", topic="From a by-function income statement to recurring EBITDA", objective="Reorganizing the income statement; the importance of EBITDA",
    shape=SP, shape_class="short problem",
    stem="Zeta SpA reports by function (€m): revenues 1.200; cost of goods sold 620 (including D&A of 40); SG&A 300 (including D&A of 20 and a one-off restructuring charge of 25); other operating income 15 (of which 12 is a gain on selling a non-core building); income from associates 8; interest expense 30; interest income 4; income taxes 70. Management's press release shows an 'EBITDA' of 400.",
    parts=[p1, p2],
    scheme=[f"[1] Steps: (1) COGS excl. D&A = 580; (2) SG&A excl. D&A and the one-off = 255; (3) recurring other income = 3; (4) recurring EBITDA = 1.200 − 580 − 255 + 3 = {ebitda}; (5) margin = {f(ebitda / 12, 2)}%; (6) D&A = 60; (7) EBIT = {ebit9}; (8) NOPAT = {ebit9} × 0,76 = {f(ebit9 * 0.76, 2)}. Management's 400 is not the recurring figure ('do not always trust published EBITDA').",
            f"[2] Steps: (1) exceptional items = −25 + 12 = −13; (2) associates +8 (below EBIT); (3) net interest = −30 + 4 = −26; (4) EBT = {ebit9} − 13 + 8 − 26 = {ebt}; (5) cross-check with the as-reported lines: 1.200 − 620 − 300 + 15 + 8 − 30 + 4 = {ebt}; (6) net income = {ebt} − 70 = {ebt - 70}; (7) effective tax rate {f(70 / ebt * 100, 1)}% differs from 24% because of the exceptionals.",
            "Not needed: management's 'EBITDA' of 400 (a trap)."],
    cites=[cite("L5", 16, "It's a non-GAAP metric: do not always trust published EBITDA!"), cite("L5", 16, "Income by associates, dividend income, non recurring gains and losses..")],
    location="L5 slides 14–19 (reorganizing the income statement)", file=F_L5, groups=["L5B"], minutes=16,
    notches=["extra_classification", "extraneous_data", "chain"],
    hc_parts=[{"n": "1", "steps": 8, "concepts": 2}, {"n": "2", "steps": 7, "concepts": 2}], units=["L5-U3"]))

# ---- L5 D: the bridge to equity, forwards and backwards ------------------------------------------------------------------------------------
bridge = {"net debt": -1400, "pension deficit": -150, "non-recurring long-term provision": -60, "minorities (market value)": -200,
          "preferred equity": -100, "associates (market value)": 250, "non-core real estate": 120}
eqv = 5000 + sum(bridge.values())
ps = eqv / 200
ev_mkt = 15 * 200 - sum(bridge.values())
disc = ev_mkt / 5000 - 1
p1 = written("1", "Equity value and value per share from the DCF.", f"Equity value = €{eqv}m; €{f(ps, 2)} per share.", 3,
             [("associates_subtracted", "associates treated as debt-like"), ("preferred_as_equity", "preferred equity left in common equity")])
p2 = written("2", "The shares trade at €15,00. What enterprise value does the market imply, and how far is it from the DCF?", f"Implied EV = €{ev_mkt}m, {f(disc * 100, 1)}% versus the DCF's 5.000.", 3)
HARD.append(hq(id="30257-L5-04", deck="L5", topic="Bridge to equity, and the enterprise value the market implies", objective="The bridge between enterprise value and equity value",
    shape=SP, shape_class="short problem",
    stem="An asset-side DCF gives Eta SpA an enterprise value of €5.000m. At the valuation date: net debt €1.400m; pension deficit €150m; a non-recurring long-term provision €60m; minorities €200m at market value (€90m book); preferred equity €100m; associates €250m at market value (€180m book); non-core real estate €120m. There are 200m common shares.",
    parts=[p1, p2],
    scheme=[f"[1] Steps: (1) start from EV 5.000; (2) − net debt 1.400; (3) − pension deficit 150 and − provision 60 (debt-like); (4) − minorities 200 and − preferred 100 (equity-like claims of others, at market value); (5) + associates 250 and + non-core real estate 120; (6) equity = {eqv}; (7) per share = {eqv} / 200 = {f(ps, 2)}.",
            f"[2] Steps: (1) market cap = 15 × 200 = 3.000; (2) add back debt-like items 1.610; (3) add equity-like claims 300; (4) subtract associates and real estate 370; (5) implied EV = {ev_mkt}; (6) versus 5.000: {f(disc * 100, 1)}%; (7) the market prices the operations about {f(-disc * 100, 1)}% below the DCF.",
            "Not needed: book values of minorities and associates (use market values)."],
    cites=[cite("L5", 27, "Moving from EV to EqV and vice-versa requires the \"bridge\" of other remaining balance sheet items"),
           cite("L5", 28, "Other debt-like claims might include long term nonrecurring provisions")],
    location="L5 slides 26–28 (the bridge to equity)", file=F_L5, groups=["L5D"], minutes=16,
    notches=["working_backwards", "extraneous_data", "extra_classification"],
    hc_parts=[{"n": "1", "steps": 7, "concepts": 2}, {"n": "2", "steps": 7, "concepts": 2}], units=["L5-U6"]))

# ================================================================================================
# SECTIONS, UNITS, EXISTING QUESTIONS, LEDGER
# ================================================================================================
def U(id, section, title, where, examinable=True, reason=None):
    u = {"id": id, "section": section, "title": title, "where": where, "examinable": examinable}
    if reason:
        u["reason"] = reason
    return u


SECTIONS = {
    "L12": [{"id": "L12A", "title": "Users and uses; the Kellanova example; fundamental skills"}, {"id": "L12B", "title": "Approaches and methods (DCF, relative, economic profit, asset-based)"},
            {"id": "L12C", "title": "Bases of value"}, {"id": "L12D", "title": "Value and uncertainty"}],
    "L3": [{"id": "L3A", "title": "Capital structure recap: MM, APV, equity-side DCF, WACC"}, {"id": "L3B", "title": "Two-stage DCF in practice and the terminal value"},
           {"id": "L3C", "title": "Growth and value"}],
    "L4": [{"id": "L4A", "title": "CAPM inputs: risk-free rate and market risk premium"}, {"id": "L4B", "title": "Beta: top-down, Blume, determinants, Hamada, bottom-up"},
           {"id": "L4C", "title": "Tax rate, leverage, cost of debt and final choices"}],
    "L5": [{"id": "L5A", "title": "Reorganizing the balance sheet"}, {"id": "L5B", "title": "Reorganizing the income statement"},
           {"id": "L5C", "title": "Cash flows for valuation"}, {"id": "L5D", "title": "The bridge to equity"}],
    "L6": [{"id": "L6", "title": "Workbook exercise selection (2.3, 2.5, 2.6, 3.8, 4.1, 4.9)"}],
}
UNITS = {
    "L12": [U("L12-U1", "L12A", "Users and uses of valuation (banks, advisors, PE/VC, strategic investors, appraisers); equity research, M&A report, fairness opinion", "slides 3–8"),
            U("L12-U2", "L12A", "Introductory example: Mars's bid for Kellanova (market value vs offer)", "slides 10–11"),
            U("L12-U3", "L12A", "Fundamental skills and the 'glue'", "slides 13–14"),
            U("L12-U4", "L12B", "Three general approaches: income, market, cost", "slide 16"),
            U("L12-U5", "L12B", "Specific methods discussed in the course", "slides 17–18"),
            U("L12-U6", "L12B", "DCF: general framework, inputs, steps, pros and cons (Netflix report)", "slides 20–27"),
            U("L12-U7", "L12B", "What we will learn on DCF: sum of the parts, NPVGO, acquisition value, APV", "slides 28–29"),
            U("L12-U8", "L12B", "Relative valuation: basis, inputs, pros and cons", "slides 31–33"),
            U("L12-U9", "L12B", "Economic profit models (EVA, residual income)", "slide 35"),
            U("L12-U10", "L12B", "Asset-based methods", "slide 37"),
            U("L12-U11", "L12C", "Price versus value; bases of value", "slides 39–40"),
            U("L12-U12", "L12C", "Market value", "slide 41"),
            U("L12-U13", "L12C", "Investment value; the apartment example", "slides 42–45"),
            U("L12-U14", "L12D", "Predictability, the risk process, scenarios", "slides 47–48"),
            U("L12-U15", "L12D", "Static vs dynamic standpoint; value of a new venture; representing risk in CF or rate", "slides 49–53"),
            U("L12-U0", "L12A", "Tables of contents", "slides 2, 9, 12, 15, 19, 30, 34, 36, 38, 46", False, "Navigation only.")],
    "L3": [U("L3-U1", "L3A", "Accounting returns and leverage without taxes (ROE formula)", "slides 4–5"),
           U("L3-U2", "L3A", "MM without taxes: leverage does not change EV", "slide 6"),
           U("L3-U3", "L3A", "MM with taxes: tax shields, VTS = D × t, APV", "slides 7–11"),
           U("L3-U4", "L3A", "MM 2: levered cost of equity; equity-side DCF", "slides 12–13"),
           U("L3-U5", "L3A", "WACC and the asset-side DCF; equivalence of the three models", "slides 14–16"),
           U("L3-U6", "L3B", "Two-stage DCF formulas (asset, equity, APV)", "slides 18–19"),
           U("L3-U7", "L3B", "Practical step-by-step: business plan, WACC, TV assumptions; CF definitions with growth", "slides 20–21"),
           U("L3-U8", "L3B", "Netflix case: a shortened 5-year first stage vs Credit Suisse's long stage", "slides 22–23", False,
             "Illustrative case: its figures are not examinable on their own; the method it illustrates is unit L3-U6 (two-stage DCF)."),
           U("L3-U9", "L3B", "Terminal value growth rules (≤ nominal GDP; can be negative; inflationary)", "slide 25"),
           U("L3-U10", "L3C", "g = ROI × reinvestment rate; FCFO = NOPAT × (1 − g/ROI)", "slides 26–27"),
           U("L3-U11", "L3C", "When growth creates value (ROI vs WACC); sensitivity", "slides 27–29"),
           U("L3-U12", "L3C", "Growth strategies that create value", "slide 30"),
           U("L3-U0", "L3A", "Tables of contents", "slides 2, 17, 24", False, "Navigation only.")],
    "L4": [U("L4-U1", "L4A", "Discount rates in the three DCF models (recap)", "slides 4–5"),
           U("L4-U2", "L4A", "CAPM and the risk-free rate (maturity, country, sample)", "slides 7–10"),
           U("L4-U3", "L4A", "Market risk premium: historical, implied, Damodaran, Fernandez", "slides 11–14"),
           U("L4-U4", "L4B", "Top-down beta: regression, sample, R²", "slides 15–16, 18–19"),
           U("L4-U5", "L4B", "Blume's adjustment", "slide 17"),
           U("L4-U6", "L4B", "Beta determinants: financial and operating leverage", "slides 20–21"),
           U("L4-U7", "L4B", "Hamada formula (unlever/relever)", "slide 22"),
           U("L4-U8", "L4B", "Bottom-up beta: steps and advantages", "slides 23–26"),
           U("L4-U9", "L4C", "The tax rate: statutory vs effective; IRES/IRAP quiz", "slides 27–29"),
           U("L4-U10", "L4C", "Leverage: standpoint, market values, total vs net debt", "slides 30–33"),
           U("L4-U11", "L4C", "Cost of debt: market YTM, rating-based (synthetic), accounting, contractual", "slides 35–37"),
           U("L4-U12", "L4C", "Two paths to kEL; option 1 = option 2 when kD = rF", "slide 39"),
           U("L4-U0", "L4A", "Acronyms, tables of contents, notes, references", "slides 2–3, 6, 34, 38, 40–43", False, "Navigation and reference only.")],
    "L5": [U("L5-U1", "L5A", "Why reorganize: operating, financing and residual items", "slides 4–5"),
           U("L5-U2", "L5A", "Reorganized balance sheet: noncash WC, core CE, net debt, surplus assets and other liabilities (Campari)", "slides 7–13"),
           U("L5-U3", "L5B", "Reorganized income statement; EBITDA and its limits (Campari)", "slides 15–19"),
           U("L5-U4", "L5C", "Cash-flow format for valuation (EBIT → FCFO → FCFE → change in cash)", "slides 21–23"),
           U("L5-U5", "L5C", "FCFO and FCFE defined and linked to BS/IS", "slides 24–25"),
           U("L5-U6", "L5D", "The bridge from EV to equity value", "slides 27–28"),
           U("L5-U0", "L5A", "Acronyms, tables of contents, notes", "slides 2–3, 6, 14, 20, 26, 29–32", False, "Navigation and reference only.")],
    "L6": [U("L6-U2.3", "L6", "Workbook 2.3 (Omega: reorganize the BS)", "slide 2"), U("L6-U2.5", "L6", "Workbook 2.5 (Square Pizza: FCFO)", "slide 3"),
           U("L6-U2.6", "L6", "Workbook 2.6 (Full House: FCFE)", "slide 4"), U("L6-U3.8", "L6", "Workbook 3.8 (Champagne: WACC)", "slide 5"),
           U("L6-U4.1", "L6", "Workbook 4.1 (EV at the valuation date)", "slide 6"), U("L6-U4.9", "L6", "Workbook 4.9 (Solar Beam: equity DCF)", "slide 7")],
}
EXISTING_UNITS = {"30257-L12-01": ["L12-U11", "L12-U12", "L12-U13"], "30257-L3-01": ["L3-U3", "L3-U4", "L3-U5"], "30257-L3-02": ["L3-U10", "L3-U11"],
                  "30257-L4-01": ["L4-U7", "L4-U8", "L4-U11"], "30257-L5-01": ["L5-U2", "L5-U4", "L5-U6"], "30257-L6-01": ["L6-U4.1", "L3-U6", "L5-U4"]}
EXISTING_GROUPS = {"30257-L12-01": ["L12C"], "30257-L3-01": ["L3A"], "30257-L3-02": ["L3C"], "30257-L4-01": ["L4B", "L4C"],
                   "30257-L5-01": ["L5C", "L5A", "L5D"], "30257-L6-01": ["L6", "L3B"]}
# extra shape for this course's Hard concept MCQs (PROXY, scored from the AY 24-25 / 26-27 mocks: MCQs take 1-2 steps)
MCQ_SHAPE = {"exam": {"n": 11, "steps": {"median": 1.5, "range": [1, 3]}, "concepts_combined": {"median": 1, "range": [1, 2]}},
             "target": {"steps_min": 3, "concepts_min": 2}}


def D(file, item, decision, ids=None, reason=""):
    return {"file": file, "item": item, "decision": decision, "ids": ids or [], "reason": reason}


HELD_MULT = "Multiples, M&A, rights issues and ESG are lectures 9-15 (from 7 Oct 2026); their decks are not in the folder yet. Held until they arrive."
NONATT = "Only in the non-attending version of the exam (research readings); the course is set up for the attending exam."
WB_WAIT = "Waiting for readable page images: Will is splitting the scanned workbook so each problem can be copied word for word (decided 2026-09-24)."
LEDGER = [
    D("syllabus (10).pdf", "Syllabus 2026-27", "used", [], "Exam format, materials (book, workbook), Financial Modeling excluded for attending students."),
    D("30257 Corporate Valuation - AY 26-27 - CVW2 Required Problems - v1 (1).pdf", "Required-problems grid", "used", [], "Green/yellow/red per problem; recorded in banks/intake_30257_notes.md."),
    D(F_M26, "MCQ 1-8", "included", ["30257-L5-10", "30257-L5-11", "30257-L5-12", "30257-L4-10", "30257-L4-11", "30257-L12-10", "30257-L3-10", "30257-L3-11"]),
    D(F_M26, "MCQ 9-13 (EV/sales, forward multiple, M&A x2, carbon beta)", "held", [], HELD_MULT),
    D(F_M26, "Open question 1 (tax shields in APV and asset-side DCF)", "included", ["30257-L3-12"]),
    D(F_M26, "Open question 2 (forward P/E breakdown)", "held", [], HELD_MULT),
    D(F_M26, "Problem 1 (FCFO)", "included", ["30257-L5-13"]),
    D(F_M26, "Problem 2 (EV/EBITDA and P/E valuation)", "held", [], HELD_MULT + " Note: the PDF's P/E solution (3.189,1) is an arithmetic slip; the solutions workbook gives 2.689,1."),
    D(F_M26, "Non-attending MCQs 1-6", "excluded", [], NONATT),
    D("Reference/.../30257 Corporate Valuation AY 24-25 - Mock Exam v1.pdf", "Questions 1-17", "duplicate", ["30257-L3-12", "30257-L5-13"], "Same items as the AY 26-27 mock except MCQ 16 (TERP, held: rights issues)."),
    D(F_M24X, "Solutions workbook", "key_source", ["30257-L5-10", "30257-L5-11", "30257-L5-12", "30257-L4-10", "30257-L4-11", "30257-L12-10", "30257-L3-10", "30257-L3-11", "30257-L3-12", "30257-L5-13"]),
    D(F_V2, "Open questions 1-2, problems 3-4, MCQ 1-4, 6, 7, 11-13", "duplicate", [], "Same as the AY mocks (kept once)."),
    D(F_V2, "MCQ 5 (Facebook IPO) and MCQ 8 (forward +2 multiple)", "held", [], HELD_MULT),
    D(F_V2, "MCQ 9 (supermarket working capital)", "included", ["30257-L5-14"], "No key in the source; solved twice."),
    D(F_V2, "MCQ 10 (young business, probability of success)", "included", ["30257-L12-11"], "No key in the source; solved twice; flagged for a check."),
    D(F_V2X, "Solutions workbook (quantitative MCQs)", "key_source", [], "Keys for MCQs 4, 6, 8 (all duplicates or held)."),
    D("Reference/Past Exams and Mock Exams/Mock exams/Valuation - Mock Exam v2.docx", "Whole file", "duplicate", [], "Word version of the v2 mock."),
    D(F_J19, "Q1 (market risk premium methods)", "included", ["30257-L4-12"]),
    D(F_J19, "Q2 (scenario vs sensitivity analysis)", "held", [], "Scenario analysis is not in the L1-6 decks (workbook 2.21 on scenarios is marked out of scope). Held until a deck covers it."),
    D(F_J19, "Q3 (carbon risk), Q4 (M&A value creation), Q5 (peer group), Q7 (rights issue/TERP)", "held", [], HELD_MULT),
    D(F_J19, "Q6 (enterprise DCF, target leverage)", "included", ["30257-L3-13"], "No key in the source; solved with Workbook 4.3's official method; flagged."),
    D(F_J19, "Q8 (levered and unlevered cost of equity from peers)", "included", ["30257-L4-13"], "No key in the source; same table as Workbook 3.5 (official method)."),
    D(F_J19, "Q9 (APV)", "included", ["30257-L3-14"]),
    D(F_J19, "Q10 (FCFO, FCFE, total cash flow)", "included", ["30257-L5-15"], "Check closes: total cash flow = change in excess cash."),
    D(F_J23, "Q2 essay (FCFO)", "included", ["30257-L5-18"]),
    D(F_J23, "Q5 essay (tax shields in three DCF models)", "included", ["30257-L3-16"]),
    D(F_J23, "Q6 (WACC bounds)", "included", ["30257-L4-17"], "Options photographed in the BSc paper; answer from this paper."),
    D(F_J23, "Q8, Q11, Q12, Q14, Q17 (MCQs; options not photographed)", "included", ["30257-L12-12", "30257-L4-14", "30257-L5-16", "30257-L3-15", "30257-L5-17"], "Kept as short-answer questions with Blackboard's correct answer (decided 2026-09-24)."),
    D(F_J23, "Q4, Q7, Q9, Q10, Q13, Q15, Q16", "held", [], HELD_MULT),
    D(F_J23, "Q1, Q3 (no photograph)", "not_a_question", [], "No photograph of these questions; Q3 is known only from the typed index (Old Exam 1)."),
    D(F_OLD1, "Typed index of the January 2023 exam", "included_adapted", ["30257-L3-17"], "Q3 taken from the index (adapted, flagged); the rest duplicates the photographs."),
    D(F_BSC, "Q1, Q4, Q5-Q11", "included", ["30257-L5-19", "30257-L4-15", "30257-L12-13", "30257-L5-21", "30257-L5-22", "30257-L3-18", "30257-L3-19", "30257-L4-16", "30257-L4-17"], "No answers recorded in the source except via the January 2023 paper for Q11; others solved twice."),
    D(F_BSC, "Q3 (FCFO from forecast statements)", "duplicate", ["30257-L5-18"], "The January 2023 essay with every figure doubled (answer 25,9 = 2 × 12,95); kept the January 2023 version."),
    D(F_BSC, "Q2 (two methods to estimate the equity risk premium)", "duplicate", ["30257-L4-12"], "The January 2019 version ('explain the methods') is the harder form; kept that one."),
    D(F_BSC, "Q12 (normalized P/E), Q13 (P/BV), Q15 (rights issue), Q16 (carbon factor), Q17 (SPACs)", "held", [], HELD_MULT),
    D(F_BSC, "Q14", "not_a_question", [], "Not photographed."),
    D("Reference/Clean/BSc - Past Exam - CLEAN PAPER.pdf", "Retyped BSc paper", "duplicate", [], "Checked word for word against the photographs on 2026-09-24; the photographs are the source."),
    D("Reference/Clean/Valuation - Past paper 1.pdf", "38 photographed pages", "not_read", [], "7 MB of photographs; the Drive connection drops on files this large. Please re-upload it split or compressed."),
    D(F_L6, "Workbook 2.3, 2.5, 2.6, 3.8, 4.9 (slide text)", "included", ["30257-L6-10", "30257-L6-11", "30257-L6-12", "30257-L6-13", "30257-L6-14"]),
    D(F_L6, "Workbook 4.1 (slide text)", "duplicate", ["30257-L3-11"], "Same numbers as AY 26-27 mock MCQ 8 (€ thousand in the workbook)."),
    D("CV Workbook Chapter 1-4.pdf", "Ch. 1-4 required (green) and related (yellow) problems not on the L6 slides", "held", [], WB_WAIT),
    D("CV Workbook Chapter 1-4.pdf", "Ch. 2 problems 21-22, Ch. 4 problems 18-20", "excluded", [], "Marked out of scope (red) on the Required Problems grid."),
    D("CV Workbook Chapters 5-6.pdf", "Ch. 5 (multiples) and Ch. 6 (M&A) problems", "held", [], HELD_MULT + " Also needs readable page images."),
    D("Corporate Valuation Workbook II - Solutions/CVW2 - Ch. 1-6", "Solutions workbooks", "key_source", ["30257-L6-10", "30257-L6-11", "30257-L6-12", "30257-L6-13", "30257-L6-14"], "Official keys; also confirm the method for Jan 2019 Q6 (4.3) and Q8 (3.5)."),
    D("Corporate Valuation Workbook II - Solutions/CVW2 - Ch. 7-15", "Solutions workbooks", "not_examinable", [], "Chapters 7-15 are out of scope or have no required problems (grid)."),
    D("Book 2026-2027.pdf", "Textbook", "not_a_question", [], "Reference reading; no exercises."),
    D("Slides/Corporate Valuation - C31 - Lectures 7-8 - Intro to Financial Modeling - v10.pdf", "Deck", "not_examinable", [], "Excluded for attending students by the syllabus."),
    D("Mock Exam/30257 Lecture 4, Lecture 5, L1-2, L3 DCF (PAPER, MARK SCHEME)", "Whole files", "excluded", [], "Written by Claude in earlier chats: not evidence."),
    D("Claude outputs/30257 Chapters 1-4 Skill cards - RemNote deck.md", "Whole file", "excluded", [], "Claude-written flashcards: not evidence."),
    D("Reference/Corporate Valuation - Overview (L1 & 2).xmind", "Mind map", "not_a_question", [], "Your notes; no questions."),
    D(F_L12, "Deck", "units", [], "16 units; 15 examinable."), D(F_L3, "Deck", "units", [], "13 units; 11 examinable."),
    D(F_L4, "Deck", "units", [], "13 units; 12 examinable."), D(F_L5, "Deck", "units", [], "7 units; 6 examinable."), D(F_L6, "Deck", "units", [], "6 units, all examinable."),
]
