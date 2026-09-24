"""30285 Empirical Methods for Finance: source intake, deck units and the questions that fill the gaps.

Same rules as c30178.py / c30257.py / c30024.py: real questions first, word for word; keys official where printed (bold in
the instructor's solution files, the green tick on the Blackboard review screens), otherwise solved twice; generated Hard
questions only for gaps; every source item in the ledger.

Exam format: multiple choice only, including derivations (syllabus; Practice #1 and #2 instructions). The decks in the
folder run to 2c (the F-test and R-squared). Everything later in the course (serial correlation and HAC, heteroscedasticity
and White errors, Montecarlo and bootstrap, APT and Fama-MacBeth, ARMA/ARIMA, panels and fixed effects, predictability and
Lettau-Ludvigson) waits for its deck.
"""
from build_banks import mcq, question, cite, f, near, CREATED, L

C = "30285"
F_1B, F_1C = "Slides/1b_Introduction_to_Content.pdf", "Slides/1c_LinearAlgebra_and_Inference_v2.pdf"
F_2, F_2B, F_2C = "Slides/2_Simple_LinRegr.pdf", "Slides/2b_Simple_LinRegr_Inference.pdf", "Slides/2c_LinearRegr_FTest.pdf"
F_SYL = "Syllabus and Additional Material/syllabus.pdf"
F_EFP = "Syllabus and Additional Material/Exam_First_Page.docx"
F_BRX = "Syllabus and Additional Material/Brooks_2nd_Index.pdf"
F_BRK = "brooks_econometr_finance_2nd.pdf"
F_PQ1 = "Practice Quiz/Practice_1_Solutions.docx"
F_PQ2 = "Practice Quiz/Practice_2_Solutions.docx"
F_PE1 = "Practice Exam/Practice_1_Solutions.docx"
F_PE2 = "Practice Exam/Practice_2_Solutions.docx"
F_PM = "Practice Material/expected value, variance, and matrix operations.pdf"
F_X1 = "Reference/Econometrics past exam 1.pdf"
F_X2 = "Reference/Econometrics past exam 2.pdf"
F_X3 = "Reference/Econometrics past exam 3.pdf"
F_XP = "Reference/Past Exams.pdf"
F_QM, F_QM2 = "Reference/quiz_mock.pdf", "Reference/quiz_mock_2.pdf"
F_SPP2 = "Reference/econometrics-final-exam-past-paper-2-empirical-methods-for-finance.pdf"
F_SX2 = "Reference/econometrics-past-exam-2-data-generating-processes-models.pdf"
F_SX3 = "Reference/econometrics-past-exam-3-apt-model-ar-processes-analysis.pdf"
F_CLEAN = "Reference/Clean/"

DOCX = ("text copied from the .docx text layer on 2026-09-24; the Greek letters are Symbol-font characters in the file and were read "
        "back as β, and the subscripts are written as Unicode subscripts; the official answer is the option set in bold")
PHOTO = ("photo of the Blackboard 'Review Test Submission' screen of the 20 Dec 2021 final; text transcribed from the image and checked "
         "word for word against the clearer screenshots in the Studocu copy (" + F_SPP2.split("/")[1] + "); the green tick marks the official answer")
PHOTO2 = ("photo of the Blackboard review screen of another sitting (1-point questions); text transcribed from the image and checked word "
          "for word; the green tick marks the official answer")
MCQ, CALC, WR = "concept MCQ", "calc MCQ", "written exercise (practice sheet)"


def s_mcq(n, prompt, options, letter, status="official", marks=1):
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
                    "verbatim_verified": kw.get("verbatim", True), "transcribed_from_image": kw.get("photo", False), "page_snapshot_asset": None},
         "subquestions": [p[0] for p in parts], "answer_key": [p[1] for p in parts], "error_tags": [],
         "marks": round(sum(marks), 2) if all(isinstance(m, (int, float)) for m in marks) else "UNKNOWN",
         "mark_scheme": kw["scheme"], "citations": kw["cites"], "slides": [], "slide_groups": kw["groups"],
         "units": kw["units"], "est_minutes": kw["minutes"], "created_at": CREATED, "negative_marking": None}
    if kw.get("check"):
        q["source"]["check"] = kw["check"]
    if q["data"] is None:
        del q["data"]
    return q


REAL, HARD = [], []


def one(id, deck, topic, obj, file, location, stem, options, letter, scheme, cites, groups, units, shape=MCQ, minutes=2, photo=False, status="official", prompt=None):
    REAL.append(realq(id=id, deck=deck, topic=topic, objective=obj, shape=shape, file=file, location=location, stem=stem,
                      parts=[s_mcq("1", prompt or stem.split("\n")[-1], options, letter, status)],
                      scheme=scheme, cites=cites, groups=groups, units=units, minutes=minutes, photo=photo))


# ================================================================================================
# REAL: instructor practice quizzes and practice exams (Prof. Croce; solutions with the key in bold)
# ================================================================================================
one("30285-L1B-10", "L1B", "What financial econometrics is", "The goal of financial econometrics",
    F_PQ2, "Practice #2 (Practice Quiz folder), question 2; " + DOCX,
    "Financial Econometrics:",
    ["Uses tools derived from statistics", "Uses statistic tools to address financial economics problems",
     "Requires us to be aware of the potential limitations of our estimators.", "All of the above"], "D",
    ["Official answer: D (bold in the solutions).",
     "Route 1: the 1b slide defines econometrics as measurement 'done by applying statistical tools' and financial econometrics as econometrics applied to financial variables — A and B are true.",
     "Route 2: C is the reason the course studies standard errors and inference (estimation uncertainty, 1c and 2b) — true, so all three hold."],
    [cite("L1B", 3, "Def of Econometrics: measurement in economics done by applying statistical tools")], ["L1B-1"], ["L1B-U1"], minutes=1)

one("30285-L1B-11", "L1B", "What financial econometrics is (variant)", "The goal of financial econometrics",
    F_PE2, "Practice #2 (Practice Exam folder), question 2; " + DOCX,
    "Financial Econometrics:",
    ["Uses special tools not derived from statistics", "Uses statistic tools to address financial economics problems",
     "Requires us know population parameters.", "All of the above"], "B",
    ["Official answer: B (bold in the solutions).",
     "Route 1: the tools are statistical (A is false) and they are applied to financial variables (B true).",
     "Route 2: econometrics estimates population parameters from a sample precisely because we do not know them (C is false; 1c 'The Population and the Sample'). So only B."],
    [cite("L1B", 3, "Def of Econometrics: measurement in economics done by applying statistical tools"),
     cite("L1C", 11, "Since our samples are not identical to the population, our estimates are subject to estimation uncertainty.")],
    ["L1B-1"], ["L1B-U1", "L1C-U6"], minutes=1)

near(75 / 50, 1.5)
one("30285-L1B-12", "L1B", "Gross, net and log return with a dividend", "Returns: raw gross, raw net and log returns",
    F_PQ2, "Practice #2 (Practice Quiz folder), question 5; " + DOCX,
    "If I buy a stock at 50, I get a dividend payout of 5 and I sell at 70",
    ["My log return is (70+5)/50", "My net return in raw units is (70+5)/50", "My raw-units return is ln(75/50)", "None of the above"], "D",
    ["Official answer: D (bold in the solutions).",
     "Route 1: gross return R = (70 + 5)/50 = 1.5; net return r = R − 1 = 0.5 = 50%; log return = ln(1.5) = 0.405.",
     "Route 2: check each option against its label — A gives the gross return, not the log; B gives the gross, not the net; C gives the log return, not a raw-units return. None matches."],
    [cite("L1B", 11, "Raw Net Return: gross return minus the initial investment")], ["L1B-2"], ["L1B-U5"], minutes=1)

one("30285-L1C-11", "L1C", "Average and variance of a data vector", "Sample average and variance in vector form",
    F_PQ1, "Practice #1 (Practice Quiz folder), question 4; " + DOCX,
    "Consider a vector X which comprises T observations of the variable x. Use 1_T to denote a vector of ones with T elements:",
    ["Avg(x) = (1_T’X)/(T-1)", "Avg(x^2) = (X’X)/(T^2)", "V(x) =  ((X’X) - (1_T’X))/T", "None of the above"], "D",
    ["Official answer: D (bold in the solutions).",
     "Route 1: Avg(x) = (1_T′X)/T, not /(T − 1); Avg(x²) = (X′X)/T, not /T²; V(x) = X′X/T − (1_T′X/T)², not (X′X − 1_T′X)/T.",
     "Route 2: test with X = (1, 3)′, T = 2: Avg = 2, Avg(x²) = 5, V = 1. Option A gives 4, B gives 2.5, C gives (10 − 4)/2 = 3. None is right."],
    [cite("L1C", 8, "The sample average can be computed as"), cite("L2B", 4, "has dimension T by 1 (vector!) and represents the linear regression setting!")],
    ["L1C-2"], ["L1C-U5", "L2B-U2"], minutes=2)

DIST = "The disturbance term that we add to our linear representation in our simple regression framework can be interpreted as:"
one("30285-L2-10", "L2", "What the disturbance term captures", "The disturbance term",
    F_PQ1, "Practice #1 (Practice Quiz folder), question 2; the same question is Practice #2 (Quiz) question 3 and Practice #2 (Exam) question 3; " + DOCX,
    DIST, ["The result of omitted variables", "Errors in measurement", "Random outside influences", "All of the above"], "D",
    ["Official answer: D (bold in all three solution files).",
     "Route 1: the 2a slide 'Why do we include a Disturbance?' lists exactly three features: omitted variables, errors in the measurement of yₜ, random outside influences.",
     "Route 2: each of A, B and C is one item of that list, so none alone is complete."],
    [cite("L2", 10, "Omitted variables: we always leave out some determinants of yt")], ["L2-1"], ["L2-U3"], minutes=1)

one("30285-L2-11", "L2", "Linear in the parameters", "Linearity: which models OLS can estimate",
    F_PQ2, "Practice #2 (Practice Quiz folder), question 7; " + DOCX,
    "Consider the following regression:\nyₜ = β₁ +  x₂ₜ / β₂ + β₃x₃ₜ + β₄x₄ₜ + uₜ",
    ["It is not linear and hence it cannot be estimated with OLS", "It suffers of heteroscedasticity and must use a White correction",
     "Is equivalent to have no constant.", "None of the above"], "A",
    ["Official answer: A (bold in the solutions).",
     "Route 1: the 2a 'Linearity' slide: linear in the parameters means the parameters are 'not multiplied together, divided, squared or cubed' — here x₂ₜ is divided by β₂.",
     "Route 2: B is about the errors, not the functional form; C is false because β₁ is still a constant. Follow the slide's definition on the exam."],
    [cite("L2", 21, "Linear in the parameters means that the parameters are not multiplied together, divided, squared or cubed etc.")],
    ["L2-3"], ["L2-U8"], minutes=1)

