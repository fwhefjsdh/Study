/* Answer Grid: pure logic (no DOM). Shared by the page (window.EP) and the Node tests (module.exports). */
/* ===== Pure logic (no DOM). Exposed as window.EP for testing. ===== */
(function(){
const TZ="Europe/Rome";
function romeToday(now){const d=now||new Date();return new Intl.DateTimeFormat("en-CA",{timeZone:TZ,year:"numeric",month:"2-digit",day:"2-digit"}).format(d);}
function toUTC(iso){const [y,m,d]=iso.split("-").map(Number);return Date.UTC(y,m-1,d);}
function addDays(iso,n){const t=new Date(toUTC(iso)+n*86400000);return t.toISOString().slice(0,10);}
function diffDays(a,b){return Math.round((toUTC(a)-toUTC(b))/86400000);} // a - b
function isISO(s){return typeof s==="string"&&/^\d{4}-\d{2}-\d{2}$/.test(s);}
function tierFor(examDate,today){
  if(!isISO(examDate))return "none";
  const d=diffDays(examDate,today);
  if(d<0)return "none";
  if(d<=14)return "RED"; if(d<=45)return "AMBER"; return "GREEN";
}
const TIER_RANK={RED:0,AMBER:1,GREEN:2,none:3};
const PRIO_RANK={exam:0,studying:1,none:2,paused:3};
function weekday(iso){return new Date(toUTC(iso)).getUTCDay();}
/* Exam plan for one scope (a deck folder or a whole subject). cards: [{q,r}] */
function examPlan(cards,cfg,today,attemptsToday){
  const live=cards.filter(c=>!["disabled","challenged"].includes((c.r||{}).status));
  const total=live.length;
  const archived=live.filter(c=>c.r.status==="archived").length;
  const streakSum=live.filter(c=>c.r.status!=="archived").reduce((n,c)=>n+Math.min(3,c.r.streak|0),0);
  const remaining=live.filter(c=>c.r.status!=="archived").reduce((n,c)=>n+(3-Math.min(3,c.r.streak|0)),0);
  const readiness=total?Math.round(100*(archived*3+streakSum)/(3*total)):0;
  const exam=isISO(cfg.exam)?cfg.exam:null;
  const frd=cfg.frd==="off"?null:Number(cfg.frd);
  const frStart=exam&&frd!=null?addDays(exam,-frd):null;
  const frActive=!!(frStart&&today>=frStart&&today<=exam);
  let studyDays=null;
  if(exam){const end=frStart?addDays(frStart,-1):addDays(exam,-1);studyDays=0;
    for(let d=today;d<=end;d=addDays(d,1))if(!(cfg.daysOff||[]).includes(weekday(d)))studyDays++;}
  const goal=exam?(studyDays>0?Math.ceil(remaining/studyDays):remaining):null;
  const due=cards.filter(c=>{const st=(c.r||{}).status;if(!["new","active"].includes(st))return false;return effectiveDue(c.r,exam,today)<=today;});
  const overdue=due.filter(c=>c.r.status!=="new"&&effectiveDue(c.r,exam,today)<today).length;
  const behind=goal!=null&&(overdue>0||due.length>goal*1.5);
  return {total,archived,remaining,readiness,exam,frd,frStart,frActive,studyDays,goal,dueToday:due.length,overdue,doneToday:attemptsToday|0,behind,
    catchUp:behind?Math.max(goal||0,due.length):null,daysLeft:exam?diffDays(exam,today):null};
}
function examCap(examDate){return isISO(examDate)?addDays(examDate,-2):null;}
function effectiveDue(r,examDate,today){
  let d=isISO(r&&r.due)?r.due:today;
  const cap=examCap(examDate);
  if(cap&&d>cap)d=cap;
  return d;
}
function clone(o){return JSON.parse(JSON.stringify(o||{}));}
function normReview(r){
  const x=clone(r);
  x.status=x.status||"new"; x.streak=x.streak|0; x.lapses=x.lapses|0;
  x.interval_days=x.interval_days==null?0:x.interval_days; x.history=Array.isArray(x.history)?x.history:[];
  if(!("last_counted_date" in x))x.last_counted_date=null;
  return x;
}
/* Apply one verdict. Returns {review, counted, note}. */
function applyVerdict(rIn,verdict,today,examDate,opts){
  const o=opts||{};const r=normReview(rIn);
  if(o.finalReview&&r.status==="archived")r.sweep=true;
  const due=effectiveDue(r,examDate,today);
  const isDue=r.status==="new"||due<=today||!!r.sweep;
  const already=r.last_counted_date===today;
  let counted=false,note="";
  if(r.sweep&&r.status==="archived"){
    r.sweep=false;
    if(verdict==="Correct"){counted=true;note="Still solid: re-archived after the final review.";}
    else{r.status="active";r.streak=0;if(verdict==="Wrong")r.lapses+=1;r.interval_days=verdict==="Wrong"?1:2;r.due=addDays(today,r.interval_days);counted=true;note="Missed in the sweep: back in the active queue.";}
  }else if(verdict==="Wrong"){
    r.streak=0;r.lapses+=1;r.interval_days=1;r.due=addDays(today,1);if(r.status!=="challenged")r.status="active";counted=true;
  }else if(verdict==="Partial"){
    r.streak=0;r.interval_days=2;r.due=addDays(today,2);if(r.status!=="challenged")r.status="active";counted=true;
  }else if(verdict==="Correct"){
    if(!isDue){note="Practised early — not counted.";}
    else if(already){note="Already counted today — not counted.";}
    else{
      r.streak+=1;counted=true;
      if(r.streak>=3){r.status="archived";r.interval_days=null;note="Third counted correct: archived.";}
      else{r.interval_days=r.streak===1?(o.easy?4:3):(o.easy?10:7);r.due=addDays(today,r.interval_days);r.status="active";if(o.easy)note="Easy: longer gap ("+r.interval_days+" days).";}
    }
  }
  if(counted)r.last_counted_date=today;
  const cap=examCap(examDate);
  if(cap&&isISO(r.due)&&r.due>cap)r.due=cap<today?today:cap;
  r.history.push({date:today,verdict,counted});
  return {review:r,counted,note};
}
function isLeech(r){return (r&&r.lapses|0)>=4;}
/* Build queue from [{q, r, course}] */
function buildQueue(items,today){
  const out=[];
  for(const it of items){
    const r=normReview(it.r); const ex=("exam" in it)?it.exam:(it.course&&it.course.exam_date);
    if(it.course&&it.course.status==="closed")continue;
    if(it.prio==="paused"&&!it.forced)continue;
    const fr=!!it.finalReview&&r.status==="archived";
    const active=(r.status==="new"||r.status==="active")||(r.status==="archived"&&(r.sweep||fr));
    if(!active)continue;
    const d=(r.status==="archived")?today:effectiveDue(r,ex,today);
    if(d>today)continue;
    out.push({...it,r,tier:tierFor(ex,today),prioRank:PRIO_RANK[it.prio||"none"]??2,effDue:d,overdue:diffDays(today,d),isNew:r.status==="new",finalReviewCard:fr||(r.status==="archived"&&!!r.sweep)});
  }
  out.sort((a,b)=>{
    const pr=(a.prioRank??2)-(b.prioRank??2); if(pr)return pr;
    const t=TIER_RANK[a.tier]-TIER_RANK[b.tier]; if(t)return t;
    if(a.isNew!==b.isNew)return a.isNew?1:-1;
    if(a.isNew)return newOrder(a.q,b.q);
    if(b.overdue!==a.overdue)return b.overdue-a.overdue;
    if((b.r.lapses|0)!==(a.r.lapses|0))return (b.r.lapses|0)-(a.r.lapses|0);
    return a.q.id.localeCompare(b.q.id);
  });
  return out;
}
/* New cards follow the deck folder in slide order: same deck, then first slide,
   actual questions before generated ones on the same slides, then id. */
function firstSlide(q){const s=Array.isArray(q.slides)&&q.slides.length?Math.min(...q.slides.map(Number)):9999;return isFinite(s)?s:9999;}
function newOrder(a,b){
  const d=String(a.course||"").localeCompare(String(b.course||""))||String(a.deck||"").localeCompare(String(b.deck||""));if(d)return d;
  const fs=firstSlide(a)-firstSlide(b);if(fs)return fs;
  const ra=((a.source||{}).type==="generated")?1:0,rb=((b.source||{}).type==="generated")?1:0;if(ra!==rb)return ra-rb;
  return String(a.created_at||"").localeCompare(String(b.created_at||""))||a.id.localeCompare(b.id);
}
function slideRanges(list){
  const s=[...new Set((list||[]).map(Number).filter(n=>isFinite(n)))].sort((x,y)=>x-y);const out=[];
  for(let i=0;i<s.length;){let j=i;while(j+1<s.length&&s[j+1]===s[j]+1)j++;out.push(i===j?String(s[i]):s[i]+"–"+s[j]);i=j+1;}
  return out.join(", ");
}
const LETTERS="ABCDEFGHIJ";
function keyIndex(sub,keyEntry){
  if(!keyEntry||!sub||!Array.isArray(sub.options)||!sub.options.length)return -1;
  const a=String(keyEntry.answer==null?"":keyEntry.answer).trim();
  if(/^[A-J]$/.test(a)){const i=LETTERS.indexOf(a);return i<sub.options.length?i:-1;}
  const i=sub.options.findIndex(o=>String(o).trim()===a);return i;
}
/* selected: {n: index} ; returns per-part results. Page code alone decides MCQ correctness. */
function mcqResults(q,selected){
  const keyBy={};(q.answer_key||[]).forEach(k=>keyBy[k.n]=k);
  return (q.subquestions||[]).map(s=>{
    const isMcq=Array.isArray(s.options)&&s.options.length>0;
    const k=keyBy[s.n]; const ki=keyIndex(s,k);
    const sel=selected&&Object.prototype.hasOwnProperty.call(selected,s.n)?selected[s.n]:null;
    return {n:s.n,isMcq,keyIndex:ki,selected:sel,answered:sel!=null,correct:isMcq?(sel!=null&&sel===ki):null,answer_status:k?k.answer_status:"unverified",marks:s.marks};
  });
}
function mcqVerdict(res){
  const m=res.filter(x=>x.isMcq); if(!m.length)return null;
  const c=m.filter(x=>x.correct).length;
  if(c===m.length)return "Correct"; if(c===0)return "Wrong"; return "Partial";
}
/* Combine: MCQ facts bound the marker's verdict. */
function combineVerdict(res,markerVerdict){
  const R={Wrong:0,Partial:1,Correct:2},N=["Wrong","Partial","Correct"];
  let mv=mcqVerdict(res);
  if(!markerVerdict)return mv;
  if(!mv)return markerVerdict; // no MCQ parts: the marker decides
  // written (non-MCQ) parts can lift an all-wrong MCQ set to Partial at most
  if(mv==="Wrong"&&res.some(x=>!x.isMcq))mv="Partial";
  let out=Math.min(R[mv],R[markerVerdict]);
  if(mcqVerdict(res)==="Correct")out=Math.max(out,1); // all options right: never below Partial
  return N[out];
}
function tagsFromSelections(q,res){
  const hits=[];
  for(const et of (q.error_tags||[])){
    const m=/^\s*([0-9]+(?:\.[0-9]+)*)\s*:\s*([A-J])\b/.exec(String(et.trap||""));
    if(!m)continue;
    const r=res.find(x=>String(x.n)===m[1]);
    if(r&&r.isMcq&&r.selected!=null&&LETTERS[r.selected]===m[2])hits.push(et.tag);
  }
  return hits;
}
function marksFor(res,negVal){
  let total=0,known=true;
  const neg=typeof negVal==="number"?negVal:null;
  for(const r of res){
    if(!r.isMcq){known=false;continue;}
    const mk=typeof r.marks==="number"?r.marks:null;
    if(r.correct){if(mk==null)known=false;else total+=mk;}
    else if(r.answered){if(neg==null)known=false;else total+=neg;}
  }
  return {total:Math.round(total*1000)/1000,known};
}
const VERDICTS=["Correct","Partial","Wrong"];
function validateMarker(o){
  const errs=[];
  if(!o||typeof o!=="object"||Array.isArray(o))return ["not an object"];
  if(!VERDICTS.includes(o.verdict))errs.push("verdict");
  if(!Array.isArray(o.reasoning_judgements)||o.reasoning_judgements.some(j=>!j||typeof j.quote!=="string"||typeof j.judgement!=="string"))errs.push("reasoning_judgements");
  if(!Array.isArray(o.error_tags_hit)||o.error_tags_hit.some(t=>typeof t!=="string"))errs.push("error_tags_hit");
  if(typeof o.correction!=="string")errs.push("correction");
  if(!["ok","partial","illegible","not_sent"].includes(o.legibility))errs.push("legibility");
  if(typeof o.alternative_method_flag!=="boolean")errs.push("alternative_method_flag");
  if(typeof o.alternative_method!=="string")errs.push("alternative_method");
  if(typeof o.provisional!=="boolean")errs.push("provisional");
  return errs;
}
const SRC_TYPES=["real","adapted","generated"],STATUS=["official","double-solved","unverified"],DIFF=["exam","exam+1","hard"];
const ID_RE=/^[A-Za-z0-9_\-.~:@+]{1,200}$/;
function validateQuestion(q){
  const e=[];const t=(v,ty)=>typeof v===ty;
  if(!q||typeof q!=="object")return ["not an object"];
  if(!t(q.id,"string")||!ID_RE.test(q.id))e.push("id missing or has illegal characters");
  if(!t(q.course,"string")||!q.course)e.push("course");
  else if(t(q.id,"string")&&!q.id.startsWith(q.course+"-"))e.push("id must start with course code + '-'");
  for(const f of ["deck","topic","syllabus_objective","shape","stem"])if(!t(q[f],"string"))e.push(f);
  if(q.data!=null&&!t(q.data,"string"))e.push("data");
  const s=q.source;
  if(!s||typeof s!=="object")e.push("source");
  else{
    if(!SRC_TYPES.includes(s.type))e.push("source.type");
    for(const f of ["file","location","label"])if(!t(s[f],"string"))e.push("source."+f);
    if(!t(s.verbatim_verified,"boolean"))e.push("source.verbatim_verified");
    if(!t(s.transcribed_from_image,"boolean"))e.push("source.transcribed_from_image");
    if(!(s.page_snapshot_asset===null||s.page_snapshot_asset===undefined||t(s.page_snapshot_asset,"string")))e.push("source.page_snapshot_asset");
    if(s.type==="real"&&s.verbatim_verified!==true)e.push("real question not verbatim-verified");
  }
  if(!(t(q.marks,"number")||q.marks==="UNKNOWN"))e.push("marks");
  if(!Array.isArray(q.subquestions)||!q.subquestions.length)e.push("subquestions");
  else{
    const keyBy={};(Array.isArray(q.answer_key)?q.answer_key:[]).forEach(k=>keyBy[k&&k.n]=k);
    q.subquestions.forEach((sq,i)=>{
      if(!sq||!t(sq.n,"string")||!t(sq.prompt,"string")){e.push("subquestions["+i+"]");return;}
      if(sq.options!=null&&!Array.isArray(sq.options))e.push("subquestions["+i+"].options");
      if(!(t(sq.marks,"number")||sq.marks==="UNKNOWN"))e.push("subquestions["+i+"].marks");
      const k=keyBy[sq.n];
      if(!k)e.push("answer_key missing "+sq.n);
      else{
        if(!STATUS.includes(k.answer_status))e.push("answer_status "+sq.n);
        if(Array.isArray(sq.options)&&sq.options.length){
          if(keyIndex(sq,k)<0)e.push("key for "+sq.n+" does not match an option");
          if(new Set(sq.options.map(o=>String(o).trim())).size!==sq.options.length)e.push("duplicate options in "+sq.n);
        }
      }
    });
  }
  if(!Array.isArray(q.mark_scheme)||q.mark_scheme.some(b=>!t(b,"string")))e.push("mark_scheme");
  if(!Array.isArray(q.error_tags)||q.error_tags.some(x=>!x||!t(x.tag,"string")||!t(x.trap,"string")))e.push("error_tags");
  if(!Array.isArray(q.citations)||q.citations.some(c=>!c||!t(c.deck,"string")||c.slide==null||!t(c.quote,"string")))e.push("citations");
  else if(q.citations.some(c=>c.quote.trim().split(/\s+/).length>25))e.push("citation quote over 25 words");
  if(!t(q.est_minutes,"number"))e.push("est_minutes");
  if(!DIFF.includes(q.difficulty))e.push("difficulty");
  if(!t(q.created_at,"string"))e.push("created_at");
  if(q.hard_check!=null&&(typeof q.hard_check!=="object"||Array.isArray(q.hard_check)))e.push("hard_check must be an object");
  return e;
}
/* Minimal, escaping Markdown renderer: paragraphs, lists, pipe tables, headings, inline code/bold/italic. */
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function inline(s){
  return esc(s).replace(/`([^`]+)`/g,"<code>$1</code>").replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>").replace(/(^|[^*])\*([^*\s][^*]*)\*/g,"$1<em>$2</em>").replace(/\^([^^\s]+)\^/g,"<sup>$1</sup>").replace(/~([^~\s]+)~/g,"<sub>$1</sub>");
}
function mdToHtml(md){
  const lines=String(md==null?"":md).replace(/\r/g,"").split("\n");const out=[];let i=0;
  while(i<lines.length){
    const L=lines[i];
    if(!L.trim()){i++;continue;}
    if(/^\s*\|/.test(L)){
      const rows=[];while(i<lines.length&&/^\s*\|/.test(lines[i])){rows.push(lines[i]);i++;}
      const cells=r=>r.trim().replace(/^\|/,"").replace(/\|$/,"").split("|").map(c=>c.trim());
      let head=null,body=rows.map(cells);
      if(rows.length>1&&/^\s*\|?\s*:?-{2,}/.test(rows[1])){head=body[0];body=body.slice(2);}
      out.push('<div class="tablewrap"><table>'+(head?"<thead><tr>"+head.map(c=>"<th>"+inline(c)+"</th>").join("")+"</tr></thead>":"")+"<tbody>"+body.map(r=>"<tr>"+r.map(c=>"<td>"+inline(c)+"</td>").join("")+"</tr>").join("")+"</tbody></table></div>");
      continue;
    }
    const hm=/^(#{1,4})\s+(.*)$/.exec(L);
    if(hm){out.push("<h4>"+inline(hm[2])+"</h4>");i++;continue;}
    if(/^\s*([-*]|\d+[.)])\s+/.test(L)){
      const ordered=/^\s*\d+[.)]\s+/.test(L);const items=[];
      while(i<lines.length&&/^\s*([-*]|\d+[.)])\s+/.test(lines[i])){items.push(lines[i].replace(/^\s*([-*]|\d+[.)])\s+/,""));i++;}
      out.push((ordered?"<ol>":"<ul>")+items.map(x=>"<li>"+inline(x)+"</li>").join("")+(ordered?"</ol>":"</ul>"));continue;
    }
    const para=[];while(i<lines.length&&lines[i].trim()&&!/^\s*\|/.test(lines[i])&&!/^\s*([-*]|\d+[.)])\s+/.test(lines[i])&&!/^#{1,4}\s/.test(lines[i])){para.push(inline(lines[i]));i++;}
    out.push("<p>"+para.join("<br>")+"</p>");
  }
  return out.join("");
}

/* ===== Harder rule: the guardrail every Claude-written question is reviewed against before it enters the bank. =====
   Source of the thresholds: the course's fingerprint.hard_target (set in Cowork from the course's own evidence).
   The rule, as stated for 30178: "harder than the slides: steps above the slide maximum AND above the exam-level
   median for the shape, at least two distinct notches, never via ambiguity or out-of-syllabus content". */
const HARD_NOTCHES={
  extra_step:"One more calculation step than the slide examples",
  extra_classification:"An extra classification decision (e.g. is this item rate-sensitive?)",
  working_backwards:"Solve backwards from a target or limit",
  cross_section:"Combines ideas from two sections of the deck",
  what_if_followon:"A what-if follow-on that re-uses the first answer",
  extraneous_data:"Data that is given but not needed",
  chain:"A later part depends on an earlier answer",
  near_true_statements:"Statements that are nearly true, with one decisive flaw"
};
const HARD_DEFAULT={rule:"Harder than the slides: more steps than the slide maximum and the exam median for the shape, at least two distinct notches, never via ambiguity or out-of-syllabus content.",
  min_notches:2,minutes_per_answer_cap:null,notches:Object.keys(HARD_NOTCHES),by_shape:{}};
function shapeClass(q){
  const hc=q&&q.hard_check;if(hc&&typeof hc.shape_class==="string"&&hc.shape_class)return hc.shape_class;
  return /exercise/i.test(String(q&&q.shape||""))?"exercise part":"concept MCQ";
}
function hardApplies(q){return !!q&&(((q.source||{}).type==="generated")||q.difficulty==="hard");}
/* Thresholds for one shape class, read from the course fingerprint. Every number says where it came from. */
function hardThresholds(course,sc){
  const fp=(course&&course.fingerprint)||{};const ht=fp.hard_target||null;
  const t=ht||HARD_DEFAULT;const bs=(t.by_shape||{})[sc]||{};
  const exam=((fp.by_shape||{})[sc]||{});const slide=(((fp.slide_baseline||{}).by_shape||{})[sc]||{});
  const num=v=>typeof v==="number"&&isFinite(v)?v:null;
  const slideMax=num(((slide.steps||{}).range||[])[1]);
  const examMedian=num((exam.steps||{}).median)??num((fp.steps||{}).median);
  const stepsMin=num(bs.steps_min);const conceptsMin=num(bs.concepts_min);
  const floor=Math.max(slideMax??-Infinity,examMedian??-Infinity);
  return {fromCourse:!!ht,rule:t.rule||HARD_DEFAULT.rule,statedBy:ht&&ht.stated_by||null,sc,slideMax,examMedian,stepsMin,conceptsMin,
    stepsFloor:isFinite(floor)?floor:null,minNotches:num(t.min_notches)??2,minutesCap:num(t.minutes_per_answer_cap),
    notches:Array.isArray(t.notches)&&t.notches.length?t.notches:HARD_DEFAULT.notches};
}
/* Deck coverage: which examinable units have a question, and which sections have a Hard question as their primary
   section (first slide_group). deck = course.decks[deck] with .units [{id,section,title,examinable,reason}] and .sections. */
function deckCoverage(deck,qs){
  const units=(deck&&Array.isArray(deck.units))?deck.units:[];const secs=(deck&&Array.isArray(deck.sections))?deck.sections:[];
  const by={};(qs||[]).forEach(q=>(Array.isArray(q.units)?q.units:[]).forEach(u=>(by[u]=by[u]||[]).push(q.id)));
  const U=units.map(u=>Object.assign({},u,{qids:by[u.id]||[]}));
  const S=secs.map(s=>{const hard=(qs||[]).filter(q=>q.difficulty==="hard"&&Array.isArray(q.slide_groups)&&q.slide_groups[0]===s.id).map(q=>q.id);
    return Object.assign({},s,{hard,units:U.filter(u=>u.section===s.id)});});
  const ex=U.filter(u=>u.examinable!==false);
  return {units:U,sections:S,examinable:ex.length,covered:ex.filter(u=>u.qids.length).length,gaps:ex.filter(u=>!u.qids.length),
    noHard:S.filter(s=>!s.hard.length),unmapped:(qs||[]).filter(q=>!Array.isArray(q.units)||!q.units.length).map(q=>q.id),hasUnits:units.length>0};
}
function answerParts(q){return (q&&Array.isArray(q.subquestions)?q.subquestions:[]).map(s=>String(s.n));}
/* Review one question against the harder rule. status: exempt | pass | fail | unreviewed */
function reviewHarder(q,course){
  if(!hardApplies(q))return {status:"exempt",applies:false,checks:[],summary:"Course material: the harder rule covers questions Claude writes."};
  const hc=q.hard_check&&typeof q.hard_check==="object"?q.hard_check:null;const sc=shapeClass(q);const T=hardThresholds(course,sc);
  const checks=[];const add=(id,label,ok,detail)=>checks.push({id,label,ok,detail});
  add("difficulty","Labelled Hard",q.difficulty==="hard",q.difficulty==="hard"?"difficulty is hard":"labelled "+(q.difficulty||"none")+": the rule needs harder than exam level");
  const parts=answerParts(q);
  const keyBad=(q.answer_key||[]).filter(k=>k&&k.answer_status==="unverified").map(k=>k.n);
  add("key","Key solved twice or official",!keyBad.length,keyBad.length?"unverified key on "+keyBad.join(", "):"every part is double-solved or official");
  const cites=(q.citations||[]).filter(c=>c&&c.slide!=null&&String(c.quote||"").trim());
  if(!hc){
    add("review","Harder-rule review recorded",false,"no hard_check block: steps, concepts and notches have not been reviewed");
    return {status:"unreviewed",applies:true,checks,thresholds:T,summary:"Not reviewed against the harder rule yet."};
  }
  const per=Array.isArray(hc.parts)?hc.parts:[];const byN={};per.forEach(p=>{if(p&&p.n!=null)byN[String(p.n)]=p;});
  const need="steps "+(T.stepsFloor!=null?"> "+T.stepsFloor:"")+(T.stepsMin!=null?(T.stepsFloor!=null?" and ":"")+"≥ "+T.stepsMin:"")+(T.conceptsMin!=null?", concepts ≥ "+T.conceptsMin:"");
  parts.forEach(n=>{
    const p=byN[n];
    if(!p){add("part:"+n,"Part "+n+" is harder than the slides",false,"no steps/concepts recorded for "+n);return;}
    const st=Number(p.steps),co=Number(p.concepts);const why=[];
    if(!isFinite(st))why.push("steps missing");
    else{if(T.stepsFloor!=null&&!(st>T.stepsFloor))why.push(st+" steps is not above "+T.stepsFloor+(T.slideMax!=null?" (slide max "+T.slideMax+", exam median "+T.examMedian+")":" (exam median)"));
      if(T.stepsMin!=null&&st<T.stepsMin)why.push(st+" steps is below the target "+T.stepsMin);}
    if(T.conceptsMin!=null){if(!isFinite(co))why.push("concepts missing");else if(co<T.conceptsMin)why.push(co+" concepts is below "+T.conceptsMin);}
    add("part:"+n,"Part "+n+" is harder than the slides",!why.length,why.length?why.join("; "):(st+" steps, "+(isFinite(co)?co:"?")+" concepts ("+need+")"));
  });
  const nn=[...new Set((Array.isArray(hc.notches)?hc.notches:[]).map(String))];const unknown=nn.filter(x=>!T.notches.includes(x));const good=nn.filter(x=>T.notches.includes(x));
  add("notches","At least "+T.minNotches+" distinct notches",good.length>=T.minNotches&&!unknown.length,
    (good.length?good.join(", "):"none")+(unknown.length?" · not on the list: "+unknown.join(", "):"")+(good.length<T.minNotches?" · need "+T.minNotches:""));
  if(T.minutesCap!=null){const per1=parts.length?Number(q.est_minutes)/parts.length:Number(q.est_minutes);
    add("minutes","Time per answer ≤ "+T.minutesCap+" min",isFinite(per1)&&per1<=T.minutesCap+1e-9,isFinite(per1)?(Math.round(per1*100)/100)+" min per answer":"est_minutes missing");}
  add("ambiguity","Not made harder through ambiguity",hc.no_ambiguity===true,hc.no_ambiguity===true?"one defensible answer per part":"not confirmed");
  add("syllabus","Stays inside the syllabus and slides",hc.in_syllabus===true&&cites.length>0,hc.in_syllabus!==true?"not confirmed":cites.length?cites.length+" slide citation"+(cites.length>1?"s":""):"no slide citation");
  const fail=checks.filter(c=>!c.ok);
  return {status:fail.length?"fail":"pass",applies:true,checks,thresholds:T,summary:fail.length?fail.length+" check"+(fail.length>1?"s":"")+" failed":"Meets the harder rule."};
}

/* ===== Export builders (pure). ===== */
function fmtDMY(iso){if(!isISO(iso))return String(iso||"");const [y,m,d]=iso.split("-");return d+"/"+m+"/"+y;}
function tsLabel(ts){const d=new Date(ts);if(isNaN(d))return String(ts||"");
  const p=new Intl.DateTimeFormat("en-GB",{timeZone:TZ,day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"}).format(d);return p.replace(",","");}
function verdictOf(a){return (a&&a.override&&a.override.verdict)||(a&&a.verdict)||(a&&a.marking&&a.marking.verdict)||null;}
function oneLine(s){return String(s==null?"":s).replace(/\s*\n\s*/g," ").trim();}
function mdCell(s){return oneLine(s).replace(/\|/g,"\\|");}
/* A sub-question prompt that only repeats the stem (single-part past-paper items) is not shown twice. */
function promptRepeatsStem(q,sub){
  const n=x=>String(x||"").toLowerCase().replace(/[^a-z0-9α-ω]+/g," ").trim();
  const p=n(sub&&sub.prompt),st=n(q&&q.stem);
  return !p||(!!st&&(st===p||st.endsWith(p)));
}
/* One typed answer per sub-question, stored as the attempt's single typed_reasoning (what marking and exports read). */
function composeTyped(q,byPart){
  const subs=(q&&q.subquestions)||[];const parts=subs.map(s=>[String(s.n),String((byPart||{})[s.n]||"").trim()]).filter(x=>x[1]);
  if(!parts.length)return "";
  if(subs.length===1)return parts[0][1];
  return parts.map(([n,t])=>"["+n+"] "+t).join("\n\n");
}
function keyLetter(sub,k){const i=keyIndex(sub,k);return i>=0?LETTERS[i]:(k?String(k.answer):"?");}
/* Markdown for one question with its attempts. opts: {attempts:"latest"|"all"|"none", key, sources, sketchPath(a)->string|null} */
function questionMarkdown(q,atts,opts){
  const o=Object.assign({attempts:"all",key:true,sources:true},opts||{});
  const L=[];const src=q.source||{};
  L.push("## "+q.id+" · "+(q.topic||""));
  const meta=[q.course+" · deck "+(q.deck||""),q.shape,q.difficulty==="hard"?"Hard":q.difficulty,(src.type||"")+(src.label?" ("+src.label+")":"")];
  if(Array.isArray(q.slides)&&q.slides.length)meta.push("slides "+slideRanges(q.slides));
  meta.push("marks "+(typeof q.marks==="number"?q.marks:"UNKNOWN"));
  L.push("*"+meta.filter(Boolean).join(" · ")+"*","");
  L.push(String(q.stem||"").trim(),"");
  if(q.data)L.push(String(q.data).trim(),"");
  (q.subquestions||[]).forEach(s=>{
    L.push("**"+s.n+"** "+oneLine(s.prompt)+(typeof s.marks==="number"?" *("+s.marks+" mk)*":""));
    if(Array.isArray(s.options)&&s.options.length){L.push("");s.options.forEach((op,i)=>L.push("- "+LETTERS[i]+". "+oneLine(op)));}
    L.push("");
  });
  const keyBy={};(q.answer_key||[]).forEach(k=>keyBy[k.n]=k);
  const list=o.attempts==="none"?[]:(o.attempts==="latest"?atts.slice(-1):atts);
  if(o.attempts!=="none"){
    L.push("### Your attempts"+(atts.length?" ("+atts.length+(o.attempts==="latest"&&atts.length>1?", latest shown":"")+")":""),"");
    if(!list.length)L.push("_Not attempted yet._","");
    list.forEach((a,idx)=>{
      const n=o.attempts==="latest"?atts.length:idx+1;const v=verdictOf(a)||"unmarked";const m=a.marking||{};
      L.push("#### Attempt "+n+" · "+tsLabel(a.ts)+" · "+v+(a.override?" (your rating: "+(a.override.rating||a.override.verdict)+")":"")+(a.marked_by?" · marked by "+({claude:"Claude",self:"you",options:"the options"}[a.marked_by]||a.marked_by):"")+(a.counted===false?" · not counted":""),"");
      const mcq=(q.subquestions||[]).filter(s=>Array.isArray(s.options)&&s.options.length);
      if(mcq.length){L.push("| Part | You chose | Key | Result |","|---|---|---|---|");
        mcq.forEach(s=>{const sel=(a.selected||{})[s.n];const k=keyLetter(s,keyBy[s.n]);L.push("| "+s.n+" | "+(sel||"—")+" | "+(o.key?k:"hidden")+" | "+(sel==null?"blank":(o.key?(sel===k?"right":"wrong"):"—"))+" |");});L.push("");}
      if(a.typed_reasoning)L.push("**Reasoning**","",String(a.typed_reasoning).trim(),"");
      if(Array.isArray(m.reasoning_judgements)&&m.reasoning_judgements.length){L.push("**Feedback on the reasoning**","");m.reasoning_judgements.forEach(j=>L.push("- "+(j.quote?"“"+oneLine(j.quote)+"” — ":"")+oneLine(j.judgement)));L.push("");}
      if(m.correction)L.push("**Correction.** "+oneLine(m.correction),"");
      const tags=(m.error_tags_hit||[]).filter(Boolean);if(tags.length)L.push("**Error tags:** "+tags.join(", "),"");
      if(m.alternative_method_flag&&m.alternative_method)L.push("**Alternative method:** "+oneLine(m.alternative_method),"");
      const sp=o.sketchPath&&a.sketch_asset?o.sketchPath(a):null;if(sp)L.push("![Working for attempt "+n+"]("+sp+")","");
    });
  }
  if(o.key){
    L.push("### Answer key","");
    (q.subquestions||[]).forEach(s=>{const k=keyBy[s.n];if(!k)return;const isM=Array.isArray(s.options)&&s.options.length;
      L.push("- **"+s.n+"** "+(isM?keyLetter(s,k)+". "+oneLine(s.options[keyIndex(s,k)]||""):oneLine(k.answer))+" *("+(k.answer_status||"unverified")+")*");});
    L.push("");
    if((q.mark_scheme||[]).length){L.push("### Mark scheme","");q.mark_scheme.forEach(b=>L.push("- "+oneLine(b)));L.push("");}
  }
  if(o.sources&&(q.citations||[]).length){L.push("### Sources","");q.citations.forEach(c=>L.push("- "+c.deck+" · slide "+c.slide+": “"+oneLine(c.quote)+"”"));L.push("");}
  return L.join("\n");
}
function summaryRow(q,atts){const last=atts[atts.length-1];const vs=atts.map(verdictOf);
  return {id:q.id,topic:q.topic||"",attempts:atts.length,last:last?verdictOf(last)||"unmarked":"—",lastDate:last?tsLabel(last.ts):"",best:vs.includes("Correct")?"Correct":vs.includes("Partial")?"Partial":vs.length?"Wrong":"—"};}
/* items: [{q, atts}] in the order to export */
function exportMarkdown(title,items,opts){
  const L=["# "+title,"","*Exported "+tsLabel(new Date().toISOString())+" · "+items.length+" question"+(items.length===1?"":"s")+"*",""];
  if(items.length>1){L.push("| Question | Topic | Attempts | Latest | Best |","|---|---|---|---|---|");
    items.forEach(({q,atts})=>{const r=summaryRow(q,atts);L.push("| "+r.id+" | "+mdCell(r.topic)+" | "+r.attempts+" | "+r.last+(r.lastDate?" ("+r.lastDate+")":"")+" | "+r.best+" |");});L.push("");}
  items.forEach(({q,atts})=>{L.push("---","",questionMarkdown(q,atts,opts));});
  return L.join("\n").replace(/\n{3,}/g,"\n\n")+"\n";
}
function csvCell(v){const s=String(v==null?"":v);return /[",\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s;}
function exportCsv(items){
  const rows=[["question_id","course","deck","topic","difficulty","source","attempt_no","attempted_at","verdict","rating","marked_by","counted","selected","key","reasoning","correction","error_tags"]];
  items.forEach(({q,atts})=>{const keyBy={};(q.answer_key||[]).forEach(k=>keyBy[k.n]=k);
    const key=(q.subquestions||[]).map(s=>s.n+" "+(Array.isArray(s.options)&&s.options.length?keyLetter(s,keyBy[s.n]):oneLine((keyBy[s.n]||{}).answer))).join("; ");
    atts.forEach((a,i)=>{const m=a.marking||{};rows.push([q.id,q.course,q.deck,q.topic,q.difficulty,(q.source||{}).type,i+1,tsLabel(a.ts),verdictOf(a),(a.override&&a.override.rating)||a.rating||"",a.marked_by||"",a.counted===false?"no":"yes",
      Object.entries(a.selected||{}).map(([n,l])=>n+" "+l).join("; "),key,oneLine(a.typed_reasoning),oneLine(m.correction),(m.error_tags_hit||[]).join("; ")]);});});
  return "﻿"+rows.map(r=>r.map(csvCell).join(",")).join("\r\n")+"\r\n";
}
function safeName(s){return String(s||"export").replace(/[^A-Za-z0-9._-]+/g,"-").replace(/^-+|-+$/g,"").slice(0,80)||"export";}

/* Minimal ZIP writer (stored, no compression). files: [{name, data: Uint8Array}] -> Uint8Array */
const CRC_T=(()=>{const t=new Uint32Array(256);for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;t[n]=c>>>0;}return t;})();
function crc32(b){let c=0xFFFFFFFF;for(let i=0;i<b.length;i++)c=CRC_T[(c^b[i])&255]^(c>>>8);return (c^0xFFFFFFFF)>>>0;}
function zipStore(files){
  const enc=new TextEncoder();const chunks=[];const central=[];let off=0;
  const d=new Date();const dt=((d.getFullYear()-1980)<<9)|((d.getMonth()+1)<<5)|d.getDate(),tm=(d.getHours()<<11)|(d.getMinutes()<<5)|(d.getSeconds()>>1);
  for(const f of files){
    const name=enc.encode(f.name);const data=typeof f.data==="string"?enc.encode(f.data):f.data;const crc=crc32(data);
    const h=new DataView(new ArrayBuffer(30));h.setUint32(0,0x04034b50,true);h.setUint16(4,20,true);h.setUint16(6,0x0800,true);h.setUint16(8,0,true);
    h.setUint16(10,tm,true);h.setUint16(12,dt,true);h.setUint32(14,crc,true);h.setUint32(18,data.length,true);h.setUint32(22,data.length,true);h.setUint16(26,name.length,true);h.setUint16(28,0,true);
    chunks.push(new Uint8Array(h.buffer),name,data);
    const c=new DataView(new ArrayBuffer(46));c.setUint32(0,0x02014b50,true);c.setUint16(4,20,true);c.setUint16(6,20,true);c.setUint16(8,0x0800,true);c.setUint16(10,0,true);
    c.setUint16(12,tm,true);c.setUint16(14,dt,true);c.setUint32(16,crc,true);c.setUint32(20,data.length,true);c.setUint32(24,data.length,true);c.setUint16(28,name.length,true);
    c.setUint16(30,0,true);c.setUint16(32,0,true);c.setUint16(34,0,true);c.setUint16(36,0,true);c.setUint32(38,0,true);c.setUint32(42,off,true);
    central.push(new Uint8Array(c.buffer),name);off+=30+name.length+data.length;
  }
  const cSize=central.reduce((n,x)=>n+x.length,0);
  const e=new DataView(new ArrayBuffer(22));e.setUint32(0,0x06054b50,true);e.setUint16(8,files.length,true);e.setUint16(10,files.length,true);e.setUint32(12,cSize,true);e.setUint32(16,off,true);
  const all=[...chunks,...central,new Uint8Array(e.buffer)];const out=new Uint8Array(all.reduce((n,x)=>n+x.length,0));let p=0;for(const x of all){out.set(x,p);p+=x.length;}
  return out;
}

const API={promptRepeatsStem,composeTyped,deckCoverage,examPlan,weekday,newOrder,firstSlide,slideRanges,romeToday,addDays,diffDays,tierFor,effectiveDue,applyVerdict,isLeech,buildQueue,keyIndex,mcqResults,mcqVerdict,combineVerdict,tagsFromSelections,marksFor,validateMarker,validateQuestion,mdToHtml,esc,LETTERS,normReview,examCap,isISO,
  HARD_NOTCHES,HARD_DEFAULT,shapeClass,hardApplies,hardThresholds,reviewHarder,answerParts,
  fmtDMY,tsLabel,verdictOf,questionMarkdown,exportMarkdown,exportCsv,summaryRow,safeName,zipStore,crc32};
if(typeof window!=="undefined")window.EP=API;
if(typeof module!=="undefined"&&module.exports)module.exports=API;
})();
