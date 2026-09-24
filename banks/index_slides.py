"""Build banks/slide_index.json from the slide PDFs and check every citation against them.

Usage: python3 banks/index_slides.py <folder with the deck PDFs>   (needs PyMuPDF: pip install pymupdf)

For each citation whose `slide` is a title (or carries its original title in `title`), the quote is searched in the
text layer of every page of that deck; the page where it appears becomes the slide number. Citations that already
have a number are checked: the quote must be on that page. Anything not found is printed and the script exits 1.
The Stern reading (30178 READING) has a broken text layer and cites printed page numbers, so it is skipped.
"""
import json, pathlib, re, sys
import pymupdf

PDF = {("30024", "S1"): "30024 - AM - Session 1 - Intro.pdf", ("30024", "S2"): "30024 - AM - Session 2.pdf",
       ("30024", "S34"): "30024 - AM - Session 3 - 4 Reclassification.pdf",
       ("30178", "INTRO"): "Introductory concepts to banking_30178_2026-27.pdf", ("30178", "IRR"): "Managing Interest Rate Risk_2026-27_PART I and 2_classroom.pdf",
       ("30178", "SVB"): "The SVB case_in class discussion.pdf",
       ("30257", "L12"): "Corporate Valuation - AY 26-27 - Lectures 1-2 - Introduction - v3.pdf", ("30257", "L3"): "Corporate Valuation - AY 26-27 - Lecture 3 - DCF Valuation - v6.pdf",
       ("30257", "L4"): "Corporate Valuation - C31 - Lecture 4 - Cost of Capital - v3.pdf", ("30257", "L5"): "Corporate Valuation - C31 - Lecture 5 - Reorganizing and CFs - v13.pdf",
       ("30257", "L6"): "Corporate Valuation - C31 - Lecture 6 - DCF Exercises - v1.pdf",
       ("30285", "L1B"): "1b_Introduction_to_Content.pdf", ("30285", "L1C"): "1c_LinearAlgebra_and_Inference_v2.pdf", ("30285", "L2"): "2_Simple_LinRegr.pdf",
       ("30285", "L2B"): "2b_Simple_LinRegr_Inference.pdf", ("30285", "L2C"): "2c_LinearRegr_FTest.pdf"}
SKIP = {("30178", "READING")}
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("ﬁ", "fi").replace("ﬂ", "fl"))

folder = pathlib.Path(sys.argv[1])
pages = {k: [norm(p.get_text()) for p in pymupdf.open(folder / v)] for k, v in PDF.items() if (folder / v).exists()}
here = pathlib.Path(__file__).parent
index, bad, checked = {}, [], 0
for f in sorted(here.glob("bank_*.json")):
    for q in json.loads(f.read_text())["questions"]:
        for c in q["citations"]:
            k = (q["course"], c["deck"])
            if k in SKIP:
                continue
            if k not in pages:
                bad.append(f"{q['id']}: no PDF for deck {c['deck']}"); continue
            hits = [i + 1 for i, p in enumerate(pages[k]) if norm(c["quote"]) in p]
            title = c.get("title", c["slide"] if not isinstance(c["slide"], int) else None)
            if title is not None:
                t = norm(title)
                pick = [h for h in hits if t in pages[k][h - 1]] or hits
                if not pick:
                    bad.append(f"{q['id']}: quote not found in {c['deck']}: {c['quote'][:60]}"); continue
                index[f"{q['course']}|{c['deck']}|{title}|{c['quote']}"] = pick[0]
            elif c["slide"] not in hits:
                bad.append(f"{q['id']}: {c['deck']} slide {c['slide']} does not contain the quote (found on {hits}): {c['quote'][:60]}")
            checked += 1
(here / "slide_index.json").write_text(json.dumps({"page_counts": {f"{a}|{b}": len(v) for (a, b), v in pages.items()}, "index": index}, ensure_ascii=False, indent=0))
print(f"{checked} citations checked against the PDFs; {len(index)} title citations indexed")
for b in bad:
    print("FAIL", b)
sys.exit(1 if bad else 0)
