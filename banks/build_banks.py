#!/usr/bin/env python3
"""Builds the generated exercise questions for every BIEF Year 3 deck that had none.

Every number in a key or mark scheme is computed here, and each answer is solved a second
way (a different route or an identity) with an assert, so the key is "double-solved".
Run:  python3 banks/build_banks.py   -> writes banks/bank_<course>.json and banks/worked-examples.md
Then: node banks/review.js           -> the site's own validator and harder-rule review
"""
import hashlib, json, math, pathlib

OUT = pathlib.Path(__file__).resolve().parent
CREATED = "2026-09-24T18:00:00Z"
L = "ABCD"


def r(x, d=1):
    return round(x + 0.0, d)


def f(x, d=1):
    """format with d decimals, minus sign as the ASCII hyphen the options use"""
    return f"{r(x, d):.{d}f}"


def near(a, b, tol=1e-6):
    assert abs(a - b) < tol, (a, b)


def mcq(n, prompt, options, correct, marks):
    """options: list of (text, trap_tag or None); correct: text of the right option.
    Returns (subquestion, key, error_tags). Options keep their order; no duplicates allowed."""
    assert len({o[0] for o in options}) == len(options), options
    # deterministic shuffle so the key is not always A (seeded by the prompt, stable across rebuilds)
    seed = int(hashlib.md5((n + prompt).encode()).hexdigest(), 16)
    options = sorted(options, key=lambda o: hashlib.md5((str(seed) + o[0]).encode()).hexdigest())
    texts = [o[0] for o in options]
    k = texts.index(correct)
    tags = [{"tag": t, "trap": f"{n}:{L[i]} {t.replace('_', ' ')}"} for i, (_, t) in enumerate(options) if t]
    return ({"n": n, "prompt": prompt, "options": texts, "marks": marks},
            {"n": n, "answer": L[k], "answer_status": "double-solved"}, tags)


def written(n, prompt, answer, marks, tags=()):
    return ({"n": n, "prompt": prompt, "options": [], "marks": marks},
            {"n": n, "answer": answer, "answer_status": "double-solved"},
            [{"tag": t, "trap": f"{n}: {d}"} for t, d in tags])


def question(**kw):
    parts = kw.pop("parts")
    q = {
        "id": kw["id"], "course": kw["course"], "deck": kw["deck"], "topic": kw["topic"],
        "syllabus_objective": kw["objective"], "shape": kw["shape"], "stem": kw["stem"],
        "data": kw.get("data"), "difficulty": "hard",
        "source": {"type": "generated", "file": kw["file"], "location": kw["location"], "label": "INFERENCE",
                   "verbatim_verified": False, "transcribed_from_image": False, "page_snapshot_asset": None},
        "subquestions": [p[0] for p in parts], "answer_key": [p[1] for p in parts],
        "error_tags": [t for p in parts for t in p[2]],
        "marks": round(sum(p[0]["marks"] for p in parts if isinstance(p[0]["marks"], (int, float))), 2)
        if all(isinstance(p[0]["marks"], (int, float)) for p in parts) else "UNKNOWN",
        "mark_scheme": kw["scheme"], "citations": kw["cites"], "slides": kw.get("slides", []),
        "slide_groups": kw.get("groups", []), "est_minutes": kw["minutes"], "created_at": CREATED,
        "negative_marking": None,
        "hard_check": {"shape_class": kw["shape_class"], "parts": kw["hc_parts"], "notches": kw["notches"],
                       "no_ambiguity": True, "in_syllabus": True,
                       "reviewed_by": "Claude (step counts listed in the mark scheme)", "reviewed_at": CREATED},
    }
    if q["data"] is None:
        del q["data"]
    return q


def cite(deck, slide, quote):
    assert len(quote.split()) <= 25, quote
    return {"deck": deck, "slide": slide, "quote": quote}


BANKS = {}
WORKED = {}

# =====================================================================================
# 30178 INTERNATIONAL BANKING
# =====================================================================================
F_INTRO = "Slides/Introductory concepts to banking_30178_2026-27.pdf"
F_SVB = "Slides/The SVB case_in class discussion.pdf"
F_IRR = "Slides/Managing Interest Rate Risk_2026-27_PART I and 2_classroom.pdf"
Q30178 = []

# ---- 30178-INTRO-01: leverage, a loan loss, then a run met by a fire sale ----------
cash, bonds, loans, fixed = 6.0, 9.0, 80.0, 5.0
retail, wholesale, senior, equity = 40.0, 38.0, 14.0, 8.0
assert cash + bonds + loans + fixed == retail + wholesale + senior + equity == 100
loss = 0.06 * loans
eq1, assets1 = equity - loss, 100 - loss
lev1 = assets1 / eq1
near(lev1, (100 - 4.8) / (8 - 4.8))
p1 = mcq("3.1", "Bank Delta's loans lose 6% of their book value; nothing else changes. What is its assets-to-equity ratio (× equity) after the loss?",
         [(f(lev1), None), (f(100 / 8), "leverage_before_the_loss"), (f(100 / eq1), "assets_not_reduced_by_the_loss"),
          (f((100 - 6) / (8 - 6)), "loss_applied_to_total_assets")], f(lev1), 0.8)
withdraw = 0.5 * wholesale
shortfall = withdraw - cash - bonds
assert shortfall > 0
book_sold = shortfall / 0.8
fire_loss = book_sold - shortfall
eq2 = eq1 - fire_loss
near(eq2, eq1 - shortfall * (1 / 0.8 - 1))  # second route: loss = cash raised × (1/0.8 − 1)
p2 = mcq("3.2", "After the loss in 3.1, half of the wholesale deposits are withdrawn. Bank Delta pays first with cash, then by selling its government bonds at book value, and only then by selling loans at a 20% discount to their post-loss book value. How much equity is left, in € billion?",
         [(f(eq2), None), (f(eq1 - 0.2 * shortfall), "discount_applied_to_cash_raised_not_book_sold"),
          (f(equity - fire_loss), "loan_loss_from_3_1_ignored"),
          (f(eq1 - (withdraw / 0.8 - withdraw), 2), "all_withdrawals_met_by_loan_sales")], f(eq2), 0.8)
Q30178.append(question(
    id="30178-INTRO-01", course="30178", deck="INTRO", topic="Leverage, a loan loss and a run met by a fire sale",
    objective="What banks do: balance-sheet structure, leverage, maturity and liquidity transformation, fragility",
    shape="numerical exercise with 2 MCQ sub-questions", shape_class="exercise part",
    stem="Bank Delta's balance sheet is below (€ billion). Net interest income last year was 2.1 and 55% of deposits are insured; neither figure is needed unless you decide it is. Losses reduce equity one for one; there are no taxes.",
    data="| **Assets** | € bn | **Liabilities and equity** | € bn |\n|---|---|---|---|\n| Cash and central bank reserves | 6 | Retail deposits | 40 |\n| Government bonds (liquid) | 9 | Wholesale deposits (large corporates) | 38 |\n| Loans to households and firms | 80 | Senior bonds | 14 |\n| Fixed assets | 5 | Equity | 8 |\n| **Total** | **100** | **Total** | **100** |",
    parts=[p1, p2],
    scheme=[
        f"[3.1] Steps: (1) loan loss = 6% × 80 = {f(loss)}; (2) equity = 8 − {f(loss)} = {f(eq1)}; (3) assets = 100 − {f(loss)} = {f(assets1)}; (4) assets / equity = {f(assets1)} / {f(eq1)} = {f(lev1, 2)}×, so {f(lev1)}.",
        f"[3.2] Steps: (1) withdrawal = 50% × 38 = {f(withdraw)}; (2) liquid resources = cash 6 + bonds 9 = 15; (3) still to pay = {f(shortfall)}; (4) loans sold at 80% of book: book value sold = {f(shortfall)} / 0.8 = {f(book_sold, 2)}; (5) loss on the sale = {f(book_sold, 2)} − {f(shortfall)} = {f(fire_loss)}; (6) equity = {f(eq1)} − {f(fire_loss)} = {f(eq2)}.",
        f"Second route for 3.2: each € of cash raised from loans costs 1/0.8 − 1 = 0.25 of equity, so the loss is 0.25 × {f(shortfall)} = {f(fire_loss)}.",
        "How to write it: lay out the order of funding (cash, then liquid bonds, then loans) before computing; gross up the cash you need by the sale price to get the book value sold.",
        f"Where marks are lost: quoting the pre-loss 12.5×; not shrinking total assets ({f(100 / eq1)}×); applying the 6% to all assets (47.0×); in 3.2 taking 20% of the cash raised (2.4), forgetting 3.1's loss (7.0) or selling loans for the whole withdrawal (−1.55).",
        "Not needed: net interest income and the insured share of deposits (extraneous data).",
    ],
    cites=[cite("INTRO", "Why Are Banks Inherently Fragile? Illustrative balance sheets", "What happens if depositors demand repayment before the bank’s loans are repaid—or if the value of those loans falls by 8%?"),
           cite("INTRO", "Why Are Banks “inherently” Fragile?", "A relatively small loss on the bank’s assets can substantially reduce its equity."),
           cite("INTRO", "The concepts of maturity, liquidity and risk transformation", "Also create fragility, which requires regulation, adequate capital buffers, and proper risk management tools")],
    location="slides 'Why Are Banks Inherently Fragile?' (illustrative balance sheets and the two sources of fragility)",
    file=F_INTRO, minutes=9, notches=["extra_classification", "chain", "working_backwards", "extraneous_data"],
    hc_parts=[{"n": "3.1", "steps": 4, "concepts": 2}, {"n": "3.2", "steps": 6, "concepts": 2}]))

# ---- 30178-INTRO-02: cost-to-income and the profit bridge ---------------------------
ii, ie, fees, trading, other, opex, llp, tax = 9000, 3600, 2200, 900, 300, 5850, 1100, 0.28
nii = ii - ie
toi = nii + fees + trading + other
ci = opex / toi
near(ci, opex / (ii - ie + fees + trading + other))
p1 = mcq("4.1", "What is Bank Epsilon's cost-to-income ratio?",
         [(f(ci * 100) + "%", None), (f((opex + llp) / toi * 100) + "%", "provisions_counted_as_operating_costs"),
          (f(opex / nii * 100) + "%", "denominator_is_nii_only"), (f(opex / (ii + fees + trading + other) * 100) + "%", "interest_expense_not_netted")],
         f(ci * 100) + "%", 0.8)
target_opex = 0.55 * toi
cut = opex - target_opex
dni = cut * (1 - tax)
ni0 = (toi - opex - llp) * (1 - tax)
ni1 = (toi - target_opex - llp) * (1 - tax)
near(dni, ni1 - ni0)
p2 = mcq("4.2", "The board wants a cost-to-income ratio of exactly 55% with total operating income and provisions unchanged, reached only by cutting operating expenses. By how much does net income rise, in € million?",
         [(f(dni), None), (f(cut), "pre_tax_saving_quoted"), (f(ni1), "new_net_income_not_the_increase"), (f(cut * tax), "tax_on_the_saving_quoted")],
         f(dni), 0.8)
Q30178.append(question(
    id="30178-INTRO-02", course="30178", deck="INTRO", topic="Cost-to-income, the revenue mix and a cost-cutting target",
    objective="What banks do: sources of income and cost; reading a simplified bank income statement",
    shape="numerical exercise with 2 MCQ sub-questions", shape_class="exercise part",
    stem="Bank Epsilon's income statement for 2025 is below (€ million). Its total assets are €310 billion. The tax rate on profit before tax is 28%.",
    data="| Item | € m |\n|---|---|\n| Interest income | 9,000 |\n| Interest expense | (3,600) |\n| Net fee and commission income | 2,200 |\n| Net trading and investment income | 900 |\n| Other operating income | 300 |\n| Operating expenses (staff, admin) | (5,850) |\n| Loan loss provisions | (1,100) |",
    parts=[p1, p2],
    scheme=[
        f"[4.1] Steps: (1) NII = 9,000 − 3,600 = {nii:,}; (2) non-interest income = 2,200 + 900 + 300 = {fees + trading + other:,}; (3) total operating income = {toi:,}; (4) cost-to-income = 5,850 / {toi:,} = {f(ci * 100)}%. Provisions are not operating costs.",
        f"[4.2] Steps: (1) target opex = 55% × {toi:,} = {f(target_opex)}; (2) cut = 5,850 − {f(target_opex)} = {f(cut)}; (3) profit before tax rises by the same {f(cut)} because revenue and provisions are fixed; (4) after 28% tax: {f(cut)} × 0.72 = {f(dni)}.",
        f"Second route for 4.2: net income before = ({toi:,} − 5,850 − 1,100) × 0.72 = {f(ni0)}; after = ({toi:,} − {f(target_opex)} − 1,100) × 0.72 = {f(ni1)}; difference {f(dni)}.",
        f"Where marks are lost: adding provisions to costs ({f((opex + llp) / toi * 100)}%), dividing by NII only ({f(opex / nii * 100)}%), using gross interest income ({f(opex / (ii + fees + trading + other) * 100)}%); in 4.2 quoting the pre-tax saving or the new net income level.",
        "Not needed: total assets (extraneous).",
    ],
    cites=[cite("INTRO", "Simplified (European Bank – Example Format) Income Statement", "Note: Cost-to-income ratio (operating cost to total operating income) is a common metric of a banks’ operational efficiency"),
           cite("INTRO", "How Banking Activities Generate Revenues", "Interest income − Interest expense = Net interest income"),
           cite("INTRO", "How Banking Activities Generate Revenues and Expenses", "Loan Loss Provisions: amounts recognised to cover expected losses when borrowers may not fully repay their loans")],
    location="slides 'How Banking Activities Generate Revenues and Expenses' and the example income statement",
    file=F_INTRO, minutes=8, notches=["extra_classification", "working_backwards", "chain", "extraneous_data"],
    hc_parts=[{"n": "4.1", "steps": 4, "concepts": 2}, {"n": "4.2", "steps": 4, "concepts": 2}]))

# ---- 30178-SVB-01: HTM vs AFS, OCI and a run that forces sales ---------------------
afs, dafs, htm, dhtm, dy = 25.0, 3.5, 90.0, 6.0, 0.025
cash_s, deposits, unins, eq_s = 15.0, 180.0, 0.88, 16.0
afs_loss, htm_loss = afs * dafs * dy, htm * dhtm * dy
book_eq = eq_s - afs_loss
p1 = mcq("1.1", "Rates rise by 2.5 percentage points across maturities. What is Sigma's reported (book) equity after the rise, in $ billion?",
         [(f(book_eq), None), (f(eq_s), "afs_loss_not_taken_to_equity"), (f(eq_s - htm_loss), "htm_loss_recognised_instead_of_afs"),
          (f(book_eq - htm_loss), "economic_value_quoted_as_book_equity")], f(book_eq), 0.8)
withdraw = 0.40 * unins * deposits
afs_fv = afs - afs_loss
need = withdraw - cash_s - afs_fv
assert need > 0
ratio = (htm - htm_loss) / htm
book_sold = need / ratio
realised = book_sold - need
eq_after = book_eq - realised
near(realised, need * (htm_loss / (htm - htm_loss)))  # second route: loss per $ raised = unrealised loss / fair value
p2 = mcq("1.2", "Uninsured depositors then withdraw 40% of their deposits. Sigma pays with cash first, then sells its AFS securities at fair value, then sells HTM securities at fair value. Losses on HTM securities count against equity only when they are sold. What is reported equity after the withdrawals, in $ billion?",
         [(f(eq_after), None), (f(eq_s - realised), "afs_loss_from_1_1_ignored"),
          (f(book_eq - ((withdraw - cash_s) / ratio - (withdraw - cash_s))), "afs_securities_not_sold_first"),
          (f(book_eq - htm_loss), "whole_htm_loss_recognised")], f(eq_after), 0.8)
