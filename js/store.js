/* Answer Grid: storage. Two backends behind one interface:
   - "artifact": inside the claude.ai Answer Grid artifact, documents live in its shared database (db capability, the same one
     Cowork writes to) and sketches in its asset store (assets capability).
   - "indexeddb": as a standalone website, everything lives in this browser's IndexedDB. Falls back to "memory" if blocked. */
(function(){
const DB_NAME="answer-grid",DB_VER=1,COLLS=["courses","questions","reviews","attempts","challenges"];
let db=null,cdb=null,assets=null,downloads=null,sample=null,mode="memory";const mem={blobs:{}};COLLS.forEach(c=>mem[c]={});
function req(r){return new Promise((res,rej)=>{r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});}
function openIdb(){
  return new Promise(res=>{
    let r;try{r=indexedDB.open(DB_NAME,DB_VER);}catch(e){return res(null);}
    r.onupgradeneeded=()=>{const d=r.result;[...COLLS,"blobs","meta"].forEach(s=>{if(!d.objectStoreNames.contains(s))d.createObjectStore(s);});};
    r.onsuccess=()=>res(r.result);r.onerror=()=>res(null);r.onblocked=()=>res(null);
  });
}
async function allIdb(store){const tx=db.transaction(store,"readonly"),os=tx.objectStore(store);const [keys,vals]=await Promise.all([req(os.getAllKeys()),req(os.getAll())]);const m={};keys.forEach((k,i)=>m[k]=vals[i]);return m;}
function txDone(tx){return new Promise((a,b)=>{tx.oncomplete=a;tx.onerror=()=>b(tx.error);tx.onabort=()=>b(tx.error);});}
async function retry(fn){for(let i=0;i<4;i++){try{return await fn();}catch(e){const c=e&&e.code;if((c==="resource_exhausted"||c==="unavailable")&&i<3){await new Promise(r=>setTimeout(r,800*(i+1)+Math.random()*400));continue;}throw e;}}}
function use(name){return (window.claude&&typeof window.claude.use==="function")?window.claude.use(name).catch(()=>null):Promise.resolve(null);}
function inArtifact(){return !!(window.claude&&typeof window.claude.use==="function");}

const Store={
  COLLS,
  get mode(){return mode;},
  get downloads(){return downloads;},
  get sample(){return sample;},
  get assets(){return assets;},
  /* onChange(coll, map) is called with live data from the artifact database (Cowork writes arrive this way). */
  async init(onChange){
    if(inArtifact()){
      [cdb,assets,downloads,sample]=await Promise.all(["db","assets","downloads","sample"].map(use));
      if(cdb){
        mode="artifact";const out={};
        await Promise.all(COLLS.map(c=>new Promise(resolve=>{let first=true;
          try{cdb.collection(c).onSnapshot(snap=>{const m={};snap.docs.forEach(d=>{if(d.exists)m[d.id]=Object.assign({},d.data(),{id:d.id});});
              if(first){first=false;out[c]=m;resolve();}else if(onChange)onChange(c,m);},
            err=>{if(first){first=false;out[c]={};resolve();}if(onChange)onChange(c,null,err);});}
          catch(e){out[c]={};resolve();}
        })));
        out.meta={};return out;
      }
    }
    db=await openIdb();mode=db?"indexeddb":"memory";
    if(db&&navigator.storage&&navigator.storage.persist){try{await navigator.storage.persist();}catch(e){}}
    const out={};for(const c of COLLS)out[c]=db?await allIdb(c):{...mem[c]};out.meta=db?await allIdb("meta"):{};return out;
  },
  async put(coll,id,doc){return Store.batch([{coll,id,doc}]);},
  async del(coll,id){return Store.batch([{coll,id,doc:null}]);},
  /* writes: [{coll,id,doc|null}] */
  async batch(writes){
    if(!writes.length)return;
    if(mode==="artifact"){
      const strip=d=>{const o=Object.assign({},d);delete o.id;return o;};
      const jobs=writes.slice();let fail=null;
      const worker=async()=>{while(jobs.length){const w=jobs.shift();try{const ref=cdb.doc(w.coll+"/"+w.id);await retry(()=>w.doc==null?ref.delete():ref.set(strip(w.doc)));}catch(e){fail=fail||e;}}};
      await Promise.all([worker(),worker(),worker()]);if(fail)throw fail;return;
    }
    if(!db){writes.forEach(w=>{if(w.doc==null)delete mem[w.coll][w.id];else mem[w.coll][w.id]=w.doc;});return;}
    const stores=[...new Set(writes.map(w=>w.coll))];const tx=db.transaction(stores,"readwrite");
    writes.forEach(w=>{const os=tx.objectStore(w.coll);if(w.doc==null)os.delete(w.id);else os.put(w.doc,w.id);});
    await txDone(tx);
  },
  /* Stores an image and resolves the id to keep on the attempt. */
  async putBlob(blob,wantedId){
    if(mode==="artifact"){if(!assets)throw Object.assign(new Error("Sketches cannot be saved in this view."),{code:"not_granted"});const r=await assets.upload(blob,{type:"image/png"});return r.id;}
    if(!db){mem.blobs[wantedId]=blob;return wantedId;}
    const tx=db.transaction("blobs","readwrite");tx.objectStore("blobs").put(blob,wantedId);await txDone(tx);return wantedId;
  },
  blobSrc(id){return mode==="artifact"?"/_blob/"+encodeURIComponent(id):null;},
  async getBlob(id){
    if(mode==="artifact"){try{const r=await fetch("/_blob/"+encodeURIComponent(id));return r.ok?await r.blob():null;}catch(e){return null;}}
    if(!db)return mem.blobs[id]||null;const tx=db.transaction("blobs","readonly");return (await req(tx.objectStore("blobs").get(id)))||null;
  },
  async delBlob(id){
    if(mode==="artifact"){if(assets)try{await assets.delete(id);}catch(e){}return;}
    if(!db){delete mem.blobs[id];return;}const tx=db.transaction("blobs","readwrite");tx.objectStore("blobs").delete(id);await txDone(tx);
  },
  async wipe(){
    if(mode==="artifact")throw new Error("Erasing is not available inside the artifact.");
    if(!db){COLLS.forEach(c=>mem[c]={});mem.blobs={};return;}
    const stores=[...COLLS,"blobs","meta"];const tx=db.transaction(stores,"readwrite");stores.forEach(s=>tx.objectStore(s).clear());await txDone(tx);
  }
};
window.AGStore=Store;
})();