FT = "Consider the following regression:\nyₜ = β₁ + β₂x₂ₜ + β₃x₃ₜ + β₄x₄ₜ + uₜ\nYou want to test H_0: 2β₂=β₃."
one("30285-L2C-12", "L2C", "The restricted regression for 2β₂ = β₃", "Building the restricted regression for an F-test",
    F_PQ1, "Practice #1 (Practice Quiz folder), question 5 (options printed as separate numbered lines); " + DOCX, FT,
    ["You can use a regular t-stat", "You cannot test this restriction",
     "The companion restricted regression for an F-test is: yₜ = β₁ + β₂(x₂ₜ + 2 x₃ₜ ) + β₄x₄ₜ + uₜ", "None of the above"], "C",
    ["Official answer: C (bold in the solutions).",
     "Route 1: substitute the restriction β₃ = 2β₂: β₂x₂ₜ + 2β₂x₃ₜ = β₂(x₂ₜ + 2x₃ₜ) — the restricted regression in C.",
     "Route 2: the restriction involves two coefficients, so a regular t-stat on one coefficient does not test it (A); it is one linear restriction (m = 1), testable with the F-test (B is false)."],
    [cite("L2C", 11, "This is the restricted regression. We actually estimate it by creating two new variables")], ["L2C-2"], ["L2C-U5", "L2C-U4"], minutes=2)

one("30285-L2C-13", "L2C", "The restricted regression for 2β₂ = β₃ (variant)", "Building the restricted regression for an F-test",
    F_PE1, "Practice #1 (Practice Exam folder), question 3 (its options are printed as questions 5-8 of the numbered list); " + DOCX, FT,
    ["You can use a regular t-stat", "You cannot test this restriction",
     "The companion restricted regression for an F-test is: yₜ = β₁ + β₂(2x₂ₜ +  x₃ₜ ) + β₄x₄ₜ + uₜ", "None of the above"], "D",
    ["Official answer: D (bold in the solutions).",
     "Route 1: with β₃ = 2β₂ the restricted regression is yₜ = β₁ + β₂(x₂ₜ + 2x₃ₜ) + β₄x₄ₜ + uₜ; option C puts the 2 on x₂ₜ, which imposes β₃ = β₂/2 instead.",
     "Route 2: A and B are false as in the quiz version (a single-coefficient t-stat does not test a restriction across two coefficients; the restriction is testable). Nothing else is right, so D."],
    [cite("L2C", 11, "This is the restricted regression. We actually estimate it by creating two new variables")], ["L2C-2"], ["L2C-U5", "L2C-U4"], minutes=2)

one("30285-L2C-14", "L2C", "Size of the variance-covariance matrix", "Multiple regression: the K×K variance-covariance matrix of β̂",
    F_PQ2, "Practice #2 (Practice Quiz folder), question 6 (options printed as separate numbered lines); " + DOCX,
    "Consider the following regression:\nyₜ = β₁ + β₂ x₂ₜ + β₃x₃ₜ + β₄x₄ₜ + uₜ",
    ["The variance-covariance matrix of the ols estimator will be 4-by-4", "The variance-covariance matrix of the ols estimator will be T-by-T",
     "Your standard errors may be extremely large", "None of the above"], "A",
    ["Official answer: A (bold in the solutions).",
     "Route 1: k = 4 coefficients (including the constant), so Var(β̂) = σ²(X′X)⁻¹ is k × k = 4 × 4.",
     "Route 2: X is T × 4, so X′X is (4 × T)(T × 4) = 4 × 4; the T × T matrix is Var(u) = σ²I_T, not Var(β̂). Nothing in the question points to large standard errors."],
    [cite("L2C", 7, "And the (K by K) variance-covariance matrix is still")], ["L2C-1"], ["L2C-U3", "L2C-U2"], minutes=1)

# ================================================================================================
# REAL: final exam of 20 Dec 2021 (photos of the Blackboard review; green tick = official answer)
# ================================================================================================
DGP = ("Consider the following data generating process (DGP):\nyₜ = β₀ + β₁xₜ + β₂zₜ + uₜ,\n"
       "Over a sample of T observations. Assume that our standard assumptions for the OLS estimator hold.")
one("30285-L2C-10", "L2C", "Testing β₁ = β₂ with a t-stat", "t-test on a linear combination of coefficients; counting restrictions",
    F_X1, "Final exam 20 Dec 2021, question 3; " + PHOTO,
    DGP + " You want to test whether H₀: β₁ = β₂",
    ["This null hypothesis can be test with an F-test in which the number of restrictions is m=2",
     "This null hypothesis can be tested with a t-stat on H₀: 2β₁ = 0 since β₁ = β₂.",
     "This null hypothesis can be tested with a t-stat on H₀: β₁ − β₂ = 0 and it requires us to use the estimated cov(β̂₁, β̂₂)",
     "None of the above"], "C",
    ["Official answer: C (green tick).",
     "Route 1: count the '=' signs: one restriction (m = 1), so A is false. Rewrite it as β₁ − β₂ = 0; t = (β̂₁ − β̂₂)/SE(β̂₁ − β̂₂) with Var(β̂₁ − β̂₂) = V(β̂₁) + V(β̂₂) − 2cov(β̂₁, β̂₂), the off-diagonal entry of σ²(X′X)⁻¹.",
     "Route 2: B substitutes the null into itself and loses β₂; it tests a different hypothesis."],
    [cite("L2C", 15, "Count the number of ‘=’ signs!"), cite("L2C", 7, "And the (K by K) variance-covariance matrix is still")],
    ["L2C-2"], ["L2C-U7", "L2C-U3", "L2B-U11"], minutes=2, photo=True)

one("30285-L2B-10", "L2B", "What the standard assumptions give you", "Assumptions, unbiasedness and BLUE; omitted variables",
    F_X1, "Final exam 20 Dec 2021, question 7; " + PHOTO, DGP,
    ["T must be equal or greater than 4 if you want to estimate all coefficients.", "The OLS estimator is unbiased and efficient given this DGP",
     "If we omit zₜ, our estimate of β₁ is for sure unbiased", "All of the above"], "B",
    ["Official answer: B (green tick).",
     "Route 1: under assumptions 1-4 OLS is BLUE — unbiased and, by Gauss-Markov, best (minimum variance) among linear unbiased estimators: B.",
     "Route 2: A is false — three coefficients need T ≥ 3, not 4. C is false — omitting zₜ puts β₂zₜ in the error, which is correlated with xₜ unless corr(zₜ, xₜ) = 0 (assumption 4 fails), so 'for sure unbiased' is wrong."],
    [cite("L2B", 10, "means that the OLS estimator has minimum variance among the class of linear unbiased estimators"),
     cite("L2B", 8, "No relationship between the error and corresponding x variate")],
    ["L2B-2"], ["L2B-U4", "L2B-U5", "L2B-U6", "L2B-U7", "L2-U3"], minutes=2, photo=True)

V16 = "Assume that V(β̂) = [16 12; 12 9] (rows separated by ';')"
UNI = "Consider the following univariate regression:\nyₜ = β₁ + β₂xₜ + uₜ,\nOver a sample of T observations. Assume that our standard assumptions for the OLS estimator hold. "
for b1, b2, want in [(0, 6, None), (5, 1, (8, 169))]:
    m3, v3 = b1 + 3 * b2, 16 + 9 * 9 + 2 * 3 * 12
    m2, v2 = b1 + 2 * b2, 16 + 4 * 9 + 2 * 2 * 12
    near(v3, 169); near(v2, 100)
    near(v3, (1 * 4 + 3 * 3) ** 2)  # route 2: V is rank one, V = (4, 3)'(4, 3), so a'Va = (4a1 + 3a2)^2
    if want:
        near(m3, want[0]); near(v3, want[1])
one("30285-L2B-12", "L2B", "Distribution of a combination of the estimates", "Normality: distribution of β̂; variance of a linear combination (sandwich rule)",
    F_X1, "Final exam 20 Dec 2021, question 11 (the matrix and the vector are printed as brackets; written here row by row); " + PHOTO,
    UNI + V16 + " and that the point estimates are [0; 6]. Under our standard assumptions, we can say that:",
    ["β̂₁ + 3β̂₂ ~ N(18, 205)", "β̂₁ ~ N(6, 16)", "β̂₁ + 2β̂₂ ~ N(12, 34)", "None of the above"], "D",
    ["Official answer: D (green tick).",
     "Route 1: β̂₁ + 3β̂₂ has mean 0 + 18 = 18 and variance 16 + 9·9 + 2·3·12 = 169, not 205 (A false); β̂₁ has mean 0, not 6 (B false); β̂₁ + 2β̂₂ has mean 12 and variance 16 + 4·9 + 2·2·12 = 100, not 34 (C false).",
     "Route 2: sandwich rule a′V a with a = (1, 3)′ and (1, 2)′; since V = (4, 3)′(4, 3), a′V a = (4a₁ + 3a₂)² = 13² = 169 and 10² = 100. Both options drop the covariance term."],
    [cite("L2B", 15, "What if the errors are not normally distributed? Will the parameter estimates still be normally distributed?"),
     cite("L1C", 14, "Rule 4 (sandwich): the v-cov matrix of a vector Y multiplied by a matrix A of scalars")],
    ["L2B-3"], ["L2B-U10", "L2B-U8", "L1C-U8"], shape=CALC, minutes=3, photo=True)

one("30285-L2C-11", "L2C", "Python: a regression on a constant", "The sample average in a regression setting; its standard error",
    F_X1, "Final exam 20 Dec 2021, question 10 (code cell [20] as printed, including its comment typo 'arrat'); " + PHOTO,
    "Consider the following Python code:\n"
    "import numpy as np\nfrom numpy.linalg import inv\n\n# convert dataframe to matrix\ny = df['LeadReal'].to_numpy()  # flat arrat\ny = y[:, None]  # 2D array (matrix)\n"
    "x = np.ones(y.shape)\nnobs = x.shape[0]\n\n# compute predicted\nalpha_hat = inv(x.T @ x) @ x.T @ y\ny_hat = x @ alpha_hat\n\n"
    "# compute residuals to get sigma hat\nres = y - y_hat\nsigma_hat = 1/(nobs - 1)*res.T @ res\nalpha_hat_se = np.sqrt(sigma_hat*inv(x.T @ x))\n\n"
    "print(f\"alpha: {np.round(alpha_hat, 3)}.\")\nprint(f\"SE alpha: {np.round(alpha_hat_se, 3)}\")",
    ["All of the below", "This code implements a multivariate regression", "This code has a typo in the main commands",
     "This code is what you need in order to estimate the mean of a variable"], "D",
    ["Official answer: D (green tick).",
     "Route 1: X is a column of ones, so (X′X)⁻¹X′y = (1/T)Σyₜ — the sample mean, as on the 2c slide 'The sample average in a regression setting'.",
     "Route 2: SE = √(s²/T) with s² = Σ(yₜ − ȳ)²/(T − 1) (one parameter estimated) — the 1c standard error of the mean. There is one regressor (not multivariate) and the commands run as written (only a comment has a typo)."],
    [cite("L2C", 4, "Estimating the sample avg. in a regression setting"), cite("L1C", 12, "First, realize that across random samples the sample estimate is a random number.")],
    ["L2C-1"], ["L2C-U1", "L1C-U7", "L1C-U9"], minutes=3, photo=True, prompt="Consider the following Python code:")