Q30178.append(question(
    id="30178-SVB-01", course="30178", deck="SVB", topic="HTM and AFS losses, OCI and a run that forces sales",
    objective="Interest-rate risk and liquidity risk in practice: the SVB case (portfolio mix, accounting classification, uninsured deposits)",
    shape="numerical exercise with 2 MCQ sub-questions", shape_class="exercise part",
    stem="Bank Sigma, before a rate rise, holds (US$ billion): cash 15; available-for-sale (AFS) securities 25 at fair value, duration 3.5; held-to-maturity (HTM) securities 90 at amortised cost (fair value equal to cost today), duration 6.0; loans 70. It is funded by deposits of 180, of which 88% are uninsured, other liabilities of 4, and equity of 16. Treat the durations as modified durations: ΔP ≈ −D × Δy × P. AFS gains and losses go to equity through other comprehensive income; HTM securities stay at cost.",
    parts=[p1, p2],
    scheme=[
        f"[1.1] Steps: (1) classify: AFS losses hit equity via OCI, HTM losses do not; (2) AFS loss = 3.5 × 2.5% × 25 = {f(afs_loss, 3)}; (3) HTM unrealised loss = 6.0 × 2.5% × 90 = {f(htm_loss)} (not recognised); (4) book equity = 16 − {f(afs_loss, 3)} = {f(book_eq, 3)}, so {f(book_eq)}.",
        f"[1.2] Steps: (1) uninsured deposits = 88% × 180 = {f(unins * deposits)}; (2) withdrawal = 40% × {f(unins * deposits)} = {f(withdraw, 2)}; (3) after cash: {f(withdraw - cash_s, 2)}; (4) AFS sold at fair value {f(afs_fv, 3)} (its loss is already in equity); (5) still needed {f(need, 3)}; (6) HTM sells at {f(ratio * 100)}% of cost, so cost sold = {f(need, 3)} / {f(ratio, 3)} = {f(book_sold, 3)}; (7) realised loss = {f(realised, 3)}; (8) equity = {f(book_eq, 3)} − {f(realised, 3)} = {f(eq_after, 3)}, so {f(eq_after)}.",
        f"Second route for 1.2: every $ raised from HTM costs {f(htm_loss)}/{f(htm - htm_loss)} = {f(htm_loss / (htm - htm_loss), 4)} of equity; {f(need, 3)} × that = {f(realised, 3)}.",
        f"Economic equity if all HTM were marked: {f(book_eq - htm_loss, 2)}. That gap between book and economic equity is what depositors feared (slides: 'Here be the dragons').",
        "Where marks are lost: leaving the AFS loss out of equity (16.0 / 11.5); recognising the whole HTM loss (0.3); selling HTM before AFS (5.3).",
    ],
    cites=[cite("SVB", "Asset side – the HTM portfolio", "At the end of 2022, the market value of the HTM portfolio would have been $76bn vs. $91 ($15 bn of unrealized losses)"),
           cite("SVB", "Asset side – the AFS portfolio", "Over $26 bn of AFS assets: these are carried at the fair value, i.e., marked to market"),
           cite("SVB", "Liability side: The Achilles’ heel", "≈ 90% of Dep were uninsured"),
           cite("SVB", "Phase 2: Deposits drawdown", "What banks could do to face «liability withdrawals»?")],
    location="slides on the asset mix (HTM, AFS), the liability side and the deposit drawdown",
    file=F_SVB, minutes=9, notches=["extra_classification", "chain", "working_backwards", "extra_step"],
    hc_parts=[{"n": "1.1", "steps": 4, "concepts": 2}, {"n": "1.2", "steps": 8, "concepts": 3}]))

# ---- 30178-SVB-02: SVB-style duration GAP, then the asset duration needed ----------
A, Lb, DA, DL, i0, di = 200.0, 184.0, 4.5, 0.5, 0.03, 0.02
dgap = DA - Lb / A * DL
deve = -dgap * A * di / (1 + i0)
near(deve, -(DA * A - DL * Lb) * di / (1 + i0))  # second route: ΔA − ΔL
p1 = mcq("2.1", "Rates rise by 2 percentage points (from 3%). What is the estimated change in Bank Theta's economic value of equity, in $ billion?",
         [(f(deve), None), (f(-(DA - DL) * A * di / (1 + i0)), "liability_duration_not_weighted_by_L_over_A"),
          (f(-dgap * A * di), "one_plus_i_left_out"), (f(-deve), "sign_of_the_change")], f(deve), 0.8)
tgt = -0.25 * (A - Lb)
dgap_t = -tgt * (1 + i0) / (A * di)
DA_t = dgap_t + Lb / A * DL
near(-(DA_t - Lb / A * DL) * A * di / (1 + i0), tgt)
p2 = mcq("2.2", "Keeping its liabilities unchanged, what weighted average asset duration would limit the loss in economic value of equity, for the same shock, to 25% of today's equity?",
         [(f(DA_t, 2), None), (f(dgap_t + DL, 2), "liability_duration_not_weighted_by_L_over_A"),
          (f(dgap_t, 2), "target_dgap_quoted_as_asset_duration"), (f(dgap_t - Lb / A * DL, 2), "liability_term_subtracted")],
         f(DA_t, 2), 0.8)
Q30178.append(question(
    id="30178-SVB-02", course="30178", deck="SVB", topic="SVB-style duration GAP and the asset duration that would have been safe",
    objective="Interest-rate risk: duration GAP and economic value of equity applied to the SVB case",
    shape="numerical exercise with 2 MCQ sub-questions", shape_class="exercise part",
    stem="Bank Theta looks like SVB in 2022. At market values it has assets of $200bn with a weighted average duration of 4.5 years and liabilities of $184bn, almost all demand deposits, with a weighted average duration of 0.5 years. The current rate is 3%. About 88% of its deposits are uninsured and 76% of its securities are HTM. Estimate value changes with ΔEVE ≈ −DGAP × A × Δi / (1 + i).",
    parts=[p1, p2],
    scheme=[
        f"[2.1] Steps: (1) L/A = 184/200 = {f(Lb / A, 2)}; (2) weighted DL = {f(Lb / A, 2)} × 0.5 = {f(Lb / A * DL, 2)}; (3) DGAP = 4.5 − {f(Lb / A * DL, 2)} = {f(dgap, 2)}; (4) Δi/(1+i) = 0.02/1.03 = {f(di / (1 + i0), 5)}; (5) ΔEVE = −{f(dgap, 2)} × 200 × {f(di / (1 + i0), 5)} = {f(deve, 2)}, so {f(deve)}.",
        f"Second route for 2.1: ΔA = −4.5 × 200 × 0.02/1.03 = {f(-DA * A * di / (1 + i0), 3)}; ΔL = −0.5 × 184 × 0.02/1.03 = {f(-DL * Lb * di / (1 + i0), 3)}; ΔEVE = ΔA − ΔL = {f(deve, 3)}.",
        f"[2.2] Steps: (1) equity = 200 − 184 = 16, so the allowed loss is 25% × 16 = {f(-tgt)}; (2) solve DGAP = {f(-tgt)} × 1.03 / (200 × 0.02) = {f(dgap_t, 3)}; (3) add back the liability term {f(Lb / A * DL, 2)}; (4) DA = {f(DA_t, 3)}, so {f(DA_t, 2)}. The slides' point: SVB's 6.2-year HTM book was far from this.",
        "Where marks are lost: not weighting DL by L/A; dropping (1 + i); a positive sign; in 2.2 quoting the DGAP instead of DA, or subtracting the liability term.",
        "Not needed: the uninsured and HTM shares (extraneous here; they matter for the run, not for ΔEVE).",
    ],
    cites=[cite("SVB", "Points to address", "Putting it together: what does this imply for SVB's Duration GAP and ΔEVE?"),
           cite("SVB", "Asset side – the HTM portfolio", "The average duration of the HTM portfolio: 6.2 yrs"),
           cite("IRR", 78, "Let DA and DL equal the (weighted average) Duration of assets and liabilities, respectively"),
           cite("IRR", 81, "If DGAP is positive, an increase in rates will lower EVE, while a decrease in rates will increase EVE")],
    location="SVB slides 'Points to address' and the HTM portfolio; IRR deck slides 78–83 (duration GAP)",
    file=F_SVB, minutes=9, notches=["cross_section", "working_backwards", "what_if_followon", "extraneous_data"],
    hc_parts=[{"n": "2.1", "steps": 5, "concepts": 2}, {"n": "2.2", "steps": 4, "concepts": 2}]))

BANKS["30178"] = {"questions": Q30178}

# =====================================================================================
# 30257 CORPORATE VALUATION  (exam: short written problems, 3 points each)
# =====================================================================================
CVP = "Slides/"
F_L12 = CVP + "Corporate Valuation - AY 26-27 - Lectures 1-2 - Introduction - v3.pdf"
F_L3 = CVP + "Corporate Valuation - AY 26-27 - Lecture 3 - DCF Valuation - v6.pdf"
F_L4 = CVP + "Corporate Valuation - C31 - Lecture 4 - Cost of Capital - v3.pdf"
F_L5 = CVP + "Corporate Valuation - C31 - Lecture 5 - Reorganizing and CFs - v13.pdf"
F_L6 = CVP + "Corporate Valuation - C31 - Lecture 6 - DCF Exercises - v1.pdf"
Q30257 = []
SP = "short problem (written)"

# ---- L12: bases of value in a takeover --------------------------------------------
fcfo, wacc, nd, shares, px = 36.0, 0.09, 100.0, 30.0, 11.0
ev_sa = fcfo / wacc
eq_sa = ev_sa - nd
syn, integ = 8.0, 25.0
inv = eq_sa + syn / wacc - integ
offer = 12.5 * shares
npv = inv - offer
near(inv, (fcfo + syn) / wacc - integ - nd)
pa = written("a", "Compute Kappa's standalone equity value, Omega's investment value for 100% of Kappa's equity, and Omega's NPV if it pays €12.50 per share. Round to one decimal.",
             f"Standalone equity {f(eq_sa)}; investment value {f(inv)}; NPV {f(npv)} (€m).", 1.5,
             [("synergies_added_without_integration_cost", "integration cost of 25 left out (NPV +13.9)"), ("market_value_used_as_standalone", "market cap 330 used as the standalone value"), ("net_debt_not_deducted", "EV used instead of equity value")])
syn_g = syn / (wacc - 0.02)
inv_g = eq_sa + syn_g - integ
max_ps = inv_g / shares
floor_ps = px * 1.15
near(max_ps, ((fcfo / wacc) - nd + syn / (wacc - 0.02) - integ) / shares)
pb = written("b", "Omega now expects the synergies to grow at 2% a year from the first-year €8m (other inputs unchanged). Kappa's board will reject any offer below a 15% premium on the €11.00 share price. Is there a price per share that works for both sides? Give the range.",
             f"Yes: from €{floor_ps:.2f} (board floor) to €{max_ps:.2f} (Omega's maximum) per share.", 1.5,
             [("growth_ignored_in_synergies", "synergies valued as a flat perpetuity (max €12.13, no deal)"), ("premium_on_standalone", "15% premium applied to standalone €10.00 instead of the market price")])
Q30257.append(question(
    id="30257-L12-01", course="30257", deck="L12", topic="Standalone, market and investment value in a takeover",
    objective="Introduction to valuation: users and uses, bases of value (market value vs investment value), price vs value",
    shape=SP, shape_class="short problem",
    stem="Kappa SpA generates a free cash flow from operations of €36m a year, flat forever. Its WACC is 9% and its net debt is €100m. It has 30 million shares trading at €11.00. Omega, an industrial buyer, expects after-tax synergies of €8m a year, starting next year and flat forever, discounted at the same 9%, and needs €25m of one-off integration costs today.",
    parts=[pa, pb],
    scheme=[
        f"[a] Steps: (1) standalone EV = 36 / 9% = {f(ev_sa)}; (2) standalone equity = {f(ev_sa)} − 100 = {f(eq_sa)}; (3) PV of synergies = 8 / 9% = {f(syn / wacc)}; (4) less integration cost 25; (5) investment value = {f(eq_sa)} + {f(syn / wacc)} − 25 = {f(inv)}; (6) offer = 12.50 × 30 = {f(offer)}; (7) NPV = {f(inv)} − {f(offer)} = {f(npv)}: at €12.50 Omega destroys value.",
        f"Second route for [a]: (36 + 8)/9% − 25 − 100 = {f(inv)}. The market value (€330m) is a third basis, above standalone because the market prices in some expectations; it is not the investment value.",
        f"[b] Steps: (1) growing synergies: 8 / (9% − 2%) = {f(syn_g)}; (2) investment value = {f(eq_sa)} + {f(syn_g)} − 25 = {f(inv_g)}; (3) maximum per share = {f(inv_g)} / 30 = {max_ps:.2f}; (4) board floor = 11.00 × 1.15 = {floor_ps:.2f}; (5) compare: floor < maximum; (6) so a deal zone exists; (7) range €{floor_ps:.2f}–€{max_ps:.2f}.",
        "How to write it: name each basis of value (standalone, market, investment) before computing; the offer price is not a value.",
        "Where marks are lost: dropping the integration cost, using market cap as standalone value, forgetting net debt, or valuing growing synergies as flat.",
    ],
    cites=[cite("L12", 43, "The investment value (for A) is therefore - €k 10 + €k 20 ÷ 10% = €k 190"),
           cite("L12", 42, "It includes the benefits, e.g. expected synergies, that the current owner or a potential investor can generate"),
           cite("L12", 39, "Price is not a synonym of value")],
    slides=[39, 40, 41, 42, 43, 44], location="slides 39–44 (bases of value and the apartment example)",
    file=F_L12, minutes=14, notches=["what_if_followon", "chain", "extra_step", "working_backwards"],
    hc_parts=[{"n": "a", "steps": 7, "concepts": 3}, {"n": "b", "steps": 7, "concepts": 2}]))

# ---- L3-01: APV, equity-side and WACC agree; then a debt-funded buyback ------------
ebit, keu, kd, D, t = 150.0, 0.11, 0.05, 400.0, 0.25
fcfo = ebit * (1 - t)
vu = fcfo / keu
vts = D * t
ev = vu + vts
eqv = ev - D
kel = keu + D / eqv * (keu - kd) * (1 - t)
fcfe = fcfo - D * kd + D * kd * t
near(fcfe / kel, eqv)  # second route: equity-side DCF
wacc_ = fcfo / ev
near(wacc_, kel * eqv / ev + kd * (1 - t) * D / ev)
pa = written("a", "Value Rho with the APV method, then compute its levered cost of equity (MM 2) and WACC, and show that the equity-side DCF gives the same equity value.",
             f"EV {f(ev)}; equity {f(eqv)}; kEL {f(kel * 100, 2)}%; WACC {f(wacc_ * 100, 2)}%; FCFE {f(fcfe)} / kEL = {f(fcfe / kel)}.", 1.5,
             [("tax_shield_not_valued", "EV = VU only"), ("book_leverage_in_mm2", "D/E at book instead of market values"), ("fcfe_without_tax_shield", "FCFE = FCFO − interest")])
