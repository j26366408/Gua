(function(root) {
  function calculateFromInput(input) {
    const text=String(input).trim();
    if (!/^\d+$/.test(text)) throw new Error('請輸入 1～10,000,000 的整數，不接受小數或其他文字。');
    const n=Number(text);
    if (!Number.isSafeInteger(n) || n<1 || n>10000000) throw new Error('N 必須介於 1 與 10,000,000 之間。');
    let total=0;
    for (let i=1;i<=n;i++) total+=i;
    const expected=n*(n+1)/2;
    return {n,total,expected,passed:total===expected};
  }
  function randomThree(cryptoProvider) {
    const limit=100000, ceiling=Math.floor(4294967296/limit)*limit;
    const values=new Set();
    while(values.size<3){
      const bytes=new Uint32Array(1);cryptoProvider.getRandomValues(bytes);
      if(bytes[0]<ceiling) values.add(bytes[0]%limit+1);
    }
    return Array.from(values);
  }
  root.examCalculator={calculateFromInput,randomThree};
  if(typeof module!=='undefined' && module.exports) module.exports=root.examCalculator;
})(typeof window!=='undefined'?window:globalThis);
