/* Answer Grid: the page. Screens, answering, marking, scheduling, exports. Data lives in AGStore (IndexedDB). */
(function(){
const E=window.EP,h=E.esc,$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const MAIN=$("#main"),BANNER=$("#banner"),DLG=$("#dlg");
const COLLS=AGStore.COLLS;
const DEFAULTS={theme:"auto",apiKey:"",model:"claude-opus-5",guard:"flag",seedMerged:false};
const S={courses:{},questions:{},reviews:{},attempts:{},challenges:{},ready:false,
  settings:loadSettings(),screen:"queue",today:E.romeToday(),A:null,
  browse:{course:"",deck:"",topic:"",status:"",src:"",guard:"",attempted:"",q:""},detail:null,sel:new Set(),
  closing:{},sweepAsk:{},importPreview:null,session:null,queueDeck:null,queueSubject:null,statsCourse:"",ex:null};
window.__AG=S;

/* ---------- small helpers ---------- */
function loadSettings(){try{return Object.assign({},DEFAULTS,JSON.parse(localStorage.getItem("ag-settings")||"{}"));}catch(e){return {...DEFAULTS};}}
function saveSettings(){try{localStorage.setItem("ag-settings",JSON.stringify(S.settings));}catch(e){}}
function applyTheme(){const t=S.settings.theme;if(t==="light"||t==="dark")document.documentElement.dataset.theme=t;else delete document.documentElement.dataset.theme;}
function toast(msg,ms){const t=$("#toast");t.textContent=msg;t.hidden=false;clearTimeout(toast._t);toast._t=setTimeout(()=>t.hidden=true,ms||3200);}
const fmtDate=iso=>E.isISO(iso)?E.fmtDMY(iso):"not set";
function newId(){return Date.now().toString(36)+Math.random().toString(36).slice(2,8);}
function srcLabel(q){const s=q.source||{};return s.label||(s.type==="real"?"COURSE-AUTHORITATIVE":"INFERENCE");}
function srcPill(q){const l=srcLabel(q);return '<span class="pill '+(l==="COURSE-AUTHORITATIVE"?"auth":"plain")+'" title="Source label">'+h(l)+"</span>"+(q.difficulty==="hard"?' <span class="pill mid" title="Written to be harder than the slide material">Hard</span>':"");}
function courseOf(q){return S.courses[q.course]||null;}
function reviewOf(id){return S.reviews[id]||{status:"new",streak:0,lapses:0,interval_days:0,due:S.today,history:[],last_counted_date:null};}
function negOf(q){const c=courseOf(q);const v=(q.negative_marking!=null&&q.negative_marking!=="")?q.negative_marking:(c?c.negative_marking:undefined);return v==null?"UNKNOWN":v;}
const numOrUnknown=v=>typeof v==="number"?String(v):"UNKNOWN";
const attemptVerdict=E.verdictOf;
function tsRomeDate(ts){try{return E.romeToday(new Date(ts));}catch(e){return "";}}
function attemptsOf(id){return Object.values(S.attempts).filter(a=>a.question_id===id).sort((a,b)=>String(a.ts).localeCompare(String(b.ts)));}
function plural(n,w){return n+" "+w+(n===1?"":"s");}
async function copyText(text){
  try{await navigator.clipboard.writeText(text);toast("Copied.");return true;}
  catch(e){const ta=document.createElement("textarea");ta.value=text;ta.style.position="fixed";ta.style.opacity="0";document.body.appendChild(ta);ta.select();
    let ok=false;try{ok=document.execCommand("copy");}catch(_){}ta.remove();toast(ok?"Copied.":"Copy was blocked. Use Download instead.");return ok;}
}
const ART=()=>AGStore.mode==="artifact";
async function download(name,data,type){
  if(ART()){const d=AGStore.downloads;if(!d){toast("Saving files isn't available in this view.");return false;}
    try{await d.save({filename:name,data});return true;}catch(e){toast(e&&e.code==="declined"?"Download cancelled.":"Download failed ("+(e&&e.code||"error")+").");return false;}}
  const blob=data instanceof Blob?data:new Blob([data],{type:type||"text/plain;charset=utf-8"});
  const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),5000);return true;
}
/* persistence: memory first, then IndexedDB */
async function put(coll,id,doc){doc.id=id;S[coll][id]=doc;try{await AGStore.put(coll,id,doc);}catch(e){toast("Could not save ("+(e&&e.name||"error")+"). Your browser storage may be full.");throw e;}}
async function putMany(writes){writes.forEach(w=>{if(w.doc==null)delete S[w.coll][w.id];else{w.doc.id=w.id;S[w.coll][w.id]=w.doc;}});
  try{await AGStore.batch(writes);}catch(e){toast("Could not save ("+(e&&e.name||"error")+").");throw e;}}

/* ---------- blobs (sketch images) ---------- */
const blobUrls=new Map();
async function blobUrl(id){const direct=AGStore.blobSrc(id);if(direct)return direct;if(blobUrls.has(id))return blobUrls.get(id);const b=await AGStore.getBlob(id);if(!b)return null;const u=URL.createObjectURL(b);blobUrls.set(id,u);return u;}
function hydrateImages(root){(root||document).querySelectorAll("img[data-blob]:not([src])").forEach(async img=>{const u=await blobUrl(img.dataset.blob);if(u)img.src=u;else img.replaceWith(Object.assign(document.createElement("span"),{className:"small muted",textContent:"(image not stored in this browser)"}));});}
function blobToDataUrl(b){return new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result);fr.onerror=()=>r(null);fr.readAsDataURL(b);});}

/* ---------- harder-rule guardrail (cached per question+course object) ---------- */
const guardCache=new WeakMap();
function guardOf(q){const c=courseOf(q)||null;const hit=guardCache.get(q);if(hit&&hit.c===c)return hit.r;const r=E.reviewHarder(q,c);guardCache.set(q,{c,r});return r;}
function guardPill(g){if(!g.applies)return "";return {pass:'<span class="pill ok" title="Meets the harder rule">Harder rule ✓</span>',fail:'<span class="pill bad" title="Fails the harder rule">Harder rule ✗</span>',unreviewed:'<span class="pill plain" title="Not reviewed against the harder rule">Not reviewed</span>'}[g.status]||"";}
function guardHeld(q){return S.settings.guard==="hold"&&["fail","unreviewed"].includes(guardOf(q).status);}

/* ---------- plan and queue ---------- */
function deckInfo(course,deck){const c=S.courses[course]||{};return ((c.decks||{})[deck])||null;}
function deckCfg(course,deck){const c=S.courses[course]||{};const d=((c.decks||{})[deck])||{};
  const exam=E.isISO(d.exam_date)?d.exam_date:(E.isISO(c.exam_date)?c.exam_date:null);
  const frd=d.final_review_days!=null?d.final_review_days:(c.final_review_days!=null?c.final_review_days:2);
  const prio=d.priority||c.priority||"none";
  const cfg={exam,examFrom:E.isISO(d.exam_date)?"deck":(exam?"subject":null),frd,prio,daysOff:Array.isArray(c.study_days_off)?c.study_days_off:[]};
  cfg.frActive=!!(exam&&frd!=="off"&&S.today>=E.addDays(exam,-Number(frd))&&S.today<=exam);return cfg;}
const qCfg=q=>deckCfg(q.course,q.deck);
function allItems(){return Object.values(S.questions).filter(q=>!guardHeld(q)).map(q=>{const cfg=qCfg(q);return {q,r:S.reviews[q.id]||{status:"new",due:S.today},course:courseOf(q),exam:cfg.exam,prio:cfg.prio,finalReview:cfg.frActive,forced:S.queueDeck===q.course+"|"+q.deck||S.queueSubject===q.course};});}
function attemptsTodayFor(ids){const set=new Set(ids);return Object.values(S.attempts).filter(a=>set.has(a.question_id)&&tsRomeDate(a.ts)===S.today).length;}
function planFor(course,deck){
  const qs=Object.values(S.questions).filter(q=>q.course===course&&(!deck||q.deck===deck));
  const cards=qs.map(q=>({q,r:E.normReview(S.reviews[q.id]||{status:"new",due:S.today})}));
  return E.examPlan(cards,deck?deckCfg(course,deck):deckCfg(course,"__none__"),S.today,attemptsTodayFor(qs.map(q=>q.id)));}
function planHtml(course,deck){const p=planFor(course,deck);if(!p.total)return "";
  let o='<div class="plan"><div class="row between"><span class="label">Exam plan</span><span class="small muted">'+(p.exam?"Exam "+fmtDate(p.exam)+" · "+plural(p.daysLeft,"day")+" to go":"No exam date: set one to get a daily goal")+"</span></div>";
  o+='<div class="row small"><span>Readiness <b class="num">'+p.readiness+'%</b></span><span class="grow bar" style="min-width:120px"><i style="width:'+p.readiness+'%"></i></span></div>';
  if(p.exam)o+='<div class="counts small"><span>Daily goal <b>'+p.goal+'</b></span><span>Done today <b>'+p.doneToday+'</b></span><span>Due now <b>'+p.dueToday+'</b></span><span>Study days left <b>'+p.studyDays+"</b></span></div>";
  if(p.frActive)o+='<p class="small"><span class="pill auth">Final review running</span> Archived cards are back in the queue until the exam.</p>';
  else if(p.frStart)o+='<p class="small muted">Final review starts '+fmtDate(p.frStart)+" ("+plural(Number(p.frd),"day")+" before the exam).</p>";
  if(p.behind)o+='<div class="notice">Catch up: aim for <b>'+p.catchUp+"</b> answers today ("+p.dueToday+" due, "+p.overdue+" overdue, goal "+p.goal+").</div>";
  return o+"</div>";}
function queue(){const all=E.buildQueue(allItems(),S.today);
  if(S.queueDeck)return all.filter(x=>x.q.course+"|"+x.q.deck===S.queueDeck);
  if(S.queueSubject)return all.filter(x=>x.q.course===S.queueSubject);
  return all;}
const subjectName=code=>{const c=S.courses[code];return (c&&c.name)||code;};
function deckTitle(course,deck){const d=deckInfo(course,deck);return (d&&d.title)||deck;}

/* ---------- banner ---------- */
function setBanner(){
  const out=[];
  if(S.dbError)out.push('<div class="notice bad">'+h(S.dbError)+"</div>");
  if(S.ready&&ART()&&!AGStore.sample)out.push('<div class="notice">Claude marking isn\'t available in this view. After you submit, mark written parts yourself against the key.</div>');
  if(S.ready&&ART()&&!AGStore.assets)out.push('<div class="notice">Sketches can\'t be saved in this view. Your working stays on screen until you leave the question.</div>');
  if(S.ready&&AGStore.mode==="memory")out.push('<div class="notice bad">This browser is not letting the page store data (private window or blocked site data). Anything you do here is lost when you close the tab. Use <b>Settings → Download full backup</b> before leaving.</div>');
  if(S.ready&&S.settings.guard==="hold"){const n=Object.values(S.questions).filter(guardHeld).length;if(n)out.push('<div class="notice info">'+plural(n,"generated question")+' held back from the queue by the harder rule. <a href="#/browse-list?guard=needs">Review them</a></div>');}
  BANNER.innerHTML=out.join("");
}

/* ---------- routing (hash) ---------- */
function parseHash(){const raw=(location.hash||"#/queue").slice(1);const [path,qs]=raw.split("?");const parts=path.split("/").filter(Boolean).map(decodeURIComponent);return {parts,params:new URLSearchParams(qs||"")};}
function nav(hash){if(location.hash===hash)route();else location.hash=hash;}
function route(){
  const {parts,params}=parseHash();const p0=parts[0]||"queue";
  if(S.A&&!S.A.submitted&&S.A.strokes.length&&!(p0==="q"&&parts[1]===S.A.qid)){
    if(Date.now()-(route.armed||0)>5000){route.armed=Date.now();history.replaceState(null,"","#/q/"+encodeURIComponent(S.A.qid));toast("Your sketch isn't saved until you submit. Go there again to leave without it.",5000);return;}
  }
  if(p0==="q"&&parts[1]){if(!S.A||S.A.qid!==parts[1]||S.A.submitted&&S.A.reopen)openQuestion(parts[1]);S.screen="answer";}
  else{S.A=null;
    if(p0==="browse"){S.screen="browse";S.subject=parts[1]||null;S.folder=parts[2]?{course:parts[1],deck:parts[2]}:null;}
    else if(p0==="browse-list"){S.screen="browse-list";const g=params.get("guard");if(g)S.browse.guard=g;const c=params.get("course");if(c!=null){S.browse.course=c;S.browse.deck=params.get("deck")||"";}}
    else if(["queue","stats","courses","settings","import"].includes(p0))S.screen=p0;
    else S.screen="queue";}
  $$("nav a").forEach(a=>{const g=a.dataset.go;const on=g===S.screen||(S.screen==="answer"&&g==="queue")||(S.screen==="browse-list"&&g==="browse")||(S.screen==="import"&&g==="settings");if(on)a.setAttribute("aria-current","page");else a.removeAttribute("aria-current");});
  render();window.scrollTo(0,0);
}
window.addEventListener("hashchange",route);

function render(){
  setBanner();
  if(!S.ready){MAIN.innerHTML='<div class="panel"><p class="muted">Loading your question bank…</p></div>';return;}
  const v={queue:viewQueue,courses:viewCourses,browse:viewBrowse,"browse-list":viewBrowseList,import:viewImport,stats:viewStats,settings:viewSettings}[S.screen];
  if(S.screen==="answer"){renderAnswer();return;}
  MAIN.innerHTML=(v||viewQueue)();hydrateImages(MAIN);renderSelBar();
}
function softRender(){if(S.screen==="answer")return;const a=document.activeElement;if(a&&MAIN.contains(a)&&/INPUT|TEXTAREA|SELECT/.test(a.tagName))return;render();}
setInterval(()=>{const t=E.romeToday();if(t!==S.today){S.today=t;$("#todayLbl").textContent=fmtDate(t);softRender();}},60000);

/* ---------- queue ---------- */
function viewQueue(){
  const Q=queue();const mins=Q.reduce((n,x)=>n+(Number(x.q.est_minutes)||0),0);
  const courses=Object.values(S.courses).filter(c=>c.status!=="closed");
  const todayIds=[...new Set(Object.values(S.attempts).filter(a=>tsRomeDate(a.ts)===S.today).map(a=>a.question_id))].filter(id=>S.questions[id]);
  let o='<section class="stack"><div class="hero"><div><div class="label">Due now</div><h2><span class="num">'+Q.length+'</span> '+(Q.length===1?"card":"cards")+' · <span class="num">'+Math.round(mins)+"</span> min</h2>"+
    (courses.length?'<div class="row" style="margin-top:8px">'+courses.map(c=>{const t=E.tierFor(c.exam_date,S.today);const n=Q.filter(x=>x.q.course===c.code).length;
      return '<span class="pill '+t+'">'+h(c.name||c.code)+" · "+(t==="none"?"no exam date":"exam "+fmtDate(c.exam_date))+" · "+n+" due</span>";}).join("")+"</div>":"")+"</div>"+
    '<div class="row">'+(todayIds.length?'<button class="btn" data-act="exportToday">Export today ('+todayIds.length+')</button>':"")+(Q.length?'<button class="btn primary big" data-act="open" data-id="'+h(Q[0].q.id)+'">Start <kbd>Enter</kbd></button>':"")+"</div></div>";
  if(S.session)o+='<div class="notice info row between"><span>Session: '+h(S.session.label)+" · "+Math.min(S.session.idx+1,S.session.ids.length)+" of "+S.session.ids.length+(S.session.record?"":" · dry run, nothing is saved")+'</span><span class="row"><button class="btn sm" data-act="resumeSession">Continue</button><button class="btn sm" data-act="endSession">End</button></span></div>';
  if(S.queueDeck||S.queueSubject)o+='<div class="row"><span class="pill auth">'+(S.queueDeck?"Deck: "+h(deckTitle(...S.queueDeck.split("|"))):"Subject: "+h(subjectName(S.queueSubject)))+'</span><button class="btn sm" data-act="allDecks">Show everything</button></div>';
  o+="</section>";
  if(!Object.keys(S.questions).length)return o+'<div class="panel empty"><p><strong>No questions yet.</strong></p><p>'+(ART()?'In Cowork, type <span class="cmd">New deck 30178: &lt;deck file&gt;</span> to add questions, or <a href="#/import">import a bank file</a>.':'Go to <a href="#/settings">Settings</a> to load the bundled 30178 bank, or <a href="#/import">import a bank file</a>.')+'</p></div>';
  if(!Q.length)return o+'<div class="panel empty"><p><strong>Nothing is due.</strong> Cards you haven\'t finished roll over, so the next ones appear on their due date.</p>'+(todayIds.length?'<p style="margin-top:8px">You answered '+plural(todayIds.length,"question")+' today. <button class="btn sm" data-act="exportToday">Export them</button></p>':"")+"</div>";
  o+='<div class="qlist" role="list">'+Q.map(x=>{
    const due=x.isNew?"new":x.r.sweep?"final review":x.overdue>0?x.overdue+"d overdue":"due today";
    return '<a class="qrow" role="listitem" href="#/q/'+encodeURIComponent(x.q.id)+'"><span class="stripe '+x.tier+'"></span><span class="qmain"><span class="t">'+h(x.q.topic||x.q.id)+'</span><span class="meta"><span class="mono">'+h(x.q.id)+"</span> · "+h(x.q.shape||"")+" · "+(Number(x.q.est_minutes)||"?")+' min</span></span><span class="tags">'+(x.q.difficulty==="hard"?'<span class="pill mid">Hard</span>':"")+(E.isLeech(x.r)?'<span class="pill bad">leech</span>':"")+'<span class="pill plain">'+h(due)+"</span></span></a>";
  }).join("")+"</div>";
  return o;
}

