(function(){
 const form=document.getElementById('auto-grade-form');if(!form)return;
 let baseline=structuredClone(initialAssessment.results);
 const number=id=>{const s=document.getElementById(id).value.trim();return /^\d+$/.test(s)?Number(s):NaN;};
 const set=(id,value)=>document.getElementById(id).value=String(value);
 function load(results){
  baseline=structuredClone(results);
  set('e-compile',results.q1?.compile?.returncode??'');set('e-sample-n',results.q1?.sample?.n??'');set('e-sample-out',results.q1?.sample?.actual??'');
  for(let i=0;i<3;i++){const t=results.q2?.tests?.[i]||{};set('e-n-'+i,t.n??'');set('e-out-'+i,t.actual??'');set('e-exit-'+i,t.returncode??'');}
  document.getElementById('e-git').value=JSON.stringify(results.q3||{},null,2);
  set('e-repository',results.q4?.repository||'j26366408/Gua');
 }
 function entered(){
  const r=structuredClone(baseline);
  r.q1={compile:{returncode:number('e-compile')},sample:{n:number('e-sample-n'),actual:number('e-sample-out'),returncode:0}};
  r.q2={tests:[0,1,2].map(i=>({n:number('e-n-'+i),actual:number('e-out-'+i),returncode:number('e-exit-'+i)}))};
  try{r.q3=JSON.parse(document.getElementById('e-git').value);}catch(e){r.q3={error:'第三題的 Git 結果不是有效的 JSON。'};}
  r.q4={...baseline.q4,repository:document.getElementById('e-repository').value.trim()};return r;
 }
 function render(results,live){
  const g=autoAssessment.judge(results),works=autoAssessment.selfTest();
  const total=works?g.total:g.total-20;
  for(let i=1;i<=4;i++){
   const c=g.checks[i-1];document.getElementById('auto-q'+i+'-score').textContent=c.points+' 分';
   document.getElementById('auto-q'+i+'-reason').textContent=(c.status==='unverified'?'待驗證：':c.passed?'通過：':'未通過：')+c.reason;
   const o=document.getElementById('overview-'+i);if(o)o.textContent=c.points+' 分';
  }
  document.getElementById('auto-q5-score').textContent=(works?20:0)+' 分';
  document.getElementById('auto-total').textContent=total;
  document.getElementById('auto-mode').textContent=live?'本次輸入已重新判定，並已嘗試連線核對 GitHub。':'已依匯入的實測紀錄判定；按下檢查會重新連線 GitHub。';
  const hero=document.getElementById('hero-score');if(hero)hero.textContent=total;
  const o=document.getElementById('overview-5');if(o)o.textContent=(works?20:0)+' 分';
  document.title='江文樺｜415217073｜'+total+'分';
 }
 async function cloudCheck(q){
  const repo=q.repository;
  if(!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repo))return {...q,http_status:null,source_match:null,bundle_match:null,error:'請輸入 owner/repository 格式。'};
  const prefix=q.prefix||'ai-numerical-exam-415217073';
  try{
   const fetchOne=async path=>{
    const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);
    try{const response=await fetch('https://api.github.com/repos/'+repo+'/contents/'+prefix+'/'+path+'?ref=main',{headers:{Accept:'application/vnd.github+json'},signal:controller.signal});if(!response.ok)throw Error('GitHub HTTP '+response.status);return await response.json();}finally{clearTimeout(timer);}
   };
   const [source,bundle]=await Promise.all([fetchOne('src/sum_to_n.f90'),fetchOne('fortran-history.bundle')]);
   return {...q,http_status:200,source_match:source.sha===baseline.q4.source_blob_sha,bundle_match:bundle.sha===baseline.q4.bundle_blob_sha,error:null};
  }catch(e){return {...q,http_status:null,source_match:null,bundle_match:null,error:'無法連線核對：'+e.message+'。這不等於未完成雲端儲存。'};}
 }
 form.addEventListener('submit',async event=>{
  event.preventDefault();const button=document.getElementById('auto-check');button.disabled=true;button.textContent='檢查中…';
  try{const r=entered();r.q4=await cloudCheck(r.q4);render(r,true);}finally{button.disabled=false;button.textContent='檢查輸入並自動評分';}
 });
 document.getElementById('auto-restore').addEventListener('click',()=>{load(initialAssessment.results);render(initialAssessment.results,false);});
 document.getElementById('auto-import').addEventListener('change',async event=>{
  try{
   const file=event.target.files[0];if(!file)return;
   if(file.size>1000000)throw Error('報告檔案超過 1 MB。');
   const report=JSON.parse(await file.text());
   if(report.schema!=='fortran-auto-assessment-v1'||!report.results)throw Error('請選擇 auto_grade.py 產生的 auto-assessment.json。');
   load(report.results);render(report.results,false);document.getElementById('auto-import-message').textContent='已載入報告，分數由本頁重新計算。';
  }catch(e){document.getElementById('auto-import-message').textContent='匯入失敗：'+e.message;}
 });
 load(initialAssessment.results);render(initialAssessment.results,false);
})();
