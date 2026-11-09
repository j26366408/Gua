"""Run the real Fortran executable, compare with an independent arithmetic oracle."""
import json, re, secrets, subprocess
from pathlib import Path
root=Path(__file__).resolve().parent
rng=secrets.SystemRandom()
ns=rng.sample(range(1,100001),3)
rows=[]
for n in ns:
 p=subprocess.run([str(root/'build/sum_to_n')],input=f'{n}\n',text=True,capture_output=True)
 match=re.search(r'SUM = (\d+)',p.stdout)
 actual=int(match.group(1)) if match else None
 expected=n*(n+1)//2
 rows.append(dict(n=n,expected=expected,actual=actual,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,passed=p.returncode==0 and actual==expected))
report={'method':'secrets.SystemRandom.sample(range(1,100001),3); no fixed seed; independent N*(N+1)//2 oracle','tests':rows,'all_passed':all(r['passed'] for r in rows)}
(root/'evidence/random-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for r in rows: print(f"N={r['n']} actual={r['actual']} expected={r['expected']} {'PASS' if r['passed'] else 'FAIL'}")
raise SystemExit(0 if report['all_passed'] else 1)