/* ---------- courses ---------- */
function courseCounts(code){
  const qs=Object.values(S.questions).filter(q=>q.course===code);const c={total:qs.length,new:0,active:0,archived:0,challenged:0,disabled:0,due:0};
  c.due=queue().filter(x=>x.q.course===code).length;qs.forEach(q=>{const st=(S.reviews[q.id]||{}).status||"new";c[st]=(c[st]||0)+1;});return c;}
function viewCourses(){
  const list=Object.values(S.courses).sort((a,b)=>String(a.code).localeCompare(String(b.code)));
  const open=list.filter(c=>c.status!=="closed"),closed=list.filter(c=>c.status==="closed");
  let o='<section class="stack"><div><div class="label">Courses</div><h2>Exam dates, plans and rules</h2></div>';
  if(!list.length)o+='<div class="panel empty">No courses yet. Load the bundled bank in <a href="#/settings">Settings</a> or <a href="#/import">import a bank file</a>.</div>';
  o+=open.map(courseCard).join("");
  if(closed.length)o+='<details class="panel"><summary><h3>Closed courses ('+closed.length+')</h3></summary><div class="stack" style="margin-top:10px">'+closed.map(c=>'<div class="row between"><span><strong class="mono">'+h(c.code)+"</strong> "+h(c.name||"")+' <span class="muted small">closed '+h(fmtDate((c.closed_at||"").slice(0,10)))+'</span></span><button class="btn sm" data-act="reopen" data-code="'+h(c.code)+'">Reopen</button></div>').join("")+"</div></details>";
  return o+"</section>";
}
function hardRulePanel(c){
  const qs=Object.values(S.questions).filter(q=>q.course===c.code&&E.hardApplies(q));
  const cnt={pass:0,fail:0,unreviewed:0};qs.forEach(q=>cnt[guardOf(q).status]++);
  const fp=c.fingerprint||{};const ht=fp.hard_target;
  const shapes=[...new Set([...Object.keys((ht&&ht.by_shape)||{}),...Object.keys(fp.by_shape||{})])];
  let o='<details class="rule"'+(cnt.fail+cnt.unreviewed?" open":"")+'><summary><span class="label">Harder rule</span> <span class="small muted">'+plural(qs.length,"generated question")+" · "+cnt.pass+" pass · "+cnt.fail+" fail · "+cnt.unreviewed+" not reviewed</span></summary>";
  o+='<div class="stack" style="margin-top:8px"><blockquote>'+h(ht?ht.rule:E.HARD_DEFAULT.rule)+"</blockquote>"+(ht&&ht.stated_by?'<p class="small muted">Stated by '+h(ht.stated_by)+"</p>":'<p class="small muted">This course has no fingerprint yet, so the default rule applies without numeric thresholds.</p>');
  if(shapes.length)o+='<div class="tablewrap"><table class="md small"><thead><tr><th>Shape</th><th>Slide max steps</th><th>Exam median steps</th><th>Each answer needs</th></tr></thead><tbody>'+shapes.map(sc=>{const T=E.hardThresholds(c,sc);
    return "<tr><td>"+h(sc)+'</td><td class="num">'+(T.slideMax??"—")+'</td><td class="num">'+(T.examMedian??"—")+"</td><td>steps "+(T.stepsFloor!=null?"&gt; "+T.stepsFloor:"")+(T.stepsMin!=null?" and ≥ "+T.stepsMin:"")+(T.conceptsMin!=null?", concepts ≥ "+T.conceptsMin:"")+"</td></tr>";}).join("")+"</tbody></table></div>";
  const T0=E.hardThresholds(c,"concept MCQ");
  o+='<p class="small">Plus at least <b>'+T0.minNotches+"</b> distinct notches"+(T0.minutesCap!=null?", at most <b>"+T0.minutesCap+"</b> min per answer":"")+", a key solved twice, no ambiguity and nothing outside the syllabus. Bank imports are checked against this before anything is added.</p>";
  o+='<div class="row"><a class="btn sm" href="#/browse-list?guard=needs&course='+encodeURIComponent(c.code)+'">Review questions that need it ('+(cnt.fail+cnt.unreviewed)+")</a></div></div></details>";
  return o;
}
function courseCard(c){
  const t=E.tierFor(c.exam_date,S.today),n=courseCounts(c.code),cid=h(c.code);
  const unk=Array.isArray(c.unknowns)?c.unknowns:[];const cl=S.closing[c.code];
  const neg=c.negative_marking==null?"UNKNOWN":c.negative_marking;
  let o='<article class="panel stack" id="course-'+cid+'"><div class="row between"><div><div class="label mono">'+cid+"</div><h3>"+h(c.name||c.code)+'</h3></div><span class="pill '+t+'">'+(t==="none"?"No exam date":t+" · "+E.diffDays(c.exam_date,S.today)+" days")+"</span></div>";
  o+='<div class="row"><label class="small muted" for="exam-'+cid+'">Exam date</label><input type="date" id="exam-'+cid+'" value="'+h(E.isISO(c.exam_date)?c.exam_date:"")+'"><button class="btn sm" data-act="saveExam" data-code="'+cid+'">Save</button>'+(E.isISO(c.exam_date)?'<span class="muted small">Reviews are capped at '+fmtDate(E.examCap(c.exam_date))+"</span>":"")+"</div>";
  o+=planHtml(c.code,null);
  o+='<div class="counts"><span>Due <b>'+n.due+"</b></span><span>New <b>"+n.new+"</b></span><span>Active <b>"+n.active+"</b></span><span>Archived <b>"+n.archived+"</b></span>"+(n.challenged?"<span>Challenged <b>"+n.challenged+"</b></span>":"")+'<span>Negative marking <b class="mono">'+h(typeof neg==="object"?JSON.stringify(neg):String(neg))+"</b></span></div>";
  o+=hardRulePanel(c);
  const DN=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];const off=Array.isArray(c.study_days_off)?c.study_days_off:[];const frv=c.final_review_days==null?"2":String(c.final_review_days);
  o+='<details><summary><span class="label">Plan settings</span></summary><div class="settings" style="margin-top:8px">'+
    '<label class="small muted">Priority<br><select id="sprio-'+cid+'">'+[["none","No priority"],["exam","Exam"],["studying","Currently studying"],["paused","Paused"]].map(([v,l])=>'<option value="'+v+'"'+((c.priority||"none")===v?" selected":"")+">"+l+"</option>").join("")+"</select></label>"+
    '<label class="small muted">Final review starts<br><select id="sfr-'+cid+'">'+[["off","Off (manual sweep only)"],["1","1 day before"],["2","2 days before"],["3","3 days before"],["5","5 days before"],["7","7 days before"]].map(([v,l])=>'<option value="'+v+'"'+(frv===v?" selected":"")+">"+l+"</option>").join("")+"</select></label></div>"+
    '<div class="small muted" style="margin-top:8px">Days you will not study (the daily goal spreads over the rest)</div><div class="days">'+[1,2,3,4,5,6,0].map(d=>'<label><input type="checkbox" id="sday-'+cid+"-"+d+'"'+(off.includes(d)?" checked":"")+"> "+DN[d]+"</label>").join("")+"</div>"+
    '<div class="row" style="margin-top:8px"><button class="btn sm primary" data-act="saveSubject" data-code="'+cid+'">Save plan settings</button></div></details>';
  if(Array.isArray(c.format_profile)&&c.format_profile.length)o+='<details><summary><span class="label">Exam format</span></summary><div class="tablewrap"><table class="md small"><tbody>'+c.format_profile.map(f=>"<tr><th>"+h(f.item)+"</th><td>"+h(f.value)+'<br><span class="muted">'+h(f.label||"")+"</span></td></tr>").join("")+"</tbody></table></div></details>";
  if(unk.length)o+='<details><summary><span class="label">'+plural(unk.length,"open question")+' about the exam</span></summary><ul class="small">'+unk.map(u=>"<li><strong>"+h(u.item)+"</strong> — settle with: "+h(u.settle_with)+"</li>").join("")+"</ul></details>";
  o+='<div class="row"><a class="btn sm" href="#/browse/'+encodeURIComponent(c.code)+'">Open subject</a><button class="btn sm" data-act="exportCourse" data-code="'+cid+'">Export attempted…</button>'+(S.sweepAsk[c.code]?'<span class="small">Bring all '+n.archived+' archived cards back today?</span><button class="btn sm primary" data-act="sweepDo" data-code="'+cid+'">Yes, sweep</button><button class="btn sm" data-act="sweepCancel" data-code="'+cid+'">Cancel</button>':'<button class="btn sm" data-act="sweepAsk" data-code="'+cid+'"'+(n.archived?"":" disabled")+">Start final review now</button>")+'<span class="grow"></span><button class="btn sm danger" data-act="closeStart" data-code="'+cid+'">Close course…</button></div>';
  if(cl)o+=closePanel(c,n,cl);
  return o+"</article>";
}
function closePanel(c,n,cl){
  const code=h(c.code);const att=Object.values(S.attempts).filter(a=>(S.questions[a.question_id]||{}).course===c.code||a.course===c.code).length;
  return '<div class="panel stack" style="background:var(--surface-2)"><h3>Close '+code+" after the exam</h3><p class=\"small muted\">Removes the course's "+n.total+" questions, their schedules, "+att+" attempts, challenges and sketches from this browser. The course settings stay, marked closed, so you can reopen it.</p>"+
    '<ol class="small"><li>Save a backup: <button class="btn sm" data-act="closeBackup" data-code="'+code+'">'+(cl.backedUp?"Backup saved ✓":"Download backup")+"</button></li>"+
    '<li>Type the course code to confirm: <input type="text" id="closeCode-'+code+'" autocomplete="off" style="width:120px" value="'+h(cl.typed||"")+'"></li></ol>'+
    (cl.msg?'<p class="small muted">'+h(cl.msg)+"</p>":"")+
    '<div class="row"><button class="btn danger solid" data-act="closeDo" data-code="'+code+'"'+(cl.running?" disabled":"")+'>Delete from this browser</button><button class="btn sm" data-act="closeCancel" data-code="'+code+'">Cancel</button></div></div>';
}

/* ---------- browse: folders ---------- */
function sectionTitle(q,id){const d=deckInfo(q.course,q.deck);const s=d&&Array.isArray(d.sections)?d.sections.find(x=>x.id===id):null;return s?s.title:id;}
function slideLine(q){if(!Array.isArray(q.slides)||!q.slides.length)return "";const g=q.slide_groups||[];
  return "Slides "+E.slideRanges(q.slides)+(g.length?" · "+sectionTitle(q,g[0])+(g.length>1?" (also "+g.slice(1).map(x=>sectionTitle(q,x)).join("; ")+")":""):"");}
function deckStats(qs){const c={total:qs.length,new:0,active:0,archived:0,challenged:0,disabled:0,due:0,attempted:0};const ids=new Set(qs.map(q=>q.id));
  c.due=E.buildQueue(allItems().filter(it=>ids.has(it.q.id)).map(it=>({...it,forced:true})),S.today).length;
  const tried=new Set(Object.values(S.attempts).map(a=>a.question_id));
  qs.forEach(q=>{const st=(S.reviews[q.id]||{}).status||"new";c[st]=(c[st]||0)+1;if(tried.has(q.id))c.attempted++;});return c;}
function selBox(id){return '<label class="sel" title="Select for export"><input type="checkbox" data-sel="'+h(id)+'"'+(S.sel.has(id)?" checked":"")+' aria-label="Select '+h(id)+'"></label>';}
function qRow(q,extra){
  const r=reviewOf(q.id);const open=S.detail===q.id;const g=guardOf(q);const n=attemptsOf(q.id).length;
  return '<div class="qitem'+(open?" open":"")+'"><div class="qrow"><span class="stripe '+E.tierFor((courseOf(q)||{}).exam_date,S.today)+'"></span>'+selBox(q.id)+'<button class="qbtn" data-act="detail" data-id="'+h(q.id)+'" aria-expanded="'+open+'"><span class="qmain"><span class="t">'+h(q.topic||q.id)+'</span><span class="meta"><span class="mono">'+h(q.id)+"</span>"+(extra?" · "+extra:"")+'</span></span><span class="tags">'+
    (n?'<span class="pill plain" title="Attempts">'+n+"×</span>":"")+guardPill(g)+(E.isLeech(r)?'<span class="pill bad">leech</span>':"")+'<span class="pill plain">'+h(r.status||"new")+"</span></span></button></div>"+(open?detailPanel(q,r):"")+"</div>";
}
function viewBrowse(){
  const qs=Object.values(S.questions);
  const head='<div class="row between"><div><div class="label">Browse</div><h2>'+(S.folder?h(deckTitle(S.folder.course,S.folder.deck)):S.subject?h(subjectName(S.subject)):"Subjects")+'</h2></div><div class="seg" role="group" aria-label="Browse view"><a href="#/browse" aria-pressed="true">Folders</a><a href="#/browse-list" aria-pressed="false">All questions</a></div></div>';
  let body;
  if(S.folder)body=viewFolder(S.folder.course,S.folder.deck,qs);
  else if(S.subject)body=viewSubject(S.subject,qs.filter(q=>q.course===S.subject));
  else body=viewSubjects(qs);
  return '<section class="stack">'+head+body+"</section>";
}
function viewSubjects(qs){
  const by={};qs.forEach(q=>(by[q.course]=by[q.course]||[]).push(q));Object.keys(S.courses).forEach(c=>{if(!by[c]&&S.courses[c].status!=="closed")by[c]=[];});
  const codes=Object.keys(by).sort();
  if(!codes.length)return '<div class="panel empty">No subjects yet. Load the bundled bank in <a href="#/settings">Settings</a>.</div>';
  return '<div class="stack">'+codes.map(code=>{const list=by[code];const st=deckStats(list);const c=S.courses[code]||{};const t=E.tierFor(c.exam_date,S.today);const decks=new Set(list.map(q=>q.deck)).size;
    return '<article class="panel stack"><div class="row between"><a class="cardlink" href="#/browse/'+encodeURIComponent(code)+'"><div class="label mono">Subject · '+h(code)+"</div><h3>"+h(subjectName(code))+'</h3></a><span class="pill '+t+'">'+(t==="none"?"No exam date":"exam "+fmtDate(c.exam_date))+'</span></div><div class="counts"><span>Decks <b>'+decks+"</b></span><span>Questions <b>"+st.total+"</b></span><span>Attempted <b>"+st.attempted+"</b></span><span>Due <b>"+st.due+"</b></span><span>Archived <b>"+st.archived+"</b></span></div>"+
      '<div class="row"><a class="btn sm primary" href="#/browse/'+encodeURIComponent(code)+'">Open</a><button class="btn sm" data-act="practiseSubject" data-course="'+h(code)+'"'+(st.due?"":" disabled")+">Practise ("+st.due+' due)</button><button class="btn sm" data-act="exportSubject" data-course="'+h(code)+'"'+(st.attempted?"":" disabled")+">Export attempted ("+st.attempted+")</button></div></article>";}).join("")+"</div>";
}
function viewSubject(code,list){
  const by={};list.forEach(q=>(by[q.deck]=by[q.deck]||[]).push(q));const decks=Object.keys(by).sort();
  let o='<div class="row"><a class="btn sm" href="#/browse">← All subjects</a><span class="grow"></span><button class="btn sm" data-act="exportSubject" data-course="'+h(code)+'">Export subject…</button></div>'+planHtml(code,null);
  if(!decks.length)return o+'<div class="panel empty">No deck folders yet. <a href="#/import">Import a bank file</a>.</div>';
  return o+'<div class="stack">'+decks.map(deck=>{const l=by[deck];const st=deckStats(l);const info=deckInfo(code,deck);const cov=new Set(l.flatMap(q=>(q.slides||[]).map(Number)));const cf=deckCfg(code,deck);
    const href="#/browse/"+encodeURIComponent(code)+"/"+encodeURIComponent(deck);
    return '<article class="panel stack"><div class="row between"><a class="cardlink" href="'+href+'"><div class="label mono">Deck folder · '+h(deck)+"</div><h3>"+h(deckTitle(code,deck))+'</h3><p class="small muted">'+(cf.exam?"Exam "+fmtDate(cf.exam)+(cf.examFrom==="deck"?" (deck date)":""):"No exam date")+(cf.prio!=="none"?" · "+h(cf.prio):"")+"</p></a></div>"+
      '<div class="counts"><span>Questions <b>'+st.total+"</b></span><span>Attempted <b>"+st.attempted+"</b></span><span>New <b>"+st.new+"</b></span><span>Archived <b>"+st.archived+"</b></span><span>Slides covered <b>"+cov.size+(info&&info.slide_count?" / "+info.slide_count:"")+"</b></span>"+(()=>{const c=E.deckCoverage(info,l);return c.hasUnits?"<span>Units covered <b>"+c.covered+" / "+c.examinable+"</b></span>"+(c.sections.length?"<span>Sections with Hard <b>"+(c.sections.length-c.noHard.length)+" / "+c.sections.length+"</b></span>":""):"";})()+"</div>"+
      '<div class="row"><a class="btn sm primary" href="'+href+'">Open folder</a><button class="btn sm" data-act="practiseDeck" data-course="'+h(code)+'" data-deck="'+h(deck)+'"'+(st.due?"":" disabled")+">Practise ("+st.due+' due)</button><button class="btn sm" data-act="exportDeck" data-course="'+h(code)+'" data-deck="'+h(deck)+'"'+(st.attempted?"":" disabled")+">Export attempted ("+st.attempted+")</button></div></article>";}).join("")+"</div>";
}
/* Coverage guardrail in the folder: every examinable deck unit needs a question; every section needs a Hard one. */
function coveragePanel(course,deck,list){
  const c=E.deckCoverage(deckInfo(course,deck),list);if(!c.hasUnits)return "";
  const ok=!c.gaps.length&&!c.noHard.length;const qid=id=>'<a class="mono" href="#/q/'+encodeURIComponent(id)+'">'+h(id.replace(course+"-",""))+"</a>";
  const sec=c.sections.length?c.sections:[{id:"",title:"Units",hard:[],units:c.units}];
  return '<details class="panel"'+(ok?"":" open")+'><summary><h3>Coverage</h3> <span class="pill '+(ok?"ok":"bad")+'" style="white-space:normal">'+c.covered+" / "+c.examinable+" units"+(c.sections.length?" · "+(c.sections.length-c.noHard.length)+" / "+c.sections.length+" sections with a Hard question":"")+"</span></summary>"+
    '<p class="small muted" style="margin-top:8px">Every examinable topic in the deck needs at least one question, and every section needs a Hard one. Non-examinable items say why.</p>'+
    '<div class="tablewrap"><table class="md small"><thead><tr><th>Unit</th><th>Questions</th></tr></thead><tbody>'+sec.map(s=>
      (s.id?'<tr><th colspan="2">'+h(s.id)+" · "+h(s.title||"")+" "+(s.hard.length?'<span class="pill ok" style="white-space:normal">Hard: '+s.hard.map(qid).join(", ")+"</span>":'<span class="pill bad">No Hard question</span>')+"</th></tr>":"")+
      s.units.map(u=>"<tr><td>"+h(u.title)+(u.where?' <span class="muted">('+h(u.where)+")</span>":"")+"</td><td>"+(u.examinable===false?'<span class="muted">Not examinable: '+h(u.reason||"")+"</span>":u.qids.length?u.qids.map(qid).join(", "):'<span class="pill bad">Gap</span>')+"</td></tr>").join("")).join("")+
    "</tbody></table></div>"+(c.unmapped.length?'<p class="small muted">Not yet mapped to a unit: '+c.unmapped.map(qid).join(", ")+".</p>":"")+"</details>";
}
/* Re-importing a course: your settings (exam dates, priority, final review, status) stay; the bank's structure
   (fingerprint, ledger, deck titles, sections and units) is refreshed. */