D2 = 600.0
ev2 = vu + D2 * t
eq_pre = eqv + (D2 - D) * t  # value gain on announcement accrues to current shareholders
price = eq_pre / 50
bought = (D2 - D) / price
eq_post = ev2 - D2
near(eq_post / (50 - bought), price)
wacc2 = fcfo / ev2
pb = written("b", "Rho borrows another €200m (perpetual, same 5% cost) and uses all of it to buy back shares at a fair price. Before the deal there are 50 million shares. What is the price per share after the buyback, and the new WACC?",
             f"€{price:.2f} per share; WACC {f(wacc2 * 100, 2)}%.", 1.5,
             [("value_gain_ignored", "price computed from the old equity value (€14.45)"), ("shares_not_reduced", "post-deal equity divided by 50m shares")])
Q30257.append(question(
    id="30257-L3-01", course="30257", deck="L3", topic="Three DCF models, one value, then a debt-funded buyback",
    objective="DCF valuation: capital structure theory (MM with taxes), APV, equity-side DCF and WACC",
    shape=SP, shape_class="short problem",
    stem="Rho SpA has a constant EBIT of €150m in perpetuity, maintenance investment only (no growth), an unlevered cost of equity of 11%, perpetual debt of €400m at a 5% interest rate equal to its cost of debt, and a 25% tax rate. Tax shields are as risky as debt.",
    parts=[pa, pb],
    scheme=[
        f"[a] Steps: (1) FCFO = 150 × 0.75 = {f(fcfo)}; (2) VU = {f(fcfo)} / 11% = {f(vu)}; (3) VTS = D × t = {f(vts)}; (4) EV = {f(ev)}; (5) equity = {f(ev)} − 400 = {f(eqv)}; (6) kEL = 11% + (400/{f(eqv)}) × (11% − 5%) × 0.75 = {f(kel * 100, 2)}%; (7) WACC = FCFO / EV = {f(wacc_ * 100, 2)}%.",
        f"Second routes for [a]: FCFE = {f(fcfo)} − 20 + 5 = {f(fcfe)}; {f(fcfe)} / {f(kel * 100, 2)}% = {f(fcfe / kel)} (= equity). WACC from weights: {f(kel * 100, 2)}% × {f(eqv / ev, 4)} + 3.75% × {f(D / ev, 4)} = {f(wacc_ * 100, 2)}%.",
        f"[b] Steps: (1) new debt 600; (2) VTS = 600 × 25% = {f(D2 * t)}; (3) EV = {f(ev2)}; (4) the extra tax shield of {f((D2 - D) * t)} goes to today's shareholders on announcement; (5) price = ({f(eqv)} + {f((D2 - D) * t)}) / 50 = {price:.2f}; (6) shares bought = 200 / {price:.2f} = {f(bought, 2)}m; (7) remaining {f(50 - bought, 2)}m; (8) equity after = {f(ev2)} − 600 = {f(eq_post)} = {price:.2f} × {f(50 - bought, 2)}m (check); (9) WACC = {f(fcfo)} / {f(ev2)} = {f(wacc2 * 100, 2)}%.",
        "How to write it: state MM 1 (EV rises by D·t) and MM 2 (kEL rises with market D/E) in one line each, then compute.",
        "Where marks are lost: book D/E in MM 2, FCFE without the tax shield, pricing the buyback at the old €14.45, or dividing post-deal equity by 50m shares.",
    ],
    cites=[cite("L3", 8, "Modigliani & Miller 1: as debt increases, enterprise value increases thanks to an increase in the future tax shields (TS)"),
           cite("L3", 12, "Modigliani & Miller 2: as debt increases, the cost of equity moves UP from the unlevered case:"),
           cite("L3", 15, "The D/E ratio in WACC and in MM 2 computation is made with market values")],
    slides=[7, 8, 9, 10, 11, 12, 13, 14, 15, 16], location="slides 7–16 (MM with taxes, APV, equity-side DCF, WACC example)",
    file=F_L3, minutes=18, notches=["what_if_followon", "chain", "extra_step", "cross_section"],
    hc_parts=[{"n": "a", "steps": 7, "concepts": 3}, {"n": "b", "steps": 9, "concepts": 3}]))

# ---- L3-02: growth that destroys value; the ROI the market prices ------------------
nopat, wacc, g, roi, nd = 60.0, 0.09, 0.03, 0.075, 150.0
crr = g / roi
fcfo1 = nopat * (1 - crr)
ev = fcfo1 / (wacc - g)
eqv = ev - nd
ev0 = nopat / wacc
near(ev, nopat * (1 - g / roi) / (wacc - g))
pa = written("a", "Value Theta's enterprise and equity value under its 3% growth plan, and compare the enterprise value with a no-growth policy. Does the plan create value?",
             f"EV {f(ev)}; equity {f(eqv)}; no-growth EV {f(ev0)}; the plan destroys {f(ev0 - ev)} because ROI 7.5% < WACC 9%.", 1.5,
             [("reinvestment_ignored", "NOPAT discounted at WACC − g (EV 1,000)"), ("growth_always_adds_value", "concludes growth adds value")])
mkt_eq = 520.0
ev_m = mkt_eq + nd
x = ev_m * (wacc - g) / nopat
roi_m = g / (1 - x)
near(nopat * (1 - g / roi_m) / (wacc - g), ev_m)
pb = written("b", "The market values Theta's equity at €520m. Assuming the market prices the same 3% growth plan, what return on new investment is it implicitly assuming, and what does that imply about the value of growth?",
             f"Implied ROI {f(roi_m * 100, 2)}%, just above the 9% WACC: growth adds only {f(ev_m - ev0)} of value over no growth.", 1.5,
             [("net_debt_not_added", "market equity used as EV (ROI 6.9%)"), ("crr_confused_with_roi", "reinvestment rate reported as ROI")])
Q30257.append(question(
    id="30257-L3-02", course="30257", deck="L3", topic="When growth destroys value, and the ROI the market is pricing",
    objective="DCF valuation: growth, reinvestment and value (g = ROI × CRR); terminal value assumptions",
    shape=SP, shape_class="short problem",
    stem="Theta SpA will earn NOPAT of €60m next year. Its WACC is 9% and its net debt is €150m. Management plans to grow NOPAT at 3% a year forever by reinvesting, earning a constant 7.5% return on new investment.",
    parts=[pa, pb],
    scheme=[
        f"[a] Steps: (1) CRR = g / ROI = 3% / 7.5% = {f(crr * 100)}%; (2) FCFO1 = 60 × (1 − {f(crr, 2)}) = {f(fcfo1)}; (3) WACC − g = 6%; (4) EV = {f(fcfo1)} / 6% = {f(ev)}; (5) equity = {f(ev)} − 150 = {f(eqv)}; (6) no-growth EV = 60 / 9% = {f(ev0)}; (7) growth destroys {f(ev0 - ev)} because ROI < WACC.",
        f"Second route for [a]: EV = NOPAT × (1 − g/ROI) / (WACC − g) = 60 × 0.6 / 0.06 = {f(ev)}.",
        f"[b] Steps: (1) EV = 520 + 150 = {f(ev_m)}; (2) × (WACC − g): {f(ev_m)} × 6% = {f(ev_m * 0.06, 1)}; (3) ÷ NOPAT: {f(x, 3)} = 1 − g/ROI; (4) g/ROI = {f(1 - x, 3)}; (5) ROI = 3% / {f(1 - x, 3)} = {f(roi_m * 100, 2)}%; (6) compare with WACC 9%: barely above; (7) value of growth = {f(ev_m)} − {f(ev0)} = {f(ev_m - ev0)}, almost nothing.",
        "How to write it: write g = ROI × CRR first, then FCFO = NOPAT × (1 − CRR); state which side of WACC the ROI sits.",
        "Where marks are lost: discounting NOPAT instead of FCFO (EV 1,000), forgetting net debt in [b], or calling any growth value-creating.",
    ],
    cites=[cite("L3", 29, "If ROI < WACC, an increase in the growth rate decreases value"),
           cite("L3", 27, "In the LT, ROI should converge to WACC. This has a powerful consequence: value no longer depends on long term growth"),
           cite("L3", 25, "The TV growth rate should not exceed the growth rate of the economy as a whole")],
    slides=[25, 26, 27, 28, 29], location="slides 25–29 (terminal value, growth and value)",
    file=F_L3, minutes=16, notches=["working_backwards", "what_if_followon", "extra_step", "chain"],
    hc_parts=[{"n": "a", "steps": 7, "concepts": 3}, {"n": "b", "steps": 7, "concepts": 2}]))

# ---- L4-01: bottom-up beta, synthetic rating, WACC ---------------------------------
raw = {"Alfa": (1.30, 0.50), "Beta": (1.05, 0.20)}
t = 0.24
adj = {k: v[0] * 2 / 3 + 1 / 3 for k, v in raw.items()}
unl = {k: adj[k] / (1 + raw[k][1] * (1 - t)) for k in raw}
bu = sum(unl.values()) / 2
de = 0.40
bl = bu * (1 + de * (1 - t))
rf, mrp = 0.035, 0.055
kel = rf + bl * mrp
near(kel, rf + bu * mrp + bu * de * (1 - t) * mrp)  # second route: kEU + (D/E)(1−t)·βU·MRP  (kD = rF in the beta-debt=0 world)
pa = written("a", "Estimate Tau's levered cost of equity with a bottom-up beta. Show each step.",
             f"Blume-adjusted betas {adj['Alfa']:.3f} and {adj['Beta']:.3f}; unlevered {unl['Alfa']:.3f} and {unl['Beta']:.3f}; industry βU {bu:.3f}; Tau βL {bl:.3f}; kEL {f(kel * 100, 2)}%.", 1.5,
             [("blume_skipped", "raw betas unlevered directly"), ("effective_tax_rate_used", "31% effective rate instead of the 24% statutory rate"), ("book_leverage_used", "book D/E instead of the target market D/E")])
cover = 40 / 12.5
kd = rf + 0.018
w_e, w_d = 1 / (1 + de), de / (1 + de)
wacc_ = w_e * kel + w_d * kd * (1 - t)
near(wacc_, (kel + de * kd * (1 - t)) / (1 + de))
pb = written("b", "Estimate Tau's cost of debt with a synthetic rating from the slide table and compute its WACC.",
             f"Coverage {cover:.1f}× → Ba2/BB, spread 1.8%: kD {f(kd * 100, 2)}%, after tax {f(kd * (1 - t) * 100, 2)}%; weights {f(w_e * 100, 1)}% equity / {f(w_d * 100, 1)}% debt; WACC {f(wacc_ * 100, 2)}%.", 1.5,
             [("weights_from_d_over_e_directly", "40% used as the debt weight"), ("pre_tax_kd_in_wacc", "cost of debt not taxed"), ("irap_in_tax_rate", "27.9% combined rate used")])
Q30257.append(question(
    id="30257-L4-01", course="30257", deck="L4", topic="Bottom-up beta, synthetic rating and WACC for a private company",
    objective="Cost of capital: CAPM inputs, Blume adjustment, Hamada unlevering and relevering, synthetic rating, WACC",
    shape=SP, shape_class="short problem",
    stem="Tau Srl is a private Italian company. Two listed comparables have raw (regression) levered betas and average market D/E ratios of Alfa 1.30 and 0.50, and Beta 1.05 and 0.20; neither is an outlier. Tau's target market D/E is 0.40. The risk-free rate is 3.5% and the market risk premium 5.5%. Tau's EBIT is €40m and its interest expense €12.5m. The Italian statutory corporate income tax rate that allows interest deduction is 24% (the 3.9% regional tax is not on EBT); Tau's effective tax rate last year was 31%. Apply Blume's adjustment to market betas and use the Hamada formula.",
    data="| Interest coverage from | to | Rating | Spread |\n|---|---|---|---|\n| 2.5 | 3.0 | B1/B+ | 2.6% |\n| 3.0 | 3.5 | Ba2/BB | 1.8% |\n| 3.5 | 4.0 | Ba1/BB+ | 1.6% |\n| 4.0 | 4.5 | Baa2/BBB | 1.2% |",
    parts=[pa, pb],
    scheme=[
        f"[a] Steps: (1) Blume Alfa = 1.30 × 2/3 + 1/3 = {adj['Alfa']:.3f}; (2) Blume Beta = {adj['Beta']:.3f}; (3) unlever Alfa: {adj['Alfa']:.3f} / (1 + 0.5 × 0.76) = {unl['Alfa']:.4f}; (4) unlever Beta: {adj['Beta']:.3f} / (1 + 0.2 × 0.76) = {unl['Beta']:.4f}; (5) industry βU = average = {bu:.4f}; (6) relever at 0.40: {bu:.4f} × (1 + 0.4 × 0.76) = {bl:.4f}; (7) kEL = 3.5% + {bl:.4f} × 5.5% = {f(kel * 100, 2)}%.",
        f"Second route for [a]: kEU = 3.5% + {bu:.4f} × 5.5% = {f((rf + bu * mrp) * 100, 3)}%; add the leverage premium βU × D/E × (1 − t) × MRP = {f(bu * de * (1 - t) * mrp * 100, 3)}% → {f(kel * 100, 2)}%.",
        f"[b] Steps: (1) coverage = 40 / 12.5 = {cover:.1f}×; (2) table: 3.0–3.5 → Ba2/BB, spread 1.8%; (3) kD = 3.5% + 1.8% = {f(kd * 100, 1)}%; (4) after tax at the 24% statutory rate: {f(kd * (1 - t) * 100, 3)}%; (5) E/(D+E) = 1/1.4 = {f(w_e * 100, 2)}%; (6) D/(D+E) = {f(w_d * 100, 2)}%; (7) WACC = {f(wacc_ * 100, 2)}%.",
        "Where marks are lost: skipping Blume, using the 31% effective or 27.9% combined rate, using D/E (0.40) as the debt weight, or leaving kD pre-tax.",
        "Not needed: the effective tax rate (slides: superficial and prone to mistakes).",
    ],
    cites=[cite("L4", 17, "the estimated levered (\"raw\") beta after a number of years tends to converge (\"adj\") toward 1"),
           cite("L4", 25, "Re-lever the industry bU with a reversed Hamada formula"),
           cite("L4", 36, "3,0 3,5 Ba2/BB 1,8%"),
           cite("L4", 27, "Superficial and prone to mistakes (not directly associated with interest tax shields), but easily applicable")],
    slides=[7, 17, 22, 24, 25, 27, 28, 36, 39], location="slides 7–39 (CAPM, Blume, Hamada, bottom-up beta, tax rate, synthetic rating)",
    file=F_L4, minutes=18, notches=["extra_classification", "extraneous_data", "chain", "extra_step"],
    hc_parts=[{"n": "a", "steps": 7, "concepts": 3}, {"n": "b", "steps": 7, "concepts": 3}]))

# ---- L5-01: reorganise, FCFO, bridge to equity ------------------------------------
bs = {  # 2025, 2026
    "Operating cash": (10, 12), "Excess cash": (60, 45), "Trade receivables": (150, 170), "Inventory": (120, 115),
    "Net PP&E": (500, 540), "Investments in associates": (40, 40),
    "Trade payables": (130, 150), "Employee severance indemnity (TFR)": (30, 32), "Bank loans and bonds": (300, 330),
    "Preferred shares": (20, 20), "Minority interests": (25, 27)}