# ---- another sitting (1-point questions, photos with green ticks) ---------------------------------------------------------------
one("30285-L2B-11", "L2B", "What the standard assumptions give you (variant)", "Assumptions, unbiasedness and BLUE; omitted-variable bias",
    F_X2, "Past exam 2, question 1; " + PHOTO2, DGP,
    ["T must be equal or greater than 3 if you want to estimate all coefficients.", "The OLS estimator is unbiased and efficient given this DGP",
     "If we omit zₜ, our estimate of β₁ is biased unless corr(zₜ, xₜ) = 0", "All of the above"], "D",
    ["Official answer: D (green tick).",
     "Route 1: three coefficients need at least three observations (A true); assumptions 1-4 make OLS BLUE (B true).",
     "Route 2: omitting zₜ moves β₂zₜ into the error; Cov(error, xₜ) = β₂Cov(zₜ, xₜ), zero only if the two are uncorrelated (C true). Compare the Dec 2021 version, where 'T ≥ 4' and 'for sure unbiased' made B the only answer."],
    [cite("L2B", 8, "No relationship between the error and corresponding x variate"),
     cite("L2B", 10, "means that the OLS estimator has minimum variance among the class of linear unbiased estimators")],
    ["L2B-2"], ["L2B-U5", "L2B-U7", "L2-U3"], minutes=2, photo=True)

one("30285-L2B-13", "L2B", "Distribution of a combination of the estimates (variant)", "Normality: distribution of β̂; variance of a linear combination",
    F_X2, "Past exam 2, question 5 (matrix and vector written row by row); " + PHOTO2,
    UNI + V16 + " and that the point estimates are [5; 1]. Under our standard assumptions, we can say that:",
    ["β̂₁ + 3β̂₂ ~ N(8, 25)", "β̂₁ ~ N(1, 16)", "β̂₁ + 2β̂₂ ~ N(11, 34)", "β̂₁ + 3β̂₂ ~ N(8, 169)"], "D",
    ["Official answer: D (green tick).",
     "Route 1: mean 5 + 3·1 = 8; variance 16 + 9·9 + 2·3·12 = 169 → D; A leaves out the covariance and the 3² (16 + 9 = 25).",
     "Route 2: (4a₁ + 3a₂)² with a = (1, 3) gives 13² = 169. B has the wrong mean (β̂₁ = 5); C has the wrong mean (7) and variance (100)."],
    [cite("L2B", 15, "What if the errors are not normally distributed? Will the parameter estimates still be normally distributed?")],
    ["L2B-3"], ["L2B-U10", "L2B-U8"], shape=CALC, minutes=3, photo=True)

# ================================================================================================
# REAL: instructor practice sheet (V. Scrutinio, Sept 2026; no key printed, so every key is solved twice)
# ================================================================================================
pa, pr = [0.4, 0.4, 0.2], [50, 20, 10]
eA = sum(p * x for p, x in zip(pa, pr))
vA = sum(p * x * x for p, x in zip(pa, pr)) - eA ** 2
near(eA, 30); near(vA, 280); near(vA, sum(p * (x - eA) ** 2 for p, x in zip(pa, pr)))
pb_, rb = [0.3, 0.4, 0.3], [30, 20, 10]
eB = sum(p * x for p, x in zip(pb_, rb))
vB = sum(p * (x - eB) ** 2 for p, x in zip(pb_, rb))
near(eB, 20); near(vB, 60); near(vB, sum(p * x * x for p, x in zip(pb_, rb)) - eB ** 2)
eP, vP = 0.4 * eA + 0.6 * eB, 0.4 ** 2 * vA + 0.6 ** 2 * vB
near(eP, 24); near(vP, 66.4)
REAL.append(realq(
    id="30285-L1B-13", deck="L1B", topic="Moments of a discrete return distribution and of an uncorrelated portfolio",
    objective="Expected value, variance and standard deviation from probabilities; portfolio mean and variance", shape=WR, file=F_PM,
    location="Practice sheet 'Discrete distribution moments and matrix exercises' (V. Scrutinio, September 2026), exercises 1-2; text checked word for word against the PDF text layer on 2026-09-24",
    stem="Consider the following distribution of returns for an asset (A):\n\nConsider now a second asset (B) with a return distribution as follows:",
    data="| Asset A: Return | Probability |\n|---|---|\n| 50 | 0.4 |\n| 20 | 0.4 |\n| 10 | 0.2 |\n\n| Asset B: Return | Probability |\n|---|---|\n| 30 | 0.3 |\n| 20 | 0.4 |\n| 10 | 0.3 |",
    parts=[s_written("1", "Compute the expected return, the variance of the return, and the standard deviation (approximate all numbers to the third decimal place where necessary).",
                     f"E(A) = {f(eA, 3)}; Var(A) = {f(vA, 3)}; SD(A) = {f(vA ** 0.5, 3)}."),
           s_written("2", "Assume now that both assets are included in a portfolio and that 40% of the capital is invested in A and 60% in B. Compute the expected value and the variance of the portfolio "
                          "under the assumption that the returns of the assets are uncorrelated (i.e. the correlation coefficient is zero). Remember that th expected value is a linear operator, that is, "
                          "given a constant a and a random variable x, we have that E(ax) = aE(x). Approximate all numbers to the third decimal place where necessary.",
                     f"E(B) = {f(eB, 3)}, Var(B) = {f(vB, 3)}; E(p) = 0.4 × 30 + 0.6 × 20 = {f(eP, 3)}; Var(p) = 0.4² × 280 + 0.6² × 60 = {f(vP, 3)} (SD {f(vP ** 0.5, 3)}).")],
    scheme=["No key in the source; solved twice (asserted in c30285.py).",
            "[1] Route 1: E = 0.4·50 + 0.4·20 + 0.2·10 = 30; E(R²) = 0.4·2500 + 0.4·400 + 0.2·100 = 1180; Var = 1180 − 30² = 280; SD = √280 = 16.733. "
            "Route 2: deviations 20, −10, −20 → 0.4·400 + 0.4·100 + 0.2·400 = 280.",
            "[2] E(B) = 9 + 8 + 3 = 20; Var(B) = 0.3·100 + 0 + 0.3·100 = 60. With zero correlation the covariance term drops: Var(p) = 0.16·280 + 0.36·60 = 44.8 + 21.6 = 66.4. "
            "Where marks are lost: using weights instead of squared weights (0.4·280 + 0.6·60 = 148)."],
    cites=[cite("L1B", 18, "Expected value: think of"), cite("L1B", 20, "Useful formulas for a portfolio with two assets")],
    groups=["L1B-3"], units=["L1B-U8", "L1B-U9", "L1B-U10"], minutes=8))

A_, B_, x_ = [[3, 5], [2, 1], [-1, 1]], [[3, -2], [1, 1]], [1, 4, 0]
Bt = [[B_[j][i] for j in range(2)] for i in range(2)]
xA = [sum(x_[k] * A_[k][j] for k in range(3)) for j in range(2)]
xAB = [sum(xA[k] * Bt[k][j] for k in range(2)) for j in range(2)]
ABt = [[sum(A_[i][k] * Bt[k][j] for k in range(2)) for j in range(2)] for i in range(3)]
assert xAB == [15, 20] and [sum(x_[i] * ABt[i][j] for i in range(3)) for j in range(2)] == xAB  # route 2: x(AB')
REAL.append(realq(
    id="30285-L1C-10", deck="L1C", topic="A row vector times a matrix times a transpose", objective="Matrix multiplication and transposes",
    shape=WR, file=F_PM,
    location="Practice sheet 'Discrete distribution moments and matrix exercises' (V. Scrutinio, September 2026), exercise 3; text checked against the PDF text layer on 2026-09-24 (matrices written row by row)",
    stem="Matrix product:\nConsider the two following matrices A and B and the vector x.\nA = [3 5; 2 1; −1 1]\nB = [3 −2; 1 1]\nx = (1 4 0)",
    parts=[s_written("1", "Perform the following computation: xAB′", "xAB′ = (15, 20).")],
    scheme=["No key in the source; solved twice (asserted in c30285.py).",
            "Route 1: xA = (1·3 + 4·2 + 0·(−1), 1·5 + 4·1 + 0·1) = (11, 9); B′ = [3 1; −2 1]; (11, 9)B′ = (33 − 18, 11 + 9) = (15, 20).",
            "Route 2: AB′ = [−1 8; 4 3; −5 0]; x(AB′) = (−1 + 16, 8 + 12) = (15, 20). Dimensions: (1×3)(3×2)(2×2) = 1×2."],
    cites=[cite("L1C", 5, "Matrix multiplication rule: Definitions")], groups=["L1C-1"], units=["L1C-U2", "L1C-U3"], minutes=4))

# ================================================================================================
# HARD: gap-filling generated questions (one per section that no existing Hard question leads)
# ================================================================================================
def hq(**kw):
    units = kw.pop("units")
    q = question(course=C, **kw)
    q["units"] = units
    return q


ROMAN = ["I", "II", "III", "IV", "V", "VI"]


def fmt_set(xs):
    xs = list(xs)
    return f"{xs[0]} only" if len(xs) == 1 else ", ".join(xs[:-1]) + f" and {xs[-1]} only"


def statements_mcq(n, intro, stmts, options, correct):
    assert correct == fmt_set([ROMAN[i] for i, (_, tt) in enumerate(stmts) if tt]), correct
    body = intro + "\n\n" + "\n".join(f"{ROMAN[i]}. {s}" for i, (s, _) in enumerate(stmts)) + "\n\nWhich of the statements are correct?"
    return mcq(n, body, options, correct, 1)


