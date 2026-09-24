/* Run with: node --test tests/ */
const test=require("node:test");const assert=require("node:assert/strict");
global.window=undefined;
const E=require("../js/logic.js");
const vm=require("node:vm");const fs=require("node:fs");const path=require("node:path");
const seedCtx={window:{}};vm.runInNewContext(fs.readFileSync(path.join(__dirname,"../data/seed.js"),"utf8"),seedCtx);
const SEED=seedCtx.window.AG_SEED;const course=SEED.courses["30178"];

function hardQ(over){
  const q=JSON.parse(JSON.stringify(SEED.questions["30178-IRR-32"]));
  q.hard_check={parts:[{n:"3.1",steps:5,concepts:2},{n:"3.2",steps:4,concepts:2}],notches:["extra_classification","working_backwards","chain"],no_ambiguity:true,in_syllabus:true};
  return Object.assign(q,over||{});
}

test("bundled bank: every question passes schema validation",()=>{
  /* IRR-12 was transcribed from a page image; it was checked against the PDF text layer on 2026-09-24. */
  for(const q of Object.values(SEED.questions))assert.deepEqual(E.validateQuestion(q),[],q.id);
});
test("harder rule thresholds come from the course fingerprint",()=>{
  const ex=E.hardThresholds(course,"exercise part");assert.equal(ex.slideMax,3);assert.equal(ex.examMedian,3);assert.equal(ex.stepsMin,4);assert.equal(ex.conceptsMin,2);assert.equal(ex.minNotches,2);assert.equal(ex.minutesCap,4.5);
  const mc=E.hardThresholds(course,"concept MCQ");assert.equal(mc.slideMax,null);assert.equal(mc.examMedian,1.5);assert.equal(mc.stepsMin,2.5);
});
test("real questions are exempt; generated questions without a review are unreviewed",()=>{
  assert.equal(E.reviewHarder(SEED.questions["30178-IRR-01"],course).status,"exempt");
  assert.equal(E.reviewHarder(SEED.questions["30178-IRR-32"],course).status,"unreviewed");
  assert.equal(E.reviewHarder(SEED.questions["30178-IRR-24"],course).status,"unreviewed");
});
test("a reviewed hard question that clears every bar passes",()=>{
  const r=E.reviewHarder(hardQ(),course);assert.equal(r.status,"pass",JSON.stringify(r.checks.filter(c=>!c.ok)));
});
test("steps at the slide maximum fail (must be strictly above)",()=>{
  const q=hardQ();q.hard_check.parts[1].steps=3;const r=E.reviewHarder(q,course);assert.equal(r.status,"fail");assert.ok(r.checks.find(c=>c.id==="part:3.2"&&!c.ok));
});
test("steps above the median but under the hard target fail",()=>{
  const q=hardQ();q.hard_check.parts[0].steps=3.5;assert.equal(E.reviewHarder(q,course).status,"fail");
});
test("one notch is not enough; unknown notches are rejected",()=>{
  let q=hardQ();q.hard_check.notches=["chain","chain"];assert.equal(E.reviewHarder(q,course).status,"fail");
  q=hardQ();q.hard_check.notches=["chain","vague_wording"];assert.equal(E.reviewHarder(q,course).status,"fail");
});
test("ambiguity, out-of-syllabus, unverified keys and exam-level labels all fail",()=>{
  let q=hardQ();q.hard_check.no_ambiguity=false;assert.equal(E.reviewHarder(q,course).status,"fail");
  q=hardQ();q.hard_check.in_syllabus=false;assert.equal(E.reviewHarder(q,course).status,"fail");
  q=hardQ();q.answer_key[0].answer_status="unverified";assert.equal(E.reviewHarder(q,course).status,"fail");
  q=hardQ({difficulty:"exam+1"});assert.equal(E.reviewHarder(q,course).status,"fail");
  q=hardQ();q.citations=[];assert.equal(E.reviewHarder(q,course).status,"fail");
});
test("time cap: minutes per answer above 4.5 fails",()=>{
  const q=hardQ({est_minutes:10});assert.equal(E.reviewHarder(q,course).status,"fail");
});
test("concept MCQ needs at least 2.5 steps and 2 concepts",()=>{
  const q=JSON.parse(JSON.stringify(SEED.questions["30178-IRR-31"]));
  q.hard_check={parts:[{n:"1",steps:2,concepts:2}],notches:["near_true_statements","cross_section"],no_ambiguity:true,in_syllabus:true};
  assert.equal(E.reviewHarder(q,course).status,"fail");
  q.hard_check.parts[0].steps=3;assert.equal(E.reviewHarder(q,course).status,"pass");
});
test("scheduling: third counted correct archives, wrong resets",()=>{
  let r={status:"new"};let t="2026-09-24";
  r=E.applyVerdict(r,"Correct",t,"2026-10-28").review;assert.equal(r.streak,1);assert.equal(r.due,"2026-09-27");
  r=E.applyVerdict(r,"Correct","2026-09-27","2026-10-28").review;assert.equal(r.due,"2026-10-04");
  r=E.applyVerdict(r,"Correct","2026-10-04","2026-10-28").review;assert.equal(r.status,"archived");
  r=E.applyVerdict({status:"active",streak:2,due:t},"Wrong",t,null).review;assert.equal(r.streak,0);assert.equal(r.lapses,1);
});
test("markdown export includes the attempt, the key and the mark scheme",()=>{
  const q=SEED.questions["30178-IRR-01"];const atts=Object.values(SEED.attempts).filter(a=>a.question_id===q.id);
  const md=E.exportMarkdown("Test",[{q,atts}],{attempts:"all",key:true,sources:true});
  assert.match(md,/## 30178-IRR-01/);assert.match(md,/#### Attempt 1/);assert.match(md,/\| A\.1 \| D \| D \| right \|/);assert.match(md,/### Mark scheme/);
  const noKey=E.questionMarkdown(q,atts,{key:false});assert.doesNotMatch(noKey,/### Answer key/);assert.match(noKey,/hidden/);
});
test("csv export has one row per attempt",()=>{
  const items=Object.values(SEED.questions).map(q=>({q,atts:Object.values(SEED.attempts).filter(a=>a.question_id===q.id)}));
  const lines=E.exportCsv(items).trim().split("\r\n");assert.equal(lines.length,1+Object.keys(SEED.attempts).length);
});
test("zip writer produces a valid archive",()=>{
  const z=E.zipStore([{name:"a/b.md",data:"hello"},{name:"a/c.txt",data:new Uint8Array([1,2,3])}]);
  const dv=new DataView(z.buffer);assert.equal(dv.getUint32(0,true),0x04034b50);assert.equal(dv.getUint32(z.length-22,true),0x06054b50);assert.equal(dv.getUint16(z.length-12,true),2);
  assert.equal(E.crc32(new TextEncoder().encode("hello")),0x3610a686);
});
test("deck coverage: gaps, Hard per section and unmapped questions",()=>{
  const deck={sections:[{id:"S1",title:"a"},{id:"S2",title:"b"}],units:[{id:"U1",section:"S1",examinable:true},{id:"U2",section:"S2",examinable:true},{id:"U0",section:"S1",examinable:false,reason:"nav"}]};
  const qs=[{id:"q1",units:["U1"],slide_groups:["S1"],difficulty:"hard"},{id:"q2",units:["U1"],slide_groups:["S2"],difficulty:"exam"},{id:"q3",slide_groups:["S2"],difficulty:"hard"}];
  const c=E.deckCoverage(deck,qs);
  assert.equal(c.examinable,2);assert.equal(c.covered,1);assert.deepEqual(c.gaps.map(u=>u.id),["U2"]);
  assert.deepEqual(c.noHard.map(s=>s.id),[]);assert.deepEqual(c.unmapped,["q3"]);
  assert.deepEqual(E.deckCoverage(deck,qs.slice(0,2)).noHard.map(s=>s.id),["S2"]);
});
