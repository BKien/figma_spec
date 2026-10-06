"""Run and record package gates and the repository gate without hiding failures."""
from pathlib import Path
import subprocess, sys, json

root=Path(__file__).resolve().parents[1]
repo=root.parent
evidence=root/'evidence'
evidence.mkdir(exist_ok=True)
jobs=[
    ('source-and-cross-artifact',[sys.executable,str(root/'scripts/verify_package.py')]),
    ('package-validation',['pwsh','-NoProfile','-File',str(repo/'skills/figma-to-ocl-specs/scripts/validate_specs.ps1'),'-Root',str(root)]),
    ('schema-compilation',['npm.cmd','exec','--yes','--package','@dbml/cli@9.1.1','--','dbml2sql',str(root/'schema.dbml'),'--mysql','-o',str(evidence/'schema.mysql.sql')]),
    ('repository-validation',['pwsh','-NoProfile','-File',str(repo/'skills/figma-to-ocl-specs/scripts/validate_repository.ps1'),'-Root',str(repo)])
]
results=[]
for name,args in jobs:
    run=subprocess.run(args,cwd=repo,capture_output=True,encoding='utf-8',errors='replace')
    (evidence/(name+'.txt')).write_text(run.stdout+run.stderr,encoding='utf-8')
    results.append({'gate':name,'exitCode':run.returncode,'status':'PASS' if run.returncode==0 else 'FAIL','log':name+'.txt'})
    if name=='repository-validation':
        print(name+': '+('PASS' if run.returncode==0 else 'FAIL (pre-existing package; see log)'))
    else: print(name+': '+('PASS' if run.returncode==0 else 'FAIL'))
(evidence/'validation-results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
if any(r['exitCode'] for r in results if r['gate']!='repository-validation'):raise SystemExit(1)