# ---- L1B-1: financial econometrics and its data -------------------------------------------------------------------------
st = [("Daily closing prices of the 40 DAX stocks from 2015 to 2024 form a panel; if some of the stocks were listed only in 2018, it is not a balanced panel.", True),
      ("Credit ratings coded AAA = 1, AA = 2, A = 3, BBB = 4 are ordinal: a bond coded 4 is riskier than one coded 2, but not twice as risky.", True),
      ("A code for the exchange a stock trades on (1 = NYSE, 2 = Nasdaq) is ordinal, because a Nasdaq stock gets the higher number.", False),
      ("Share prices are cardinal: a price of €12 is twice a price of €6.", True),
      ("Because recorded prices are those at which the trade took place, financial data have no measurement error and are not noisy.", False)]
p = statements_mcq("1", "Consider the following statements about financial data.", st,
                   [("I, II and IV only", None), ("I, II, III and IV only", "code_read_as_ordinal"), ("I, II, IV and V only", "no_error_read_as_no_noise"),
                    ("II and IV only", "unbalanced_panel_read_as_not_a_panel")], "I, II and IV only")
HARD.append(hq(id="30285-L1B-02", deck="L1B", topic="Data dimensions, number scales and data quality",
    objective="Financial econometrics and its data: time series, cross-section, panel; cardinal, ordinal and nominal numbers; data quality",
    shape="concept MCQ (statements)", shape_class="calc MCQ", stem="Financial data: statements.", parts=[p],
    scheme=["[1] Steps: (1) I: T (days) and N (stocks) → panel; different time spans → not balanced — true; (2) II: ratings only order the bonds — ordinal, 'better' but not 'twice as good' — true; "
            "(3) III: exchange codes are arbitrary labels — nominal, not ordinal — false; (4) IV: prices have equal distances and a meaningful ratio — cardinal — true; "
            "(5) V: the slide says there is no measurement error but financial data are 'noisy' — false; (6) I, II and IV.",
            "Second route: II, III and IV are the slide's three scales (ordering with no ratio, no ordering, ratios meaningful); only III gives a label an order it does not have."],
    cites=[cite("L1B", 6, "When all series have the same time-span, we call it Balanced Panel."),
           cite("L1B", 10, "Nominal numbers: occur where there is no natural ordering of the values at all."),
           cite("L1B", 4, "No possibility for measurement error but financial data are “noisy”")],
    location="1b slides: goal of financial econometrics, good news about the data, data dimensions, cardinal/ordinal/nominal", file=F_1B, groups=["L1B-1"], minutes=4,
    notches=["near_true_statements", "extra_classification"], hc_parts=[{"n": "1", "steps": 6, "concepts": 3}], units=["L1B-U1", "L1B-U2", "L1B-U3", "L1B-U4"]))

# ---- L1B-3: risk — moments, covariance, correlation and a portfolio ----------------------------------------------------
pr3 = [0.25, 0.50, 0.25]
r1, r2 = [20.0, 10.0, -4.0], [-5.0, 5.0, 15.0]
E = lambda r: sum(p * x for p, x in zip(pr3, r))
e1, e2 = E(r1), E(r2)
v1 = sum(p * (x - e1) ** 2 for p, x in zip(pr3, r1))
v2 = sum(p * (x - e2) ** 2 for p, x in zip(pr3, r2))
cv = sum(p * (a - e1) * (b - e2) for p, a, b in zip(pr3, r1, r2))
corr = cv / (v1 * v2) ** 0.5
w = 0.4
ep, vp = w * e1 + (1 - w) * e2, w * w * v1 + (1 - w) ** 2 * v2 + 2 * w * (1 - w) * cv
near(e1, 9); near(e2, 5); near(v1, 73); near(v2, 50); near(cv, -60); near(ep, 6.6); near(vp, 0.88)
rp = [w * a + (1 - w) * b for a, b in zip(r1, r2)]                     # route 2: portfolio return state by state
near(E(rp), ep); near(sum(p * (x - ep) ** 2 for p, x in zip(pr3, rp)), vp)
near(cv, E([a * b for a, b in zip(r1, r2)]) - e1 * e2)                 # route 2 for the covariance: E(R1R2) - E(R1)E(R2)
sd = lambda v: f(v ** 0.5, 2)
opts = [(f"E(Rp) = {f(ep, 1)}%; σ(Rp) = {sd(vp)}%; corr = {f(corr, 2)}", None),
        (f"E(Rp) = {f(ep, 1)}%; σ(Rp) = {sd(w * w * v1 + (1 - w) ** 2 * v2)}%; corr = {f(corr, 2)}", "covariance_term_dropped"),
        (f"E(Rp) = {f(ep, 1)}%; σ(Rp) = {sd(w * w * v1 + (1 - w) ** 2 * v2 + w * (1 - w) * cv)}%; corr = {f(corr, 2)}", "covariance_term_not_doubled"),
        (f"E(Rp) = {f(ep, 1)}%; σ(Rp) = {sd(vp)}%; corr = {f(cv / (v1 + v2), 2)}", "correlation_over_sum_of_variances")]
p = mcq("1", "Invest 40% in asset 1 and 60% in asset 2. What are the portfolio's expected return and standard deviation, and the correlation between the two assets?", opts, opts[0][0], 1)
HARD.append(hq(id="30285-L1B-03", deck="L1B", topic="Expected value, variance, covariance, correlation and a near-riskless portfolio",
    objective="Risk: expected values from probabilities, variance, covariance and correlation, portfolio variance",
    shape="numerical MCQ with derivation", shape_class="calc MCQ",
    stem="Next year's returns (%) on two assets depend on the state of the economy.",
    data="| State | Probability | Asset 1 | Asset 2 |\n|---|---|---|---|\n| Boom | 0.25 | 20 | −5 |\n| Normal | 0.50 | 10 | 5 |\n| Bust | 0.25 | −4 | 15 |",
    parts=[p],
    scheme=[f"[1] Steps: (1) E(R1) = 5 + 5 − 1 = 9; (2) E(R2) = −1.25 + 2.5 + 3.75 = 5; (3) V(R1) = 0.25·121 + 0.5·1 + 0.25·169 = 73; (4) V(R2) = 0.25·100 + 0 + 0.25·100 = 50; "
            f"(5) COV = 0.25·(11)(−10) + 0.5·(1)(0) + 0.25·(−13)(10) = −60; (6) corr = −60/√(73·50) = {f(corr, 3)}; "
            f"(7) V(Rp) = 0.16·73 + 0.36·50 + 2·0.4·0.6·(−60) = 11.68 + 18 − 28.8 = {f(vp, 2)}; σ = {f(vp ** 0.5, 3)}%; E(Rp) = {f(ep, 1)}%.",
            f"Second route: portfolio return by state = 5, 7, 7.4 → mean {f(ep, 1)}, variance 0.25·2.56 + 0.5·0.16 + 0.25·0.64 = {f(vp, 2)} (asserted).",
            "Where marks are lost: dropping or not doubling the covariance term, dividing the covariance by the sum of the variances instead of the product of the standard deviations."],
    cites=[cite("L1B", 20, "Useful formulas for a portfolio with two assets"),
           cite("L1B", 23, "The correlation between two variables ranges from -1 (perfectly inverse) to +1 (perfect positive)."),
           cite("L1B", 19, "Variance: Average value of squared deviations from mean")],
    location="1b slides: averages and expected values, variance, variance of a sum and covariance, correlation", file=F_1B, groups=["L1B-3"], minutes=5,
    notches=["chain", "extra_step", "cross_section"], hc_parts=[{"n": "1", "steps": 8, "concepts": 3}], units=["L1B-U8", "L1B-U9", "L1B-U10", "L1B-U11", "L2-U5"]))

# ---- L1C-1: linear algebra --------------------------------------------------------------------------------------------------
X = [[1, 2], [1, -1], [1, 4]]
y = [3, 0, 6]
A = [[2, 1], [0, 3]]
XtX = [[sum(X[t][i] * X[t][j] for t in range(3)) for j in range(2)] for i in range(2)]
Xty = [sum(X[t][i] * y[t] for t in range(3)) for i in range(2)]
XA0 = [sum(X[0][k] * A[k][j] for k in range(2)) for j in range(2)]
S = [[XtX[i][j] + A[i][j] for j in range(2)] for i in range(2)]
assert XtX == [[3, 5], [5, 21]] and Xty == [9, 30] and XA0 == [2, 7] and S == [[5, 6], [5, 24]]
assert sum(X[t][1] for t in range(3)) == XtX[0][1]                     # route 2: off-diagonal of X'X = sum of the regressor
st = [("X′X = [3 5; 5 21].", True), ("X′y = (9, 30)′.", True), ("XA is 3 × 2 and its first row is (2, 7).", True),
      ("AX is defined and is 2 × 2.", False), ("X′X + A = [5 6; 5 24], and it is symmetric like X′X.", False)]
p = statements_mcq("1", "X = [1 2; 1 −1; 1 4] (3 × 2), y = (3, 0, 6)′ and A = [2 1; 0 3]. Rows are separated by ';'.", st,
                   [("I, II and III only", None), ("I, II, III and V only", "sum_assumed_symmetric"), ("I, II, III and IV only", "non_conformable_product"),
                    ("I and III only", "xty_rows_and_columns_mixed")], "I, II and III only")
HARD.append(hq(id="30285-L1C-02", deck="L1C", topic="X′X, X′y, conformability and a matrix sum",
    objective="Linear algebra: vectors and matrices, transposes, multiplication and sums",
    shape="concept MCQ (statements)", shape_class="calc MCQ", stem="Matrix algebra: statements.", parts=[p],
    scheme=["[1] Steps: (1) X′X: 1+1+1 = 3; 2−1+4 = 5; 4+1+16 = 21 — I true; (2) X′y: 3+0+6 = 9; 6+0+24 = 30 — II true; (3) XA: (3×2)(2×2) = 3×2; row 1 = (1·2 + 2·0, 1·1 + 2·3) = (2, 7) — III true; "
            "(4) AX: (2×2)(3×2) — 2 ≠ 3, not conformable — IV false; (5) X′X + A = [5 6; 5 24] is right but 6 ≠ 5, so it is not symmetric — V false; (6) I, II and III.",
            "Second route: the off-diagonal of X′X with a column of ones is the sum of the regressor (2 − 1 + 4 = 5); a product AB is defined only if A's columns equal B's rows."],
    cites=[cite("L1C", 5, "Matrix multiplication rule: Definitions"), cite("L1C", 6, "Rule to sum up matrices: Definitions"),
           cite("L1C", 4, "Def of a Matrix A matrix with dimension T (rows) × N (columns) is a collection of N column vectors with T entries.")],
    location="1c slides: vectors and matrices, multiplication (X′X example), sums", file=F_1C, groups=["L1C-1"], minutes=5,
    notches=["near_true_statements", "extra_step"], hc_parts=[{"n": "1", "steps": 7, "concepts": 3}], units=["L1C-U2", "L1C-U3", "L1C-U4"]))

