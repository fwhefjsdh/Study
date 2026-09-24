/* Pre-creation review: runs every generated bank question through the site's own validator (validateQuestion)
   and the harder-rule guardrail (reviewHarder) against its course's fingerprint. Exits non-zero on any failure. */
const fs=require("fs"),path=require("path"),vm=require("vm");
const E=require("../js/logic.js");
const ctx={window:{}};vm.runInNewContext(fs.readFileSync(path.join(__dirname,"../data/seed.js"),"utf8"),ctx);
const known={...ctx.window.AG_SEED.courses};
let bad=0,n=0;const ids=new Set(Object.keys(ctx.window.AG_SEED.questions));
for(const f of fs.readdirSync(__dirname).filter(f=>/^bank_.*\.json$/.test(f)).sort()){
  const b=JSON.parse(fs.readFileSync(path.join(__dirname,f),"utf8"));(b.courses||[]).forEach(c=>known[c.code]=c);
  for(const q of b.questions){n++;
    const errs=E.validateQuestion(q);if(ids.has(q.id))errs.push("duplicate id");ids.add(q.id);
    const g=E.reviewHarder(q,known[q.course]);
    if(g.status!=="pass")errs.push("harder rule: "+g.checks.filter(c=>!c.ok).map(c=>c.label+" ("+c.detail+")").join("; "));
    (q.subquestions||[]).forEach(s=>{if(s.options&&s.options.length){const r=E.mcqResults(q,{[s.n]:E.keyIndex(s,q.answer_key.find(k=>k.n===s.n))});if(!r.find(x=>x.n===s.n).correct)errs.push("key does not mark itself correct: "+s.n);}});
    const T=g.thresholds;
    console.log((errs.length?"FAIL ":"pass ")+q.id.padEnd(15)+" "+(T?`[${T.sc}: steps > ${T.stepsFloor} & ≥ ${T.stepsMin}, concepts ≥ ${T.conceptsMin}, ≤ ${T.minutesCap} min/answer]`:"")+(errs.length?"\n     "+errs.join("\n     "):""));
    if(errs.length)bad++;}
}
console.log(`\n${n-bad}/${n} questions pass validation and the harder rule.`);process.exit(bad?1:0);