const COURSE_BANK_FIELDS=["fingerprint","source_ledger","format_profile","unknowns","inventory","name","folder_path"],DECK_BANK_FIELDS=["file","title","slide_count","sections","units","reading"];
function mergeCourse(cur,inc){
  const out=Object.assign({},inc,cur);COURSE_BANK_FIELDS.forEach(k=>{if(inc[k]!==undefined)out[k]=inc[k];});
  const decks=Object.assign({},inc.decks||{},cur.decks||{});
  Object.entries(inc.decks||{}).forEach(([d,v])=>{decks[d]=Object.assign({},v,(cur.decks||{})[d]||{});DECK_BANK_FIELDS.forEach(k=>{if(v&&v[k]!==undefined)decks[d][k]=v[k];});});
  out.decks=decks;return out;
}
function viewFolder(course,deck,qs){
  const list=qs.filter(q=>q.course===course&&q.deck===deck).sort(E.newOrder);const info=deckInfo(course,deck)||{};const st=deckStats(list);
  const n=info.slide_count||Math.max(0,...list.flatMap(q=>(q.slides||[]).map(Number)));
  const perSlide=[],empty=[];for(let i=1;i<=n;i++){const hit=list.filter(q=>(q.slides||[]).map(Number).includes(i));if(hit.length)perSlide.push([i,hit]);else empty.push(i);}
  const cfg=deckCfg(course,deck);const sid=h(deck);const subj=S.courses[course]||{};
  const prioSel='<select id="dprio-'+sid+'">'+[["","Inherit ("+(subj.priority||"none")+")"],["exam","Exam"],["studying","Currently studying"],["none","No priority"],["paused","Paused"]].map(([v,l])=>'<option value="'+v+'"'+(v===(info.priority||"")?" selected":"")+">"+l+"</option>").join("")+"</select>";
  const inh=subj.final_review_days!=null?subj.final_review_days:2;
  const frSel='<select id="dfr-'+sid+'">'+[["","Inherit ("+(inh==="off"?"off":inh+" days")+")"],["off","Off"],["1","1 day before"],["2","2 days before"],["3","3 days before"],["5","5 days before"],["7","7 days before"]].map(([v,l])=>'<option value="'+v+'"'+(String(info.final_review_days==null?"":info.final_review_days)===v?" selected":"")+">"+l+"</option>").join("")+"</select>";
  const allIds=list.map(q=>q.id),tried=new Set(Object.values(S.attempts).map(a=>a.question_id));const triedIds=allIds.filter(id=>tried.has(id));
  let o='<div class="row"><a class="btn sm" href="#/browse/'+encodeURIComponent(course)+'">← '+h(subjectName(course))+"</a></div>"+
    '<article class="panel stack"><p class="small muted">'+list.length+" questions in slide order · "+perSlide.length+" of "+(n||"?")+" slides have a question · "+st.attempted+" attempted</p>"+
    '<div class="row"><button class="btn sm primary" data-act="practiseDeck" data-course="'+h(course)+'" data-deck="'+sid+'"'+(st.due?"":" disabled")+">Practise due ("+st.due+')</button><button class="btn sm" data-act="sessionAll" data-course="'+h(course)+'" data-deck="'+sid+'">All in slide order</button><button class="btn sm" data-act="sessionDry" data-course="'+h(course)+'" data-deck="'+sid+'">Dry run</button><span class="grow"></span><button class="btn sm" data-act="exportDeck" data-course="'+h(course)+'" data-deck="'+sid+'"'+(st.attempted?"":" disabled")+">Export folder…</button></div>"+planHtml(course,deck)+"</article>";
  o+='<details class="panel"><summary><h3>Deck settings</h3></summary><div class="settings" style="margin-top:10px"><label class="small muted">Exam date for this deck<br><input type="date" id="dexam-'+sid+'" value="'+h(E.isISO(info.exam_date)?info.exam_date:"")+'"></label><label class="small muted">Priority<br>'+prioSel+'</label><label class="small muted">Final review starts<br>'+frSel+'</label><button class="btn sm primary" data-act="saveDeck" data-course="'+h(course)+'" data-deck="'+sid+'">Save</button></div><p class="small muted" style="margin-top:8px">'+(cfg.examFrom==="subject"?"Blank date uses the subject's exam date ("+fmtDate(cfg.exam)+").":cfg.examFrom==="deck"?"This deck has its own exam date.":"No exam date on the deck or the subject.")+' Paused decks stay out of the main queue but keep their schedule.</p><div class="row" style="margin-top:8px"><button class="btn sm" data-act="sweepDeck" data-course="'+h(course)+'" data-deck="'+sid+'">Start final review now</button></div></details>';
  o+=coveragePanel(course,deck,list);
  o+='<div class="row small"><span class="muted">Select:</span><button class="btn sm ghost" data-act="selSet" data-ids="'+h(triedIds.join(","))+'">Attempted ('+triedIds.length+')</button><button class="btn sm ghost" data-act="selSet" data-ids="'+h(allIds.join(","))+'">All</button>'+(S.sel.size?'<button class="btn sm ghost" data-act="selClear">None</button>':"")+"</div>";
  o+='<div class="qlist">'+list.map(q=>qRow(q,(Array.isArray(q.slides)&&q.slides.length?"slides "+h(E.slideRanges(q.slides)):"slides not mapped")+" · "+h((q.source||{}).type||""))).join("")+"</div>";
  if(perSlide.length)o+='<details class="panel"><summary><h3>Slide by slide</h3></summary><div class="tablewrap" style="margin-top:10px"><table class="md small"><thead><tr><th>Slide</th><th>Questions</th></tr></thead><tbody>'+perSlide.map(([i,hs])=>'<tr><td class="mono">'+i+"</td><td>"+hs.map(q=>'<span class="mono">'+h(q.id.replace(q.course+"-",""))+"</span> "+h(q.topic||"")).join("<br>")+"</td></tr>").join("")+"</tbody></table></div>"+(empty.length?'<p class="small muted">No question yet on slides '+h(E.slideRanges(empty))+".</p>":"")+"</details>";
  return o;
}

/* ---------- browse: list with filters ---------- */
function filteredList(){
  const f=S.browse;const tried=new Set(Object.values(S.attempts).map(a=>a.question_id));const qq=f.q.trim().toLowerCase();
  return Object.values(S.questions).filter(q=>(!f.course||q.course===f.course)&&(!f.deck||q.deck===f.deck)&&(!f.topic||q.topic===f.topic)&&
    (!f.status||((S.reviews[q.id]||{}).status||"new")===f.status)&&(!f.src||(q.source||{}).type===f.src)&&
    (!f.attempted||(f.attempted==="yes")===tried.has(q.id))&&
    (!f.guard||(f.guard==="needs"?["fail","unreviewed"].includes(guardOf(q).status):guardOf(q).status===f.guard))&&
    (!qq||(q.id+" "+(q.topic||"")+" "+(q.stem||"")).toLowerCase().includes(qq))).sort(E.newOrder);
}
function viewBrowseList(){
  const f=S.browse;const qs=Object.values(S.questions);
  const uniq=k=>[...new Set(qs.filter(q=>!f.course||q.course===f.course).map(k))].filter(Boolean).sort();
  const sel=(key,label,vals,cur)=>'<label class="small muted">'+label+'<br><select data-filter="'+key+'"><option value="">All</option>'+vals.map(v=>{const [val,lab]=Array.isArray(v)?v:[v,v];return '<option'+(val===cur?" selected":"")+' value="'+h(val)+'">'+h(lab)+"</option>";}).join("")+"</select></label>";
  const rows=filteredList();const tried=rows.filter(q=>attemptsOf(q.id).length).map(q=>q.id);
  let o='<section class="stack"><div class="row between"><div><div class="label">Browse</div><h2>Question bank</h2></div><div class="seg" role="group"><a href="#/browse" aria-pressed="false">Folders</a><a href="#/browse-list" aria-pressed="true">All questions</a></div></div>'+
    '<div class="filters"><label class="small muted search">Search<br><input type="search" data-filter="q" value="'+h(f.q)+'" placeholder="id, topic or text"></label>'+
    sel("course","Course",[...new Set(qs.map(q=>q.course))].sort(),f.course)+sel("deck","Deck",uniq(q=>q.deck),f.deck)+sel("topic","Topic",uniq(q=>q.topic),f.topic)+
    sel("status","Status",["new","active","archived","challenged","disabled"],f.status)+sel("src","Source",["real","adapted","generated"],f.src)+
    sel("attempted","Attempted",[["yes","Attempted"],["no","Not attempted"]],f.attempted)+
    sel("guard","Harder rule",[["needs","Needs review"],["pass","Pass"],["fail","Fail"],["unreviewed","Not reviewed"],["exempt","Exempt (course material)"]],f.guard)+"</div>";
  o+='<div class="row between small"><span class="muted">'+plural(rows.length,"question")+'</span><span class="row"><span class="muted">Select:</span><button class="btn sm ghost" data-act="selSet" data-ids="'+h(tried.join(","))+'">Attempted here ('+tried.length+')</button><button class="btn sm ghost" data-act="selSet" data-ids="'+h(rows.map(q=>q.id).join(","))+'">All shown</button>'+(S.sel.size?'<button class="btn sm ghost" data-act="selClear">None</button>':"")+"</span></div>";
  if(rows.length)o+='<div class="qlist">'+rows.map(q=>{const r=reviewOf(q.id);return qRow(q,(Array.isArray(q.slides)&&q.slides.length?"slides "+h(E.slideRanges(q.slides))+" · ":"")+h((q.source||{}).type||"")+" · streak "+(r.streak|0)+(r.status==="active"&&r.due?" · due "+fmtDate(E.effectiveDue(r,(courseOf(q)||{}).exam_date,S.today)):""));}).join("")+"</div>";
  else o+='<div class="panel empty">No questions match these filters.</div>';
  return o+"</section>";
}
function renderSelBar(){
  let bar=$("#selbar");const show=S.sel.size&&["browse","browse-list"].includes(S.screen);
  if(!show){if(bar)bar.hidden=true;return;}
  if(!bar){bar=document.createElement("div");bar.id="selbar";bar.className="selbar";document.body.appendChild(bar);}
  const tried=[...S.sel].filter(id=>attemptsOf(id).length).length;
  bar.hidden=false;bar.innerHTML='<span><b class="num">'+S.sel.size+"</b> selected · "+tried+' attempted</span><span class="row"><button class="btn sm" data-act="selClear">Clear</button><button class="btn sm primary" data-act="exportSel">Export…</button></span>';
}

/* ---------- question detail (browse) ---------- */
function detailPanel(q,r){
  const atts=attemptsOf(q.id).reverse();const ch=Object.values(S.challenges).filter(c=>c.question_id===q.id);
  let p='<div class="detail stack"><div class="row">'+srcPill(q)+'<span class="small muted">'+h(q.syllabus_objective||"")+"</span></div>"+
    '<div class="row"><a class="btn sm primary" href="#/q/'+encodeURIComponent(q.id)+'">Practise now</a><button class="btn sm" data-act="exportOne" data-id="'+h(q.id)+'">Export…</button>'+(r.status==="archived"?'<button class="btn sm" data-act="restore" data-id="'+h(q.id)+'">Restore to active</button>':"")+'<button class="btn sm" data-act="toggleDisable" data-id="'+h(q.id)+'">'+(r.status==="disabled"?"Enable":"Disable")+"</button></div>";
  p+=guardPanel(q);
  if(ch.length)p+='<div class="small stack">'+ch.map(c=>'<div class="row"><span class="pill '+(c.resolved?"ok":"mid")+'">'+(c.resolved?"challenge resolved":"challenge open")+"</span> "+h(c.note||"")+(c.resolved?"":' <button class="btn sm" data-act="resolveChallenge" data-cid="'+h(c.id)+'">Resolve and return to queue</button>')+"</div>").join("")+"</div>";
  p+='<div class="label">'+plural(atts.length,"attempt")+"</div>";
  p+=atts.map(a=>{const v=attemptVerdict(a);const m=a.marking||{};
    return '<div class="attempt"><div class="row"><span class="pill '+h(v||"plain")+'">'+h(v||"unmarked")+'</span><span class="small mono muted">'+h(E.tsLabel(a.ts))+"</span>"+(a.override?'<span class="small muted">rated '+h(a.override.rating||"")+"</span>":"")+(a.counted===false?'<span class="small muted">not counted</span>':"")+'</div><p class="small">Selected: <span class="mono">'+h(Object.entries(a.selected||{}).map(([n,l])=>n+" "+l).join(", ")||"—")+"</span></p>"+
      (a.typed_reasoning?'<p class="small prewrap">'+h(a.typed_reasoning)+"</p>":"")+(m.correction?'<p class="small"><strong>Correction.</strong> '+h(m.correction)+"</p>":"")+(a.sketch_asset?'<img class="sketchimg" alt="Your working" data-blob="'+h(a.sketch_asset)+'" loading="lazy">':"")+"</div>";}).join("");
  return p+"</div>";
}
function guardPanel(q){
  const g=guardOf(q);if(!g.applies)return '<p class="small muted">Harder rule: exempt. '+h(g.summary)+"</p>";
  const T=g.thresholds;const hc=q.hard_check||{};const byN={};(hc.parts||[]).forEach(p=>byN[String(p.n)]=p);const nn=new Set(hc.notches||[]);
  let o='<details class="rule"'+(g.status!=="pass"?" open":"")+'><summary>'+guardPill(g)+' <span class="small muted">'+h(g.summary)+"</span></summary><div class=\"stack\" style=\"margin-top:8px\">";
  o+='<ul class="checks">'+g.checks.map(c=>'<li class="'+(c.ok?"ok":"bad")+'"><span aria-hidden="true">'+(c.ok?"✓":"✗")+"</span> <b>"+h(c.label)+'</b> <span class="muted">— '+h(c.detail)+"</span></li>").join("")+"</ul>";
  if(hc.reviewed_at)o+='<p class="small muted">Reviewed '+h(E.tsLabel(hc.reviewed_at))+(hc.reviewed_by?" by "+h(hc.reviewed_by):"")+"</p>";
  o+='<details><summary><span class="label">'+(q.hard_check?"Edit the review":"Record a review")+'</span></summary><form class="stack hardform" data-id="'+h(q.id)+'" style="margin-top:8px"><p class="small muted">Count what a student has to do for each answer. Shape class: <b>'+h(T.sc)+"</b>. Each answer needs steps "+(T.stepsFloor!=null?"&gt; "+T.stepsFloor:"")+(T.stepsMin!=null?" and ≥ "+T.stepsMin:"")+(T.conceptsMin!=null?", concepts ≥ "+T.conceptsMin:"")+".</p>";
  o+='<div class="partgrid">'+E.answerParts(q).map(n=>{const p=byN[n]||{};return '<span class="mono">'+h(n)+'</span><label class="small">Steps <input type="number" step="0.5" min="0" name="steps:'+h(n)+'" value="'+h(p.steps??"")+'"></label><label class="small">Concepts <input type="number" step="0.5" min="0" name="concepts:'+h(n)+'" value="'+h(p.concepts??"")+'"></label>';}).join("")+"</div>";
  o+='<fieldset><legend class="small">Notches used (at least '+T.minNotches+')</legend><div class="notches">'+T.notches.map(k=>'<label class="small"><input type="checkbox" name="notch" value="'+h(k)+'"'+(nn.has(k)?" checked":"")+"> <b>"+h(k.replace(/_/g," "))+"</b>"+(E.HARD_NOTCHES[k]?' <span class="muted">'+h(E.HARD_NOTCHES[k])+"</span>":"")+"</label>").join("")+"</div></fieldset>";
  o+='<label class="small"><input type="checkbox" name="no_ambiguity"'+(hc.no_ambiguity?" checked":"")+"> Each part has exactly one defensible answer; it is not harder because of vague wording</label>";
  o+='<label class="small"><input type="checkbox" name="in_syllabus"'+(hc.in_syllabus?" checked":"")+"> Everything needed is in the slides or syllabus</label>";
  if(q.difficulty!=="hard")o+='<label class="small"><input type="checkbox" name="relabel"> Relabel as Hard (only if the counts above pass)</label>';
  o+='<div class="row"><button class="btn sm primary" type="submit">Save review</button></div></form></details></div></details>';
  return o;
}

