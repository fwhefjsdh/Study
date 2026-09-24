/* Pre-creation review. Exits non-zero on any failure.
   Per question:  the site's own validator (validateQuestion); MCQ keys mark themselves correct;
                  generated questions pass the harder rule (reviewHarder) against the course fingerprint;
                  real questions are verbatim-verified; adapted questions carry a "check" note for Will.
   Per course with a coverage block (units + ledger):
                  every question maps to known units; every examinable deck unit has at least one question;
                  every deck section has at least one Hard question whose primary section (first slide_group) it is;
                  every ledger item has a decision, and every id it names exists. */
const fs=require("fs"),path=require("path"),vm=require("vm");
const E=require("../js/logic.js");
const ctx={window:{}};vm.runInNewContext(fs.readFileSync(path.join(__dirname,"../data/seed.js"),"utf8"),ctx);
const SEED=ctx.window.AG_SEED;const known={...SEED.courses};
const all={};Object.values(SEED.questions).forEach(q=>all[q.id]=q);
let bad=0,n=0;const fromBank=new Set();const coverage=[];
const DECISIONS=["included","included_adapted","duplicate","held","excluded","key_source","used","units","not_examinable","not_a_question"];

for(const f of fs.readdirSync(__dirname).filter(f=>/^bank_.*\.json$/.test(f)).sort()){
  const b=JSON.parse(fs.readFileSync(path.join(__dirname,f),"utf8"));(b.courses||[]).forEach(c=>known[c.code]=c);
  if(b.coverage)coverage.push(b.coverage);
  for(const q of b.questions){n++;
    const errs=E.validateQuestion(q);if(fromBank.has(q.id))errs.push("duplicate id in the banks");fromBank.add(q.id);all[q.id]=q;
    const g=E.reviewHarder(q,known[q.course]);const type=(q.source||{}).type;
    if(type==="generated"&&g.status!=="pass")errs.push("harder rule: "+g.checks.filter(c=>!c.ok).map(c=>c.label+" ("+c.detail+")").join("; "));
    if(type!=="generated"&&g.status!=="exempt"&&g.status!=="pass")errs.push("harder rule on a "+type+" question marked hard: "+g.status);
    if(type==="adapted"&&!(q.source.check||"").trim())errs.push("adapted question without a check note for Will");
    (q.subquestions||[]).forEach(s=>{if(s.options&&s.options.length){const r=E.mcqResults(q,{[s.n]:E.keyIndex(s,q.answer_key.find(k=>k.n===s.n))});if(!r.find(x=>x.n===s.n).correct)errs.push("key does not mark itself correct: "+s.n);}});
    const T=g.thresholds;const tag=type==="generated"?"":` [${type}${type==="adapted"?", check flagged":""}]`;
    console.log((errs.length?"FAIL ":"pass ")+q.id.padEnd(16)+(T&&type==="generated"?` [${T.sc}: steps > ${T.stepsFloor} & ≥ ${T.stepsMin}, concepts ≥ ${T.conceptsMin}, ≤ ${T.minutesCap} min/answer]`:tag)+(errs.length?"\n     "+errs.join("\n     "):""));
    if(errs.length)bad++;}
}
console.log(`\n${n-bad}/${n} bank questions pass validation, key self-check and the harder rule.`);

let covBad=0;
for(const cv of coverage){
  const course=cv.course;const qs=Object.values(all).filter(q=>q.course===course);
  const unitOf=q=>q.units||cv.existing_units[q.id]||[];
  const units={};Object.values(cv.units).flat().forEach(u=>units[u.id]=u);
  const errs=[];
  qs.forEach(q=>{const us=unitOf(q);if(!us.length)errs.push(`${q.id} maps to no deck unit`);us.forEach(u=>{if(!units[u])errs.push(`${q.id} names unknown unit ${u}`);});});
  const covered={};qs.forEach(q=>unitOf(q).forEach(u=>(covered[u]=covered[u]||[]).push(q.id)));
  const lines=[];
  for(const [deck,us] of Object.entries(cv.units)){
    const ex=us.filter(u=>u.examinable);const gaps=ex.filter(u=>!covered[u.id]);
    us.filter(u=>!u.examinable&&!(u.reason||"").trim()).forEach(u=>errs.push(`${u.id} is marked non-examinable without a reason`));
    gaps.forEach(u=>errs.push(`GAP: ${u.id} "${u.title}" has no question`));
    lines.push(`  ${deck.padEnd(6)} ${ex.length-gaps.length}/${ex.length} examinable units covered; ${us.length-ex.length} non-examinable (reasons given)`);
  }
  const sections={};const deckSecs=Object.assign({},cv.sections);
  (known[course]&&known[course].decks||{}).IRR&&(deckSecs.IRR=known[course].decks.IRR.sections);
  qs.filter(q=>q.difficulty==="hard"&&q.slide_groups&&q.slide_groups.length).forEach(q=>(sections[q.deck+"/"+q.slide_groups[0]]=sections[q.deck+"/"+q.slide_groups[0]]||[]).push(q.id));
  for(const [deck,secs] of Object.entries(deckSecs)){
    const miss=(secs||[]).filter(s=>!sections[deck+"/"+s.id]);
    miss.forEach(s=>errs.push(`NO HARD: ${deck} section ${s.id} "${s.title}" has no Hard question as its primary section`));
    lines.push(`  ${deck.padEnd(6)} ${(secs||[]).length-miss.length}/${(secs||[]).length} sections have a Hard question`);
  }
  (cv.ledger||[]).forEach((d,i)=>{if(!DECISIONS.includes(d.decision))errs.push(`ledger[${i}] ${d.file} / ${d.item}: no valid decision`);
    if(["held","excluded","duplicate"].includes(d.decision)&&!(d.reason||"").trim())errs.push(`ledger[${i}] ${d.item}: ${d.decision} without a reason`);
    (d.ids||[]).forEach(id=>{if(!all[id])errs.push(`ledger[${i}] ${d.item}: names ${id}, which does not exist`);});
    if(d.decision.startsWith("included")&&!(d.ids||[]).length)errs.push(`ledger[${i}] ${d.item}: included but names no question`);});
  const counts={};(cv.ledger||[]).forEach(d=>counts[d.decision]=(counts[d.decision]||0)+1);
  console.log(`\nCoverage ${course}: ${qs.length} questions (${qs.filter(q=>q.source.type==="real").length} real, ${qs.filter(q=>q.source.type==="adapted").length} adapted, ${qs.filter(q=>q.source.type==="generated").length} generated; ${qs.filter(q=>q.difficulty==="hard").length} Hard)`);
  lines.forEach(l=>console.log(l));
  console.log("  ledger: "+Object.entries(counts).map(([k,v])=>k+" "+v).join(", "));
  errs.forEach(e=>console.log("  FAIL "+e));if(errs.length)covBad+=errs.length;else console.log("  pass: no gaps");
}
process.exit(bad||covBad?1:0);
