# Worked examples, one per subject

Each example uses different numbers from the practice questions in Answer Grid, so you can study the method without seeing the answers. Every number below is computed and cross-checked in `banks/build_banks.py`.

## 30178 International Banking: an SVB-style run

**Problem.** A bank holds cash 10, AFS securities 30 (duration 4.0) and HTM securities 60 at cost (duration 5.0); deposits are 150, 80% uninsured; equity is 12 ($bn). Rates rise 2 points. Then 40% of uninsured deposits leave. The bank pays with cash, then AFS, then HTM, all at fair value. What is reported equity at the end?

**Solution.**

1. Classify first. AFS is marked to market through OCI, so its loss hits equity now. HTM stays at cost; its loss hits equity only if securities are sold.
2. AFS loss = 4.0 × 2% × 30 = 2.40. Reported equity = 12 − 2.40 = **9.60**.
3. HTM unrealised loss = 5.0 × 2% × 60 = 6.00. It is not recognised yet, but it is why depositors worry: economic equity is only 3.60.
4. Withdrawal = 40% × 80% × 150 = 48.0.
5. Pay 10 from cash and 27.6 from AFS (fair value). Still needed: 10.4.
6. HTM sells at 90% of cost, so cost sold = 10.4 / 0.90 = 11.56.
7. Realised loss = 11.56 − 10.4 = 1.16.
8. Reported equity = 9.60 − 1.16 = **8.44**.

Check: each $ raised from HTM costs 6/54 = 0.1111 of equity; 10.4 × that = 1.16.

**Traps:** forgetting that the AFS loss is already in equity; recognising the whole HTM loss; selling HTM before AFS.

## 30257 Corporate Valuation: bottom-up beta and WACC

**Problem.** A private company's comparables have raw levered betas and market D/E of 1.45 and 0.60, and 0.90 and 0.25. Target D/E is 0.50, the statutory tax rate 24%, the risk-free rate 3% and the MRP 6%. EBIT is €50m and interest €18m. Use Blume's adjustment, the Hamada formula and the slide's synthetic-rating table. Find the WACC.

**Solution.**

1. Blume: 1.45 × 2/3 + 1/3 = 1.300; 0.90 × 2/3 + 1/3 = 0.933.
2. Unlever: 1.300 / (1 + 0.60 × 0.76) = 0.8929; 0.933 / (1 + 0.25 × 0.76) = 0.7843.
3. Industry βU = average = 0.8386.
4. Relever at 0.50: 0.8386 × (1 + 0.50 × 0.76) = 1.1572.
5. kEL = 3% + 1.1572 × 6% = **9.94%**.
6. Interest coverage = 50 / 18 = 2.78× → band 2.5–3.0, B1/B+, spread 2.6% → kD = 5.6%, after tax 4.256%.
7. Weights from D/E = 0.50: equity 66.67%, debt 33.33%.
8. WACC = 0.6667 × 9.943% + 0.3333 × 4.256% = **8.05%**.

**Traps:** skipping Blume; using the effective tax rate; taking 0.50 as the debt weight (it is D/E, so the weight is 0.5/1.5); leaving kD pre-tax.

## 30285 Empirical Methods: OLS by hand and a t-test

**Problem.** Data (x, y): (2, 3), (4, 4), (6, 8), (8, 9), (10, 11). Estimate y = α + βx + u by OLS, then test β = 0 at 5% (t with 3 df, critical value 3.18).

**Solution.**

1. Means: x̄ = 6, ȳ = 7.
2. Deviations: x − x̄ = (−4, −2, 0, 2, 4); y − ȳ = (−4, −3, 1, 2, 4).
3. Σ(x − x̄)(y − ȳ) = 42; Σ(x − x̄)² = 40.
4. β̂ = 42/40 = **1.05**; α̂ = 7 − 1.05 × 6 = **0.70**.
5. Residuals: (0.20, −0.90, 1.00, −0.10, −0.20); RSS = 1.90.
6. s² = RSS/(T − 2) = 0.6333; s = 0.7958.
7. SE(β̂) = s/√Σ(x − x̄)² = 0.7958/√40 = 0.1258.
8. t = 1.05/0.1258 = **8.34** > 3.18: reject β = 0.

Check: β̂ = Cov(x, y)/Var(x) with E[xy] − x̄ȳ gives the same slope.

**Traps:** dividing RSS by T; forgetting Σ(x − x̄)² in the SE; testing against the wrong null.

## 30024 Financial Statement Analysis: management account method

**Problem.** Inventories 180, trade receivables 220, operating prepayments 15; trade payables 200, accrued operating expenses 35, customer prepayments 25; PP&E 700, right-of-use assets 60, investment property 120; bank debt 420, lease liabilities 65, cash 50, marketable securities 30 (€k). Compute ONWC, NIC and NFP.

**Solution.**

1. Operating current assets = 180 + 220 + 15 = 415.
2. Operating current liabilities = 200 + 35 + 25 = 260.
3. ONWC = **155**.
4. Operating non-current assets = PP&E 700 + right-of-use 60 = 760. Investment property is non-operating: leave it out.
5. NIC = 155 + 760 = **915**.
6. Gross financial debt = 420 + lease liabilities 65 = 485.
7. Financial assets = cash 50 + securities 30 = 80.
8. NFP = **405**.

**Traps:** leaving leases out of NFP or right-of-use assets out of NIC; putting investment property in NIC; treating tax payable or loans to related parties as operating.