/* ---------- stats ---------- */
function viewStats(){
  const codes=[...new Set(Object.values(S.questions).map(q=>q.course))].sort();const sc=S.statsCourse||"";
  const qs=Object.values(S.questions).filter(q=>!sc||q.course===sc);const qids=new Set(qs.map(q=>q.id));
  const atts=Object.values(S.attempts).filter(a=>qids.has(a.question_id));
  const byDay={};atts.forEach(a=>{const d=tsRomeDate(a.ts);byDay[d]=(byDay[d]||0)+1;});
  let streak=0,d=byDay[S.today]?S.today:E.addDays(S.today,-1);while(byDay[d]){streak++;d=E.addDays(d,-1);}
  const last7=Object.entries(byDay).filter(([k])=>E.diffDays(S.today,k)<7).reduce((n,[,v])=>n+v,0);
  const a30=atts.filter(a=>E.diffDays(S.today,tsRomeDate(a.ts))<30);const ok30=a30.filter(a=>attemptVerdict(a)==="Correct").length;
  let o='<section class="stack"><div class="row between"><div><div class="label">Stats</div><h2>How your practice is going</h2></div><label class="small muted">Subject<br><select id="statsCourse"><option value="">All subjects</option>'+codes.map(c=>'<option value="'+h(c)+'"'+(c===sc?" selected":"")+">"+h(subjectName(c))+"</option>").join("")+"</select></label></div>";
  o+='<div class="tiles"><div class="stat"><div class="label">Streak</div><div class="v">'+streak+'</div><div class="small muted">'+(streak===1?"day":"days")+' in a row</div></div><div class="stat"><div class="label">Last 7 days</div><div class="v">'+last7+'</div><div class="small muted">answers</div></div><div class="stat"><div class="label">Correct, 30 days</div><div class="v">'+(a30.length?Math.round(100*ok30/a30.length)+"%":"—")+'</div><div class="small muted">'+ok30+" of "+a30.length+"</div></div></div>";
  const endSun=E.addDays(S.today,6-E.weekday(S.today));const start=E.addDays(endSun,-83);const cells=[];
  for(let i=0;i<84;i++){const day=E.addDays(start,i);const n=byDay[day]||0;const l=day>S.today?-1:n===0?0:n<=2?1:n<=5?2:n<=9?3:4;cells.push(l<0?'<i style="visibility:hidden"></i>':'<i data-l="'+l+'" title="'+fmtDate(day)+": "+plural(n,"answer")+'"></i>');}
  o+='<div class="panel stack"><div><div class="label">Practice history</div><h3>Answers per day, last 12 weeks</h3></div><div class="heat" role="img" aria-label="Answers per day over the last 12 weeks">'+cells.join("")+'</div><div class="row small muted"><span>Less</span>'+[0,1,2,3,4].map(l=>'<span class="heatkey" data-l="'+l+'"></span>').join("")+"<span>More</span></div></div>";
  const fc=Array(14).fill(0);
  qs.forEach(q=>{const r=E.normReview(S.reviews[q.id]||{status:"new",due:S.today});if(!["new","active"].includes(r.status)||guardHeld(q))return;const cfg=qCfg(q);if(cfg.prio==="paused")return;const k=Math.max(0,E.diffDays(E.effectiveDue(r,cfg.exam,S.today),S.today));if(k<14)fc[k]++;});
  const mx=Math.max(1,...fc);
  o+='<div class="panel stack"><div><div class="label">Forecast</div><h3>Cards due, next 14 days</h3><p class="small muted">Today includes anything overdue and every new card.</p></div><div class="fc" role="img" aria-label="Cards due per day for the next 14 days">'+fc.map((n,i)=>'<div title="'+fmtDate(E.addDays(S.today,i))+": "+n+' due"><span class="small num muted">'+(n&&(n===mx||i===0)?n:"")+'</span><span class="b" style="height:'+Math.round(100*n/mx)+'%"></span></div>').join("")+'</div><div class="fcx">'+fc.map((n,i)=>"<span>"+(i===0?"Today":i%2===0?E.addDays(S.today,i).slice(8)+"/"+E.addDays(S.today,i).slice(5,7):"")+"</span>").join("")+"</div></div>";
  const levels=[["New","m0"],["Learning","m1"],["Growing","m2"],["Solidifying","m3"],["Mastered","m4"]];
  const decks={};qs.forEach(q=>{const k=q.course+"|"+q.deck;(decks[k]=decks[k]||[]).push(q);});
  o+='<div class="panel stack"><div><div class="label">Mastery</div><h3>Where each deck folder stands</h3><p class="small muted">Learning = no counted correct in a row · Growing = 1 · Solidifying = 2 · Mastered = archived after 3.</p></div><div class="row">'+levels.map(([l,c])=>'<span class="key"><i class="'+c+'"></i>'+l+"</span>").join("")+"</div>";
  o+=Object.keys(decks).sort().map(k=>{const [course,deck]=k.split("|");const cnt=[0,0,0,0,0];
    decks[k].forEach(q=>{const r=E.normReview(S.reviews[q.id]||{status:"new"});if(r.status==="disabled")return;cnt[r.status==="new"?0:r.status==="archived"?4:Math.min(3,1+(r.streak|0))]++;});
    return '<div class="stack" style="gap:4px"><div class="row between small"><span><strong>'+h(deckTitle(course,deck))+'</strong> <span class="muted mono">'+h(course)+'</span></span><span class="muted num">'+cnt.map((n,i)=>levels[i][0]+" "+n).join(" · ")+'</span></div><div class="stack5" role="img" aria-label="'+h(cnt.map((n,i)=>levels[i][0]+" "+n).join(", "))+'">'+cnt.map((n,i)=>n?'<i class="'+levels[i][1]+'" style="flex:'+n+'" title="'+levels[i][0]+": "+n+'"></i>':"").join("")+"</div></div>";}).join("")+"</div>";
  const agg={};
  atts.forEach(a=>{const q=S.questions[a.question_id];if(!q||!Array.isArray(q.slides))return;const ok=attemptVerdict(a)==="Correct";
    q.slides.forEach(sl=>{const k=q.course+"|"+q.deck+"|"+sl;const x=agg[k]=agg[k]||{course:q.course,deck:q.deck,slide:sl,n:0,ok:0,qs:new Set()};x.n++;if(ok)x.ok++;x.qs.add(q.id.replace(q.course+"-",""));});});
  const rows=Object.values(agg).sort((a,b)=>(a.ok/a.n)-(b.ok/b.n)||b.n-a.n).slice(0,12);
  o+='<div class="panel stack"><div><div class="label">Weakest slides</div><h3>Correct rate by slide</h3><p class="small muted">Each answer counts towards every slide its question uses. The 12 weakest are shown.</p></div>'+
    (rows.length?'<div class="tablewrap"><table class="md small"><thead><tr><th>Deck</th><th>Slide</th><th>Answers</th><th>Correct</th><th>Questions</th></tr></thead><tbody>'+rows.map(x=>{const pc=Math.round(100*x.ok/x.n);
      return "<tr><td>"+h(deckTitle(x.course,x.deck))+'</td><td class="mono">'+x.slide+'</td><td class="num">'+x.n+'</td><td><span class="num">'+pc+'%</span> <span class="bar inline"><i style="width:'+pc+'%"></i></span></td><td class="mono">'+h([...x.qs].join(", "))+"</td></tr>";}).join("")+"</tbody></table></div>":'<p class="small muted">No answers yet.</p>')+"</div>";
  return o+"</section>";
}

/* ---------- settings ---------- */
function viewSettings(){
  const st=S.settings;const docs=COLLS.reduce((n,c)=>n+Object.keys(S[c]).length,0);
  let o='<section class="stack"><div><div class="label">Settings</div><h2>Marking, rules and your data</h2></div>';
  if(!ART())o+='<div class="panel stack"><h3>Appearance</h3><div class="seg" role="group" aria-label="Theme">'+[["auto","Match device"],["light","Light"],["dark","Dark"]].map(([v,l])=>'<button data-act="theme" data-v="'+v+'" aria-pressed="'+(st.theme===v)+'">'+l+"</button>").join("")+"</div></div>";
  if(ART())o+='<div class="panel stack"><h3>Claude marking</h3><p class="small muted">'+(AGStore.sample?"Multiple-choice parts are marked from the key. When you write reasoning, Claude marks it using your claude.ai account; the first time, you are asked to allow it.":"Claude marking isn't available in this view, so you mark written parts yourself against the key.")+"</p></div>";
  else o+='<div class="panel stack"><h3>Claude marking (optional)</h3><p class="small muted">Multiple-choice parts are always marked here, from the key. To have Claude judge your written reasoning, add an Anthropic API key. The key stays in this browser and is sent only to api.anthropic.com. Without one, you mark written parts yourself against the revealed key.</p>'+
    '<div class="settings"><label class="small muted">API key<br><input type="password" id="apiKey" autocomplete="off" placeholder="sk-ant-…" value="'+h(st.apiKey)+'"></label><label class="small muted">Model<br><select id="apiModel">'+[["claude-opus-5","Claude Opus 5 (recommended)"],["claude-sonnet-5","Claude Sonnet 5 (cheaper)"]].map(([v,l])=>'<option value="'+v+'"'+(st.model===v?" selected":"")+">"+l+"</option>").join("")+'</select></label></div><div class="row"><button class="btn sm primary" data-act="saveKey">Save</button>'+(st.apiKey?'<button class="btn sm" data-act="testKey">Test the key</button><button class="btn sm danger" data-act="clearKey">Remove key</button>':"")+'<span class="small muted" id="keyMsg">'+(st.apiKey?"Claude marking is on.":"Claude marking is off.")+"</span></div></div>";
  o+='<div class="panel stack"><h3>Harder rule on the queue</h3><p class="small muted">Imports always block generated questions that fail the harder rule. This decides what happens to generated questions already in the bank that fail it or were never reviewed.</p><div class="seg" role="group">'+[["flag","Flag them"],["hold","Hold them back from the queue"]].map(([v,l])=>'<button data-act="guardMode" data-v="'+v+'" aria-pressed="'+(st.guard===v)+'">'+l+"</button>").join("")+'</div><p><a href="#/browse-list?guard=needs">See the questions that need review</a></p></div>';
  o+='<div class="panel stack"><h3>Your data</h3><p class="small muted">'+(ART()?"Stored in this artifact's database, so it follows you across devices, and questions Cowork adds show up here. "+docs+" records.":"Stored in this browser only ("+(AGStore.mode==="indexeddb"?"IndexedDB":"memory: not saved")+"). "+docs+" records. Download a backup now and then, and before clearing browser data or switching device.")+'</p>'+
    '<div class="row"><button class="btn sm primary" data-act="backupAll">Download full backup (.json)</button><a class="btn sm" href="#/import">Restore or import…</a><button class="btn sm" data-act="exAll">Export all attempted…</button><button class="btn sm" data-act="exMistakes">Mistakes list (.md)</button></div>'+
    (window.AG_SEED?'<div class="row"><button class="btn sm" data-act="mergeSeed">Add the bundled 30178 bank</button><span class="small muted">Adds any bundled questions you don\'t have. Never overwrites your progress.</span></div>':"")+
    (ART()?"":'<details><summary><span class="label" style="color:var(--bad)">Erase everything</span></summary><div class="row" style="margin-top:8px"><input type="text" id="eraseConfirm" placeholder="Type ERASE" autocomplete="off"><button class="btn sm danger solid" data-act="eraseAll">Erase this browser\'s data</button></div></details>')+"</div>";
  o+='<div class="panel stack"><h3>Keyboard shortcuts</h3><div class="tablewrap"><table class="md small"><tbody>'+
    [["Enter","Start the next card · submit · next card"],["A–D or 1–4","Choose an option (moves to the next part)"],["Ctrl/⌘ + Enter","Submit from inside the reasoning box"],["1 · 2 · 3 · 4","After submitting: Forgot · Partial · Effort · Easy"],["E","After submitting: export this question"],["Esc","Leave the reasoning box"]].map(([k,v])=>"<tr><th><kbd>"+k+"</kbd></th><td>"+v+"</td></tr>").join("")+"</tbody></table></div></div>";
  return o+"</section>";
}

/* ---------- import (bank files and backups) — the harder-rule review runs here before anything is written ---------- */
function viewImport(){
  const pv=S.importPreview;
  let o='<section class="stack"><div><div class="label">Import</div><h2>Add questions or restore a backup</h2><p class="muted small">Drop a bank file (<span class="cmd">bank_&lt;course&gt;_&lt;deck&gt;.json</span>: an array of questions or <span class="cmd">{questions:[…]}</span>, optionally with <span class="cmd">courses</span>) or an Answer Grid backup. Every question is validated, and every generated question is reviewed against its course\'s harder rule. Anything that fails is not added.</p></div>'+
    '<label class="drop" id="drop"><input type="file" id="importFile" accept=".json,application/json"><span>Drop a .json file here or <u>choose one</u></span></label>'+
    '<textarea id="importText" class="mono" placeholder="…or paste the JSON here" style="min-height:120px;font-size:.85rem">'+h(S.importText||"")+'</textarea><div class="row"><button class="btn primary" data-act="importCheck">Check</button><a class="btn sm" href="#/settings">Back</a></div>';
  if(pv){
    o+='<div class="panel stack"><h3>Review</h3>';
    if(pv.fileError)o+='<div class="notice bad">'+h(pv.fileError)+"</div>";
    else{
      o+='<div class="counts"><span>Ready to add <b>'+pv.ok.length+"</b></span><span>Blocked <b>"+pv.bad.length+"</b></span>"+(pv.skip.length?"<span>Already in the bank <b>"+pv.skip.length+"</b></span>":"")+(pv.courses.length?"<span>Courses <b>"+pv.courses.length+"</b></span>":"")+(pv.progress?"<span>Progress records <b>"+pv.progress+"</b></span>":"")+"</div>";
      if(pv.bad.length)o+='<div class="stack"><div class="label">Blocked</div><ul class="small blocked">'+pv.bad.map(b=>'<li><span class="mono">'+h(b.id)+"</span> — "+h(b.errs.join("; "))+"</li>").join("")+"</ul></div>";
      if(pv.ok.length)o+='<div class="tablewrap"><table class="md small"><thead><tr><th>Id</th><th>Topic</th><th>Source</th><th>Harder rule</th></tr></thead><tbody>'+pv.ok.map(q=>{const g=E.reviewHarder(q,pv.courseFor(q));return '<tr><td class="mono">'+h(q.id)+"</td><td>"+h(q.topic)+"</td><td>"+h(q.source.type)+"</td><td>"+(g.applies?"✓ pass":"exempt")+"</td></tr>";}).join("")+"</tbody></table></div>";
      if(pv.ok.length||pv.courses.length||pv.progress)o+='<div class="row"><button class="btn primary" data-act="importWrite"'+(pv.writing?" disabled":"")+">Add "+plural(pv.ok.length,"question")+(pv.progress?" and restore progress":"")+"</button>"+(pv.msg?'<span class="small muted">'+h(pv.msg)+"</span>":"")+"</div>";
    }
    o+="</div>";
  }
  return o+"</section>";
}
function checkImport(text){
  let data;try{data=JSON.parse(text);}catch(e){return {fileError:"Not valid JSON: "+e.message};}
  const asMap=v=>Array.isArray(v)?Object.fromEntries(v.filter(x=>x&&x.id!=null).map(x=>[x.id,x])):(v&&typeof v==="object"?v:{});
  let qs=Array.isArray(data)?data:Array.isArray(data&&data.questions)?data.questions:(data&&data.questions&&typeof data.questions==="object"?Object.values(data.questions):null);
  if(!qs)return {fileError:"Expected an array of questions, {questions:[…]} or an Answer Grid backup."};
  const inCourses=Array.isArray(data.courses)?Object.fromEntries(data.courses.filter(c=>c&&(c.code||c.id)).map(c=>[c.code||c.id,c])):asMap(data.courses);if(data.course&&typeof data.course==="object"&&data.course.code)inCourses[data.course.code]=data.course;
  const courses=Object.values(inCourses).filter(c=>c&&c.code);
  const courseFor=q=>inCourses[q.course]||S.courses[q.course]||null;
  const seen=new Set(),ok=[],bad=[],skip=[];
  for(const q of qs){const id=q&&q.id||"(no id)";
    if(q&&q.id&&S.questions[q.id]){skip.push(id);continue;}
    const errs=E.validateQuestion(q);
    if(q&&q.id&&seen.has(q.id))errs.push("duplicate id in this file");if(q&&q.id)seen.add(q.id);
    if(!errs.length){const g=E.reviewHarder(q,courseFor(q));if(g.applies&&g.status!=="pass")errs.push("harder rule: "+(g.status==="unreviewed"?"no hard_check review":g.checks.filter(c=>!c.ok).map(c=>c.label+" ("+c.detail+")").join("; ")));}
    (errs.length?bad:ok).push(errs.length?{id,errs}:q);}
  const prog={reviews:asMap(data.reviews),attempts:asMap(data.attempts),challenges:asMap(data.challenges)};
  const progress=Object.values(prog).reduce((n,m)=>n+Object.keys(m).length,0);
  return {ok,bad,skip,courses,courseFor,prog,progress};
}
async function writeImport(){
  const pv=S.importPreview;if(!pv||pv.writing)return;pv.writing=true;render();
  try{
    const w=[];
    pv.courses.forEach(c=>{const cur=S.courses[c.code];w.push({coll:"courses",id:c.code,doc:cur?mergeCourse(cur,c):{status:"active",...c}});});
    pv.ok.forEach(q=>{if(!S.courses[q.course]&&!pv.courses.some(c=>c.code===q.course))w.push({coll:"courses",id:q.course,doc:{code:q.course,name:q.course,status:"active"}});
      w.push({coll:"questions",id:q.id,doc:q});
      if(!pv.prog.reviews[q.id]&&!S.reviews[q.id])w.push({coll:"reviews",id:q.id,doc:{status:"new",streak:0,interval_days:0,due:S.today,lapses:0,last_counted_date:null,history:[]}});});
    ["reviews","attempts","challenges"].forEach(c=>Object.entries(pv.prog[c]).forEach(([id,doc])=>{if(!S[c][id])w.push({coll:c,id,doc});}));
    const seenK=new Set();const uniq=w.filter(x=>{const k=x.coll+"/"+x.id;if(seenK.has(k))return false;seenK.add(k);return true;});
    await putMany(uniq);pv.msg="Done: "+plural(pv.ok.length,"question")+" added.";toast(pv.msg);S.importPreview=null;S.importText="";nav("#/browse");
  }catch(e){pv.msg="Import failed: "+(e&&e.message||e);}
  pv.writing=false;render();
}

