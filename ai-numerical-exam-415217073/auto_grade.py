"""Automatically compile, execute, inspect Git history, and verify GitHub copies.
Requires Python 3.9+, Git, and gfortran. Uses only the Python standard library.
"""
import argparse,base64,datetime,hashlib,json,os,re,secrets,shlex,shutil,subprocess,tempfile,urllib.request
from pathlib import Path


def command(args,cwd=None,input_text=None):
    try:
        p=subprocess.run([str(x) for x in args],cwd=cwd,input=input_text,text=True,capture_output=True,timeout=40)
        return {'command':[str(x) for x in args],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    except (OSError,subprocess.TimeoutExpired) as e:
        return {'command':[str(x) for x in args],'returncode':None,'stdout':'','stderr':str(e)}


def without_comment(line):
    quote=None; i=0
    while i<len(line):
        c=line[i]
        if quote:
            if c==quote:
                if i+1<len(line) and line[i+1]==quote: i+=1
                else: quote=None
        elif c in "\"'": quote=c
        elif c=='!': return line[:i].rstrip(),line[i+1:]
        i+=1
    return line.rstrip(),''


def run_case(executable,n):
    r=command([executable],input_text=f'{n}\n')
    m=re.search(r'SUM\s*=\s*(\d+)',r['stdout'])
    return {'n':n,'actual':int(m.group(1)) if m else None,'expected':n*(n+1)//2,**r}


def points(q):
    result=[]
    a=q['q1'];sample=a.get('sample',{})
    result.append(a.get('compile',{}).get('returncode')==0 and sample.get('returncode')==0 and type(sample.get('n')) is int and 1<=sample['n']<=10000000 and sample.get('actual')==sample['n']*(sample['n']+1)//2)
    b=q['q2'].get('tests',[])
    result.append(len(b)==3 and len({x.get('n') for x in b})==3 and all(type(x.get('n')) is int and 1<=x['n']<=10000000 and x.get('returncode')==0 and x.get('actual')==x['n']*(x['n']+1)//2 for x in b))
    c=q['q3'];original=c.get('original_source','');annotated=c.get('annotated_source','')
    lines=[x for x in annotated.splitlines() if without_comment(x)[0].strip()]
    stripped=lambda text:[without_comment(x)[0].strip() for x in text.splitlines() if without_comment(x)[0].strip()]
    result.append(bool(original) and bool(lines) and c.get('original_commit')!=c.get('annotated_commit') and c.get('original_commit') in c.get('annotated_parents',[]) and all(without_comment(x)[1].strip() for x in lines) and stripped(original)==stripped(annotated) and c.get('original_compile',{}).get('returncode')==0 and c.get('annotated_compile',{}).get('returncode')==0 and len(c.get('retests',[]))==3 and all(x.get('returncode')==0 and x.get('actual')==x['n']*(x['n']+1)//2 for x in c.get('retests',[])))
    d=q['q4']
    result.append(d.get('source_match') is True and d.get('bundle_match') is True and d.get('http_status')==200)
    return [20 if x else 0 for x in result]


def self_test():
    # Numeric and comment parsing edge cases; actual scoring negative cases.
    assert without_comment("print *, 'a!b' ! explain")==("print *, 'a!b'",' explain')
    assert without_comment('total = total + i ! add')[0]=='total = total + i'
    q={'q1':{'compile':{'returncode':0},'sample':{'returncode':0,'n':10,'actual':55}},'q2':{'tests':[{'n':n,'actual':n*(n+1)//2,'returncode':0} for n in [1,2,3]]},'q3':{},'q4':{}}
    assert points(q)==[20,20,0,0]
    q['q1']['sample']['actual']=54;assert points(q)[0]==0
    q['q2']['tests'][2]['actual']=7;assert points(q)[1]==0
    q['q4']={'source_match':True,'bundle_match':False,'http_status':200};assert points(q)[3]==0
    return True


def github_bytes(repository,path):
    url='https://api.github.com/repos/'+repository+'/contents/'+path+'?ref=main'
    headers={'Accept':'application/vnd.github+json','User-Agent':'Fortran-Exam-Auto-Grader'}
    token=os.environ.get('GITHUB_TOKEN')
    if token: headers['Authorization']='Bearer '+token
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=20) as response:
        data=json.load(response)
    return base64.b64decode(data['content']),data['sha'],url


def main():
    parser=argparse.ArgumentParser(description='Automatically grade the four Fortran/Git achievement tasks.')
    parser.add_argument('--project',default='.')
    parser.add_argument('--github',default='j26366408/Gua')
    parser.add_argument('--prefix',default='ai-numerical-exam-415217073')
    parser.add_argument('--output',default='auto-assessment.json')
    parser.add_argument('--compiler',default=None)
    args=parser.parse_args()
    project=Path(args.project).resolve()
    source=project/'src/sum_to_n.f90'
    if not source.is_file():source=project/'sum_to_n.f90'
    bundle=project/'fortran-history.bundle'
    compiler=args.compiler or shutil.which('gfortran') or shutil.which('gfortran-14')
    flags=shlex.split(os.environ.get('FORTRAN_GRADER_FLAGS',''))
    results={k:{} for k in ['q1','q2','q3','q4']}
    rng=secrets.SystemRandom();ns=rng.sample(range(1,100001),3)
    with tempfile.TemporaryDirectory(prefix='fortran-grader-') as tmp:
        folder=Path(tmp);exe=folder/('sum_to_n.exe' if os.name=='nt' else 'sum_to_n')
        if compiler and source.is_file():
            build=command([compiler,*flags,'-std=f2008','-Wall','-Wextra','-Werror','-fcheck=all','-O2',source,'-o',exe])
            results['q1']={'compile':build,'sample':run_case(exe,10) if build['returncode']==0 else {}}
            results['q2']={'method':'SystemRandom.sample(range(1,100001),3)','tests':[run_case(exe,n) for n in ns] if build['returncode']==0 else []}
        else:results['q1']={'error':'Cannot verify: gfortran or source file is missing.'}
        if shutil.which('git') and bundle.is_file():
            history=folder/'history';cloned=command(['git','clone','--quiet','--branch','main',bundle,history])
            if cloned['returncode']!=0: results['q3']={'error':'Cannot restore Git history.','clone':cloned}
            if cloned['returncode']==0:
                logs=command(['git','log','--reverse','--format=%H','--','src/sum_to_n.f90'],cwd=history)['stdout'].splitlines()
                if len(logs)>=2:
                    first,last=logs[0],logs[-1]
                    raw1=command(['git','show',first+':src/sum_to_n.f90'],cwd=history)['stdout']
                    raw2=command(['git','show',last+':src/sum_to_n.f90'],cwd=history)['stdout']
                    parents=command(['git','show','-s','--format=%P',last],cwd=history)['stdout'].split()
                    original_path=folder/'original.f90';original_path.write_text(raw1,encoding='utf-8')
                    annotated_path=folder/'annotated.f90';annotated_path.write_text(raw2,encoding='utf-8')
                    b1=command([compiler,*flags,'-std=f2008','-O2',original_path,'-o',exe]) if compiler else {}
                    b2=command([compiler,*flags,'-std=f2008','-O2',annotated_path,'-o',exe]) if compiler else {}
                    results['q3']={'original_commit':first,'annotated_commit':last,'annotated_parents':parents,'original_source':raw1,'annotated_source':raw2,'original_compile':b1,'annotated_compile':b2,'retests':[run_case(exe,n) for n in ns] if b2.get('returncode')==0 else [],'bundle_verify':command(['git','bundle','verify',bundle],cwd=history)}
        try:
            cloud_source,source_sha,source_url=github_bytes(args.github,args.prefix+'/src/sum_to_n.f90')
            cloud_bundle,bundle_sha,bundle_url=github_bytes(args.github,args.prefix+'/fortran-history.bundle')
            results['q4']={'repository':args.github,'prefix':args.prefix,'http_status':200,'source_match':cloud_source==source.read_bytes(),'bundle_match':cloud_bundle==bundle.read_bytes(),'source_blob_sha':source_sha,'bundle_blob_sha':bundle_sha,'source_url':source_url,'bundle_url':bundle_url}
        except Exception as error:
            results['q4']={'repository':args.github,'prefix':args.prefix,'error':'Cannot verify GitHub: '+str(error),'http_status':getattr(error,'code',None),'source_match':None,'bundle_match':None}
    self_test();scores=points(results)
    statuses=['passed' if p else ('unverified' if results['q'+str(i+1)].get('error') or (i==2 and not results['q3']) else 'failed') for i,p in enumerate(scores)]
    report={'schema':'fortran-auto-assessment-v1','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results,'scores':scores,'statuses':statuses,'question5':20,'total':sum(scores)+20,'system_self_test':True,'note':'A missing tool, unavailable network or private repository is unverified, not proof the task was never completed.'}
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for i,(score,status) in enumerate(zip(scores,statuses),1):print(f'Q{i}: {score}/20 ({status})')
    print(f'Q5: 20/20 (self-test passed)\nTOTAL: {report["total"]}/100\nReport: {out}')

if __name__=='__main__':main()
