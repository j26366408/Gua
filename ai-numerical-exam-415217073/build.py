"""Compile using installed gfortran, or the unpacked workspace GNU toolchain."""
from pathlib import Path
import json,shutil,subprocess,sys
root=Path(__file__).resolve().parent
compiler=shutil.which('gfortran') or shutil.which('gfortran-14')
extra=[]
if not compiler:
 toolchain=root.parent/'toolchain/root/usr'
 compiler=str(toolchain/'bin/x86_64-linux-gnu-gfortran-14')
 extra=['-B',str(toolchain/'lib/gcc/x86_64-linux-gnu/14')+'/', '-B','/usr/lib/gcc/x86_64-linux-gnu/14/','-L',str(toolchain/'lib/gcc/x86_64-linux-gnu/14')]
(root/'build').mkdir(exist_ok=True)
cmd=[compiler,*extra,'-std=f2008','-Wall','-Wextra','-Werror','-fcheck=all','-O2','src/sum_to_n.f90','-o','build/sum_to_n']
p=subprocess.run(cmd,cwd=root,text=True,capture_output=True)
label=sys.argv[1] if len(sys.argv)>1 else 'build'
version=subprocess.run([compiler,'--version'],text=True,capture_output=True).stdout.splitlines()[0]
report=dict(compiler=version,command=cmd,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
(root/f'evidence/{label}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(version); print('Compile exit:',p.returncode); print(p.stdout+p.stderr,end='')
raise SystemExit(p.returncode)