# ---- L2-1: regression basics and the disturbance ----------------------------------------------------------------------------
fit = lambda x: -1.74 + 1.64 * x
res2, res5 = 39.0 - fit(23.2), 17.2 - fit(12.3)
near(res2, 2.692); near(res5, -1.232)
near(res2 + res5, (39.0 + 17.2) - (2 * -1.74 + 1.64 * (23.2 + 12.3)))   # route 2: sum of the two residuals
st = [("In the fund XXX regression, the fund's excess return is the regressand (the explained, LHS variable) and the market's excess return is the regressor (the explanatory, RHS variable).", True),
      (f"With the slide's fitted line ŷₜ = −1.74 + 1.64xₜ, the residual is +{f(res2, 2)} pp in year 2 (x = 23.2, y = 39.0) and {f(res5, 2)} pp in year 5 (x = 12.3, y = 17.2).", True),
      ("The disturbance uₜ captures errors in measuring the market's excess return xₜ; errors in measuring yₜ are ruled out because prices are transaction prices.", False),
      ("If the fund's returns also depend on its exposure to small caps, which the regression leaves out, that effect ends up in uₜ.", True),
      ("The disturbance is needed only when T is small: with enough years, the points would lie exactly on y = a + bx.", False)]
p = statements_mcq("1", "Consider the following statements about the simple regression yₜ = α + βxₜ + uₜ of the fund XXX example.", st,
                   [("I, II and IV only", None), ("I, II, III and IV only", "measurement_error_in_x"), ("I and IV only", "residual_sign_reversed"),
                    ("I, II, IV and V only", "disturbance_only_small_samples")], "I, II and IV only")
HARD.append(hq(id="30285-L2-02", deck="L2", topic="Regression vocabulary, residuals and what the disturbance captures",
    objective="Regression basics: dependent and independent variables; the line of best fit; the disturbance term",
    shape="concept MCQ (statements)", shape_class="calc MCQ", stem="Simple regression: statements.", parts=[p],
    scheme=[f"[1] Steps: (1) I: y = regressand/LHS, x = regressor/RHS — true; (2) II: ŷ₂ = −1.74 + 1.64·23.2 = 36.308, û₂ = +{f(res2, 3)}; ŷ₅ = 18.432, û₅ = {f(res5, 3)} — true; "
            "(3) III: the slide lists errors in the measurement of yₜ, not xₜ — false; (4) IV: an omitted determinant is the first item on the slide's list — true; "
            "(5) V: random outside influences never vanish with more data; y = a + bx is 'completely deterministic' — false; (6) I, II and IV.",
            "Second route for II: residual = actual − fitted; the fund beat the line in year 2 and fell short in year 5, so the signs are + and −."],
    cites=[cite("L2", 4, "Denote the dependent variable by y and the independent variable(s) by x1, x2, ... , xk"),
           cite("L2", 10, "There may be errors in the measurement of yt that cannot be modelled."),
           cite("L2", 7, "Suppose that we have the following data on the excess returns on a fund manager’s portfolio")],
    location="2a slides: regression, notation, fund XXX data, line of best fit, disturbance, using the estimates", file=F_2, groups=["L2-1"], minutes=5,
    notches=["near_true_statements", "extra_step"], hc_parts=[{"n": "1", "steps": 7, "concepts": 3}], units=["L2-U1", "L2-U2", "L2-U3"]))

# ---- L2-3: linearity, extrapolation, estimation uncertainty -----------------------------------------------------------------
st = [("yₜ = β₁ + β₂ ln(xₜ) + uₜ can be estimated by OLS after defining zₜ = ln(xₜ).", True),
      ("Yₜ = e^β₁ · Xₜ^β₂ · e^uₜ can be estimated by OLS after taking logs of both sides.", True),
      ("yₜ = β₁ + β₂xₜ^β₃ + uₜ is linear in the parameters, because only xₜ is raised to a power.", False),
      ("The fund XXX line was estimated with market excess returns between 6.9% and 23.2%, so its intercept of −1.74 is a precise estimate of the fund's excess return when the market's excess return is zero.", False),
      ("Across different random samples the OLS estimate β̂ changes, so β̂ is a random variable; its standard error measures this estimation uncertainty.", True)]
p = statements_mcq("1", "Consider the following statements about what OLS can estimate and how far to trust it.", st,
                   [("I, II and V only", None), ("I, II, III and V only", "power_of_x_read_as_linear"), ("I, II, IV and V only", "intercept_extrapolated"),
                    ("I and V only", "log_model_not_linearised")], "I, II and V only")
HARD.append(hq(id="30285-L2-03", deck="L2", topic="Linear in parameters, transformations and extrapolating the intercept",
    objective="Important issues: linearity and transformations; accuracy of the intercept; population vs sample",
    shape="concept MCQ (statements)", shape_class="calc MCQ", stem="OLS: statements.", parts=[p],
    scheme=["[1] Steps: (1) I: nonlinear in the variable only; substitute zₜ = ln xₜ — true; (2) II: logs give ln Yₜ = β₁ + β₂ ln Xₜ + uₜ, linear in β₁, β₂ — true; "
            "(3) III: β₃ is an exponent on a parameter's regressor — intrinsically non-linear — false; (4) IV: no observations near x = 0, so the intercept is an extrapolation — false; "
            "(5) V: the estimator is a random variable across samples — true; (6) I, II and V.",
            "Second route: apply the slide's test to each model — are the parameters multiplied, divided or raised to a power? Only III fails it."],
    cites=[cite("L2", 21, "Linear in the parameters means that the parameters are not multiplied together, divided, squared or cubed etc."),
           cite("L2", 23, "Care needs to be exercised when considering the intercept estimate, particularly if there are no or few observations close to the y-axis"),
           cite("L2", 24, "Since our samples are not identical to the population, our estimates are subject to estimation uncertainty.")],
    location="2a slides: linearity, linear and non-linear models, accuracy of the intercept, population and sample", file=F_2, groups=["L2-3"], minutes=5,
    notches=["near_true_statements", "extra_classification", "extra_step"], hc_parts=[{"n": "1", "steps": 7, "concepts": 3}], units=["L2-U8", "L2-U9", "L2-U10", "L1C-U6"]))

# ---- L2B-1: OLS in matrix form ---------------------------------------------------------------------------------------------------
z6, y6 = [0, 1, 2, 3], [1, 3, 4, 6]
T6 = 4
a, b_, d = T6, sum(z6), sum(v * v for v in z6)
det = a * d - b_ * b_
inv = [[d / det, -b_ / det], [-b_ / det, a / det]]
xty = [sum(y6), sum(u * v for u, v in zip(z6, y6))]
beta = [inv[0][0] * xty[0] + inv[0][1] * xty[1], inv[1][0] * xty[0] + inv[1][1] * xty[1]]
near(det, 20); near(beta[0], 1.1); near(beta[1], 1.6)
zb, yb = sum(z6) / 4, sum(y6) / 4
b2 = sum((u - zb) * (v - yb) for u, v in zip(z6, y6)) / sum((u - zb) ** 2 for u in z6)
near(b2, beta[1]); near(yb - b2 * zb, beta[0])                            # route 2: cov/var and ybar - b*zbar
yhat5 = beta[0] + 5 * beta[1]
wrong_inv = [[d / det, b_ / det], [b_ / det, a / det]]
wb = [wrong_inv[0][0] * xty[0] + wrong_inv[0][1] * xty[1], wrong_inv[1][0] * xty[0] + wrong_inv[1][1] * xty[1]]
nd = [d * xty[0] - b_ * xty[1], -b_ * xty[0] + a * xty[1]]
opts = [(f"β̂ = ({f(beta[0])}, {f(beta[1])})′; ŷ at z = 5 is {f(yhat5)}", None),
        (f"β̂ = ({f(wb[0])}, {f(wb[1])})′; ŷ at z = 5 is {f(wb[0] + 5 * wb[1])}", "off_diagonal_signs_not_flipped"),
        (f"β̂ = ({f(nd[0])}, {f(nd[1])})′; ŷ at z = 5 is {f(nd[0] + 5 * nd[1])}", "determinant_left_out"),
        (f"β̂ = ({f(beta[1])}, {f(beta[0])})′; ŷ at z = 5 is {f(beta[1] + 5 * beta[0])}", "constant_and_slope_swapped")]
p = mcq("1", "Using β̂ = (X′X/T)⁻¹(X′Y/T) with X = [1_T Z], what is β̂ = (β̂₁, β̂₂)′ (constant first), and the fitted value when z = 5?", opts, opts[0][0], 1)
HARD.append(hq(id="30285-L2B-02", deck="L2B", topic="OLS by matrix algebra: X′X, its inverse and β̂",
    objective="OLS in matrix form: inverse of a 2×2 matrix, X′X and X′Y, the estimator β̂ = (X′X)⁻¹X′Y",
    shape="numerical MCQ with derivation", shape_class="calc MCQ",
    stem="Four observations: Z = (0, 1, 2, 3)′ and Y = (1, 3, 4, 6)′. The regression is Y = Xβ + u with X = [1_T Z] (T × 2).", parts=[p],
    scheme=[f"[1] Steps: (1) X′X = [4 6; 6 14]; (2) det = 4·14 − 6·6 = 20; (3) (X′X)⁻¹ = (1/20)[14 −6; −6 4]; (4) X′Y = (14, 29)′; "
            f"(5) β̂₁ = (14·14 − 6·29)/20 = 22/20 = 1.1; (6) β̂₂ = (−6·14 + 4·29)/20 = 32/20 = 1.6; (7) ŷ = 1.1 + 1.6·5 = {f(yhat5)}. The T's cancel: (X′X/T)⁻¹(X′Y/T) = (X′X)⁻¹X′Y.",
            "Second route: β̂₂ = cov(y, z)/var(z) = 8/5 = 1.6; β̂₁ = ȳ − β̂₂z̄ = 3.5 − 2.4 = 1.1 (asserted).",
            "Where marks are lost: not flipping the signs of the off-diagonal entries, forgetting to divide by the determinant, swapping the constant and the slope."],
    cites=[cite("L2B", 3, "Computation: in the 2x2 case"), cite("L2B", 5, "Using FOCs, one can prove that the OLS estimator can be expressed as"),
           cite("L2B", 4, "has dimension T by 1 (vector!) and represents the linear regression setting!")],
    location="2b slides: inverse of a squared matrix, definitions, linear regression in matrix format, extra derivations", file=F_2B, groups=["L2B-1"], minutes=5,
    notches=["chain", "cross_section", "extra_step"], hc_parts=[{"n": "1", "steps": 7, "concepts": 3}], units=["L2B-U1", "L2B-U2", "L2B-U3"]))