/* ---------- answering ---------- */
function draftKey(id){return "ag-draft:"+id;}
function loadDraft(id){try{return JSON.parse(localStorage.getItem(draftKey(id))||"null");}catch(e){return null;}}
function saveDraft(){const A=S.A;if(!A||A.submitted||A.dry)return;try{if(!Object.keys(A.selected).length&&!(A.typed||"").trim())localStorage.removeItem(draftKey(A.qid));else localStorage.setItem(draftKey(A.qid),JSON.stringify({sel:A.selected,typed:A.typed||"",typedBy:A.typedBy||{},ts:Date.now()}));}catch(e){}}
function clearDraft(id){try{localStorage.removeItem(draftKey(id));}catch(e){}}
function openQuestion(id){
  const q=S.questions[id];if(!q){S.A={qid:id,missing:true,strokes:[]};return;}
  const dr=loadDraft(id);const firstMcq=(q.subquestions||[]).find(s=>Array.isArray(s.options)&&s.options.length);
  const subs=q.subquestions||[];
  const typedBy=dr&&dr.typedBy?dr.typedBy:(dr&&dr.typed&&subs.length?{[subs[0].n]:dr.typed}:{});
  S.A={dry:!!(S.session&&!S.session.record&&S.session.ids.includes(id)),qid:id,selected:dr?dr.sel||{}:{},typedBy,typed:E.composeTyped(q,typedBy),restored:!!dr,started:Date.now(),timerOn:false,submitted:false,strokes:[],penSeen:false,tool:"pen",full:false,markStatus:"idle",sketch:null,sketchNote:"",note:"",cur:firstMcq?String(firstMcq.n):null};
}
function goQuestion(id){if(S.A&&S.A.qid===id&&!S.A.submitted){nav("#/q/"+encodeURIComponent(id));return;}openQuestion(id);nav("#/q/"+encodeURIComponent(id));}
function renderAnswer(){
  const A=S.A;const q=A&&S.questions[A.qid];
  if(!q){MAIN.innerHTML='<div class="panel">That question is not in the bank. <a class="btn sm" href="#/queue">Back to the queue</a></div>';return;}
  const c=courseOf(q);const neg=negOf(q);
  let o='<article class="panel stack answer" id="answerCard"><div class="qhead"><div><div class="label mono">'+h(q.id)+(S.session&&S.session.ids.includes(q.id)?" · "+(S.session.idx+1)+" of "+S.session.ids.length:"")+"</div><h2>"+h(q.topic||"")+'</h2></div><div class="row" style="gap:6px">'+srcPill(q)+'<span class="pill plain">'+h(q.shape||"")+"</span></div></div>";
  o+='<div class="row small muted"><span>'+h(c?c.name||c.code:q.course)+" · deck "+h(q.deck||"")+"</span><span>· marks <span class=\"mono\">"+h(numOrUnknown(q.marks))+'</span></span><span>· wrong answer <span class="mono">'+h(String(typeof neg==="object"?JSON.stringify(neg):neg))+'</span></span><span class="grow"></span><button class="btn sm ghost" data-act="timer">'+(A.timerOn?"Hide timer":"Timer")+'</button><span class="timer" id="timer"'+(A.timerOn?"":" hidden")+"></span></div>";
  if(A.dry)o+='<div class="notice info">Dry run: nothing you do here is saved or changes the schedule.</div>';
  if(A.restored&&!A.submitted)o+='<div class="notice info row between"><span>Picked up your unsubmitted draft.</span><button class="btn sm" data-act="discardDraft">Start fresh</button></div>';
  if(slideLine(q))o+='<p class="small"><span class="label">From the deck</span> '+h(slideLine(q))+"</p>";
  o+='<div class="md">'+E.mdToHtml(q.stem)+"</div>";
  if(q.data)o+='<div class="md">'+E.mdToHtml(q.data)+"</div>";
  o+=(q.subquestions||[]).map(s=>{const isM=Array.isArray(s.options)&&s.options.length;
    return '<div class="sub'+(isM&&String(s.n)===A.cur&&!A.submitted?" cur":"")+'" data-sub="'+h(s.n)+'"><div class="row between"><div class="md"><span class="n">'+h(s.n)+"</span> "+(E.promptRepeatsStem(q,s)?"":E.mdToHtml(s.prompt).replace(/^<p>/,"<span>").replace(/<\/p>$/,"</span>"))+'</div><span class="small muted mono">'+h(numOrUnknown(s.marks))+" mk</span></div>"+
      (isM?'<div class="opts" role="group" aria-label="Options for '+h(s.n)+'">'+s.options.map((op,i)=>'<button class="opt" data-act="pick" data-n="'+h(s.n)+'" data-i="'+i+'" aria-pressed="'+(A.selected[s.n]===i)+'"'+(A.submitted?" disabled":"")+'><span class="L">'+E.LETTERS[i]+'</span><span class="md">'+E.mdToHtml(op).replace(/^<p>/,"").replace(/<\/p>$/,"")+"</span></button>").join("")+"</div>":"")+
      '<div class="stack partans"><label class="label" for="typed-'+h(s.n)+'">'+(isM?"Your reasoning for "+h(s.n):"Your answer to "+h(s.n))+'</label><textarea class="parttyped" id="typed-'+h(s.n)+'" data-part="'+h(s.n)+'" rows="'+(isM?3:5)+'" placeholder="'+(isM?"Why this option: steps, classifications, assumptions.":"Write your answer and show the working.")+(canMark()?" Claude marks this.":"")+'"'+(A.submitted?" readonly":"")+"></textarea></div></div>";}).join("");
  o+='<details class="stack sketchwrap"'+(A.strokes.length||A.padOpen?" open":"")+'><summary><span class="label">Working (sketch pad)</span></summary><div class="sketch" id="sketch"><div class="tools"><button data-act="tool" data-tool="pen" aria-pressed="'+(A.tool==="pen")+'">Pen</button><button data-act="tool" data-tool="eraser" aria-pressed="'+(A.tool==="eraser")+'">Eraser</button><button data-act="undo">Undo</button><button data-act="clearPad">Clear</button><span class="grow"></span><button data-act="fullPad">'+(A.full?"Done":"Expand")+'</button></div><canvas id="pad" aria-label="Sketch pad for your working"></canvas></div><p class="small muted">Saved with the attempt so you can look back at it and include it in exports. It is not sent for marking.</p></details>';
  o+='<section id="reveal" class="reveal" hidden></section></article>';
  o+='<div class="actionbar" id="actionbar"></div>';
  MAIN.innerHTML=o;
  $$(".parttyped").forEach(t=>{t.value=(A.typedBy||{})[t.dataset.part]||"";});
  const sw=$(".sketchwrap");sw.addEventListener("toggle",()=>{A.padOpen=sw.open;if(sw.open)sizePad();});
  setupPad();renderActionBar();
  if(A.submitted){markKeyOnOptions(q,A);renderReveal();}
}
function renderActionBar(){
  const A=S.A;const el=$("#actionbar");if(!el||!A)return;const q=S.questions[A.qid];
  if(!A.submitted){const parts=(q.subquestions||[]).filter(s=>Array.isArray(s.options)&&s.options.length);const done=parts.filter(s=>A.selected[s.n]!=null).length;
    el.innerHTML='<span class="small muted">'+(parts.length?done+" of "+parts.length+" chosen":"")+'<span class="hide-sm">'+(parts.length?" · ":"")+'keys A–D, Enter to submit</span></span><button class="btn primary" data-act="submit">Submit <kbd>Enter</kbd></button>';return;}
  const final=A.override?A.override.verdict:A.verdict;const cur=final?(A.override&&A.override.rating)||ratingOf(final,A.easy):null;
  el.innerHTML='<div class="seg" role="group" aria-label="How did it go?">'+[["Forgot","Wrong",0,1],["Partial","Partial",0,2],["Effort","Correct",0,3],["Easy","Correct",1,4]].map(([l,v,e,k])=>'<button data-act="rate" data-v="'+v+'" data-easy="'+e+'" aria-pressed="'+(cur===l)+'" title="Key '+k+'">'+l+"</button>").join("")+'</div><span class="grow"></span><button class="btn" data-act="exportCurrent" title="Key E">Export</button><button class="btn primary" data-act="next"'+(A.markStatus==="running"?" disabled":"")+">Next <kbd>Enter</kbd></button>";
}
setInterval(()=>{const A=S.A;if(!A||!A.timerOn||S.screen!=="answer")return;const el=$("#timer");if(!el)return;const s=Math.floor(((A.stopped||Date.now())-A.started)/1000);const q=S.questions[A.qid]||{};el.textContent=String(Math.floor(s/60)).padStart(2,"0")+":"+String(s%60).padStart(2,"0")+" / "+(Number(q.est_minutes)||"?")+" min";},1000);
function pick(n,i){const A=S.A;if(!A||A.submitted)return;A.selected[n]=A.selected[n]===i?undefined:i;if(A.selected[n]===undefined)delete A.selected[n];
  $$('.opt[data-n="'+CSS.escape(n)+'"]').forEach(x=>x.setAttribute("aria-pressed",String(+x.dataset.i===A.selected[n])));setCur(n);saveDraft();renderActionBar();}
function setCur(n){const A=S.A;A.cur=String(n);$$(".sub").forEach(s=>s.classList.toggle("cur",s.dataset.sub===A.cur&&!!s.querySelector(".opt")));}

/* ----- sketch pad ----- */
function padCtx(){const c=$("#pad");return c&&c.getContext("2d");}
function sizePad(){const c=$("#pad");if(!c)return;const r=c.getBoundingClientRect();if(!r.width)return;const dpr=window.devicePixelRatio||1;c.width=Math.max(1,Math.round(r.width*dpr));c.height=Math.max(1,Math.round(r.height*dpr));c.getContext("2d").setTransform(dpr,0,0,dpr,0,0);if(S.A)S.A.padSize=[r.width,r.height];redraw();}
function strokeColor(){return getComputedStyle(document.documentElement).getPropertyValue("--stroke").trim()||"#10213f";}
function drawSeg(x,st,a,b,color){x.save();x.globalCompositeOperation=st.tool==="eraser"?"destination-out":"source-over";x.strokeStyle=color;x.lineCap="round";x.lineJoin="round";
  x.lineWidth=st.tool==="eraser"?22:Math.max(.8,2.6*(0.35+(b[2]||0.5)));x.beginPath();x.moveTo(a[0],a[1]);x.lineTo(b[0],b[1]);x.stroke();x.restore();}
function drawStroke(x,st,color){const p=st.pts;if(p.length===1){drawSeg(x,st,p[0],[p[0][0]+.1,p[0][1]+.1,p[0][2]],color);return;}for(let i=1;i<p.length;i++)drawSeg(x,st,p[i-1],p[i],color);}
function redraw(){const x=padCtx();if(!x||!S.A)return;const c=$("#pad");x.clearRect(0,0,c.width,c.height);const col=strokeColor();S.A.strokes.forEach(s=>drawStroke(x,s,col));}
function setupPad(){
  const c=$("#pad");if(!c)return;const A=S.A;let cur=null,pid=null;
  const pt=e=>{const r=c.getBoundingClientRect();return [e.clientX-r.left,e.clientY-r.top,e.pointerType==="mouse"?0.5:(e.pressure||0.5)];};
  c.addEventListener("pointerdown",e=>{if(A.submitted)return;if(e.pointerType==="pen")A.penSeen=true;if(e.pointerType==="touch"&&(A.penSeen||cur))return;
    e.preventDefault();try{c.setPointerCapture(e.pointerId);}catch(_){}pid=e.pointerId;cur={tool:A.tool,pts:[pt(e)]};});
  c.addEventListener("pointermove",e=>{if(!cur||e.pointerId!==pid)return;e.preventDefault();const evs=e.getCoalescedEvents?e.getCoalescedEvents():[e];const x=padCtx();const col=strokeColor();
    for(const ev of (evs.length?evs:[e])){const p=pt(ev);const last=cur.pts[cur.pts.length-1];cur.pts.push(p);drawSeg(x,cur,last,p,col);}});
  const end=e=>{if(!cur||e.pointerId!==pid)return;if(cur.pts.length===1)drawStroke(padCtx(),cur,strokeColor());A.strokes.push(cur);cur=null;pid=null;};
  c.addEventListener("pointerup",end);c.addEventListener("pointercancel",end);sizePad();
}
window.addEventListener("resize",()=>{if(S.screen==="answer")sizePad();});
function sketchBlob(){return new Promise(res=>{const src=$("#pad");if(!src||!S.A.strokes.length)return res(null);const b0=src.getBoundingClientRect();const r=b0.width?b0:{width:(S.A.padSize||[800,340])[0],height:(S.A.padSize||[800,340])[1]};const sc=2;
  const off=document.createElement("canvas");off.width=Math.max(1,Math.round(r.width*sc));off.height=Math.max(1,Math.round(r.height*sc));const x=off.getContext("2d");
  const ink=document.createElement("canvas");ink.width=off.width;ink.height=off.height;const ix=ink.getContext("2d");ix.setTransform(sc,0,0,sc,0,0);S.A.strokes.forEach(s=>drawStroke(ix,s,"#10213f"));
  x.fillStyle="#ffffff";x.fillRect(0,0,off.width,off.height);x.drawImage(ink,0,0);off.toBlob(b=>res(b),"image/png");});}

/* ----- submit, marking, scheduling ----- */
const MARKER_RULES=`You are marking one exam attempt strictly against the supplied answer key and mark scheme. Use no outside knowledge.

Quote the exact phrase or step from the student's typed reasoning that each judgement refers to.

Do not change or question the answer key. If the key's status is "unverified", say that the mark is provisional.

If the student used a valid method the scheme does not list, set alternative_method_flag to true and describe it. Do not invent credit.

If the selected options are all correct but the reasoning is fundamentally wrong or absent, the verdict is Partial.

The verdict is Correct only when every sub-question is correct and the reasoning is sound.`;
const MARK_SCHEMA={type:"object",additionalProperties:false,required:["verdict","reasoning_judgements","error_tags_hit","correction","legibility","alternative_method_flag","alternative_method","provisional"],properties:{
  verdict:{type:"string",enum:["Correct","Partial","Wrong"]},
  reasoning_judgements:{type:"array",items:{type:"object",additionalProperties:false,required:["quote","judgement"],properties:{quote:{type:"string"},judgement:{type:"string"}}}},
  error_tags_hit:{type:"array",items:{type:"string"}},correction:{type:"string",description:"the specific step that went wrong, and the right step, in at most 3 sentences"},
  legibility:{type:"string",enum:["ok","partial","illegible","not_sent"]},alternative_method_flag:{type:"boolean"},alternative_method:{type:"string"},provisional:{type:"boolean"}}};