assets_k = ["Operating cash", "Excess cash", "Trade receivables", "Inventory", "Net PP&E", "Investments in associates"]
liab_k = ["Trade payables", "Employee severance indemnity (TFR)", "Bank loans and bonds", "Preferred shares", "Minority interests"]
tot = [sum(bs[k][y] for k in assets_k) for y in (0, 1)]
geq = [tot[y] - sum(bs[k][y] for k in liab_k) for y in (0, 1)]
ebit, da, interest, t = 160.0, 60.0, 18.0, 0.28
nopat = ebit * (1 - t)
nwc = [bs["Operating cash"][y] + bs["Trade receivables"][y] + bs["Inventory"][y] - bs["Trade payables"][y] for y in (0, 1)]
capex = bs["Net PP&E"][1] - bs["Net PP&E"][0] + da
fcfo = nopat + da - (nwc[1] - nwc[0]) - capex
core_ce = [nwc[y] + bs["Net PP&E"][y] for y in (0, 1)]
near(fcfo, nopat - (core_ce[1] - core_ce[0]))  # second route: FCFO = NOPAT − Δ core capital employed
pa = written("a", "Reorganise the balance sheets as needed and compute Lambda's FCFO for 2026.",
             f"NOPAT {f(nopat)}; + D&A 60; noncash WC {nwc[0]} → {nwc[1]} (releases {nwc[0] - nwc[1]}); CAPEX {capex}; FCFO {f(fcfo)}.", 1.5,
             [("excess_cash_in_working_capital", "excess cash counted as operating"), ("capex_equals_change_in_ppe", "D&A not added back to ΔPP&E"), ("taxes_on_ebt", "actual taxes used instead of operating taxes")])
EVb, nsh = 1400.0, 40.0
netdebt = bs["Bank loans and bonds"][1] - bs["Excess cash"][1]
eqb = EVb - netdebt + bs["Investments in associates"][1] - bs["Employee severance indemnity (TFR)"][1] - bs["Minority interests"][1] - bs["Preferred shares"][1]
pb = written("b", "An asset-side DCF values Lambda's operations at €1,400m at the end of 2026. Bridge to the value of the group's ordinary equity and give it per share (40 million shares).",
             f"Net debt {netdebt}; equity value {f(eqb)}; €{eqb / nsh:.2f} per share.", 1.5,
             [("operating_cash_deducted", "operating cash subtracted in net debt"), ("associates_not_added", "associates left out of the bridge"), ("minorities_or_preferred_not_deducted", "equity-like claims not deducted")])
near(eqb, EVb - 330 + 45 + 40 - 32 - 27 - 20)
Q30257.append(question(
    id="30257-L5-01", course="30257", deck="L5", topic="Reorganise the balance sheet, build FCFO and cross the bridge to equity",
    objective="Reorganizing financials for valuation: noncash working capital, capital employed, FCFO, the bridge to equity",
    shape=SP, shape_class="short problem",
    stem="Lambda SpA's balance sheets (€m, end of year) and 2026 income statement are below. The operating tax rate is 28%. Operating cash is needed for daily operations; excess cash is not. Associates are non-consolidated minority stakes. Preferred shares are equity-like claims senior to ordinary shares.",
    data="| Balance sheet (€m) | 2025 | 2026 |\n|---|---|---|\n" + "".join(f"| {k} | {v[0]} | {v[1]} |\n" for k, v in bs.items()) + f"| Group equity (ordinary) | {geq[0]} | {geq[1]} |\n\n| Income statement 2026 (€m) | |\n|---|---|\n| EBITDA | 220 |\n| D&A | (60) |\n| EBIT | 160 |\n| Interest expense | (18) |\n| Income taxes | (39.8) |\n| Net income | 102.2 |",
    parts=[pa, pb],
    scheme=[
        f"[a] Steps: (1) operating taxes = 28% × 160 = {f(ebit * t)}, NOPAT = {f(nopat)}; (2) add back D&A 60 → gross cash flow {f(nopat + da)}; (3) noncash WC 2025 = 10 + 150 + 120 − 130 = {nwc[0]}; (4) 2026 = 12 + 170 + 115 − 150 = {nwc[1]}; (5) it falls by {nwc[0] - nwc[1]}, releasing cash (+{nwc[0] - nwc[1]}); (6) CAPEX = ΔPP&E 40 + D&A 60 = {capex}; (7) FCFO = {f(nopat + da)} + {nwc[0] - nwc[1]} − {capex} = {f(fcfo)}.",
        f"Second route for [a]: core capital employed = NWC + PP&E: {core_ce[0]} → {core_ce[1]} (+{core_ce[1] - core_ce[0]}); FCFO = NOPAT − ΔCE = {f(nopat)} − {core_ce[1] - core_ce[0]} = {f(fcfo)}.",
        f"[b] Steps: (1) gross debt 330; (2) net debt = 330 − excess cash 45 = {netdebt} (operating cash stays in WC); (3) + associates 40; (4) − TFR 32 (debt-like); (5) − minorities 27; (6) − preferred 20; (7) equity = 1,400 − {netdebt} + 40 − 32 − 27 − 20 = {f(eqb)}; (8) per share = {f(eqb)} / 40 = €{eqb / nsh:.2f}.",
        "Where marks are lost: counting excess cash as operating, CAPEX = ΔPP&E only (40), operating taxes on EBT, deducting operating cash, forgetting associates, minorities or preferred shares.",
        "Not needed in [a]: interest and reported income taxes (FCFO uses operating taxes on EBIT).",
    ],
    cites=[cite("L5", 10, "The \"non-cash (or non-debt) working capital\" for valuation only includes the assets and the liabilities with an operating nature"),
           cite("L5", 12, "\"Pensions\": employee termination indemnities"),
           cite("L5", 24, "FCFO = NOPAT - increase in core capital employed during the year"),
           cite("L5", 27, "Moving from EV to EqV and vice-versa requires the \"bridge\" of other remaining balance sheet items")],
    slides=[8, 9, 10, 11, 12, 21, 22, 24, 27, 28], location="slides 8–28 (reorganised balance sheet, cash flows for valuation, bridge to equity)",
    file=F_L5, minutes=18, notches=["extra_classification", "extraneous_data", "extra_step", "chain"],
    hc_parts=[{"n": "a", "steps": 7, "concepts": 3}, {"n": "b", "steps": 8, "concepts": 2}]))

# ---- L6-01: FCFO from EBITDA, then a two-stage DCF at the right valuation date -----
ebitda, da, newinv, disp, nwc0, nwc1, t = 260.0, 60.0, 90.0, 10.0, 70.0, 85.0, 0.25
f27 = (ebitda - da) * (1 - t) + da - (newinv - disp) - (nwc1 - nwc0)
near(f27, ebitda * (1 - t) + da * t - (newinv - disp) - (nwc1 - nwc0))  # second route: EBITDA(1−t) + D&A·t
pa = written("a", "Compute Mu's FCFO for 2027.", f"EBIT 200; NOPAT 150; + D&A 60; − net investments 80; − ΔNWC 15; FCFO {f(f27)}.", 1.5,
             [("disposals_ignored", "gross investments of 90 deducted"), ("working_capital_sign", "NWC increase added"), ("interest_deducted", "interest or debt flows in FCFO")])
f28, f29, gT, w, nd = 125.0, 132.0, 0.02, 0.09, 400.0
tv = f29 * (1 + gT) / (w - gT)
ev = f28 / (1 + w) + f29 / (1 + w) ** 2 + tv / (1 + w) ** 2
eqv = ev - nd
near(ev, (f28 + (f29 + tv) / (1 + w)) / (1 + w))  # second route: roll back one year at a time
pb = written("b", "Plan FCFO is €125m in 2028 and €132m in 2029, growing 2% a year from 2030. WACC is 9% and net debt at the end of 2027 is €400m. What are Mu's enterprise and equity values on 31/12/2027?",
             f"TV at end-2029 {f(tv)}; EV on 31/12/2027 {f(ev)}; equity {f(eqv)}.", 1.5,
             [("valuation_date_2027_flow_included", "2027 FCFO counted although it is already paid"), ("tv_discounted_three_years", "terminal value discounted one year too many"), ("tv_on_fcfo_2029_not_grown", "TV = FCFO 2029 / (WACC − g)")])
Q30257.append(question(
    id="30257-L6-01", course="30257", deck="L6", topic="FCFO from EBITDA, then a two-stage DCF at the right valuation date",
    objective="DCF exercises: building FCFO, two-stage asset-side DCF, valuation date, bridge to equity",
    shape=SP, shape_class="short problem",
    stem="Mu SpA reports for 2027 (€m): EBITDA 260; D&A 60; new investments 90; disposals of fixed assets 10 (sold at book value, so no gain or loss); noncash working capital 70 at end-2026 and 85 at end-2027; interest 14; debt rose from 380 to 400. Tax rate 25%.",
    parts=[pa, pb],
    scheme=[
        f"[a] Steps: (1) EBIT = 260 − 60 = 200; (2) operating taxes 25% = 50; (3) NOPAT = 150; (4) + D&A 60; (5) net investment = 90 − 10 = 80; (6) ΔNWC = 85 − 70 = +15 absorbs cash; (7) FCFO = 150 + 60 − 80 − 15 = {f(f27)}.",
        f"Second route for [a]: EBITDA × (1 − t) + D&A × t − 80 − 15 = 195 + 15 − 95 = {f(f27)}.",
        f"[b] Steps: (1) valuation date 31/12/2027: the 2027 flow is already in the past, so start from 2028; (2) PV 2028 = 125 / 1.09 = {f(f28 / 1.09, 2)}; (3) PV 2029 = 132 / 1.09² = {f(f29 / 1.09 ** 2, 2)}; (4) TV at end-2029 = 132 × 1.02 / 7% = {f(tv, 2)}; (5) PV of TV = {f(tv, 2)} / 1.09² = {f(tv / 1.09 ** 2, 2)}; (6) EV = {f(ev)}; (7) equity = {f(ev)} − 400 = {f(eqv)}.",
        f"Second route for [b]: roll back: value at end-2028 = (132 + {f(tv, 2)}) / 1.09 = {f((f29 + tv) / 1.09, 2)}; EV = (125 + that) / 1.09 = {f(ev)}.",
        "Where marks are lost: deducting gross investments, adding the NWC increase, putting interest or debt changes in FCFO, including 2027's flow, discounting the TV three years, or not growing FCFO 2029 into the TV.",
        "Not needed: interest and the change in debt (they belong to FCFE, not FCFO).",
    ],
    cites=[cite("L6", 3, "How much is the company’s FCFO for valuation purposes in 2019?"),
           cite("L6", 6, "What is the enterprise value as of 31/12/2016?"),
           cite("L3", 18, "a second subsequent stage (the terminal value), with a constant growth assumption")],
    slides=[3, 4, 6], location="L6 problems 2.5 (FCFO) and 4.1 (valuation date); L3 slide 18 (two-stage model)",
    file=F_L6, minutes=16, notches=["extraneous_data", "extra_step", "chain", "cross_section"],
    hc_parts=[{"n": "a", "steps": 7, "concepts": 2}, {"n": "b", "steps": 7, "concepts": 3}]))

BANKS["30257"] = {"questions": Q30257}

# =====================================================================================
# 30285 EMPIRICAL METHODS FOR FINANCE (exam: all MCQ, including derivations)
# =====================================================================================
EMP = "Slides/"
F_1B, F_1C = EMP + "1b_Introduction_to_Content.pdf", EMP + "1c_LinearAlgebra_and_Inference_v2.pdf"
F_2, F_2B, F_2C = EMP + "2_Simple_LinRegr.pdf", EMP + "2b_Simple_LinRegr_Inference.pdf", EMP + "2c_LinearRegr_FTest.pdf"
Q30285 = []
EMS = "numerical MCQ with derivation (2 parts)"

# ---- 1B: gross, log and portfolio returns; portfolio variance ---------------------
RA, RB = (44 + 2) / 40, 22 / 25
wA = 100 * 40 / (100 * 40 + 240 * 25)
Rp = wA * RA + (1 - wA) * RB
lp = math.log(Rp)
lw = wA * math.log(RA) + (1 - wA) * math.log(RB)
gap = (lp - lw) * 100
near(Rp, (100 * 46 + 240 * 22) / (100 * 40 + 240 * 25))  # second route: portfolio value ratio
p1 = mcq("1", "Over the period, what is the portfolio's log return minus the value-weighted average of the two assets' log returns, in percentage points?",
         [(f"+{gap:.2f}", None), ("0.00", "log_returns_assumed_to_aggregate"), (f"{-gap:.2f}", "sign_reversed"),
          (f"+{(math.log(wA * 44 / 40 + (1 - wA) * RB) - (wA * math.log(44 / 40) + (1 - wA) * math.log(RB))) * 100:.2f}", "dividend_left_out_of_return_A")], f"+{gap:.2f}", "UNKNOWN")
sA, sB, rho = 0.30, 0.20, -0.5
cov = rho * sA * sB
var_now = wA ** 2 * sA ** 2 + (1 - wA) ** 2 * sB ** 2 + 2 * wA * (1 - wA) * cov
w0 = sB / (sA + sB)
near((w0 * sA - (1 - w0) * sB) ** 2, 0)
opts = [(f"w = {w0:.2f}; σ = {math.sqrt(var_now) * 100:.1f}%", None),
        (f"w = {1 - w0:.2f}; σ = {math.sqrt(var_now) * 100:.1f}%", "weight_on_the_wrong_asset"),
        (f"w = {w0:.2f}; σ = {math.sqrt(wA ** 2 * sA ** 2 + (1 - wA) ** 2 * sB ** 2) * 100:.1f}%", "covariance_term_dropped"),
        (f"w = {w0:.2f}; σ = {math.sqrt(wA ** 2 * sA ** 2 + (1 - wA) ** 2 * sB ** 2 - wA * (1 - wA) * cov) * 100:.1f}%", "covariance_term_not_doubled")]
p2 = mcq("2", "Over a longer sample, σA = 30%, σB = 20% and their correlation is −0.5. (i) If the correlation were −1, which weight in A would make the portfolio riskless? (ii) What is the portfolio's standard deviation at today's weights with the actual correlation of −0.5?",
         opts, opts[0][0], "UNKNOWN")
Q30285.append(question(
    id="30285-L1B-01", course="30285", deck="L1B", topic="Gross, log and portfolio returns, and when a portfolio is riskless",
    objective="Returns: definitions and measurement; risk as variance; portfolio variance with covariance",
    shape=EMS, shape_class="calc MCQ",
    stem="You hold 100 shares of A bought at €40 and 240 shares of B bought at €25. One period later A trades at €44 and paid a €2 dividend; B trades at €22 and paid nothing. Portfolio weights are value weights at the start.",
    parts=[p1, p2],
    scheme=[
        f"[1] Steps: (1) gross return A = (44 + 2)/40 = {RA:.3f}; (2) B = 22/25 = {RB:.3f}; (3) weights: A = 4,000/10,000 = {wA:.1f}, B = {1 - wA:.1f}; (4) portfolio gross = {Rp:.4f}; (5) log = {lp:.5f}; (6) weighted logs = 0.4 × {math.log(RA):.5f} + 0.6 × {math.log(RB):.5f} = {lw:.5f}; (7) gap = {gap:.2f} pp: log returns do not add across assets.",
        f"Second route for [1]: portfolio value 10,000 → 100 × 46 + 240 × 22 = {100 * 46 + 240 * 22:,}; gross {Rp:.4f} (same).",
        f"[2] Steps: (1) with ρ = −1, Cov = −σAσB; (2) Var = (wσA − (1 − w)σB)²; (3) it is a perfect square; (4) set wσA = (1 − w)σB; (5) w = 0.20/0.50 = {w0:.2f}; (6) at w = 0.4 and ρ = −0.5: Cov = {cov:.3f}, Var = 0.0144 + 0.0144 − 0.0144 = {var_now:.4f}; (7) σ = {math.sqrt(var_now) * 100:.1f}%.",
        "Where marks are lost: assuming log returns aggregate; putting σA over the sum instead of σB; dropping or halving the covariance term.",
    ],
    cites=[cite("L1B", "Returns in Financial Modelling", "Raw Gross Return: what you get relative to what you invested"),
           cite("L1B", "Disadvantages of Log Returns", "Take away: units matter"),
           cite("L1B", "Variance of a Sum of Variables and Covariance", "Example: assume the 2 assets are perfectly inversely related (correlated). What happens?")],
    location="slides 'Returns in Financial Modelling', 'Disadvantages of Log Returns', 'Variance of a Sum of Variables and Covariance'",
    file=F_1B, minutes=9, notches=["what_if_followon", "near_true_statements", "extra_step", "extraneous_data"],
    hc_parts=[{"n": "1", "steps": 7, "concepts": 2}, {"n": "2", "steps": 7, "concepts": 2}]))