# ---- L2B-2: assumptions and properties --------------------------------------------------------------------------------------------
s2 = 40 / (12 - 2)
se = (s2 / 25) ** 0.5
near(s2, 4.0); near(se, 0.4); near(se, (4.0 * 1 / 25) ** 0.5)
st = [("If an omitted variable that is correlated with xₜ ends up in uₜ, then Cov(uₜ, xₜ) ≠ 0 and OLS is biased.", True),
      ("If Var(uₜ) grows with xₜ, the OLS estimator is biased.", False),
      ("In a simple regression with T = 12 and Σûₜ² = 40, the estimate of σ² is s² = 4.0.", True),
      ("'Best' in BLUE means that OLS has the smallest variance of all estimators, linear or not.", False),
      ("Lowering the size of a test from 5% to 1% makes a type I error less likely and a type II error more likely.", True),
      ("With s² = 4.0 and Σ(xₜ − x̄)² = 25, SE(β̂) = 0.4.", True)]
p = statements_mcq("1", "Consider the following statements about the assumptions and properties of OLS in yₜ = α + βxₜ + uₜ.", st,
                   [("I, III, V and VI only", None), ("I, II, III, V and VI only", "heteroscedasticity_read_as_bias"), ("I, V and VI only", "s2_divided_by_T"),
                    ("I, III, IV, V and VI only", "best_among_all_estimators")], "I, III, V and VI only")
HARD.append(hq(id="30285-L2B-03", deck="L2B", topic="Which assumption does what: bias, BLUE, s², test errors and a standard error",
    objective="Assumptions 1-4; unbiasedness vs efficiency; BLUE; estimating σ²; variance of β̂; type I and II errors",
    shape="concept MCQ (statements)", shape_class="calc MCQ", stem="OLS properties: statements.", parts=[p],
    scheme=["[1] Steps: (1) I: assumption 4 (Cov(uₜ, xₜ) = 0) fails → biased — true; (2) II: a non-constant variance breaks assumption 2, which BLUE needs, but unbiasedness needs only E(u|X) = 0 — false; "
            "(3) III: s² = 40/(12 − 2) = 4.0 (not 40/12 = 3.33) — true; (4) IV: 'best' is among linear unbiased estimators (Gauss-Markov) — false; "
            "(5) V: a smaller size means fewer false rejections and more failures to reject a false null — true; (6) VI: SE = √(s²/Σ(x − x̄)²) = √(4/25) = 0.4 — true; (7) I, III, V and VI.",
            "Second route for VI: Var(β̂₂) = σ²/(T·V(x)) on the slide, and T·V(x) = Σ(x − x̄)² = 25."],
    cites=[cite("L2B", 8, "No relationship between the error and corresponding x variate"),
           cite("L2B", 10, "means that the OLS estimator has minimum variance among the class of linear unbiased estimators"),
           cite("L2B", 17, "Reducing the probability of type I error increases 1:1 the prob of type 2 error.")],
    location="2b slides: PRF and SRF, assumptions, implications, BLUE, variance of the estimator, estimation of σ², inference errors", file=F_2B, groups=["L2B-2"], minutes=5,
    notches=["near_true_statements", "extra_step", "cross_section"], hc_parts=[{"n": "1", "steps": 7, "concepts": 4}],
    units=["L2B-U5", "L2B-U6", "L2B-U7", "L2B-U8", "L2B-U9", "L2B-U12"]))

# ---- L2C-1: multiple regression, the K x K variance-covariance matrix -----------------------------------------------------------------
V = [[0.04, 0.00, 0.01], [0.00, 0.09, 0.05], [0.01, 0.05, 0.16]]
bh = [0.5, 1.2, 0.7]
vd = V[1][1] + V[2][2] - 2 * V[1][2]
t = (bh[1] - bh[2]) / vd ** 0.5
vc = V[1][1] + 4 * V[2][2] + 2 * 2 * V[1][2]
near(vd, 0.15); near(vc, 0.93)
aa = [0, 1, -1]; near(sum(aa[i] * V[i][j] * aa[j] for i in range(3) for j in range(3)), vd)   # route 2: a'Va
cc = [0, 1, 2]; near(sum(cc[i] * V[i][j] * cc[j] for i in range(3) for j in range(3)), vc)
assert abs(t) < 2.01
opts = [(f"t = {f(t, 2)}, do not reject H₀; V(β̂₂ + 2β̂₃) = {f(vc, 2)}", None),
        (f"t = {f(0.5 / (0.09 + 0.16) ** 0.5, 2)}, do not reject H₀; V(β̂₂ + 2β̂₃) = {f(0.09 + 0.64, 2)}", "covariance_ignored"),
        (f"t = {f(0.5 / (0.09 + 0.16 + 0.10) ** 0.5, 2)}, do not reject H₀; V(β̂₂ + 2β̂₃) = {f(0.09 + 0.64 - 0.20, 2)}", "covariance_sign_flipped"),
        (f"t = {f(0.5 / vd, 2)}, reject H₀; V(β̂₂ + 2β̂₃) = {f(vc, 2)}", "variance_not_square_rooted")]
p = mcq("1", "Test H₀: β₂ = β₃ at 5% (two-sided; t with 50 degrees of freedom, critical value 2.01). What are the t-statistic and the decision, and what is the variance of β̂₂ + 2β̂₃?", opts, opts[0][0], 1)
HARD.append(hq(id="30285-L2C-02", deck="L2C", topic="Reading the K × K variance-covariance matrix: a t-test on β₂ − β₃",
    objective="Multiple regression: the K×K variance-covariance matrix σ²(X′X)⁻¹; testing a linear combination; variance of a combination",
    shape="numerical MCQ with derivation", shape_class="calc MCQ",
    stem="yₜ = β₁ + β₂x₂ₜ + β₃x₃ₜ + uₜ is estimated by OLS on T = 53 observations: β̂ = (0.5, 1.2, 0.7)′ and the estimated variance-covariance matrix of β̂ is "
         "[0.04 0.00 0.01; 0.00 0.09 0.05; 0.01 0.05 0.16] (rows separated by ';').", parts=[p],
    scheme=[f"[1] Steps: (1) the matrix is K × K = 3 × 3 and V(β̂₂) = 0.09, V(β̂₃) = 0.16, cov = 0.05; (2) β̂₂ − β̂₃ = 0.5; (3) V(β̂₂ − β̂₃) = 0.09 + 0.16 − 2·0.05 = 0.15; "
            f"(4) SE = √0.15 = {f(vd ** 0.5, 4)}; (5) t = 0.5/{f(vd ** 0.5, 4)} = {f(t, 3)} < 2.01 → do not reject; (6) V(β̂₂ + 2β̂₃) = 0.09 + 4·0.16 + 2·2·0.05 = {f(vc, 2)}.",
            "Second route: a′Va with a = (0, 1, −1)′ and (0, 1, 2)′ — the sandwich rule (asserted).",
            "Where marks are lost: dropping the covariance, adding it with the wrong sign, dividing by the variance instead of the standard error; degrees of freedom T − k = 50."],
    cites=[cite("L2C", 7, "And the (K by K) variance-covariance matrix is still"), cite("L2C", 6, "Just add more columns to your X matrix and more betas!!"),
           cite("L2B", 16, "Use a N(0,1) for (2-0)/0.5 = 4")],
    location="2c slides: multiple linear regression, OLS results; 2b hypothesis testing; 1c sandwich rule", file=F_2C, groups=["L2C-1"], minutes=5,
    notches=["cross_section", "extra_step", "what_if_followon"], hc_parts=[{"n": "1", "steps": 6, "concepts": 3}],
    units=["L2C-U2", "L2C-U3", "L2B-U10", "L2B-U11"]))

# ---- L2C-3: goodness of fit ------------------------------------------------------------------------------------------------------
T9, k9, TSS, RSS = 45, 4, 200.0, 150.0
R2 = 1 - RSS / TSS
aR2 = 1 - (T9 - 1) / (T9 - k9) * (1 - R2)
F9 = R2 / (1 - R2) * (T9 - k9) / (k9 - 1)
near(R2, 0.25); near(F9, ((TSS - RSS) / (k9 - 1)) / (RSS / (T9 - k9)))   # route 2: ESS/(k-1) over RSS/(T-k)
R2b = 1 - 147.0 / TSS
aR2b = 1 - (T9 - 1) / (T9 - 5) * (1 - R2b)
assert R2b > R2 and aR2b < aR2 and F9 > 2.83
st = [("R² = 0.25 and the explained sum of squares is 50.", True),
      (f"Adjusted R² is about {f(aR2, 3)}.", True),
      (f"The F-statistic for H₀: β₂ = β₃ = β₄ = 0 is about {f(F9, 2)}, with (3, 41) degrees of freedom.", True),
      ("Adding a fifth regressor that lowers the RSS to 147 raises both R² and adjusted R².", False),
      ("With the F(3, 41) critical value of 2.83 at 5%, we reject that all slope coefficients are zero.", True)]
p = statements_mcq("1", "A regression with a constant and three regressors (k = 4) on T = 45 observations has TSS = 200 and RSS = 150.", st,
                   [("I, II, III and V only", None), ("I, II, III, IV and V only", "adjusted_r2_always_rises"), ("I, III and V only", "adjusted_r2_formula_misapplied"),
                    ("I, II and III only", "f_statistic_not_compared")], "I, II, III and V only")