function markerPrompt(q,A){
  const qv={id:q.id,topic:q.topic,stem:q.stem,data:q.data||"",subquestions:(q.subquestions||[]).map(s=>({n:s.n,prompt:s.prompt,options:(s.options||[]).map((o,i)=>E.LETTERS[i]+". "+o),marks:s.marks}))};
  const picks=A.mcq.map(r=>r.isMcq?{n:r.n,selected:r.selected==null?"(blank)":E.LETTERS[r.selected],correct_per_page_code:r.correct}:{n:r.n,written_part:true});
  return MARKER_RULES+"\n\nThe page has already decided each multiple-choice part by comparing the selection with the key; those results are final and you must not re-decide them. Judge the reasoning, and judge any written part against the mark scheme.\nNo handwriting is sent for this attempt: set \"legibility\" to \"not_sent\".\n\nQUESTION:\n"+JSON.stringify(qv)+"\n\nANSWER KEY:\n"+JSON.stringify(q.answer_key||[])+"\n\nMARK SCHEME:\n"+JSON.stringify(q.mark_scheme||[])+"\n\nERROR TAGS (each names the wrong option or mistake it catches):\n"+JSON.stringify(q.error_tags||[])+"\n\nCITATIONS:\n"+JSON.stringify(q.citations||[])+"\n\nSTUDENT ANSWER:\n"+JSON.stringify({selections:picks,typed_reasoning:A.typed||""});
}
async function callClaude(prompt,maxTokens){
  const st=S.settings;const headers={"content-type":"application/json","x-api-key":st.apiKey,"anthropic-version":"2023-06-01","anthropic-dangerous-direct-browser-access":"true"};
  const body={model:st.model,max_tokens:maxTokens||16000,output_config:{effort:"high",format:{type:"json_schema",schema:MARK_SCHEMA}},messages:[{role:"user",content:prompt}]};
  if(st.model==="claude-opus-5"){headers["anthropic-beta"]="server-side-fallback-2026-07-01";body.fallbacks="default";}
  const ctl=new AbortController();const t=setTimeout(()=>ctl.abort(),180000);
  try{const res=await fetch("https://api.anthropic.com/v1/messages",{method:"POST",headers,body:JSON.stringify(body),signal:ctl.signal});
    if(res.status===401||res.status===403)return {ok:false,code:"auth"};
    if(res.status===429)return {ok:false,code:"rate_limited"};
    if(!res.ok){let m="";try{m=((await res.json()).error||{}).message||"";}catch(e){}return {ok:false,code:"http_"+res.status,msg:m};}
    const j=await res.json();if(j.stop_reason==="refusal")return {ok:false,code:"refusal"};
    const text=(j.content||[]).filter(b=>b.type==="text").map(b=>b.text).join("");
    try{return {ok:true,o:JSON.parse(text)};}catch(e){return {ok:false,code:"invalid_json"};}
  }catch(e){return {ok:false,code:e&&e.name==="AbortError"?"timeout":"network"};}
  finally{clearTimeout(t);}
}
const canMark=()=>!!(AGStore.sample||S.settings.apiKey);
async function sampleMarker(q,A){
  try{const o=await AGStore.sample.json(markerPrompt(q,A)+"\n\nReply with only one JSON object matching this JSON Schema:\n"+JSON.stringify(MARK_SCHEMA),{modelTier:"complex",cache:false});
    return validateOr(o);}
  catch(e){const c=e&&e.code;if(["not_granted","sampling_disabled","not_declared","capability_disabled","capability_removed"].includes(c))return {ok:false,code:"not_granted"};
    return {ok:false,code:c==="rate_limited"?"rate_limited":c==="invalid_json"?"invalid_json":(c||"error")};}
}
function validateOr(o){return E.validateMarker(o).length?{ok:false,code:"schema"}:{ok:true,o};}
async function runMarker(q,A){
  if(AGStore.sample)return sampleMarker(q,A);
  let last={ok:false,code:"invalid"};
  for(let i=0;i<2;i++){const r=await callClaude(markerPrompt(q,A));if(r.ok){const errs=E.validateMarker(r.o);if(!errs.length)return r;last={ok:false,code:"schema"};continue;}
    if(["invalid_json","network","http_500","http_529","http_503"].includes(r.code)){last=r;continue;}return r;}
  return last;
}
async function submitAnswer(){
  const A=S.A,q=S.questions[A.qid];if(!A||A.submitted||!q)return;
  A.typedBy=A.typedBy||{};$$(".parttyped").forEach(t=>{A.typedBy[t.dataset.part]=t.value;});A.typed=E.composeTyped(q,A.typedBy);const blank=!Object.keys(A.selected).length&&!A.typed.trim()&&!A.strokes.length;
  if(blank&&!A.blankArmed){A.blankArmed=true;toast("Nothing chosen or written. Submit again to record a blank attempt (it counts as Wrong).",4500);return;}
  if(A.full){A.full=false;$("#sketch").classList.remove("full");}
  A.submitted=true;A.stopped=Date.now();clearDraft(q.id);
  $$(".parttyped").forEach(t=>{t.readOnly=true;});$$(".opt").forEach(b=>b.disabled=true);$$(".sub.cur").forEach(s=>s.classList.remove("cur"));
  A.mcq=E.mcqResults(q,A.selected);A.tags=E.tagsFromSelections(q,A.mcq);
  A.reviewBefore=E.normReview(S.reviews[q.id]||{status:"new",due:S.today});
  A.provisional=(q.answer_key||[]).some(k=>k.answer_status==="unverified");
  const written=A.mcq.some(r=>!r.isMcq);markKeyOnOptions(q,A);
  A.sketchPromise=A.dry?Promise.resolve(null):sketchBlob();
  if(canMark()&&(A.typed.trim()||written)){A.markStatus="running";renderReveal();renderActionBar();
    const res=await runMarker(q,A);if(S.A!==A)return;
    if(res.ok){A.marking=res.o;if(A.provisional)A.marking.provisional=true;A.marking.marked_by="claude";A.markStatus="done";await finalize(E.combineVerdict(A.mcq,res.o.verdict),"claude");}
    else{A.markStatus="failed";A.markFail=res.code;A.markMsg=res.msg||"";if(!written)await finalize(E.mcqVerdict(A.mcq),"options");else renderReveal();}
  }else if(written){A.markStatus="self";renderReveal();}
  else{A.markStatus="skipped";await finalize(E.mcqVerdict(A.mcq),"options");}
  renderActionBar();
  const rv=$("#reveal");if(rv)rv.scrollIntoView({behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth",block:"start"});
}
function markKeyOnOptions(q,A){A.mcq.forEach(r=>{if(!r.isMcq)return;$$('.opt[data-n="'+CSS.escape(String(r.n))+'"]').forEach(b=>{const i=+b.dataset.i;b.disabled=true;if(i===r.keyIndex)b.classList.add("isKey");if(i===r.selected&&!r.correct)b.classList.add("isWrongPick");});});}
const ratingOf=(v,easy)=>v==="Wrong"?"Forgot":v==="Partial"?"Partial":(easy?"Easy":"Effort");
async function finalize(verdict,how,easy){
  const A=S.A,q=S.questions[A.qid];if(!verdict){renderReveal();return;}
  const cfg=qCfg(q);A.easy=!!easy;
  const out=E.applyVerdict(A.reviewBefore,verdict,S.today,cfg.exam,{easy:!!easy,finalReview:cfg.frActive});
  const latest=S.reviews[q.id];if(latest&&latest.status==="challenged")out.review.status="challenged";
  A.verdict=verdict;A.verdictHow=how;A.counted=out.counted;A.note=out.note;
  const selected={};A.mcq.forEach(r=>{if(r.isMcq&&r.selected!=null)selected[r.n]=E.LETTERS[r.selected];});
  const marking=A.marking||{verdict,reasoning_judgements:[],error_tags_hit:A.tags,correction:"",legibility:"not_sent",alternative_method_flag:false,alternative_method:"",provisional:!!A.provisional,marked_by:how};
  if(A.marking)marking.error_tags_hit=[...new Set([...(A.marking.error_tags_hit||[]),...A.tags])];
  A.attemptId=A.attemptId||newId();
  const att={question_id:q.id,course:q.course,ts:new Date().toISOString(),selected,typed_reasoning:A.typed||"",sketch_asset:null,marking,override:null,verdict,rating:ratingOf(verdict,easy),counted:out.counted,marked_by:how,seconds:Math.round((A.stopped-A.started)/1000)};
  A.attempt=att;
  if(A.dry){A.saved=false;A.note=(A.note?A.note+" ":"")+"Dry run: nothing was saved.";renderReveal();return;}
  try{const b=await A.sketchPromise;if(b){const sid=await AGStore.putBlob(b,"sk-"+A.attemptId);att.sketch_asset=sid;A.sketch=sid;}}catch(e){A.sketchNote="The sketch could not be saved ("+(e&&(e.code||e.name)||"error")+").";}
  try{await putMany([{coll:"attempts",id:A.attemptId,doc:att},{coll:"reviews",id:q.id,doc:out.review}]);A.saved=true;}catch(e){A.saveError="Not saved: "+(e&&e.message||e);}
  if(S.session&&S.session.ids.includes(q.id))S.session.done=(S.session.done||0)+1;
  renderReveal();renderActionBar();
}
async function overrideVerdict(v,easy){
  const A=S.A,q=S.questions[A.qid];if(!A||!A.submitted||A.markStatus==="running")return;
  if(!A.verdict){await finalize(v,"self",easy);return;}
  const cur=A.override||{verdict:A.verdict,rating:ratingOf(A.verdict,A.easy)};if(v===cur.verdict&&ratingOf(v,easy)===cur.rating)return;
  const cfg=qCfg(q);const out=E.applyVerdict(A.reviewBefore,v,S.today,cfg.exam,{easy:!!easy,finalReview:cfg.frActive});
  const latest=S.reviews[q.id];if(latest&&latest.status==="challenged")out.review.status="challenged";
  A.override={verdict:v,rating:ratingOf(v,easy),note:(v===A.verdict?"Rated ":"Changed from "+A.verdict+" to ")+ratingOf(v,easy)+" on "+S.today};A.counted=out.counted;A.note=out.note;
  if(!A.dry&&A.saved){const att=Object.assign({},S.attempts[A.attemptId],{override:A.override,counted:out.counted,rating:A.override.rating});
    try{await putMany([{coll:"attempts",id:A.attemptId,doc:att},{coll:"reviews",id:q.id,doc:out.review}]);toast("Rated "+A.override.rating+". Schedule updated.");}catch(e){}}
  renderReveal();renderActionBar();
}
function renderReveal(){
  const A=S.A,q=S.questions[A.qid];const el=$("#reveal");if(!el||!q)return;el.hidden=false;
  const final=A.override?A.override.verdict:A.verdict;const neg=negOf(q);const mk=E.marksFor(A.mcq,typeof neg==="number"?neg:null);
  let o='<div class="stack">';
  if(final){o+='<div class="verdict"><span class="big '+final+'">'+final+"</span>"+(A.override?'<span class="pill plain">your rating</span>':{self:'<span class="pill plain">self-marked</span>',options:'<span class="pill plain">from the options</span>',claude:'<span class="pill plain">marked by Claude</span>'}[A.verdictHow]||"")+(A.marking&&A.marking.provisional?'<span class="pill mid">provisional: key unverified</span>':"")+'<span class="small muted">Marks <span class="mono">'+(mk.known?mk.total:"UNKNOWN")+"</span></span></div>";
    o+='<p class="small">'+(A.counted?"Counted for the schedule.":"")+(A.note?" "+h(A.note):"")+(A.saveError?' <span style="color:var(--bad)">'+h(A.saveError)+"</span>":"")+"</p>";}
  else if(A.markStatus==="running")o+='<p class="muted"><span class="spinner" aria-hidden="true"></span> Claude is marking your reasoning. The key is shown above while you wait.</p>';
  else if(A.markStatus==="failed")o+='<div class="notice">'+({rate_limited:"Marking is rate-limited right now. ",auth:"The API key was rejected; check it in Settings. ",network:"Could not reach Claude. ",timeout:"Marking timed out. ",refusal:"Claude declined to mark this. ",not_granted:"Claude marking wasn't allowed in this view. "}[A.markFail]||"Marking failed ("+h(A.markFail)+(A.markMsg?": "+h(A.markMsg):"")+"). ")+"Mark yourself below against the key.</div>";
  else if(A.markStatus==="self")o+='<div class="notice">This question has a written part. Compare your answer with the key and mark scheme below, then rate yourself.</div>';
  o+='<div class="subres">'+A.mcq.map(r=>{const kk=(q.answer_key||[]).find(k=>k.n===r.n)||{};
    if(!r.isMcq)return '<span class="mono">'+h(r.n)+"</span><span>Written · key: "+h(kk.answer||"")+"</span>";
    return '<span class="mono">'+h(r.n)+'</span><span><span class="pill '+(r.correct?"ok":r.answered?"bad":"plain")+'">'+(r.correct?"right":r.answered?"wrong":"blank")+'</span> you chose <span class="mono">'+(r.selected==null?"—":E.LETTERS[r.selected])+'</span> · key <span class="mono">'+(r.keyIndex>=0?E.LETTERS[r.keyIndex]:"?")+'</span> <span class="small muted">('+h(kk.answer_status||"unverified")+")</span></span>";}).join("")+"</div>";
  const m=A.marking;
  if(m&&m.reasoning_judgements&&m.reasoning_judgements.length)o+='<div class="stack"><div class="label">On your reasoning</div>'+m.reasoning_judgements.map(j=>"<div>"+(j.quote?"<blockquote>"+h(j.quote)+"</blockquote>":"")+'<p class="small" style="margin-top:4px">'+h(j.judgement)+"</p></div>").join("")+"</div>";
  if(m&&m.alternative_method_flag)o+='<p class="small"><strong>Alternative method.</strong> '+h(m.alternative_method)+"</p>";
  const tags=[...new Set([...(A.tags||[]),...((m&&m.error_tags_hit)||[])])].filter(Boolean);
  if(tags.length)o+='<div class="row"><span class="label">Trap you fell into</span>'+tags.map(t=>'<span class="pill bad">'+h(t.replace(/_/g," "))+"</span>").join("")+"</div>";
  if(m&&m.correction)o+='<div><div class="label">Correction</div><p>'+h(m.correction)+"</p></div>";
  if((q.mark_scheme||[]).length)o+='<div><div class="label">Mark scheme</div><ul class="md">'+q.mark_scheme.map(b=>"<li>"+E.mdToHtml(b).replace(/^<p>/,"").replace(/<\/p>$/,"")+"</li>").join("")+"</ul></div>";
  if((q.citations||[]).length)o+='<details><summary><span class="label">Sources ('+q.citations.length+')</span></summary><div class="stack">'+q.citations.map(c=>'<div class="cite"><span class="src">'+h(c.deck)+" · slide "+h(c.slide)+"</span><blockquote>"+h(c.quote)+"</blockquote></div>").join("")+"</div></details>";
  const s=q.source||{};o+='<p class="small muted">Source: '+h(s.type||"")+" · "+h(s.file||"")+" "+h(s.location||"")+"</p>";
  if(A.sketchNote)o+='<p class="small" style="color:var(--mid)">'+h(A.sketchNote)+"</p>";
  o+='<p class="small muted">'+(final?"Your rating sets the next gap: Easy gives 4 then 10 days instead of 3 then 7. Forgot and Partial override the marker.":"Rate yourself to record the attempt.")+"</p>";
  o+='<div class="row"><button class="btn sm" data-act="challengeOpen">Report a problem with this question</button><button class="btn sm" data-act="toggleDisable" data-id="'+h(q.id)+'">'+(((S.reviews[q.id]||{}).status==="disabled")?"Enable question":"Disable question")+"</button></div>";
  if(A.challengeOpen)o+='<div class="panel stack" style="background:var(--surface-2)"><label for="challengeNote" class="label">What is wrong with this question?</label><textarea id="challengeNote" placeholder="For example: the key for 3.2 looks wrong because sight deposits were stated as non-repricing."></textarea><div class="row"><button class="btn sm primary" data-act="challengeSend">Save the report</button><span class="small muted">The card leaves the queue until you resolve it from Browse.</span></div></div>';
  if(A.challenged)o+='<p class="small"><span class="pill mid">reported</span> Out of the queue until you resolve it.</p>';
  el.innerHTML=o+"</div>";
}
async function sendChallenge(){
  const A=S.A,q=S.questions[A.qid];const note=($("#challengeNote")||{}).value||"";if(!note.trim()){toast("Add a short note saying what is wrong.");return;}
  const cur=E.normReview(S.reviews[q.id]||{status:"new",due:S.today});cur.status_before_challenge=cur.status==="challenged"?(cur.status_before_challenge||"active"):cur.status;cur.status="challenged";
  const cid=newId();
  try{await putMany([{coll:"challenges",id:cid,doc:{question_id:q.id,note:note.trim(),ts:new Date().toISOString(),resolved:false,resolution:""}},{coll:"reviews",id:q.id,doc:cur}]);A.challenged=true;A.challengeOpen=false;toast("Saved.");}catch(e){}
  renderReveal();
}
async function resolveChallenge(cid){
  const c=S.challenges[cid];if(!c)return;const r=E.normReview(S.reviews[c.question_id]||{});const w=[{coll:"challenges",id:cid,doc:Object.assign({},c,{resolved:true,resolution:"resolved "+S.today})}];
  const others=Object.values(S.challenges).filter(x=>x.question_id===c.question_id&&!x.resolved&&x.id!==cid);
  if(!others.length&&r.status==="challenged"){r.status=r.status_before_challenge||"active";delete r.status_before_challenge;w.push({coll:"reviews",id:c.question_id,doc:r});}
  await putMany(w);toast("Resolved: back in the queue.");render();
}
function nextCard(){
  const A=S.A;if(A&&A.markStatus==="running")return;
  if(A&&A.submitted&&!A.verdict&&!A.dry){toast("Rate yourself first: Forgot, Partial, Effort or Easy (keys 1–4).");return;}
  if(S.session){S.session.idx++;if(S.session.idx<S.session.ids.length){goQuestion(S.session.ids[S.session.idx]);return;}toast("Session finished.");S.session=null;nav("#/queue");return;}
  const Q=queue().filter(x=>!A||x.q.id!==A.qid);if(Q.length)goQuestion(Q[0].q.id);else{toast("That's everything due. Nice work.");nav("#/queue");}
}

/* ---------- course & question actions ---------- */
async function patchCourse(code,patch){const c=Object.assign({},S.courses[code],patch,{updated_at:new Date().toISOString()});await put("courses",code,c);}
async function toggleDisable(id){
  const cur=E.normReview(S.reviews[id]||{status:"new",due:S.today});
  if(cur.status==="disabled"){cur.status=cur.status_before_disable||"active";delete cur.status_before_disable;}else{cur.status_before_disable=cur.status;cur.status="disabled";}
  await put("reviews",id,cur);toast(cur.status==="disabled"?"Disabled: it stays in the bank but never comes up.":"Enabled again.");
  if(S.screen==="answer")renderReveal();else render();
}
async function sweep(code,deck){
  const ids=Object.values(S.questions).filter(q=>q.course===code&&(!deck||q.deck===deck)&&(S.reviews[q.id]||{}).status==="archived").map(q=>q.id);
  if(!ids.length){toast("No archived cards to bring back yet.");return;}
  await putMany(ids.map(id=>{const r=E.normReview(S.reviews[id]);r.sweep=true;r.due=S.today;return {coll:"reviews",id,doc:r};}));
  toast(plural(ids.length,"archived card")+" due today.");S.sweepAsk[code]=false;render();
}
async function restore(id){const r=E.normReview(S.reviews[id]);r.status="active";r.streak=0;r.sweep=false;r.due=S.today;r.history.push({date:S.today,verdict:"restored",counted:false});await put("reviews",id,r);toast("Restored: due today.");render();}
async function saveHardReview(form){
  const id=form.dataset.id;const q=S.questions[id];if(!q)return;const fd=new FormData(form);
  const parts=E.answerParts(q).map(n=>{const st=fd.get("steps:"+n),co=fd.get("concepts:"+n);return {n,steps:st===""?null:Number(st),concepts:co===""?null:Number(co)};});
  const hc={shape_class:E.shapeClass(q),parts,notches:fd.getAll("notch"),no_ambiguity:fd.get("no_ambiguity")==="on",in_syllabus:fd.get("in_syllabus")==="on",reviewed_by:"you (in Answer Grid)",reviewed_at:new Date().toISOString()};
  const nq=Object.assign({},q,{hard_check:hc});
  if(fd.get("relabel")==="on"){const trial=E.reviewHarder(Object.assign({},nq,{difficulty:"hard"}),courseOf(q));
    if(trial.status==="pass")nq.difficulty="hard";else toast("Not relabelled: the review does not pass yet.",4000);}
  await put("questions",id,nq);const g=guardOf(nq);toast(g.status==="pass"?"Review saved: meets the harder rule.":"Review saved: "+g.summary+".");render();
}
function bundle(code){
  const qs=Object.values(S.questions).filter(q=>!code||q.course===code);const ids=new Set(qs.map(q=>q.id));
  return {app:"answer-grid",format:1,exported_at:new Date().toISOString(),course:code||"all",courses:Object.values(S.courses).filter(c=>!code||c.code===code),questions:qs,
    reviews:Object.values(S.reviews).filter(r=>ids.has(r.id)),attempts:Object.values(S.attempts).filter(a=>ids.has(a.question_id)),challenges:Object.values(S.challenges).filter(c=>ids.has(c.question_id))};
}
function mistakesMd(code){
  const lines=[];
  Object.values(S.attempts).filter(a=>!code||(S.questions[a.question_id]||{}).course===code).sort((a,b)=>String(a.ts).localeCompare(String(b.ts))).forEach(a=>{
    const v=attemptVerdict(a);if(v!=="Wrong"&&v!=="Partial")return;const q=S.questions[a.question_id]||{};const m=a.marking||{};
    lines.push("| "+a.question_id+" | "+String(q.topic||"").replace(/\|/g,"/")+" | "+v+" | "+(((m.error_tags_hit||[]).join(", "))||"—")+" | "+String(m.correction||"—").replace(/\|/g,"/")+" | "+E.fmtDMY(tsRomeDate(a.ts))+" |");});
  const leeches=Object.values(S.questions).filter(q=>(!code||q.course===code)&&E.isLeech(S.reviews[q.id])).map(q=>"- "+q.id+" · "+(q.topic||"")+" · "+S.reviews[q.id].lapses+" lapses");
  return "# Mistakes"+(code?" · "+code:"")+" · "+E.fmtDMY(S.today)+"\n\n| Question | Topic | Verdict | Trap | Correction | Date |\n|---|---|---|---|---|---|\n"+(lines.join("\n")||"| — | No mistakes recorded | | | | |")+"\n"+(leeches.length?"\n## Leeches (4+ lapses)\n\n"+leeches.join("\n")+"\n":"");
}
async function closeCourse(code){
  const cl=S.closing[code];const typed=(($("#closeCode-"+CSS.escape(code))||{}).value||"").trim();cl.typed=typed;
  if(!cl.backedUp){toast("Download the backup first.");render();return;}
  if(typed!==code){toast("Type "+code+" to confirm.");render();return;}
  const b=bundle(code);cl.running=true;render();
  const w=[...b.attempts.map(a=>({coll:"attempts",id:a.id,doc:null})),...b.challenges.map(c=>({coll:"challenges",id:c.id,doc:null})),...b.reviews.map(r=>({coll:"reviews",id:r.id,doc:null})),...b.questions.map(q=>({coll:"questions",id:q.id,doc:null}))];
  try{await putMany(w);for(const a of b.attempts)if(a.sketch_asset)try{await AGStore.delBlob(a.sketch_asset);}catch(e){}
    await patchCourse(code,{status:"closed",closed_at:new Date().toISOString(),closed_summary:{questions:b.questions.length,attempts:b.attempts.length}});delete S.closing[code];toast(code+" closed.");}
  catch(e){cl.running=false;cl.msg="Some deletions failed. Try again.";}
  render();
}
async function mergeSeed(silent){
  const seed=window.AG_SEED;if(!seed){if(!silent)toast("No bundled bank found.");return 0;}
  const w=[];
  Object.entries(seed.courses||{}).forEach(([id,c])=>{if(!S.courses[id])w.push({coll:"courses",id,doc:c});});
  Object.entries(seed.questions||{}).forEach(([id,q])=>{if(!S.questions[id])w.push({coll:"questions",id,doc:q});});
  const haveQ=new Set([...Object.keys(S.questions),...w.filter(x=>x.coll==="questions").map(x=>x.id)]);
  ["reviews","attempts","challenges"].forEach(c=>Object.entries(seed[c]||{}).forEach(([id,d])=>{if(!S[c][id]&&(c!=="reviews"||!S.reviews[id]))w.push({coll:c,id,doc:d});}));
  await putMany(w);const n=w.filter(x=>x.coll==="questions").length;
  if(!silent)toast(n?plural(n,"question")+" added from the bundled bank.":"You already have every bundled question.");
  return n;
}

/* ---------- export dialog ---------- */
function openExport(ids,title,opts){
  const uniq=[...new Set(ids)].filter(id=>S.questions[id]);
  if(!uniq.length){toast("Nothing to export here yet.");return;}
  S.ex=Object.assign({ids:uniq,title,only:"attempted",attempts:"all",key:true,sources:true,sketches:true,format:"md"},opts||{});renderExport();
  if(!DLG.open)DLG.showModal();
}
function exItems(ex){
  const qs=ex.ids.map(id=>S.questions[id]).filter(Boolean);
  let items=qs.map(q=>{let atts=attemptsOf(q.id);if(ex.attempts==="today")atts=atts.filter(a=>tsRomeDate(a.ts)===S.today);return {q,atts};});
  if(ex.only==="attempted")items=items.filter(x=>x.atts.length);
  return items;
}
function renderExport(){
  const ex=S.ex;const items=exItems(ex);const nAtt=items.reduce((n,x)=>n+x.atts.length,0);const total=ex.ids.length;
  const radio=(name,val,label,hint)=>'<label class="choice"><input type="radio" name="'+name+'" value="'+val+'"'+(ex[name]===val?" checked":"")+"> <span><b>"+label+"</b>"+(hint?'<br><span class="small muted">'+hint+"</span>":"")+"</span></label>";
  const check=(name,label)=>'<label class="small"><input type="checkbox" name="'+name+'"'+(ex[name]?" checked":"")+"> "+label+"</label>";
  const fmt=[["md","Markdown (.md)","One readable file: questions, your answers, feedback, key"],["print",ART()?"Printable page (.html)":"Print or save as PDF",ART()?"Formatted pages with your sketches. Open the file and print it or save it as a PDF.":"Formatted pages, with your sketches"],["zip","Folder (.zip)","One Markdown file per question, plus sketches and an index"],["csv","Spreadsheet (.csv)","One row per attempt"],["json","Data (.json)","Re-importable into Answer Grid"]];
  DLG.innerHTML='<form method="dialog" class="stack" id="exForm"><div class="row between"><div><div class="label">Export</div><h2>'+h(ex.title)+'</h2></div><button class="btn sm ghost" value="cancel" aria-label="Close">✕</button></div>'+
    '<p class="small"><b class="num">'+items.length+"</b> of "+total+" question"+(total===1?"":"s")+" · <b class=\"num\">"+nAtt+"</b> attempt"+(nAtt===1?"":"s")+"</p>"+
    '<fieldset><legend class="label">Questions</legend><div class="choices">'+radio("only","attempted","Only ones I've attempted")+radio("only","all","Everything selected","Unattempted questions are listed without answers")+"</div></fieldset>"+
    '<fieldset><legend class="label">Attempts</legend><div class="choices">'+radio("attempts","all","All attempts")+radio("attempts","latest","Latest only")+radio("attempts","today","Today's only")+radio("attempts","none","None (questions only)")+"</div></fieldset>"+
    '<fieldset><legend class="label">Include</legend><div class="row">'+check("key","Answer key and mark scheme")+check("sources","Slide sources")+check("sketches","Sketches (print and folder)")+"</div></fieldset>"+
    '<fieldset><legend class="label">Format</legend><div class="choices">'+fmt.map(([v,l,hint])=>radio("format",v,l,hint)).join("")+"</div></fieldset>"+
    '<div class="row between"><span class="small muted" id="exMsg"></span><span class="row">'+(ex.format==="md"?'<button class="btn" type="button" data-act="exCopy"'+(items.length?"":" disabled")+">Copy</button>":"")+'<button class="btn primary" type="button" data-act="exGo"'+(items.length?"":" disabled")+">"+(ex.format==="print"&&!ART()?"Open print view":"Download")+"</button></span></div></form>";
}
async function sketchMap(items,asDataUrl){
  const m={};for(const {atts} of items)for(const a of atts)if(a.sketch_asset){const b=await AGStore.getBlob(a.sketch_asset);if(b)m[a.id]=asDataUrl?await blobToDataUrl(b):b;}return m;
}
async function runExport(copyOnly){
  const ex=S.ex;const items=exItems(ex);if(!items.length)return;
  const opts={attempts:ex.attempts==="today"?"all":ex.attempts,key:ex.key,sources:ex.sources};
  const base=E.safeName(ex.title)+"-"+S.today;
  let ok=true;
  if(ex.format==="md"){const md=E.exportMarkdown(ex.title,items,opts);if(copyOnly){copyText(md);return;}ok=await download(base+".md",md,"text/markdown;charset=utf-8");}
  else if(ex.format==="csv")ok=await download(base+".csv",E.exportCsv(items),"text/csv;charset=utf-8");
  else if(ex.format==="json"){const ids=new Set(items.map(x=>x.q.id));const courses=[...new Set(items.map(x=>x.q.course))].map(c=>S.courses[c]).filter(Boolean);
    ok=await download(base+".json",JSON.stringify({app:"answer-grid",format:1,exported_at:new Date().toISOString(),title:ex.title,courses,questions:items.map(x=>x.q),reviews:Object.values(S.reviews).filter(r=>ids.has(r.id)),attempts:items.flatMap(x=>x.atts),challenges:Object.values(S.challenges).filter(c=>ids.has(c.question_id))},null,2),"application/json");}
  else if(ex.format==="zip"){
    const sk=ex.sketches?await sketchMap(items,false):{};const files=[];const folder=E.safeName(ex.title);
    files.push({name:folder+"/README.md",data:E.exportMarkdown(ex.title,items,Object.assign({},opts,{attempts:"none",key:false,sources:false})).replace(/\n---\n[\s\S]*$/,"\n")+"\nEach question is in `questions/`, sketches in `sketches/`.\n"});
    items.forEach(({q,atts})=>files.push({name:folder+"/questions/"+E.safeName(q.id)+".md",data:E.questionMarkdown(q,atts,Object.assign({},opts,{sketchPath:a=>sk[a.id]?"../sketches/"+E.safeName(a.id)+".png":null}))}));
    for(const [id,b] of Object.entries(sk))files.push({name:folder+"/sketches/"+E.safeName(id)+".png",data:new Uint8Array(await b.arrayBuffer())});
    ok=await download(base+".zip",new Blob([E.zipStore(files)],{type:"application/zip"}));}
  else if(ex.format==="print"){const html=printHtml(ex.title,items,opts,ex.sketches?await sketchMap(items,true):{});if(!ART()){openPrint(html);return;}ok=await download(base+".html",html,"text/html;charset=utf-8");}
  if(ok&&!copyOnly){if(DLG.open)DLG.close();toast("Exported "+plural(items.length,"question")+".");}
}
function printHtml(title,items,o,sk){
  const css="body{font:11pt/1.5 'IBM Plex Sans',system-ui,sans-serif;color:#152033;max-width:760px;margin:24px auto;padding:0 16px}h1{font-size:18pt;margin:0 0 4px}h2{font-size:13pt;margin:0}h3{font-size:10pt;text-transform:uppercase;letter-spacing:.06em;color:#5a6679;margin:14px 0 4px}.q{border-top:2px solid #152033;padding-top:12px;margin-top:22px;break-inside:auto}.meta{color:#5a6679;font-size:9pt}table{border-collapse:collapse;margin:6px 0;font-size:9.5pt}td,th{border:1px solid #c9d1dc;padding:3px 8px;text-align:left;vertical-align:top}th{background:#f1f4f8}ol.opts{margin:4px 0 8px;padding-left:1.6em}ol.opts li.key{font-weight:600}ol.opts li.key::after{content:'  ✓ key';color:#17804f;font-weight:600}.att{border:1px solid #d5dbe4;border-radius:8px;padding:8px 12px;margin:8px 0;break-inside:avoid}.Correct{color:#17804f}.Partial{color:#a86a0c}.Wrong{color:#b73232}.pre{white-space:pre-wrap}img{max-width:100%;border:1px solid #d5dbe4;border-radius:6px}blockquote{margin:4px 0;padding:2px 10px;border-left:3px solid #2446c7;color:#333}.summary td:nth-child(n+3){white-space:nowrap}@media print{body{margin:0}.noprint{display:none}}";
  const keyBy=q=>{const m={};(q.answer_key||[]).forEach(k=>m[k.n]=k);return m;};
  let b='<h1>'+h(title)+'</h1><p class="meta">Exported '+h(E.tsLabel(new Date().toISOString()))+" · "+plural(items.length,"question")+'</p><p class="noprint"><button onclick="print()">Print / Save as PDF</button></p>';
  if(items.length>1)b+='<table class="summary"><thead><tr><th>Question</th><th>Topic</th><th>Attempts</th><th>Latest</th><th>Best</th></tr></thead><tbody>'+items.map(({q,atts})=>{const r=E.summaryRow(q,atts);return "<tr><td>"+h(r.id)+"</td><td>"+h(r.topic)+"</td><td>"+r.attempts+'</td><td class="'+h(r.last)+'">'+h(r.last)+"</td><td>"+h(r.best)+"</td></tr>";}).join("")+"</tbody></table>";
  items.forEach(({q,atts})=>{const kb=keyBy(q);const list=o.attempts==="none"?[]:o.attempts==="latest"?atts.slice(-1):atts;
    b+='<section class="q"><h2>'+h(q.id)+" · "+h(q.topic||"")+'</h2><p class="meta">'+h([q.course+" · deck "+q.deck,q.shape,q.difficulty==="hard"?"Hard":q.difficulty,(q.source||{}).type,Array.isArray(q.slides)&&q.slides.length?"slides "+E.slideRanges(q.slides):""].filter(Boolean).join(" · "))+"</p>"+E.mdToHtml(q.stem)+(q.data?E.mdToHtml(q.data):"");
    (q.subquestions||[]).forEach(s=>{const isM=Array.isArray(s.options)&&s.options.length;const ki=isM?E.keyIndex(s,kb[s.n]):-1;
      b+="<p><b>"+h(s.n)+"</b> "+E.mdToHtml(s.prompt).replace(/^<p>|<\/p>$/g,"")+"</p>"+(isM?'<ol class="opts" type="A">'+s.options.map((op,i)=>"<li"+(o.key&&i===ki?' class="key"':"")+">"+E.mdToHtml(op).replace(/^<p>|<\/p>$/g,"")+"</li>").join("")+"</ol>":"");});
    if(o.attempts!=="none"){b+="<h3>Your attempts</h3>"+(list.length?"":"<p><i>Not attempted yet.</i></p>");
      list.forEach((a,i)=>{const v=E.verdictOf(a)||"unmarked";const m=a.marking||{};const n=o.attempts==="latest"?atts.length:i+1;
        const mcq=(q.subquestions||[]).filter(s=>Array.isArray(s.options)&&s.options.length);
        b+='<div class="att"><b>Attempt '+n+'</b> · <span class="meta">'+h(E.tsLabel(a.ts))+'</span> · <b class="'+h(v)+'">'+h(v)+"</b>"+(a.override?' <span class="meta">(rated '+h(a.override.rating||"")+")</span>":"");
        if(mcq.length)b+="<table><tr><th>Part</th><th>You chose</th>"+(o.key?"<th>Key</th>":"")+"</tr>"+mcq.map(s=>{const sel=(a.selected||{})[s.n];const ki=E.keyIndex(s,kb[s.n]);const k=ki>=0?E.LETTERS[ki]:"?";return "<tr><td>"+h(s.n)+'</td><td class="'+(o.key?(sel===k?"Correct":"Wrong"):"")+'">'+h(sel||"—")+"</td>"+(o.key?"<td>"+k+"</td>":"")+"</tr>";}).join("")+"</table>";
        if(a.typed_reasoning)b+='<p class="pre">'+h(a.typed_reasoning)+"</p>";
        if(Array.isArray(m.reasoning_judgements))m.reasoning_judgements.forEach(j=>{b+=(j.quote?"<blockquote>"+h(j.quote)+"</blockquote>":"")+"<p>"+h(j.judgement)+"</p>";});
        if(m.correction)b+="<p><b>Correction.</b> "+h(m.correction)+"</p>";
        if((m.error_tags_hit||[]).length)b+="<p><b>Traps:</b> "+h(m.error_tags_hit.join(", ").replace(/_/g," "))+"</p>";
        if(sk[a.id])b+='<img alt="Working" src="'+sk[a.id]+'">';
        b+="</div>";});}
    if(o.key){b+="<h3>Answer key</h3><ul>"+(q.subquestions||[]).map(s=>{const k=kb[s.n];if(!k)return "";const isM=Array.isArray(s.options)&&s.options.length;const ki=isM?E.keyIndex(s,k):-1;return "<li><b>"+h(s.n)+"</b> "+(isM?(ki>=0?E.LETTERS[ki]+". "+h(s.options[ki]):h(k.answer)):h(k.answer))+' <span class="meta">('+h(k.answer_status||"")+")</span></li>";}).join("")+"</ul>";
      if((q.mark_scheme||[]).length)b+="<h3>Mark scheme</h3><ul>"+q.mark_scheme.map(x=>"<li>"+E.mdToHtml(x).replace(/^<p>|<\/p>$/g,"")+"</li>").join("")+"</ul>";}
    if(o.sources&&(q.citations||[]).length)b+="<h3>Sources</h3><ul>"+q.citations.map(c=>"<li>"+h(c.deck)+" · slide "+h(c.slide)+": “"+h(c.quote)+"”</li>").join("")+"</ul>";
    b+="</section>";});
  return '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>'+h(title)+"</title><style>"+css+"</style></head><body>"+b+"</body></html>";
}
async function openPrint(html){
  const w=window.open("","_blank");
  if(w){w.document.open();w.document.write(html);w.document.close();setTimeout(()=>{try{w.focus();w.print();}catch(e){}},400);DLG.close();}
  else{await download(E.safeName(S.ex.title)+".html",html,"text/html;charset=utf-8");DLG.close();toast("Pop-up blocked: saved as an HTML file instead. Open it and print.",5000);}
}

/* ---------- events ---------- */
document.addEventListener("change",e=>{
  const t=e.target;
  if(t.dataset&&t.dataset.filter&&t.tagName==="SELECT"){S.browse[t.dataset.filter]=t.value;if(t.dataset.filter==="course"){S.browse.deck="";S.browse.topic="";}render();}
  if(t.id==="statsCourse"){S.statsCourse=t.value;render();}
  if(t.id==="importFile"&&t.files&&t.files[0])readImportFile(t.files[0]);
  if(t.dataset&&t.dataset.sel!=null){if(t.checked)S.sel.add(t.dataset.sel);else S.sel.delete(t.dataset.sel);renderSelBar();}
  if(t.form&&t.form.id==="exForm"){const ex=S.ex;if(t.type==="radio")ex[t.name]=t.value;else if(t.type==="checkbox")ex[t.name]=t.checked;renderExport();}
});
let searchT=0;
document.addEventListener("input",e=>{const t=e.target;
  if(t.classList&&t.classList.contains("parttyped")&&S.A&&!S.A.submitted){const q=S.questions[S.A.qid];S.A.typedBy=S.A.typedBy||{};S.A.typedBy[t.dataset.part]=t.value;S.A.typed=E.composeTyped(q,S.A.typedBy);clearTimeout(saveDraft._t);saveDraft._t=setTimeout(saveDraft,400);}
  if(t.dataset&&t.dataset.filter==="q"){S.browse.q=t.value;clearTimeout(searchT);searchT=setTimeout(()=>{const pos=t.selectionStart;render();const n=$('input[data-filter="q"]');if(n){n.focus();try{n.setSelectionRange(pos,pos);}catch(_){}}},200);}
  if(t.id&&t.id.startsWith("closeCode-")){const c=t.id.slice(10);if(S.closing[c])S.closing[c].typed=t.value;}
});
document.addEventListener("submit",e=>{const f=e.target;if(f.classList.contains("hardform")){e.preventDefault();saveHardReview(f);}});
function readImportFile(f){const fr=new FileReader();fr.onload=()=>{S.importText=String(fr.result||"");const ta=$("#importText");if(ta)ta.value=S.importText;S.importPreview=checkImport(S.importText);render();};fr.readAsText(f);}
document.addEventListener("dragover",e=>{if(S.screen==="import"){e.preventDefault();const d=$("#drop");if(d)d.classList.add("over");}});
document.addEventListener("dragleave",e=>{const d=$("#drop");if(d&&e.target===d)d.classList.remove("over");});
document.addEventListener("drop",e=>{if(S.screen!=="import")return;e.preventDefault();const f=e.dataTransfer&&e.dataTransfer.files&&e.dataTransfer.files[0];if(f)readImportFile(f);});

document.addEventListener("click",async e=>{
  const b=e.target.closest("[data-act]");if(!b||b.disabled)return;const act=b.dataset.act,A=S.A;
  switch(act){
    case "open":goQuestion(b.dataset.id);break;
    case "pick":pick(b.dataset.n,+b.dataset.i);break;
    case "submit":submitAnswer();break;
    case "discardDraft":clearDraft(A.qid);openQuestion(A.qid);renderAnswer();break;
    case "timer":A.timerOn=!A.timerOn;$("#timer").hidden=!A.timerOn;b.textContent=A.timerOn?"Hide timer":"Timer";break;
    case "tool":A.tool=b.dataset.tool;$$('[data-act="tool"]').forEach(x=>x.setAttribute("aria-pressed",String(x.dataset.tool===A.tool)));break;
    case "undo":A.strokes.pop();redraw();break;
    case "clearPad":A.strokes=[];redraw();break;
    case "fullPad":A.full=!A.full;$("#sketch").classList.toggle("full",A.full);b.textContent=A.full?"Done":"Expand";sizePad();break;
    case "rate":overrideVerdict(b.dataset.v,b.dataset.easy==="1");break;
    case "next":nextCard();break;
    case "exportCurrent":openExport([A.qid],A.qid+" · "+(S.questions[A.qid].topic||""),{attempts:"all"});break;
    case "challengeOpen":A.challengeOpen=!A.challengeOpen;renderReveal();break;
    case "challengeSend":sendChallenge();break;
    case "resolveChallenge":resolveChallenge(b.dataset.cid);break;
    case "toggleDisable":toggleDisable(b.dataset.id);break;
    case "detail":S.detail=S.detail===b.dataset.id?null:b.dataset.id;render();break;
    case "restore":restore(b.dataset.id);break;
    case "practiseSubject":S.queueSubject=b.dataset.course;S.queueDeck=null;nav("#/queue");break;
    case "practiseDeck":S.queueDeck=b.dataset.course+"|"+b.dataset.deck;S.queueSubject=null;nav("#/queue");break;
    case "allDecks":S.queueDeck=null;S.queueSubject=null;render();break;
    case "sessionAll":case "sessionDry":{const list=Object.values(S.questions).filter(q=>q.course===b.dataset.course&&q.deck===b.dataset.deck&&!["disabled","challenged"].includes((S.reviews[q.id]||{}).status)).sort(E.newOrder);
      if(!list.length){toast("No questions in this deck.");break;}
      S.session={ids:list.map(q=>q.id),idx:0,record:act==="sessionAll",label:deckTitle(b.dataset.course,b.dataset.deck)+(act==="sessionAll"?" · slide order":" · dry run")};goQuestion(S.session.ids[0]);break;}
    case "endSession":S.session=null;render();break;
    case "resumeSession":if(S.session)goQuestion(S.session.ids[Math.min(S.session.idx,S.session.ids.length-1)]);break;
    case "saveExam":{const v=($("#exam-"+CSS.escape(b.dataset.code))||{}).value||"";await patchCourse(b.dataset.code,{exam_date:v||null});toast("Exam date saved.");render();break;}
    case "saveSubject":{const code=b.dataset.code;const v=id=>(document.getElementById(id)||{}).value||"";const fr=v("sfr-"+code);const off=[0,1,2,3,4,5,6].filter(d=>(document.getElementById("sday-"+code+"-"+d)||{}).checked);
      await patchCourse(code,{priority:v("sprio-"+code)||"none",final_review_days:fr==="off"?"off":Number(fr),study_days_off:off});toast("Plan settings saved.");render();break;}
    case "saveDeck":{const {course,deck}=b.dataset;const v=id=>(document.getElementById(id)||{}).value||"";const ex=v("dexam-"+deck),pr=v("dprio-"+deck),fr=v("dfr-"+deck);const c=S.courses[course]||{code:course};
      const decks=Object.assign({},c.decks||{});decks[deck]=Object.assign({},decks[deck]||{},{exam_date:ex||null,priority:pr||null,final_review_days:fr===""?null:(fr==="off"?"off":Number(fr))});await patchCourse(course,{decks});toast("Deck settings saved.");render();break;}
    case "sweepDeck":sweep(b.dataset.course,b.dataset.deck);break;
    case "sweepAsk":S.sweepAsk[b.dataset.code]=true;render();break;
    case "sweepCancel":S.sweepAsk[b.dataset.code]=false;render();break;
    case "sweepDo":sweep(b.dataset.code);break;
    case "closeStart":S.closing[b.dataset.code]=S.closing[b.dataset.code]||{};render();break;
    case "closeCancel":delete S.closing[b.dataset.code];render();break;
    case "closeBackup":{const c=b.dataset.code;if(await download(c+"-backup-"+S.today+".json",JSON.stringify(bundle(c),null,2),"application/json"))S.closing[c].backedUp=true;render();break;}
    case "closeDo":closeCourse(b.dataset.code);break;
    case "reopen":await patchCourse(b.dataset.code,{status:"active"});toast("Reopened. Restore its questions from the backup file in Import.");render();break;
    case "selSet":{const ids=(b.dataset.ids||"").split(",").filter(Boolean);ids.forEach(id=>S.sel.add(id));$$("input[data-sel]").forEach(x=>x.checked=S.sel.has(x.dataset.sel));renderSelBar();if(!ids.length)toast("Nothing to select.");break;}
    case "selClear":S.sel.clear();$$("input[data-sel]").forEach(x=>x.checked=false);renderSelBar();render();break;
    case "exportSel":openExport([...S.sel].sort((a,b)=>E.newOrder(S.questions[a],S.questions[b])),plural(S.sel.size,"selected question"));break;
    case "exportOne":openExport([b.dataset.id],b.dataset.id+" · "+(S.questions[b.dataset.id].topic||""),{only:"all"});break;
    case "exportDeck":{const {course,deck}=b.dataset;openExport(Object.values(S.questions).filter(q=>q.course===course&&q.deck===deck).sort(E.newOrder).map(q=>q.id),deckTitle(course,deck));break;}
    case "exportSubject":case "exportCourse":{const code=b.dataset.course||b.dataset.code;openExport(Object.values(S.questions).filter(q=>q.course===code).sort(E.newOrder).map(q=>q.id),subjectName(code));break;}
    case "exportToday":{const ids=[...new Set(Object.values(S.attempts).filter(a=>tsRomeDate(a.ts)===S.today).map(a=>a.question_id))].filter(id=>S.questions[id]).sort((a,b)=>E.newOrder(S.questions[a],S.questions[b]));openExport(ids,"Session "+E.fmtDMY(S.today),{attempts:"today"});break;}
    case "exAll":openExport(Object.values(S.questions).sort(E.newOrder).map(q=>q.id),"All attempted questions");break;
    case "exGo":runExport(false);break;
    case "exCopy":runExport(true);break;
    case "exMistakes":download("mistakes-"+S.today+".md",mistakesMd(""),"text/markdown;charset=utf-8");break;
    case "backupAll":download("answer-grid-backup-"+S.today+".json",JSON.stringify(bundle(""),null,2),"application/json");break;
    case "mergeSeed":await mergeSeed(false);render();break;
    case "eraseAll":if((($("#eraseConfirm")||{}).value||"").trim()!=="ERASE"){toast("Type ERASE to confirm.");break;}
      await AGStore.wipe();COLLS.forEach(c=>S[c]={});S.sel.clear();S.settings.seedMerged=true;saveSettings();toast("Erased. Add the bundled bank or import a backup to start again.",5000);render();break;
    case "theme":S.settings.theme=b.dataset.v;saveSettings();applyTheme();render();break;
    case "guardMode":S.settings.guard=b.dataset.v;saveSettings();render();break;
    case "saveKey":S.settings.apiKey=($("#apiKey").value||"").trim();S.settings.model=$("#apiModel").value;saveSettings();toast(S.settings.apiKey?"Saved. Claude will mark your reasoning.":"Saved.");render();break;
    case "clearKey":S.settings.apiKey="";saveSettings();render();break;
    case "testKey":{const m=$("#keyMsg");m.textContent="Testing…";const r=await callClaude('Mark this as a test. Return verdict "Correct", legibility "not_sent", empty arrays and strings, false booleans.',2000);
      m.textContent=r.ok?"The key works.":({auth:"The key was rejected.",rate_limited:"Rate-limited; try later.",network:"Could not reach api.anthropic.com."}[r.code]||"Failed: "+r.code+(r.msg?" ("+r.msg+")":""));break;}
    case "importCheck":S.importText=$("#importText").value;S.importPreview=checkImport(S.importText);render();break;
    case "importWrite":writeImport();break;
  }
});
DLG.addEventListener("close",()=>{S.ex=null;});

/* keyboard: low-friction answering */
document.addEventListener("keydown",e=>{
  if(DLG.open||e.altKey)return;const t=e.target;const typing=/INPUT|TEXTAREA|SELECT/.test(t.tagName)||t.isContentEditable;const A=S.A;
  if(S.screen==="answer"&&A&&!A.submitted&&e.key==="Enter"&&(e.metaKey||e.ctrlKey)){e.preventDefault();submitAnswer();return;}
  if(typing){if(e.key==="Escape")t.blur();return;}
  if(e.metaKey||e.ctrlKey)return;
  const k=e.key;
  if(S.screen==="answer"&&A&&S.questions[A.qid]){
    const q=S.questions[A.qid];
    if(!A.submitted){
      const mcq=(q.subquestions||[]).filter(s=>Array.isArray(s.options)&&s.options.length);
      let i=-1;if(/^[a-jA-J]$/.test(k))i=k.toUpperCase().charCodeAt(0)-65;else if(/^[1-9]$/.test(k))i=Number(k)-1;
      if(i>=0&&mcq.length){const cur=mcq.find(s=>String(s.n)===A.cur)||mcq[0];if(i<cur.options.length){e.preventDefault();pick(String(cur.n),i);
        if(A.selected[cur.n]!=null){const nx=mcq[mcq.indexOf(cur)+1];if(nx)setCur(nx.n);}}return;}
      if(k==="Enter"&&!(t.closest&&t.closest("button,a,summary"))){e.preventDefault();submitAnswer();return;}
      if((k==="ArrowDown"||k==="ArrowUp")&&mcq.length>1&&A.cur){const ix=mcq.findIndex(s=>String(s.n)===A.cur);const nx=mcq[Math.max(0,Math.min(mcq.length-1,ix+(k==="ArrowDown"?1:-1)))];if(nx){e.preventDefault();setCur(nx.n);}}
    }else{
      const map={"1":["Wrong",0],"2":["Partial",0],"3":["Correct",0],"4":["Correct",1]};
      if(map[k]){e.preventDefault();overrideVerdict(map[k][0],map[k][1]===1);return;}
      if((k==="Enter"&&!(t.closest&&t.closest("button,a,summary")))||k==="n"){e.preventDefault();nextCard();return;}
      if(k==="e"){e.preventDefault();openExport([A.qid],A.qid+" · "+(q.topic||""),{attempts:"all"});}
    }
    return;
  }
  if(S.screen==="queue"&&k==="Enter"&&!(t.closest&&t.closest("button,a,summary"))){const Q=queue();if(Q.length){e.preventDefault();goQuestion(Q[0].q.id);}}
});

/* ---------- boot ---------- */
async function boot(){
  applyTheme();$("#todayLbl").textContent=fmtDate(S.today);
  const data=await AGStore.init((c,m,err)=>{if(err){S.dbError="Live updates stopped ("+(err.code||"error")+"). Reload the page.";setBanner();return;}S[c]=m;softRender();});
  COLLS.forEach(c=>S[c]=data[c]||{});
  COLLS.forEach(c=>Object.entries(S[c]).forEach(([id,d])=>{if(d&&typeof d==="object")d.id=id;}));
  if(!ART()&&!Object.keys(S.questions).length&&!S.settings.seedMerged){await mergeSeed(true);S.settings.seedMerged=true;saveSettings();}
  S.ready=true;route();
}
boot();
})();
