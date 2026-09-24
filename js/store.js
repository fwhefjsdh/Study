/* Answer Grid: local storage. Everything lives in this browser's IndexedDB (documents + sketch images).
   If IndexedDB is unavailable (some private windows), it falls back to memory and says so. */
(function(){
const DB_NAME="answer-grid",DB_VER=1,COLLS=["courses","questions","reviews","attempts","challenges"];
let db=null,mode="memory";const mem={blobs:{}};COLLS.forEach(c=>mem[c]={});
function req(r){return new Promise((res,rej)=>{r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});}
function open(){
  return new Promise(res=>{
    let r;try{r=indexedDB.open(DB_NAME,DB_VER);}catch(e){return res(null);}
    r.onupgradeneeded=()=>{const d=r.result;[...COLLS,"blobs","meta"].forEach(s=>{if(!d.objectStoreNames.contains(s))d.createObjectStore(s);});};
    r.onsuccess=()=>res(r.result);r.onerror=()=>res(null);r.onblocked=()=>res(null);
  });
}
async function all(store){
  const tx=db.transaction(store,"readonly"),os=tx.objectStore(store);
  const [keys,vals]=await Promise.all([req(os.getAllKeys()),req(os.getAll())]);
  const m={};keys.forEach((k,i)=>m[k]=vals[i]);return m;
}
const Store={
  COLLS,
  get mode(){return mode;},
  async init(){
    db=await open();mode=db?"indexeddb":"memory";
    if(db&&navigator.storage&&navigator.storage.persist){try{await navigator.storage.persist();}catch(e){}}
    const out={};
    for(const c of COLLS)out[c]=db?await all(c):{...mem[c]};
    out.meta=db?await all("meta"):{};
    return out;
  },
  async put(coll,id,doc){if(!db){mem[coll][id]=doc;return;}const tx=db.transaction(coll,"readwrite");tx.objectStore(coll).put(doc,id);await new Promise((a,b)=>{tx.oncomplete=a;tx.onerror=()=>b(tx.error);tx.onabort=()=>b(tx.error);});},
  async del(coll,id){if(!db){delete mem[coll][id];return;}const tx=db.transaction(coll,"readwrite");tx.objectStore(coll).delete(id);await new Promise((a,b)=>{tx.oncomplete=a;tx.onerror=()=>b(tx.error);});},
  /* writes: [{coll,id,doc|null}] in one transaction */
  async batch(writes){
    if(!writes.length)return;
    if(!db){writes.forEach(w=>{if(w.doc==null)delete mem[w.coll][w.id];else mem[w.coll][w.id]=w.doc;});return;}
    const stores=[...new Set(writes.map(w=>w.coll))];const tx=db.transaction(stores,"readwrite");
    writes.forEach(w=>{const os=tx.objectStore(w.coll);if(w.doc==null)os.delete(w.id);else os.put(w.doc,w.id);});
    await new Promise((a,b)=>{tx.oncomplete=a;tx.onerror=()=>b(tx.error);tx.onabort=()=>b(tx.error);});
  },
  async putMeta(k,v){return Store.put("meta",k,v);},
  async putBlob(id,blob){if(!db){mem.blobs[id]=blob;return;}return Store.put("blobs",id,blob);},
  async getBlob(id){if(!db)return mem.blobs[id]||null;const tx=db.transaction("blobs","readonly");return (await req(tx.objectStore("blobs").get(id)))||null;},
  async delBlob(id){if(!db){delete mem.blobs[id];return;}return Store.del("blobs",id);},
  async blobIds(){if(!db)return Object.keys(mem.blobs);const tx=db.transaction("blobs","readonly");return req(tx.objectStore("blobs").getAllKeys());},
  async wipe(){
    if(!db){COLLS.forEach(c=>mem[c]={});mem.blobs={};return;}
    const stores=[...COLLS,"blobs","meta"];const tx=db.transaction(stores,"readwrite");stores.forEach(s=>tx.objectStore(s).clear());
    await new Promise((a,b)=>{tx.oncomplete=a;tx.onerror=()=>b(tx.error);});
  },
  async usage(){try{if(navigator.storage&&navigator.storage.estimate)return await navigator.storage.estimate();}catch(e){}return null;}
};
window.AGStore=Store;
})();