HARD.append(hq(id="30285-L2C-03", deck="L2C", topic="R², adjusted R² and the regression F-test from the sums of squares",
    objective="Goodness of fit: TSS = ESS + RSS, R², R² and the F-test, adjusted R²",
    shape="concept MCQ (statements)", shape_class="calc MCQ", stem="Goodness of fit: statements.", parts=[p],
    scheme=[f"[1] Steps: (1) R² = 1 − 150/200 = 0.25; ESS = 200 − 150 = 50 — I true; (2) adj R² = 1 − (44/41)(0.75) = {f(aR2, 4)} — II true; "
            f"(3) F = (0.25/0.75)(41/3) = {f(F9, 3)} with (k − 1, T − k) = (3, 41) — III true; (4) new R² = {f(R2b,3)} but adj R² = 1 − (44/40)(0.735) = {f(aR2b, 4)} falls — IV false; "
            f"(5) {f(F9, 2)} > 2.83 → reject — V true; (6) I, II, III and V.",
            f"Second route for III: F = (ESS/3)/(RSS/41) = 16.667/3.659 = {f(F9, 3)} (asserted).",
            "Where marks are lost: assuming adjusted R² always rises with R², using (T − 1)/(T − k) the wrong way up, reading the degrees of freedom in the wrong order."],
    cites=[cite("L2C", 18, "R2 must always lie between zero and one"), cite("L2C", 20, "The F-test for the assumption that all coefficients are null, except the intercept"),
           cite("L2C", 21, "So if we add an extra regressor, k increases and unless R2 increases by a more than offsetting amount")],
    location="2c slides: defining R², R² and the F-test, adjusted R²", file=F_2C, groups=["L2C-3"], minutes=5,
    notches=["what_if_followon", "extra_step", "near_true_statements"], hc_parts=[{"n": "1", "steps": 7, "concepts": 3}], units=["L2C-U9", "L2C-U10", "L2C-U11"]))

# ================================================================================================
# Deck sections and units
# ================================================================================================
SECTIONS = {
    "L1B": [{"id": "L1B-1", "title": "Financial econometrics and its data"}, {"id": "L1B-2", "title": "Returns"},
            {"id": "L1B-3", "title": "Risk: expected values, variance, covariance and correlation"}],
    "L1C": [{"id": "L1C-1", "title": "Linear algebra"}, {"id": "L1C-2", "title": "Statistics in vector form and standard errors"}],
    "L2": [{"id": "L2-1", "title": "Regression and the disturbance term"}, {"id": "L2-2", "title": "Deriving and using the OLS estimator"},
           {"id": "L2-3", "title": "Important issues: linearity, the intercept, the sample"}],
    "L2B": [{"id": "L2B-1", "title": "OLS in matrix form"}, {"id": "L2B-2", "title": "Assumptions and properties of OLS"}, {"id": "L2B-3", "title": "Inference"}],
    "L2C": [{"id": "L2C-1", "title": "Multiple regression"}, {"id": "L2C-2", "title": "Testing multiple hypotheses: the F-test"}, {"id": "L2C-3", "title": "Goodness of fit"}],
}


def U(id, section, title, where, examinable=True, reason=None):
    u = {"id": id, "section": section, "title": title, "where": where, "examinable": examinable}
    if reason:
        u["reason"] = reason
    return u


UNITS = {
    "L1B": [U("L1B-U1", "L1B-1", "What financial econometrics is and what it is used for", "slides 2–3"),
            U("L1B-U2", "L1B-1", "Financial data: frequency, quality, noise", "slide 4"),
            U("L1B-U3", "L1B-1", "Data dimensions: time series, cross-section, panel (balanced)", "slides 5–9"),
            U("L1B-U4", "L1B-1", "Cardinal, ordinal and nominal numbers", "slide 10"),
            U("L1B-U5", "L1B-2", "Raw gross, raw net and log returns", "slides 11–12"),
            U("L1B-U6", "L1B-2", "Portfolio returns; log returns do not add up across assets", "slide 13"),
            U("L1B-U7", "L1B-3", "The value of $1 invested in 1899 (nominal and real)", "slides 14–16", False,
              "Charts only (a historical illustration with no figures to work with); the return definitions behind them are examined through L1B-U5."),
            U("L1B-U8", "L1B-3", "Histograms, averages and expected values", "slides 17–18"),
            U("L1B-U9", "L1B-3", "Variance and standard deviation as risk", "slide 19"),
            U("L1B-U10", "L1B-3", "Portfolio variance and covariance", "slides 20–22"),
            U("L1B-U11", "L1B-3", "Correlation", "slide 23")],
    "L1C": [U("L1C-U1", "L1C-1", "Guidance: what computations and derivations the exam needs", "slide 3", False,
              "Course guidance on how the exam treats computations (Python) and derivations ('just the simplest ones'), not content."),
            U("L1C-U2", "L1C-1", "Vectors, matrices, transposes and the variance-covariance matrix", "slide 4"),
            U("L1C-U3", "L1C-1", "Matrix multiplication", "slide 5"),
            U("L1C-U4", "L1C-1", "Matrix sums", "slide 6"),
            U("L1C-U5", "L1C-2", "Sample average and variance in vector form", "slide 8"),
            U("L1C-U6", "L1C-2", "Population and sample; estimation uncertainty and inference", "slides 10–11"),
            U("L1C-U7", "L1C-2", "The sample mean as a random variable; its standard error σ/√T", "slide 12"),
            U("L1C-U8", "L1C-2", "Rules for random vectors: expectation, var-cov matrix, the sandwich rule", "slide 14"),
            U("L1C-U9", "L1C-2", "The sample mean in vector form: expectation and variance by the sandwich rule", "slide 15")],
    "L2": [U("L2-U1", "L2-1", "Regression: definition and notation (dependent and independent variables)", "slides 3–4"),
           U("L2-U2", "L2-1", "Simple regression: examples and the fund XXX data", "slides 6–8"),
           U("L2-U3", "L2-1", "Line of best fit and the disturbance term", "slides 9–10"),
           U("L2-U4", "L2-2", "OLS: minimising the residual sum of squares; actual and fitted values", "slides 12–15"),
           U("L2-U5", "L2-2", "Covariance review", "slide 16"),
           U("L2-U6", "L2-2", "The OLS estimator: β̂ = cov/var, α̂ = ȳ − β̂x̄; its derivation", "slides 17, 27–28"),
           U("L2-U7", "L2-2", "Using the estimates; estimators vs estimates", "slides 18–19"),
           U("L2-U8", "L2-3", "Linearity in the parameters and transformations", "slides 21–22"),
           U("L2-U9", "L2-3", "Accuracy of the intercept: extrapolation", "slide 23"),
           U("L2-U10", "L2-3", "Population and sample: estimation uncertainty", "slide 24")],
    "L2B": [U("L2B-U1", "L2B-1", "Inverse of a 2×2 matrix", "slides 3, 21"),
            U("L2B-U2", "L2B-1", "Average, variance and covariance in matrix form; Xβ", "slide 4"),
            U("L2B-U3", "L2B-1", "OLS in matrix form: β̂ = (X′X/T)⁻¹(X′Y/T)", "slides 5, 22–23"),
            U("L2B-U4", "L2B-2", "Population and sample regression functions (PRF, SRF)", "slide 7"),
            U("L2B-U5", "L2B-2", "Assumptions 1-4 on the errors", "slide 8"),
            U("L2B-U6", "L2B-2", "Consistency and unbiasedness", "slide 9"),
            U("L2B-U7", "L2B-2", "BLUE and the Gauss-Markov theorem", "slide 10"),
            U("L2B-U8", "L2B-2", "Efficiency and the variance of β̂: σ²(X′X)⁻¹", "slides 11–12"),
            U("L2B-U9", "L2B-2", "Estimating σ²: s² = Σû²/(T − 2)", "slide 13"),
            U("L2B-U10", "L2B-3", "Normality and the distribution of β̂; t vs normal", "slide 15"),
            U("L2B-U11", "L2B-3", "Hypothesis tests (two- and one-sided)", "slide 16"),
            U("L2B-U12", "L2B-3", "Type I and type II errors", "slide 17"),
            U("L2B-U13", "L2B-3", "Confidence intervals", "slide 18")],
    "L2C": [U("L2C-U1", "L2C-1", "The sample average as a regression on a constant", "slide 4"),
            U("L2C-U2", "L2C-1", "Simple and multiple regression in matrix form", "slides 5–6"),
            U("L2C-U3", "L2C-1", "OLS results: the K×K var-cov matrix and s² = û′û/(T − k)", "slide 7"),
            U("L2C-U4", "L2C-2", "Why an F-test: restricted and unrestricted regressions", "slide 9"),
            U("L2C-U5", "L2C-2", "Imposing a restriction: building the restricted regression", "slides 10–11"),
            U("L2C-U6", "L2C-2", "The F-statistic, its distribution and the decision", "slides 12–14"),
            U("L2C-U7", "L2C-2", "Counting restrictions; the regression F-statistic", "slide 15"),
            U("L2C-U8", "L2C-2", "Worked example: unit sensitivity to two factors", "slide 16"),
            U("L2C-U9", "L2C-3", "R-squared: TSS, ESS and RSS", "slides 18–19"),
            U("L2C-U10", "L2C-3", "R-squared and the F-test", "slide 20"),
            U("L2C-U11", "L2C-3", "Adjusted R-squared", "slide 21")],
}

EXISTING_UNITS = {"30285-L1B-01": ["L1B-U5", "L1B-U6", "L1B-U10"], "30285-L1C-01": ["L1C-U5", "L1C-U7", "L1C-U8", "L1C-U9"],
                  "30285-L2-01": ["L2-U4", "L2-U5", "L2-U6", "L2-U7", "L2B-U9", "L2B-U11"], "30285-L2B-01": ["L2B-U8", "L2B-U10", "L2B-U11", "L2B-U13"],
                  "30285-L2C-01": ["L2C-U5", "L2C-U6", "L2C-U7", "L2C-U8", "L2C-U10", "L2C-U11"]}
EXISTING_GROUPS = {"30285-L1B-01": ["L1B-2", "L1B-3"], "30285-L1C-01": ["L1C-2"], "30285-L2-01": ["L2-2"], "30285-L2B-01": ["L2B-3"], "30285-L2C-01": ["L2C-2", "L2C-3"]}


def D(file, item, decision, ids=None, reason=""):
    return {"file": file, "item": item, "decision": decision, "ids": ids or [], "reason": reason}