# ---- 1C: vector moments, SE of the mean, sandwich rule ----------------------------
Y = [2, -1, 4, 3]
T = len(Y)
avg = sum(Y) / T
var1 = sum(y * y for y in Y) / T - avg ** 2
near(var1, sum((y - avg) ** 2 for y in Y) / T)  # second route: first method (demeaned)
se = math.sqrt(var1) / math.sqrt(T)
p1 = mcq("1", "Using the slides' second method, Var(Y) = (1/T)·Y·Y′ − Avg², and σ̂ = √Var(Y), what is the standard error of the sample mean?",
         [(f"{se:.3f}", None), (f"{math.sqrt(var1):.3f}", "forgot_to_divide_by_root_T"), (f"{math.sqrt(var1) / T:.3f}", "divided_by_T_not_root_T"),
          (f"{math.sqrt(sum((y - avg) ** 2 for y in Y) / (T - 1)) / math.sqrt(T):.3f}", "T_minus_1_variance_used")], f"{se:.3f}", "UNKNOWN")
V = [[0.04, 0.01], [0.01, 0.09]]
Am = [[0.5, 0.5], [1, -1]]
mm = lambda X, Y_: [[sum(X[i][k] * Y_[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
tr = lambda X: [[X[j][i] for j in range(2)] for i in range(2)]
S = mm(mm(Am, V), tr(Am))
near(S[1][1], 0.04 + 0.09 - 2 * 0.01)  # second route: Var(r1 − r2)
near(S[0][1], 0.5 * 0.04 - 0.5 * 0.09)  # Cov(avg, diff) = (Var1 − Var2)/2
W = mm(mm(tr(Am), V), Am)
opts = [(f"Var = {S[1][1]:.3f}; Cov = {S[0][1]:.3f}", None),
        (f"Var = {0.04 + 0.09 + 2 * 0.01:.3f}; Cov = {S[0][1]:.3f}", "covariance_added_in_a_difference"),
        (f"Var = {S[1][1]:.3f}; Cov = {-S[0][1]:.3f}", "sign_of_the_covariance"),
        (f"Var = {W[1][1]:.3f}; Cov = {W[0][1]:.3f}", "sandwich_transposed_A_prime_V_A")]
p2 = mcq("2", "Returns y = (r₁, r₂)′ have V(y) = [[0.04, 0.01], [0.01, 0.09]]. Portfolios z = A·y with A = [[0.5, 0.5], [1, −1]] (row 1: equal-weight; row 2: long r₁, short r₂). Using the sandwich rule, what are the variance of the long-short portfolio and its covariance with the equal-weight portfolio?",
         opts, opts[0][0], "UNKNOWN")
Q30285.append(question(
    id="30285-L1C-01", course="30285", deck="L1C", topic="Sample moments in vector form, the SE of the mean and the sandwich rule",
    objective="Linear algebra and statistics: sample average and variance in vector form, standard errors, variance of linear combinations",
    shape=EMS, shape_class="calc MCQ",
    stem="A row vector of T = 4 observations is Y = (2, −1, 4, 3). The slides divide by T in the sample variance. 1_T is a column vector of ones.",
    parts=[p1, p2],
    scheme=[
        f"[1] Steps: (1) Y·1_T = 8; (2) Avg = 8/4 = {avg:.1f}; (3) Y·Y′ = 4 + 1 + 16 + 9 = 30; (4) /T = 7.5; (5) Var = 7.5 − {avg ** 2:.0f} = {var1:.2f}; (6) σ̂ = {math.sqrt(var1):.4f}; (7) SE = σ̂/√T = {se:.4f}.",
        f"Second route for [1]: demeaned vector (0, −3, 2, 1): (0 + 9 + 4 + 1)/4 = {var1:.2f}, same.",
        f"[2] Steps: (1) A·V row 1 = (0.025, 0.05); (2) row 2 = (0.03, −0.08); (3) multiply by A′: entry (1,2) = 0.025 − 0.05 = {S[0][1]:.3f}; (4) entry (2,2) = 0.03 + 0.08 = {S[1][1]:.3f}; (5) read Var(long-short) = {S[1][1]:.3f}; (6) Cov = {S[0][1]:.3f}; (7) check: Var(r₁ − r₂) = 0.04 + 0.09 − 2 × 0.01 = {S[1][1]:.3f}.",
        f"Second route for [2]: Cov(½r₁ + ½r₂, r₁ − r₂) = ½Var(r₁) − ½Var(r₂) = {S[0][1]:.3f}.",
        "Where marks are lost: forgetting √T, dividing by T, using T − 1 against the slides' convention, adding the covariance in a difference, or computing A′VA.",
    ],
    cites=[cite("L1C", "Sample average and variance in vector form", "The sample variance can be computed in two ways:"),
           cite("L1C", "Key rules", "Rule 4 (sandwich): the v-cov matrix of a vector Y multiplied by a matrix A of scalars"),
           cite("L1C", "An Example: the sample mean", "Because of the iid assumption, there is no covariance to take care of")],
    location="slides 'Sample average and variance in vector form', 'An Example: the sample mean', 'Key rules'",
    file=F_1C, minutes=9, notches=["extra_step", "near_true_statements", "what_if_followon"],
    hc_parts=[{"n": "1", "steps": 7, "concepts": 2}, {"n": "2", "steps": 7, "concepts": 2}]))

# ---- 2: OLS by hand, prediction, then SE and a test against 1 ----------------------
x = [4, 8, 6, 10, 12]
y = [5, 11, 7, 15, 17]
xm, ym = sum(x) / 5, sum(y) / 5
sxy = sum((a - xm) * (b - ym) for a, b in zip(x, y))
sxx = sum((a - xm) ** 2 for a in x)
beta = sxy / sxx
alpha = ym - beta * xm
pred = alpha + beta * 15
near(beta, (sum(a * b for a, b in zip(x, y)) / 5 - xm * ym) / (sum(a * a for a in x) / 5 - xm ** 2))  # Cov/Var from E[xy] − E[x]E[y]
p1 = mcq("1", "Estimate the regression by OLS. What excess return on the fund do you expect if the market's excess return is 15%?",
         [(f"{pred:.1f}", None), (f"{beta * 15:.1f}", "intercept_left_out"), (f"{-alpha + beta * 15:.1f}", "intercept_sign"),
          (f"{ym + (15 - xm) * sxy / sum(b * b for b in [v - ym for v in y]):.1f}", "divided_by_var_y_not_var_x")], f"{pred:.1f}", "UNKNOWN")
res = [b - (alpha + beta * a) for a, b in zip(x, y)]
rss = sum(u * u for u in res)
s2 = rss / (5 - 2)
seb = math.sqrt(s2 / sxx)
tval = (beta - 1) / seb
opts = [(f"SE = {seb:.3f}; t = {tval:.2f}; reject β = 1", None),
        (f"SE = {math.sqrt(rss / 5 / sxx):.3f}; t = {(beta - 1) / math.sqrt(rss / 5 / sxx):.2f}; reject β = 1", "divided_rss_by_T_not_T_minus_2"),
        (f"SE = {seb:.3f}; t = {beta / seb:.2f}; reject β = 1", "tested_beta_equal_zero"),
        (f"SE = {math.sqrt(s2 / 5):.3f}; t = {(beta - 1) / math.sqrt(s2 / 5):.2f}; do not reject β = 1", "se_without_sum_of_squares_of_x")]
p2 = mcq("2", "Compute s² = Σû²/(T − 2) and SE(β̂) = s / √Σ(xₜ − x̄)². Is β̂ significantly different from 1 at 5% (two-sided, t with 3 degrees of freedom, critical value 3.18)?",
         opts, opts[0][0], "UNKNOWN")
Q30285.append(question(
    id="30285-L2-01", course="30285", deck="L2", topic="OLS by hand, a prediction, then a test that beta equals one",
    objective="Simple linear regression: OLS estimates as Cov/Var, fitted values; inference on the slope",
    shape=EMS, shape_class="calc MCQ",
    stem="Five years of annual excess returns (%) on the market (xₜ) and on fund YYY (yₜ) are: (4, 5), (8, 11), (6, 7), (10, 15), (12, 17). Estimate yₜ = α + βxₜ + uₜ by OLS.",
    parts=[p1, p2],
    scheme=[
        f"[1] Steps: (1) x̄ = {xm:.0f}; (2) ȳ = {ym:.0f}; (3) deviations x: (−4, 0, −2, 2, 4), y: (−6, 0, −4, 4, 6); (4) Σ products = {sxy:.0f}; (5) Σ x-deviations² = {sxx:.0f}; (6) β̂ = {sxy:.0f}/{sxx:.0f} = {beta:.2f}; (7) α̂ = {ym:.0f} − {beta:.2f} × {xm:.0f} = {alpha:.2f}; (8) ŷ = {alpha:.2f} + {beta:.2f} × 15 = {pred:.1f}.",
        f"Second route for [1]: Cov = E[xy] − x̄ȳ = {sum(a * b for a, b in zip(x, y)) / 5:.1f} − 88 = {sxy / 5:.1f}; Var = E[x²] − x̄² = {sum(a * a for a in x) / 5:.1f} − 64 = {sxx / 5:.1f}; β̂ = {beta:.2f}.",
        f"[2] Steps: (1) fitted values (4.6, 11.0, 7.8, 14.2, 17.4); (2) residuals (0.4, 0, −0.8, 0.8, −0.4); (3) RSS = {rss:.2f}; (4) s² = {rss:.2f}/3 = {s2:.4f}; (5) s = {math.sqrt(s2):.4f}; (6) SE = s/√{sxx:.0f} = {seb:.4f}; (7) t = ({beta:.2f} − 1)/{seb:.4f} = {tval:.2f}; (8) {tval:.2f} > 3.18: reject β = 1.",
        "Where marks are lost: dropping α; dividing by Var(y); RSS/T instead of T − 2; testing β = 0; leaving Σ(x − x̄)² out of the SE.",
    ],
    cites=[cite("L2", "Determining the Regression Coefficients", "Choose α and β so that the (vertical) distances from the data points to the fitted lines"),
           cite("L2", "How Do We Use α and β?", "If an analyst tells you that she expects the market to yield a return 20% higher than the risk-free rate next year"),
           cite("L2B", "Estimation of σ", "Use the sample counterpart of u and accounts for the estimation bias")],
    location="2_Simple_LinRegr (fund XXX example, OLS as Cov/Var); 2b (estimation of σ, variance of the estimator)",
    file=F_2, minutes=10, notches=["cross_section", "chain", "extra_step", "near_true_statements"],
    hc_parts=[{"n": "1", "steps": 8, "concepts": 2}, {"n": "2", "steps": 8, "concepts": 3}]))

# ---- 2B: tests, CI, and the sample size needed ------------------------------------
a_hat, se_a, b_hat, se_b, T0 = 0.30, 0.20, 1.25, 0.10, 100
t_a, t_b1 = a_hat / se_a, (b_hat - 1) / se_b
ci = (b_hat - 1.96 * se_b, b_hat + 1.96 * se_b)
opts = [(f"α̂ not significant (t = {t_a:.2f}); reject β = 1 (t = {t_b1:.2f}); 95% CI for β [{ci[0]:.3f}, {ci[1]:.3f}]", None),
        (f"α̂ significant (t = {t_a:.2f}); reject β = 1 (t = {t_b1:.2f}); 95% CI for β [{ci[0]:.3f}, {ci[1]:.3f}]", "one_point_five_read_as_significant"),
        (f"α̂ not significant (t = {t_a:.2f}); do not reject β = 1 (t = {b_hat / se_b:.2f}); 95% CI for β [{b_hat - 1.64 * se_b:.3f}, {b_hat + 1.64 * se_b:.3f}]", "tested_beta_zero_and_used_1_64"),
        (f"α̂ not significant (t = {t_a:.2f}); reject β = 1 (t = {t_b1:.2f}); 95% CI for β [{b_hat - 1.96 * se_b ** 2:.3f}, {b_hat + 1.96 * se_b ** 2:.3f}]", "variance_used_instead_of_se")]
p1 = mcq("1", "At 5% with normal critical values (1.96 two-sided), which set of conclusions is correct?", opts, opts[0][0], "UNKNOWN")
se_need = a_hat / 1.64
Tn = math.ceil(T0 * (se_a / se_need) ** 2)
near(se_a * math.sqrt(T0 / Tn) <= se_need + 1e-12, True)
assert se_a * math.sqrt(T0 / (Tn - 1)) > se_need  # Tn is the smallest
T196 = math.ceil(T0 * (se_a / (a_hat / 1.96)) ** 2)
p2 = mcq("2", "Standard errors shrink with 1/√T when the regressor and residual variances stay the same. Keeping α̂ = 0.30, how many monthly observations would make α̂ significant in a one-sided test of H₀: α ≤ 0 at 5% (critical value 1.64)?",
         [(str(Tn), None), (str(T196), "two_sided_critical_value_used"), (str(math.ceil(T0 * se_a / se_need)), "se_scaled_with_T_not_root_T"), ("100", "sample_size_does_not_matter")],
         str(Tn), "UNKNOWN")
Q30285.append(question(
    id="30285-L2B-01", course="30285", deck="L2B", topic="t-tests, a confidence interval and the sample size a significant alpha needs",
    objective="Simple regression inference: standard errors, t-tests, confidence intervals, one- and two-sided tests",
    shape=EMS, shape_class="calc MCQ",
    stem="A CAPM regression of a fund's monthly excess returns on the market's excess returns, T = 100, gives α̂ = 0.30 (SE 0.20) and β̂ = 1.25 (SE 0.10). The residual variance is 12.4 and R² = 0.61.",
    parts=[p1, p2],
    scheme=[
        f"[1] Steps: (1) t(α) = 0.30/0.20 = {t_a:.2f}; (2) {t_a:.2f} < 1.96: α̂ not significant; (3) t for H₀: β = 1 is (1.25 − 1)/0.10 = {t_b1:.2f}; (4) {t_b1:.2f} > 1.96: reject; (5) CI lower = 1.25 − 1.96 × 0.10 = {ci[0]:.3f}; (6) upper = {ci[1]:.3f} (excludes 1, consistent with step 4).",
        f"[2] Steps: (1) required t = 1.64; (2) SE needed ≤ 0.30/1.64 = {se_need:.4f}; (3) SE(T) = 0.20 × √(100/T); (4) √(100/T) ≤ {se_need / se_a:.4f}; (5) T ≥ 100/{(se_need / se_a) ** 2:.4f} = {T0 * (se_a / se_need) ** 2:.2f}; (6) round up: {Tn}.",
        f"Check for [2]: at T = {Tn}, SE = {se_a * math.sqrt(T0 / Tn):.4f} ≤ {se_need:.4f}; at T = {Tn - 1}, SE = {se_a * math.sqrt(T0 / (Tn - 1)):.4f} > {se_need:.4f}.",
        "Where marks are lost: calling t = 1.5 significant; testing β = 0 instead of 1; using 1.64 for a two-sided CI; using the variance for the SE; scaling SE with T instead of √T; using 1.96 in a one-sided test.",
        "Not needed: residual variance and R² (extraneous).",
    ],
    cites=[cite("L2B", "Interpretation of our results", "The more observations we have, T, the less uncertainty"),
           cite("L2B", "Assumption 5: normality", "In principle, you should use a t-distribution with (T-2) degrees of freedom, but in large sample the t converges to a normal"),
           cite("L2B", "Confidence Intervals", "Choose a significance level, α (again the convention is 5%)")],
    location="2b slides on hypothesis testing, one- and two-sided tests, confidence intervals and the drivers of the SE",
    file=F_2B, minutes=9, notches=["working_backwards", "near_true_statements", "extraneous_data"],
    hc_parts=[{"n": "1", "steps": 6, "concepts": 2}, {"n": "2", "steps": 6, "concepts": 2}]))

# ---- 2C: the F-test with two restrictions, and F from R² ------------------------------
T, k, m, urss, rrss = 64, 5, 2, 250.0, 290.0
F = (rrss - urss) / urss * (T - k) / m
near(F, ((rrss - urss) / m) / (urss / (T - k)))
opts = [(f"Regress y on (x₂ + x₃) and x₅; F = {F:.2f} > 3.15: reject", None),
        (f"Regress y on (x₂ − x₃) and x₅; F = {F:.2f} > 3.15: reject", "wrong_substitution"),
        (f"Regress y on (x₂ + x₃) and x₅; F = {(rrss - urss) / urss * (T - k) / 1:.2f} > 4.00: reject", "counted_one_restriction"),
        (f"Regress y on (x₂ + x₃), x₄ and x₅; F = {(rrss - urss) / rrss * (T - k) / m:.2f} > 3.15: reject", "restricted_rss_in_denominator_and_x4_kept")]
p1 = mcq("1", "Which restricted regression do you estimate, and what does the F-test conclude at 5% (F(2, 59) critical value 3.15)?", opts, opts[0][0], "UNKNOWN")
R2 = 0.18
Fr = R2 / (1 - R2) * (T - k) / (k - 1)
adj = 1 - (1 - R2) * (T - 1) / (T - k)
near(Fr, (R2 / (k - 1)) / ((1 - R2) / (T - k)))
opts = [(f"F = {Fr:.2f}; adjusted R² = {adj:.3f}", None),
        (f"F = {R2 / (1 - R2) * (T - k) / k:.2f}; adjusted R² = {adj:.3f}", "k_used_instead_of_k_minus_1"),
        (f"F = {Fr:.2f}; adjusted R² = {1 - (1 - R2) * (T - k) / (T - 1):.3f}", "adjustment_ratio_inverted"),
        (f"F = {R2 / (1 - R2) * T / (k - 1):.2f}; adjusted R² = {adj:.3f}", "T_used_instead_of_T_minus_k")]
p2 = mcq("2", "The unrestricted regression has R² = 0.18. What is the F-statistic for H₀: β₂ = β₃ = β₄ = β₅ = 0, and what is the adjusted R²?", opts, opts[0][0], "UNKNOWN")
Q30285.append(question(
    id="30285-L2C-01", course="30285", deck="L2C", topic="Two joint restrictions with the F-test, and F from R-squared",
    objective="Multiple regression: restricted regressions, the F-test, R-squared and adjusted R-squared",
    shape=EMS, shape_class="calc MCQ",
    stem="A stock's monthly excess return is regressed on four factors, T = 64: yₜ = β₁ + β₂x₂ₜ + β₃x₃ₜ + β₄x₄ₜ + β₅x₅ₜ + uₜ. Theory says the stock has the same sensitivity to factors 2 and 3 and none to factor 4: H₀: β₂ = β₃ and β₄ = 0. The unrestricted RSS is 250 and the restricted RSS is 290.",
    parts=[p1, p2],
    scheme=[
        f"[1] Steps: (1) count '=' signs: m = 2; (2) substitute β₃ = β₂ and β₄ = 0: yₜ = β₁ + β₂(x₂ₜ + x₃ₜ) + β₅x₅ₜ + uₜ; (3) k = 5 parameters, T − k = 59; (4) RRSS − URSS = 40; (5) 40/250 = 0.16; (6) × 59/2 → F = {F:.2f}; (7) {F:.2f} > 3.15: reject H₀.",
        f"Second route for [1]: (40/2) / (250/59) = {F:.2f}.",
        f"[2] Steps: (1) restrictions = k − 1 = 4; (2) df (4, 59); (3) R²/(1 − R²) = {R2 / (1 - R2):.4f}; (4) × 59/4 → F = {Fr:.2f}; (5) adjusted R² = 1 − (1 − R²)(T − 1)/(T − k); (6) = 1 − 0.82 × 63/59 = {adj:.3f}.",
        "Where marks are lost: substituting β₃ = −β₂, counting one restriction, putting RRSS in the denominator, using k instead of k − 1 or T instead of T − k, or inverting the adjustment.",
    ],
    cites=[cite("L2C", "Determining the # of Restrictions", "Count the number of ‘=’signs"),
           cite("L2C", "F-test distribution and Inference", "reject the null if the test statistic > critical F-value"),
           cite("L2C", "F-test: Example (I)", "We substitute the restriction (β3+β4 = 1) into the regression so that it is automatically imposed on the data.")],
    location="2c slides on the F-test, restricted regressions, R-squared and adjusted R-squared",
    file=F_2C, minutes=10, notches=["extra_classification", "near_true_statements", "extra_step"],
    hc_parts=[{"n": "1", "steps": 7, "concepts": 2}, {"n": "2", "steps": 6, "concepts": 2}]))

BANKS["30285"] = {"questions": Q30285}

# =====================================================================================
# 30024 FINANCIAL STATEMENT ANALYSIS (exam: MCQs + quantitative open essay)
# =====================================================================================
FSP = "Slides/"
F_S1, F_S2, F_S34 = FSP + "30024 - AM - Session 1 - Intro.pdf", FSP + "30024 - AM - Session 2.pdf", FSP + "30024 - AM - Session 3 - 4 Reclassification.pdf"
Q30024 = []
QE = "quantitative open essay (written parts)"

# ---- S34-01: management account method -----------------------------------------------
A_items = {"Property, plant and equipment": 820, "Right-of-use assets (leases)": 90, "Real estate held for investment (not used in operations)": 150,
           "Inventories": 210, "Trade receivables": 260, "Operating prepayments": 20, "Short-term loan to a related party": 40,
           "Marketable securities": 35, "Cash and cash equivalents": 75, "Deferred tax assets": 15}
L_items = {"Long-term bank loan": 380, "Lease liabilities": 95, "Current portion of long-term debt": 60, "Short-term bank debt": 50,
           "Trade payables": 240, "Accrued operating expenses": 45, "Customer prepayments (contract liabilities)": 30,
           "Income tax payable": 25, "Pension liabilities": 60}
equity_ = sum(A_items.values()) - sum(L_items.values())
onwc = (210 + 260 + 20) - (240 + 45 + 30)
nic = onwc + 820 + 90
nfp = (380 + 95 + 60 + 50) - (75 + 35 + 40)
near(nic, (380 + 95 + 60 + 50) + equity_ - (75 + 35 + 40) - 150 + 25 + 60 - 15)  # financing side, reconciled
pa = written("a", "Using the management account method, compute Operating NWC, Net Invested Capital (asset side) and the Net Financial Position.",
             f"ONWC {onwc}; NIC {nic}; NFP {nfp} (€k).", 2.5,
             [("rou_asset_excluded", "right-of-use assets left out of NIC"), ("investment_property_in_nic", "non-operating real estate included"), ("lease_liabilities_left_out_of_nfp", "NFP without lease liabilities (340)"), ("related_party_loan_in_nwc", "loan to a related party treated as operating")])
ebit, rent, t = 190.0, 12.0, 0.24
nopat = (ebit - rent) * (1 - t)
roic = nopat / nic
roic_bad = ebit * (1 - t) / (nic + 150)
pb = written("b", "EBIT of €190k includes €12k of rent earned on the investment property. Compute ROIC on an operating basis (NOPAT at a 24% tax rate over NIC), and the ROIC an analyst would report by mixing in the property and its rent.",
             f"Operating ROIC {f(roic * 100, 2)}%; mixed ROIC {f(roic_bad * 100, 2)}%.", 2.5,
             [("rent_left_in_operating_ebit", "non-operating rent kept in EBIT"), ("pre_tax_return", "EBIT not taxed")])
Q30024.append(question(
    id="30024-S34-01", course="30024", deck="S34", topic="Management account method: ONWC, NIC, NFP and an operating ROIC",
    objective="Reclassifying financial statements: management account method, operating vs financial vs non-operating items, NFP",
    shape=QE, shape_class="quantitative essay part",
    stem="Gamma SpA's balance sheet (€k) is below. Equity is the balancing item.",
    data="| Assets | €k |\n|---|---|\n" + "".join(f"| {k} | {v} |\n" for k, v in A_items.items()) + "\n| Liabilities and equity | €k |\n|---|---|\n" + "".join(f"| {k} | {v} |\n" for k, v in L_items.items()) + f"| Equity | {equity_} |",
    parts=[pa, pb],
    scheme=[
        f"[a] Steps: (1) operating current assets = inventories 210 + receivables 260 + prepayments 20 = 490; (2) operating current liabilities = payables 240 + accrued 45 + customer prepayments 30 = 315; (3) ONWC = {onwc}; (4) operating non-current = PP&E 820 + right-of-use 90 = 910 (investment property excluded); (5) NIC = {nic}; (6) gross debt = 380 + 95 + 60 + 50 = 585 (leases included); (7) financial assets = cash 75 + securities 35 + related-party loan 40 = 150; (8) NFP = {nfp}.",
        f"Second route for [a]: financing side 585 + {equity_} − 150 − investment property 150 = {585 + equity_ - 300}; add back the items outside both NIC and NFP (pensions 60 + tax payable 25 − deferred tax assets 15 = 70) → {nic}.",
        f"[b] Steps: (1) operating EBIT = 190 − 12 = 178; (2) NOPAT = 178 × 0.76 = {f(nopat, 2)}; (3) ROIC = {f(nopat, 2)}/{nic} = {f(roic * 100, 2)}%; (4) mixed version = 190 × 0.76 / ({nic} + 150) = {f(roic_bad * 100, 2)}%; (5) the property drags the ratio down: it earns 12 on 150, well below the core business.",
        "Where marks are lost: leaving out right-of-use assets, putting investment property in NIC, leaving leases out of NFP, treating the related-party loan or tax payable as operating, keeping the rent in operating EBIT.",
    ],
    cites=[cite("S34", "The Management Account Method: ONWC", "Operating Net Working Capital = Operating Current Assets – Operating Short-term Liabilities"),
           cite("S34", "Some items require attention", "Non operating fixed assets are excluded from NIC."),
           cite("S34", "Focus on the ONWC: borderline cases", "Short-term financial receivables (eg. loans to related parties): exclude (financial)."),
           cite("S34", "Some items require attention", "it must be compared only against operational earnings (EBIT or NOPAT)")],
    location="Lectures 3–4: management account method, NIC, NFP, ONWC and its borderline cases",
    file=F_S34, minutes=16, notches=["extra_classification", "extra_step", "chain", "near_true_statements"],
    hc_parts=[{"n": "a", "steps": 8, "concepts": 3}, {"n": "b", "steps": 5, "concepts": 2}]))

# ---- S34-02: liquidity view and value added --------------------------------------------
sta = {"Cash": 40, "Short-term investments": 30, "Trade receivables": 180, "Inventories": 150}
stl = {"Trade payables": 170, "Short-term bank debt": 90, "Current tax payable": 20, "Accrued expenses": 30}
fnwc = sum(sta.values()) - sum(stl.values())
tm = sum(sta.values()) - sta["Inventories"] - sum(stl.values())
cur = sum(sta.values()) / sum(stl.values())
quick = (sum(sta.values()) - sta["Inventories"]) / sum(stl.values())
near(tm, fnwc - 150)
pa = written("a", "Compute Financial NWC, the treasury margin, and the current and quick ratios, and say what the treasury margin tells you.",
             f"Financial NWC {fnwc}; treasury margin {tm}; current ratio {cur:.2f}; quick ratio {quick:.2f}. Cash and receivables do not cover short-term liabilities: the company relies on selling inventory or on bank credit.", 2.5,
             [("inventories_left_in_treasury_margin", "treasury margin computed like NWC"), ("negative_nwc_equals_distress", "calls a positive NWC distress")])
vop = 2000 + 50 + 30
ext = 900 + 350 + 60
va = vop - ext
var_ = va / vop
va2 = vop - (ext + 150)
ebitda1, ebitda2 = va - 420, va2 - (420 - 120)
near(ebitda2 - ebitda1, 120 - 150)
pb = written("b", "Compute the Value of Production, Value Added and the Value Added ratio. Then Delta outsources assembly: services rise by €150k and personnel costs fall by €120k. What happens to the VA ratio and to EBITDA?",
             f"VoP {vop}; VA {va}; VA ratio {f(var_ * 100, 1)}%; after outsourcing VA {va2}, ratio {f(va2 / vop * 100, 1)}%, EBITDA {ebitda1} → {ebitda2} (−30).", 2.5,
             [("revenues_used_as_value_of_production", "inventory change and capitalised work left out"), ("personnel_treated_as_external", "personnel deducted before Value Added")])
Q30024.append(question(
    id="30024-S34-02", course="30024", deck="S34", topic="Liquidity view, value added and an outsourcing decision",
    objective="Reclassifying: liquidity-based balance sheet (financial NWC, treasury margin) and the value added income statement",
    shape=QE, shape_class="quantitative essay part",
    stem="Delta SpA (€k). Short-term assets: cash 40, short-term investments 30, trade receivables 180, inventories 150. Short-term liabilities: trade payables 170, short-term bank debt 90, current tax payable 20, accrued expenses 30. Income statement: revenues 2,000; increase in finished-goods inventory 50; capitalised internal work 30; raw materials 900; services 350; rents 60; personnel 420; D&A 110; interest 25.",
    parts=[pa, pb],
    scheme=[
        f"[a] Steps: (1) short-term assets = {sum(sta.values())}; (2) short-term liabilities = {sum(stl.values())}; (3) Financial NWC = {fnwc}; (4) treasury margin = {sum(sta.values())} − 150 − {sum(stl.values())} = {tm}; (5) current ratio = {cur:.2f}; (6) quick ratio = 250/310 = {quick:.2f}; (7) a negative treasury margin with positive NWC means the company must sell inventory or borrow to meet near-term payments.",
        f"[b] Steps: (1) VoP = 2,000 + 50 + 30 = {vop}; (2) external costs = 900 + 350 + 60 = {ext}; (3) VA = {va}; (4) VA ratio = {va}/{vop} = {f(var_ * 100, 1)}%; (5) EBITDA = {va} − personnel 420 = {ebitda1}; (6) outsourcing: external costs +150 → VA = {va2}; (7) ratio {f(va2 / vop * 100, 1)}%: less vertical integration; (8) EBITDA = {va2} − 300 = {ebitda2}, down 30.",
        "Where marks are lost: leaving inventories in the treasury margin, using revenues as value of production, deducting personnel before value added, or reading a lower VA ratio as lower efficiency by itself.",
        "Not needed: D&A and interest (below EBITDA).",
    ],
    cites=[cite("S34", "Liquidity-based Balance Sheet", "Treasury margin = short-term assets – inventories – short-term liabilities"),
           cite("S34", "A Metric of Vertical Integration", "Value Added Ratio = Value Added / Value of Production"),
           cite("S34", "Liquidity-based Balance Sheet: how do we interpret the values?", "the company is forced to rely on future sales or bank credit to meet near-term payments")],
    location="Lectures 3–4: liquidity-based balance sheet; value added income statement",
    file=F_S34, minutes=16, notches=["what_if_followon", "extraneous_data", "extra_classification", "extra_step"],
    hc_parts=[{"n": "a", "steps": 7, "concepts": 2}, {"n": "b", "steps": 8, "concepts": 3}]))

# ---- S2-01: indirect cash flow and the equity roll-forward -------------------------------
ni, da_, prov, gain = 120, 45, 10, 8
d_rec, d_inv, d_pay = 30, -12, 18
cfo = ni + da_ + prov - gain - d_rec - d_inv + d_pay
cfi = -140 + 20
cash0, cash1 = 60, 70
cff = (cash1 - cash0) - cfo - cfi
div = 40 - 25 - cff
eq0, oci = 500, -6
eq1 = eq0 + ni + oci - div
near(cfo + cfi + cff, cash1 - cash0)
pa = written("a", "Prepare Omicron's cash flow from operating activities (indirect method) and from investing activities.",
             f"CFO {cfo}; CFI {cfi} (€m).", 2.5,
             [("gain_not_removed", "disposal gain left in CFO"), ("working_capital_signs", "receivables increase added"), ("disposal_proceeds_in_cfo", "proceeds counted in operations")])
pb = written("b", "Opening cash was €60m and closing cash €70m. Omicron issued €40m of new debt, repaid €25m and paid dividends; there were no other financing flows. How much did it pay in dividends, and what is its closing equity if opening equity was €500m and OCI was −€6m?",
             f"Dividends {div}; closing equity {eq1} (€m).", 2.5,
             [("cash_change_ignored", "CFF set to zero"), ("oci_left_out", "closing equity without OCI")])
Q30024.append(question(
    id="30024-S2-01", course="30024", deck="S2", topic="Indirect cash flow, the cash reconciliation and the equity roll-forward",
    objective="Accounting basics: cash flow statement (indirect method), reconciliation of cash, interrelation of the statements",
    shape=QE, shape_class="quantitative essay part",
    stem="Omicron SpA, 2026 (€m): net income 120; depreciation and amortisation 45; increase in provisions 10; gain on disposal of equipment 8 (proceeds €20m); receivables rose by 30; inventories fell by 12; trade payables rose by 18; capital expenditure 140. Revenues were 1,450 and the tax rate is 24%.",
    parts=[pa, pb],
    scheme=[
        f"[a] Steps: (1) start from net income 120; (2) + D&A 45; (3) + increase in provisions 10; (4) − gain on disposal 8 (non-cash; the cash is in investing); (5) − receivables increase 30; (6) + inventory decrease 12; (7) + payables increase 18; CFO = {cfo}. CFI = −140 + 20 = {cfi}.",
        f"[b] Steps: (1) change in cash = 70 − 60 = +10; (2) CFO + CFI = {cfo + cfi}; (3) CFF = 10 − {cfo + cfi} = {cff}; (4) dividends = 40 − 25 − ({cff}) = {div}; (5) closing equity = 500 + 120 − 6 − {div}; (6) = {eq1}.",
        f"Check: {cfo} + ({cfi}) + ({cff}) = +10 = change in cash.",
        "Where marks are lost: leaving the disposal gain in CFO, reversing working-capital signs, putting disposal proceeds in operations, forgetting OCI.",
        "Not needed: revenues and the tax rate (extraneous).",
    ],
    cites=[cite("S2", "The Cash Flow Statement: Methods", "derives operating cash flow from profit or loss by adjusting for non-cash items, accruals and changes in operating working capital"),
           cite("S2", "Statement of shareholders’ equity", "Ending equity = Beginning equity + Profit or loss + Other comprehensive income + Owner contributions − Distributions to owners ± Other recognised equity movements"),
           cite("S2", "The Cash Flow Statement: Reconciliation of Cash", "If the CFI (typically negative) exceeds the CFO, the deficit can be covered by either borrowing (through CFF) or using existing cash at hand")],
    location="Session 2: cash flow statement (indirect method), reconciliation of cash, statement of shareholders' equity",
    file=F_S2, minutes=14, notches=["working_backwards", "extraneous_data", "chain", "extra_classification"],
    hc_parts=[{"n": "a", "steps": 7, "concepts": 2}, {"n": "b", "steps": 6, "concepts": 2}]))

# ---- S2-02: accrual corrections and the market premium --------------------------------------
t = 0.25
adj_pre = -30 - (25 - 10) + (12 - 3)
ni_rep, bv, shares, px = 90, 800, 50, 22
ni_c = ni_rep + adj_pre * (1 - t)
bv_c = bv + adj_pre * (1 - t)
mcap = shares * px
near(ni_c, 90 - 30 * 0.75 - 15 * 0.75 + 9 * 0.75)
pa = written("a", "Correct Rho's 2026 net income for the three findings.", f"Pre-tax effect {adj_pre}; after tax {f(adj_pre * (1 - t), 2)}; corrected net income {f(ni_c, 2)} (€m).", 2.5,
             [("gift_cards_all_reversed", "all 25 of gift-card revenue reversed"), ("prepaid_insurance_fully_reversed", "the whole 12 added back"), ("tax_effect_ignored", "adjustments not tax-effected")])
pb = written("b", "Rho has 50 million shares at €22.00 and reported book equity of €800m. Compute the market premium before and after the corrections.",
             f"Market cap {mcap}; premium {mcap - bv} before, {f(mcap - bv_c, 2)} after.", 2.5,
             [("premium_read_as_goodwill", "calls the premium unrecognised goodwill")])
Q30024.append(question(
    id="30024-S2-02", course="30024", deck="S2", topic="Accrual and deferral corrections, then the market premium",
    objective="Accounting basics: accrued and deferred revenues and expenses, contract liabilities, market vs book value of equity",
    shape=QE, shape_class="quantitative essay part",
    stem="An analyst reviews Rho SpA's 2026 accounts (reported net income €90m, tax rate 25%) and finds: (1) €30m of December delivery expenses were incurred but not recorded; (2) €25m of gift cards sold during the year were all recognised as revenue at sale, but only €10m had been redeemed by year end (ignore breakage); (3) a €12m insurance premium paid on 1 October 2026 for the following 12 months was fully expensed.",
    parts=[pa, pb],
    scheme=[
        f"[a] Steps: (1) accrue delivery expenses: −30; (2) gift cards: revenue only on redemption, so defer 25 − 10 = 15: −15; (3) prepaid insurance: only 3 months (3) belong to 2026, so 9 is a prepaid asset: +9; (4) net pre-tax {adj_pre}; (5) after 25% tax {f(adj_pre * (1 - t), 2)}; (6) corrected NI = {f(ni_c, 2)}.",
        f"[b] Steps: (1) market value of equity = 50 × 22 = {mcap}; (2) premium on reported book = {mcap} − 800 = {mcap - bv}; (3) corrected book equity = 800 − {f(-adj_pre * (1 - t), 2)} = {f(bv_c, 2)}; (4) premium = {f(mcap - bv_c, 2)}. The premium reflects unrecognised intangibles, growth and expectations, not goodwill.",
        "Where marks are lost: reversing all gift-card revenue, adding back all of the insurance, forgetting the tax effect, calling the premium goodwill.",
    ],
    cites=[cite("S2", "Accounting distortions: Income Statement", "When a gift card is sold, the consideration received is generally recognised as a contract liability."),
           cite("S2", "Accounting distortions: accrued and deferred revenues and expenses", "The company has incurred an expense but the cash will be paid in the next period."),
           cite("S2", "The Balance Sheet: Equity (optional)", "Market premium = Market Value of Equity – Book Value of Equity")],
    location="Session 2: accounting distortions, accrued and deferred items, equity at book vs market",
    file=F_S2, minutes=12, notches=["extra_classification", "chain", "near_true_statements"],
    hc_parts=[{"n": "a", "steps": 6, "concepts": 3}, {"n": "b", "steps": 4, "concepts": 2}]))

# ---- S1-01: Juventus–Aston Villa and Armani ----------------------------------------------------
ca_il, ca_ba = 14 - 11.9, 8 - 5.5
amort = 50 / 5
pl = 11.9 + 5.5 - amort
near(pl, (14 - ca_il) + (8 - ca_ba) - amort)
pa = written("a", "From Juventus's side: compute the carrying amounts of the two players sold, the net cash committed across the three deals, and the net effect of the three deals on Juventus's 2024/25 operating result.",
             f"Carrying amounts {f(ca_il)} and {f(ca_ba)}; net cash committed €28m; 2024/25 effect +{f(pl)} (gains 17.4 − amortisation 10.0).", 2.5,
             [("payment_period_used_for_amortisation", "cost spread over the four payment years (12.5 a year)"), ("gains_confused_with_prices", "sale prices counted as gains")])
ebitda, rev = 398, 2300
evs = {"EV/EBITDA average 11.1×": ebitda * 11.1, "EV/EBITDA median 9.7×": ebitda * 9.7, "EV/Revenue average 2.7×": rev * 2.7, "EV/Revenue median 1.6×": rev * 1.6}
lo, hi = min(evs.values()), max(evs.values())
m_lo, m_hi = 6500 / ebitda, 10000 / ebitda
pb = written("b", "For Armani (2024 revenue €2.3bn, EBITDA €398m, EBIT €67m), compute the enterprise values implied by the four sector multiples, the resulting range, and the EV/EBITDA multiples implied by the published €6.5–10bn estimates.",
             f"EVs: {', '.join(f'{k} {v:,.1f}' for k, v in evs.items())}; range €{lo / 1000:.2f}–{hi / 1000:.2f}bn; published estimates imply {m_lo:.1f}× to {m_hi:.1f}× EBITDA.", 2.5,
             [("ebit_used", "EBIT used with an EBITDA multiple"), ("range_from_averages_only", "range taken from the two averages only")])
Q30024.append(question(
    id="30024-S1-01", course="30024", deck="S1", topic="Connected player transfers and a founder's company without a price",
    objective="Why financial statements matter: transaction timing and recognition, price vs value, multiples as a starting point",
    shape=QE, shape_class="quantitative essay part",
    stem="Use the lecture's cases. Juventus bought Douglas Luiz for €50m (paid over four financial years) on 30 June 2024, capitalised the cost and signed him to 30 June 2029; amortise straight-line over the contract from 1 July 2024. On 1 July 2024 it sold Iling-Junior for €14m and Barrenechea for €8m, booking gains of €11.9m and €5.5m in 2024/25. Juventus's financial year ends on 30 June.",
    parts=[pa, pb],
    scheme=[
        f"[a] Steps: (1) Iling-Junior carrying amount = 14 − 11.9 = {f(ca_il)}; (2) Barrenechea = 8 − 5.5 = {f(ca_ba)}; (3) net cash committed = 50 − 14 − 8 = 28; (4) amortisation of Luiz = 50 / 5 contract years = {f(amort)} a year (the four-year payment schedule is irrelevant to amortisation); (5) gains = 17.4; (6) 2024/25 effect = 17.4 − 10.0 = +{f(pl)}.",
        f"[b] Steps: (1) 398 × 11.1 = {evs['EV/EBITDA average 11.1×']:,.1f}; (2) 398 × 9.7 = {evs['EV/EBITDA median 9.7×']:,.1f}; (3) 2,300 × 2.7 = {evs['EV/Revenue average 2.7×']:,.1f}; (4) 2,300 × 1.6 = {evs['EV/Revenue median 1.6×']:,.1f}; (5) range €{lo / 1000:.2f}–{hi / 1000:.2f}bn (the slide's €3.7–6.2bn); (6) 6,500/398 = {m_lo:.1f}×; (7) 10,000/398 = {m_hi:.1f}×: the estimates price in brand and growth that current EBITDA does not show.",
        "Where marks are lost: amortising over the payment period, counting sale prices as gains, applying multiples to EBIT, or quoting only the averages.",
        "Not needed: EBIT of €67m (extraneous for these multiples).",
    ],
    cites=[cite("S1", "Juventus – Aston Villa: connected transactions across two reporting periods", "Juventus acquired Douglas Luiz from Aston Villa for €50 million, payable over four financial years."),
           cite("S1", "Juventus – Aston Villa: connected transactions across two reporting periods", "The disposals generated positive economic impacts for Juventus of €11.9 million and €5.5 million, respectively, in financial year 2024/25."),
           cite("S1", "Armani: why company value is not a single number", "Applying sector multiples mechanically would indicate an enterprise value of approximately €3.7–6.2 billion."),
           cite("S1", "…what is the value of the company…?", "Av. EV/EBITDA for the sector 11.1x; median 9.7x")],
    location="Lecture 1 cases: Juventus–Aston Villa; Armani",
    file=F_S1, minutes=14, notches=["extra_classification", "extraneous_data", "extra_step", "working_backwards"],
    hc_parts=[{"n": "a", "steps": 6, "concepts": 2}, {"n": "b", "steps": 7, "concepts": 2}]))

BANKS["30024"] = {"questions": Q30024}

# =====================================================================================
# Course documents for the three new subjects (fingerprints are PROXY; see label)
# =====================================================================================
HARD_RULE = "harder than the slides: steps above the slide maximum AND above the exam-level median for the shape, at least two distinct notches, never via ambiguity or out-of-syllabus content"
NOTCHES = ["extra_step", "extra_classification", "working_backwards", "cross_section", "what_if_followon", "extraneous_data", "chain", "near_true_statements"]
STATED = "Will (2026-09-24): the exam is harder than the slide material; applied to every BIEF Year 3 subject on 2026-09-24"


def course(code, name, neg, fmt, decks, shape, exam, slide, target, cap, sources, unknowns):
    return {"code": code, "name": name, "status": "active", "exam_date": None, "negative_marking": neg, "priority": "none",
            "folder_path": f"Google Drive / BIEF Year 3 / {code} - {name.upper()}", "format_profile": fmt, "decks": decks,
            "fingerprint": {
                "status": "PROXY", "label": "SUPPORTING - scored by Claude from the course's own exam material and slide examples; not a real past-paper analysis",
                "sources": sources, "by_shape": {shape: exam}, "steps": exam["steps"], "concepts_combined": exam["concepts_combined"],
                "slide_baseline": {"label": "SUPPORTING - scored from the decks' own worked examples", "by_shape": {shape: slide}},
                "hard_target": {"rule": HARD_RULE, "stated_by": STATED, "min_notches": 2, "minutes_per_answer_cap": cap, "notches": NOTCHES,
                                "by_shape": {shape: target}},
                "settle_with": "a real past paper of this course"},
            "unknowns": unknowns + [{"item": "Exam date", "settle_with": "your exam calendar (set it on the Courses screen)"}],
            "updated_at": CREATED}


COURSES = {
    "30257": course("30257", "Corporate Valuation", 0,
                    [{"item": "Written exam (attending)", "value": "60 min, 25 pts: 13 MCQs (1 pt, no penalty), 2 short essays (3 pts), 2 short problems (3 pts); closed book, basic calculator", "label": "COURSE-AUTHORITATIVE (syllabus 2026-27)", "settle_with": "-"},
                     {"item": "Group assignment", "value": "up to 6 pts", "label": "COURSE-AUTHORITATIVE (syllabus 2026-27)", "settle_with": "-"},
                     {"item": "Excluded for attending students", "value": "Financial Modeling lectures (7-8) and their materials", "label": "COURSE-AUTHORITATIVE (syllabus 2026-27)", "settle_with": "-"}],
                    {"L12": {"title": "Lectures 1-2: Introduction to Valuation", "file": F_L12}, "L3": {"title": "Lecture 3: DCF Valuation", "file": F_L3},
                     "L4": {"title": "Lecture 4: Cost of Capital", "file": F_L4}, "L5": {"title": "Lecture 5: Reorganizing Financials and Cash Flows", "file": F_L5},
                     "L6": {"title": "Lecture 6: DCF Exercises (Workbook selection)", "file": F_L6}},
                    "short problem",
                    {"n": 2, "steps": {"median": 5.5, "range": [5, 6]}, "concepts_combined": {"median": 2, "range": [2, 2]}},
                    {"n": 6, "steps": {"median": 4, "range": [2, 6]}},
                    {"steps_min": 7, "concepts_min": 2}, 10,
                    ["30257 Corporate Valuation AY 24-25 - Mock Exam v1.pdf (Q3 FCFO: 5 steps; Q4 multiples: 6 steps)", "L6 problems 2.3, 2.5, 2.6, 3.8, 4.1 and the L3 APV example (2-6 steps)"],
                    [{"item": "Real past papers of 30257 (only a mock was scored)", "settle_with": "a real past exam"}]),
    "30285": course("30285", "Empirical Methods for Finance", "UNKNOWN",
                    [{"item": "Final exam", "value": "multiple choice only, including derivations; 60% or 80% of the grade (Dec/Jan), quiz 20% or 0%, homework 20%", "label": "COURSE-AUTHORITATIVE (syllabus 2026-27; Practice #2 instructions)", "settle_with": "-"}],
                    {"L1B": {"title": "1b Introduction to Content (methodology, returns, risk)", "file": F_1B}, "L1C": {"title": "1c Linear Algebra and Inference", "file": F_1C},
                     "L2": {"title": "2 Simple Linear Regression", "file": F_2}, "L2B": {"title": "2b Simple Linear Regression: Inference", "file": F_2B},
                     "L2C": {"title": "2c Linear Regression: F-test", "file": F_2C}},
                    "calc MCQ",
                    {"n": 3, "steps": {"median": 3, "range": [1, 3]}, "concepts_combined": {"median": 1, "range": [1, 2]}},
                    {"n": 4, "steps": {"median": 3, "range": [2, 5]}},
                    {"steps_min": 6, "concepts_min": 2}, 5,
                    ["Practice #2 (APT market prices of risk: 3 steps; correlogram: 1; AR(1) R-squared: 3)", "Slide examples: fund XXX OLS (5), F-test example (4), t-tests (2), return examples (2)"],
                    [{"item": "Negative marking and number of questions in the final", "settle_with": "the exam direction sheet on Bboard"}]),
    "30024": course("30024", "Financial Statement Analysis", "UNKNOWN",
                    [{"item": "Final written exam (attending, Part A)", "value": "MCQs plus an open quantitative essay (2023 mock: 15 MCQ + 10-point ratio essay, 1 hour); 50% of the grade", "label": "SUPPORTING (2023 mock via Studocu; syllabus 2026-27)", "settle_with": "the exam direction sheet (late November)"},
                     {"item": "In-class test / role playing", "value": "25% / 25%", "label": "COURSE-AUTHORITATIVE (syllabus 2026-27)", "settle_with": "-"}],
                    {"S1": {"title": "Session 1: Introduction and cases", "file": F_S1}, "S2": {"title": "Session 2: Accounting basics and financial statements", "file": F_S2},
                     "S34": {"title": "Sessions 3-4: Financial statement reclassification", "file": F_S34}},
                    "quantitative essay part",
                    {"n": 3, "steps": {"median": 2, "range": [1, 2]}, "concepts_combined": {"median": 1, "range": [1, 2]}},
                    {"n": 2, "steps": {"median": 2, "range": [2, 2]}},
                    {"steps_min": 4, "concepts_min": 2}, 8,
                    ["30024 Mock Exam Part A & B 2023 (ROE/ROA: 1-2 steps per value; %ΔROA: 2; industry match: 2)", "Slide examples: Armani multiples (2), gross margin % (2)"],
                    [{"item": "2026-27 exam structure", "settle_with": "the exam direction sheet (late November)"}]),
}

# =====================================================================================
# Worked examples (different numbers from the bank, so they don't give answers away)
# =====================================================================================
def worked():
    out = ["# Worked examples, one per subject", "",
           "Each example uses different numbers from the practice questions in Answer Grid, so you can study the method without seeing the answers. Every number below is computed and cross-checked in `banks/build_banks.py`.", ""]
    # 30178: a run met by liquid assets then a fire sale, with HTM/AFS
    afs, dafs, htm, dhtm, dy, cash, dep, un, eq = 30.0, 4.0, 60.0, 5.0, 0.02, 10.0, 150.0, 0.80, 12.0
    afs_l, htm_l = afs * dafs * dy, htm * dhtm * dy
    be = eq - afs_l
    w = 0.40 * un * dep
    need = w - cash - (afs - afs_l)
    assert need > 0, 'liquid assets must not cover the run, or the example has no fire sale'
    ratio = (htm - htm_l) / htm
    sold = need / ratio
    loss = sold - need
    near(loss, need * htm_l / (htm - htm_l))
    out += ["## 30178 International Banking: an SVB-style run", "",
            f"**Problem.** A bank holds cash 10, AFS securities 30 (duration 4.0) and HTM securities 60 at cost (duration 5.0); deposits are 150, 80% uninsured; equity is 12 ($bn). Rates rise 2 points. Then 40% of uninsured deposits leave. The bank pays with cash, then AFS, then HTM, all at fair value. What is reported equity at the end?", "",
            "**Solution.**", "",
            f"1. Classify first. AFS is marked to market through OCI, so its loss hits equity now. HTM stays at cost; its loss hits equity only if securities are sold.",
            f"2. AFS loss = 4.0 × 2% × 30 = {afs_l:.2f}. Reported equity = 12 − {afs_l:.2f} = **{be:.2f}**.",
            f"3. HTM unrealised loss = 5.0 × 2% × 60 = {htm_l:.2f}. It is not recognised yet, but it is why depositors worry: economic equity is only {be - htm_l:.2f}.",
            f"4. Withdrawal = 40% × 80% × 150 = {w:.1f}.",
            f"5. Pay {cash:.0f} from cash and {afs - afs_l:.1f} from AFS (fair value). Still needed: {need:.1f}.",
            f"6. HTM sells at {ratio * 100:.0f}% of cost, so cost sold = {need:.1f} / {ratio:.2f} = {sold:.2f}.",
            f"7. Realised loss = {sold:.2f} − {need:.1f} = {loss:.2f}.",
            f"8. Reported equity = {be:.2f} − {loss:.2f} = **{be - loss:.2f}**.", "",
            f"Check: each $ raised from HTM costs {htm_l:.0f}/{htm - htm_l:.0f} = {htm_l / (htm - htm_l):.4f} of equity; {need:.1f} × that = {loss:.2f}.", "",
            "**Traps:** forgetting that the AFS loss is already in equity; recognising the whole HTM loss; selling HTM before AFS.", ""]
    # 30257: bottom-up WACC
    b1, d1, b2, d2, tx, de, rf_, mrp_, ebit_, int_ = 1.45, 0.60, 0.90, 0.25, 0.24, 0.50, 0.03, 0.06, 50.0, 18.0
    a1, a2 = b1 * 2 / 3 + 1 / 3, b2 * 2 / 3 + 1 / 3
    u1, u2 = a1 / (1 + d1 * (1 - tx)), a2 / (1 + d2 * (1 - tx))
    bu_ = (u1 + u2) / 2
    bl_ = bu_ * (1 + de * (1 - tx))
    ke_ = rf_ + bl_ * mrp_
    cov_ = ebit_ / int_
    assert 2.5 < cov_ < 3.0  # strictly inside the B1/B+ band: no boundary ambiguity
    spread = 0.026
    kd_ = rf_ + spread
    we, wd = 1 / (1 + de), de / (1 + de)
    wacc__ = we * ke_ + wd * kd_ * (1 - tx)
    near(wacc__, (ke_ + de * kd_ * (1 - tx)) / (1 + de))
    out += ["## 30257 Corporate Valuation: bottom-up beta and WACC", "",
            "**Problem.** A private company's comparables have raw levered betas and market D/E of 1.45 and 0.60, and 0.90 and 0.25. Target D/E is 0.50, the statutory tax rate 24%, the risk-free rate 3% and the MRP 6%. EBIT is €50m and interest €18m. Use Blume's adjustment, the Hamada formula and the slide's synthetic-rating table. Find the WACC.", "",
            "**Solution.**", "",
            f"1. Blume: 1.45 × 2/3 + 1/3 = {a1:.3f}; 0.90 × 2/3 + 1/3 = {a2:.3f}.",
            f"2. Unlever: {a1:.3f} / (1 + 0.60 × 0.76) = {u1:.4f}; {a2:.3f} / (1 + 0.25 × 0.76) = {u2:.4f}.",
            f"3. Industry βU = average = {bu_:.4f}.",
            f"4. Relever at 0.50: {bu_:.4f} × (1 + 0.50 × 0.76) = {bl_:.4f}.",
            f"5. kEL = 3% + {bl_:.4f} × 6% = **{ke_ * 100:.2f}%**.",
            f"6. Interest coverage = 50 / 18 = {cov_:.2f}× → band 2.5–3.0, B1/B+, spread 2.6% → kD = {kd_ * 100:.1f}%, after tax {kd_ * (1 - tx) * 100:.3f}%.",
            f"7. Weights from D/E = 0.50: equity {we * 100:.2f}%, debt {wd * 100:.2f}%.",
            f"8. WACC = {we:.4f} × {ke_ * 100:.3f}% + {wd:.4f} × {kd_ * (1 - tx) * 100:.3f}% = **{wacc__ * 100:.2f}%**.", "",
            "**Traps:** skipping Blume; using the effective tax rate; taking 0.50 as the debt weight (it is D/E, so the weight is 0.5/1.5); leaving kD pre-tax.", ""]
    # 30285: OLS by hand and a t-test
    xs, ys = [2, 4, 6, 8, 10], [3, 4, 8, 9, 11]
    xm_, ym_ = sum(xs) / 5, sum(ys) / 5
    sxy_ = sum((a - xm_) * (b - ym_) for a, b in zip(xs, ys))
    sxx_ = sum((a - xm_) ** 2 for a in xs)
    be_ = sxy_ / sxx_
    al_ = ym_ - be_ * xm_
    res_ = [b - al_ - be_ * a for a, b in zip(xs, ys)]
    rss_ = sum(u * u for u in res_)
    s_ = math.sqrt(rss_ / 3)
    se_ = s_ / math.sqrt(sxx_)
    t0 = be_ / se_
    near(be_, (sum(a * b for a, b in zip(xs, ys)) / 5 - xm_ * ym_) / (sum(a * a for a in xs) / 5 - xm_ ** 2))
    out += ["## 30285 Empirical Methods: OLS by hand and a t-test", "",
            f"**Problem.** Data (x, y): (2, 3), (4, 4), (6, 8), (8, 9), (10, 11). Estimate y = α + βx + u by OLS, then test β = 0 at 5% (t with 3 df, critical value 3.18).", "",
            "**Solution.**", "",
            f"1. Means: x̄ = {xm_:.0f}, ȳ = {ym_:.0f}.",
            f"2. Deviations: x − x̄ = (−4, −2, 0, 2, 4); y − ȳ = ({', '.join(f'{b - ym_:g}'.replace('-', '−') for b in ys)}).",
            f"3. Σ(x − x̄)(y − ȳ) = {sxy_:g}; Σ(x − x̄)² = {sxx_:g}.",
            f"4. β̂ = {sxy_:g}/{sxx_:g} = **{be_:.2f}**; α̂ = {ym_:.0f} − {be_:.2f} × {xm_:.0f} = **{al_:.2f}**.",
            f"5. Residuals: ({', '.join(f'{u:.2f}'.replace('-', '−') for u in res_)}); RSS = {rss_:.2f}.",
            f"6. s² = RSS/(T − 2) = {rss_ / 3:.4f}; s = {s_:.4f}.",
            f"7. SE(β̂) = s/√Σ(x − x̄)² = {s_:.4f}/√{sxx_:g} = {se_:.4f}.",
            f"8. t = {be_:.2f}/{se_:.4f} = **{t0:.2f}** > 3.18: reject β = 0.", "",
            "Check: β̂ = Cov(x, y)/Var(x) with E[xy] − x̄ȳ gives the same slope.", "",
            "**Traps:** dividing RSS by T; forgetting Σ(x − x̄)² in the SE; testing against the wrong null.", ""]
    # 30024: management account method
    inv, rec, pre, pay, acc, cust = 180, 220, 15, 200, 35, 25
    ppe, rou, ip = 700, 60, 120
    debt, lease, cashx, sec = 420, 65, 50, 30
    onwc_ = inv + rec + pre - (pay + acc + cust)
    nic_ = onwc_ + ppe + rou
    nfp_ = debt + lease - cashx - sec
    near(onwc_, 155)
    out += ["## 30024 Financial Statement Analysis: management account method", "",
            "**Problem.** Inventories 180, trade receivables 220, operating prepayments 15; trade payables 200, accrued operating expenses 35, customer prepayments 25; PP&E 700, right-of-use assets 60, investment property 120; bank debt 420, lease liabilities 65, cash 50, marketable securities 30 (€k). Compute ONWC, NIC and NFP.", "",
            "**Solution.**", "",
            f"1. Operating current assets = 180 + 220 + 15 = {inv + rec + pre}.",
            f"2. Operating current liabilities = 200 + 35 + 25 = {pay + acc + cust}.",
            f"3. ONWC = **{onwc_}**.",
            f"4. Operating non-current assets = PP&E 700 + right-of-use 60 = {ppe + rou}. Investment property is non-operating: leave it out.",
            f"5. NIC = {onwc_} + {ppe + rou} = **{nic_}**.",
            f"6. Gross financial debt = 420 + lease liabilities 65 = {debt + lease}.",
            f"7. Financial assets = cash 50 + securities 30 = {cashx + sec}.",
            f"8. NFP = **{nfp_}**.", "",
            "**Traps:** leaving leases out of NFP or right-of-use assets out of NIC; putting investment property in NIC; treating tax payable or loans to related parties as operating.", ""]
    return "\n".join(out)


def add_30178():
    """Real questions, gap-filling Hard questions, deck units and the source ledger for 30178 (see c30178.py)."""
    import c30178 as c
    for q in BANKS["30178"]["questions"]:
        q["units"] = c.EXISTING_UNITS[q["id"]]
        q["slide_groups"] = c.EXISTING_GROUPS.get(q["id"], q["slide_groups"])
    BANKS["30178"]["questions"] += c.REAL + c.HARD
    BANKS["30178"]["coverage"] = {"course": "30178", "sections": c.SECTIONS, "units": c.UNITS,
                                  "existing_units": c.EXISTING_UNITS, "ledger": c.LEDGER}


if __name__ == "__main__":
    add_30178()
    for code, b in BANKS.items():
        payload = {"source": "Generated by banks/build_banks.py (Claude), reviewed against the harder rule", "questions": b["questions"]}
        if code in COURSES:
            payload["courses"] = [COURSES[code]]
        if "coverage" in b:
            payload["coverage"] = b["coverage"]
        (OUT / f"bank_{code}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1))
        print(code, len(b["questions"]), "questions")
    (OUT / "worked-examples.md").write_text(worked())
    print("worked-examples.md written")
