(function(root){
 const integer=n=>Number.isSafeInteger(n)&&n>=1&&n<=10000000;
 const caseOK=t=>t&&integer(t.n)&&t.returncode===0&&Number.isSafeInteger(t.actual)&&t.actual===t.n*(t.n+1)/2;
 function splitComment(line){
  let quote=null;
  for(let i=0;i<line.length;i++){
   const c=line[i];
   if(quote){if(c===quote){if(line[i+1]===quote)i++;else quote=null;}}
   else if(c==='"'||c==="'")quote=c;
   else if(c==='!')return [line.slice(0,i).trim(),line.slice(i+1).trim()];
  }
  return [line.trim(),''];
 }
 function judge(results){
  const a=results.q1||{},b=results.q2||{},c=results.q3||{},d=results.q4||{};
  const checks=[];
  const add=(passed,reason,unknown=false)=>checks.push({passed,status:passed?'passed':unknown?'unverified':'failed',points:passed?20:0,reason});
  const first=a.compile?.returncode===0&&caseOK(a.sample);
  add(first,first?`編譯結束碼 0；N=${a.sample.n} 的實際輸出與公式一致。`:'編譯結束碼或實際加總結果未符合條件。',Boolean(a.error));
  const tests=b.tests||[];
  const second=tests.length===3&&new Set(tests.map(t=>t.n)).size===3&&tests.every(caseOK);
  add(second,second?'三組不同 N 的實際結果皆與 N(N+1)/2 一致。':'需要三組不同的有效整數 N，且每組實際結果正確。',Boolean(b.error));
  const originals=String(c.original_source||'').split(/\r?\n/).map(splitComment).filter(t=>t[0]);
  const annotated=String(c.annotated_source||'').split(/\r?\n/).map(splitComment).filter(t=>t[0]);
  const sha=/^[0-9a-f]{40}$/;
  const third=sha.test(c.original_commit||'')&&sha.test(c.annotated_commit||'')&&c.original_commit!==c.annotated_commit&&(c.annotated_parents||[]).includes(c.original_commit)&&originals.length>0&&annotated.length===originals.length&&annotated.every((t,i)=>t[1]&&t[0]===originals[i][0])&&c.original_compile?.returncode===0&&c.annotated_compile?.returncode===0&&(c.retests||[]).length===3&&c.retests.every(caseOK);
  add(third,third?`兩個相連的 Git 版本；${annotated.length} 行全部有註解，程式內容相同，兩版編譯及新版複測成功。`:'版本關係、逐行註解、程式一致性或重新編譯測試未符合條件。',!c.original_commit);
  const fourth=d.http_status===200&&d.source_match===true&&d.bundle_match===true;
  add(fourth,fourth?'GitHub 原始碼及 Git bundle 均與本地端內容一致。':d.error||'GitHub 原始碼或完整版本歷史與預期內容不一致。',Boolean(d.error)||d.http_status==null);
  return {checks,scores:checks.map(x=>x.points),fifth:20,total:checks.reduce((n,x)=>n+x.points,20)};
 }
 function selfTest(){
  const valid={n:10,actual:55,returncode:0};
  if(!caseOK(valid)||caseOK({...valid,actual:54})||caseOK({...valid,n:0})||caseOK({...valid,returncode:1}))return false;
  if(splitComment("print *, 'a!b' ! explain")[0]!=="print *, 'a!b'")return false;
  if(judge({}).total!==20)return false;
  if(judge({q1:{compile:{returncode:0},sample:valid}}).total!==40)return false;
  if(judge({q2:{tests:[valid,valid,valid]}}).scores[1]!==0)return false;
  if(judge({q4:{http_status:200,source_match:true,bundle_match:false}}).scores[3]!==0)return false;
  return true;
 }
 root.autoAssessment={judge,caseOK,splitComment,selfTest};
 if(typeof module!=='undefined'&&module.exports)module.exports=root.autoAssessment;
})(typeof window!=='undefined'?window:globalThis);