LATER = "Taught after deck 2c ({}); that deck is not in the folder yet. Held until it arrives."
H_SC = LATER.format("serial correlation, the correlogram and HAC standard errors")
H_HET = LATER.format("heteroscedasticity, residual plots and White standard errors")
H_MC = LATER.format("Montecarlo simulations and the bootstrap")
H_APT = LATER.format("APT: time-series and cross-sectional tests, Fama-MacBeth")
H_TS = LATER.format("AR, MA and ARIMA processes")
H_PAN = LATER.format("panel data: fixed effects, time effects, between estimator")
H_PRED = LATER.format("return predictability and Lettau-Ludvigson")
LEDGER = [
    D(F_SYL, "Syllabus 2026-27", "used", [], "Final exam 60% or 80% of the grade, quiz and homework; sets the course format."),
    D(F_EFP, "Exam first page", "used", [], "Instructions: 15 MCQs in 35 minutes; sets the count and the time per question."),
    D("Slides/1_Introduction_to_Course", "Course introduction deck", "not_examinable", [], "Course organisation (grading, calendar, materials), not examinable content."),
    D(F_1B, "1b deck", "units", [], "Sections L1B-1 to L1B-3."), D(F_1C, "1c deck", "units", [], "Sections L1C-1 and L1C-2."),
    D(F_2, "2a deck", "units", [], "Sections L2-1 to L2-3."), D(F_2B, "2b deck", "units", [], "Sections L2B-1 to L2B-3."),
    D(F_2C, "2c deck", "units", [], "Sections L2C-1 to L2C-3."),
    D(F_PM, "Exercises 1-2 (moments, uncorrelated portfolio)", "included", ["30285-L1B-13"]),
    D(F_PM, "Exercise 3 (xAB′)", "included", ["30285-L1C-10"]),
    # Practice Quiz #1
    D(F_PQ1, "Q1 (APT, MKT 6% / LL 5%)", "held", [], H_APT),
    D(F_PQ1, "Q2 (disturbance term)", "included", ["30285-L2-10"]),
    D(F_PQ1, "Q3 (correlogram, 100 observations)", "held", [], H_SC),
    D(F_PQ1, "Q4 (average and variance in vector form)", "included", ["30285-L1C-11"]),
    D(F_PQ1, "Q5 (restricted regression for 2β₂ = β₃)", "included", ["30285-L2C-12"]),
    D(F_PQ1, "Q6 (Python: HAC options commented out)", "held", [], H_SC),
    D(F_PQ1, "Q7 (Montecarlo)", "held", [], H_MC),
    D(F_PQ1, "Q8 (residual scatter plot)", "held", [], H_HET),
    D(F_PQ1, "Q9 (standard error of the mean under heteroscedasticity: White)", "held", [], H_HET + " The key (c) depends on the White correction."),
    D(F_PQ1, "Q10 (T = 8 chi-square sample, Montecarlo)", "held", [], H_MC),
    # Practice Exam #1
    D(F_PE1, "Q1 (APT, MKT 5% / LL 5%)", "held", [], H_APT),
    D(F_PE1, "Q2 (correlogram)", "held", [], H_SC),
    D(F_PE1, "Q3 (restricted regression, variant with 2x₂ₜ + x₃ₜ)", "included", ["30285-L2C-13"]),
    D(F_PE1, "Q4 (Montecarlo)", "held", [], H_MC),
    D(F_PE1, "Q5 (residual scatter plot)", "held", [], H_HET),
    D(F_PE1, "Q6 (Fama-MacBeth)", "held", [], H_APT),
    D(F_PE1, "Q7 (ARIMA(0,1,0))", "held", [], H_TS),
    D(F_PE1, "Q8 (Lettau and Ludvigson)", "held", [], H_PRED),
    D(F_PE1, "Q9 (fixed effects)", "held", [], H_PAN),
    D(F_PE1, "Q10 (APT, two assets, market prices of risk)", "held", [], H_APT),
    D(F_PE1, "Essay (AR(1) cash flow: present value 5.5 and its variance)", "held", [], H_TS),
    # Practice Quiz #2
    D(F_PQ2, "Q1 (what financial econometrics is)", "included", ["30285-L1B-10"]),
    D(F_PQ2, "Q2 (disturbance term)", "duplicate", ["30285-L2-10"], "Word for word the same as Practice Quiz #1 Q2."),
    D(F_PQ2, "Q3 (correlogram)", "held", [], H_SC),
    D(F_PQ2, "Q4 (buy at 50, dividend 5, sell at 70)", "included", ["30285-L1B-12"]),
    D(F_PQ2, "Q5 (bootstrap)", "held", [], H_MC),
    D(F_PQ2, "Q6 (Python command for heteroscedasticity)", "held", [], H_HET),
    D(F_PQ2, "Q7 (residual scatter plot)", "held", [], H_HET),
    D(F_PQ2, "Q8 (correlogram of residuals, HAC with L = 4)", "held", [], H_SC),
    D(F_PQ2, "Q9 (4-by-4 variance-covariance matrix)", "included", ["30285-L2C-14"]),
    D(F_PQ2, "Q10 (x₂ₜ/β₂: not linear)", "included", ["30285-L2-11"]),
    # Practice Exam #2
    D(F_PE2, "Q1 (what financial econometrics is, variant)", "included", ["30285-L1B-11"]),
    D(F_PE2, "Q2 (disturbance term)", "duplicate", ["30285-L2-10"], "Word for word the same as Practice Quiz #1 Q2."),
    D(F_PE2, "Q3 (AR(1) correlogram)", "held", [], H_SC),
    D(F_PE2, "Q4 (bootstrap)", "held", [], H_MC),
    D(F_PE2, "Q5 (Fama-MacBeth, 10 stocks and 200 observations)", "held", [], H_APT),
    D(F_PE2, "Q6 (ARIMA(0,0,0))", "held", [], H_TS),
    D(F_PE2, "Q7 (panel: fixed or random effects)", "held", [], H_PAN),
    D(F_PE2, "Q8 (between estimator)", "held", [], H_PAN),
    D(F_PE2, "Q9 (APT, two assets)", "held", [], H_APT),
    D(F_PE2, "Q10 (time fixed effects)", "held", [], H_PAN),
    D(F_PE2, "Essay (AR(1): population R² = ρ², SE of ρ̂, White errors)", "held", [], H_TS + " Part 3 also needs White errors."),
    D("Practice Quiz/ and Practice Exam/ (Practice_1 and Practice_2 question papers, .pdf and .docx)", "All items", "duplicate", [],
      "The same questions as the solution files, without the bold key; the solution files are used."),
    # Past exams
    D(F_X1, "20 Dec 2021 final: Q1 (APT), Q4 (cross-sectional APT tests), Q8 (APT market prices of risk)", "held", [], H_APT),
    D(F_X1, "20 Dec 2021 final: Q2 (correlogram, 12 observations)", "held", [], H_SC),
    D(F_X1, "20 Dec 2021 final: Q3 (t-test on β₁ − β₂)", "included", ["30285-L2C-10"]),
    D(F_X1, "20 Dec 2021 final: Q5, Q6", "not_read", [], "Not in the photos or in the Studocu screenshots of the review."),
    D(F_X1, "20 Dec 2021 final: Q7 (DGP: T ≥ 4, BLUE, omitted zₜ)", "included", ["30285-L2B-10"]),
    D(F_X1, "20 Dec 2021 final: Q9 (panel inputs)", "held", [], H_PAN),
    D(F_X1, "20 Dec 2021 final: Q10 (Python: regression on a constant)", "included", ["30285-L2C-11"]),
    D(F_X1, "20 Dec 2021 final: Q11 (V(β̂) = [16 12; 12 9], estimates (0, 6))", "included", ["30285-L2B-12"]),
    D(F_X1, "20 Dec 2021 final: Q12-Q15 (MA(2) process)", "held", [], H_TS),
    D(F_SPP2, "Whole file", "key_source", ["30285-L2C-10", "30285-L2B-10", "30285-L2C-11", "30285-L2B-12"],
      "Studocu copy of the 20 Dec 2021 Blackboard review (Q1-Q4, Q7-Q15, green ticks): used to check the transcription and the keys of the photos."),
    D(F_X2, "Q1 (DGP: T ≥ 3, BLUE, omitted-variable bias)", "included", ["30285-L2B-11"]),
    D(F_X2, "Q2 (correlogram, 52 observations)", "held", [], H_SC),
    D(F_X2, "Q3 (ARIMA(0,1,0))", "held", [], H_TS),
    D(F_X2, "Q4 (panel, time fixed effects)", "held", [], H_PAN),
    D(F_X2, "Q5 (V(β̂) = [16 12; 12 9], estimates (5, 1))", "included", ["30285-L2B-13"]),
    D(F_X2, "Q6 (cross-sectional APT tests), Q7 (APT: two assets, market prices of risk)", "held", [], H_APT),
    D(F_X2, "Q8 (Montecarlo)", "held", [], H_MC),
    D(F_X2, "Q9 (Lettau and Ludvigson)", "held", [], H_PRED),
    D(F_X2, "Page 6 (partial variant of Q10-Q11: Python code, estimates (5, 3))", "duplicate", ["30285-L2C-11", "30285-L2B-13"],
      "Same questions with other numbers: the Python item is the Dec 2021 Q10; (5, 3) gives β̂₁ + 3β̂₂ ~ N(14, 169), the same method as Q5."),
    D(F_X3, "Whole file (32 photos of a sitting, no answers marked)", "duplicate", ["30285-L2B-10", "30285-L2B-12", "30285-L2C-11"],
      "The in-scope items (DGP with T ≥ 4, V(β̂) with estimates (0, 6), the Python code) are the Dec 2021 questions word for word."),
    D(F_X3, "AR(2), MA(2), ARIMA(1,0,0) and ARIMA(2,2,2) items; APT, panel, Montecarlo and Lettau-Ludvigson items", "held", [], H_TS + " The other topics are held for the same reason (see above)."),
    D(F_XP, "Whole file ('Finx 2019' student notes on past exams)", "duplicate", ["30285-L2B-10", "30285-L2C-11"],
      "A student's OneNote copy of the same past-exam questions with the student's own answers highlighted; the official keys come from the Blackboard ticks."),
    D(F_XP, "Predictability items (r = 8% + xₜ + e, AR(1) x with ρ = 0.9, R² and serial correlation of expected returns)", "held", [], H_PRED),
    D(F_QM, "Whole file", "duplicate", ["30285-L2-10", "30285-L1C-11", "30285-L2C-12"], "Studocu copy of Practice Quiz #1."),
    D(F_QM2, "Whole file", "duplicate", ["30285-L2-10", "30285-L1C-11", "30285-L2C-12"], "Studocu copy of Practice Quiz #1 with a student's marks."),
    D(F_SX2, "Whole file", "duplicate", ["30285-L2B-11", "30285-L2B-13"], "Studocu copy of 'Econometrics past exam 2' (same title, same pages)."),
    D(F_SX3, "Whole file", "duplicate", ["30285-L2B-10"], "Studocu copy of 'Econometrics past exam 3' (same title, same size)."),
    D(F_CLEAN, "Copies of past exams 1-3, Past Exams, quiz_mock, quiz_mock_2", "duplicate", [], "Same files as in Reference/."),
    D(F_BRK, "Textbook (Brooks, 2nd edition)", "excluded", [], "Reference textbook; its end-of-chapter questions are not course exam material, and the slides define the syllabus."),
    D(F_BRX, "Brooks index", "excluded", [], "Reference only: the textbook index."),
    D("Mock Exams/ (Claude-written mocks)", "All items", "excluded", [], "Claude-written mocks are not evidence."),
]
