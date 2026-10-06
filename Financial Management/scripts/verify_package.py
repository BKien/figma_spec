"""Check source fidelity and cross-artifact invariants without claiming OCL execution."""
from pathlib import Path
import hashlib, json, re, sys
sys.dont_write_bytecode=True
import build_specs as b

root=b.ROOT
failures=[]
checks=[]
def check(name, condition):
    checks.append({'check':name,'passed':bool(condition)})
    if not condition:failures.append(name)

manifest=json.loads((root/'source/manifest.json').read_text(encoding='utf-8'))
for item in manifest['files']:
    check('Source SHA-256: '+item['path'],hashlib.sha256((root/'source'/item['path']).read_bytes()).hexdigest()==item['sha256'])

sources=b.source_apis()
source_ids={s['sections']['API ID'] for s in sources}
api_paths=list((root/'01-inception/api').glob('api-*.md'))
actual_ids={re.search(r'^# (API-[A-Z-]+)',p.read_text(encoding='utf-8')).group(1) for p in api_paths}
check('All 18 supplied endpoints are present',len(source_ids)==18 and actual_ids==source_ids)
check('18 normalized use cases',len(list((root/'01-inception/uc').glob('uc-*.md')))==18)
check('All source use-case entries accounted for',len([r for r in json.loads((root/'source/use-cases.json').read_text(encoding='utf-8'))['rows'] if r['cells'] and re.match(r'^UC-\d',str(r['cells'][0] or ''))])==17)

expected={'account_type':{'Checking','Credit Card','Savings','Investment','Loan'},
          'status':{'Complete','Pending','Failed'}, 'goal_type':{'Saving','Expense_Limit'}}
for path in api_paths:
    text=path.read_text(encoding='utf-8')
    for field,body in re.findall(r'(?ms)^### `([^`]+)`\s*\n(.*?)(?=^### |^## |\Z)',text):
        enum=re.search(r'^- Allowed values: (.+)',body,re.M)
        if enum and field.rsplit('.',1)[-1] in expected:
            target=expected[field.rsplit('.',1)[-1]]
            if field=='data.savingGoal.goal_type':target={'Saving'}
            check(path.name+' enum '+field,set(enum.group(1).split('; '))==target)
    check(path.name+' body has no domain validation',not re.search(r'^- Validation: .*\b(owner|balance|greater than|non-empty|existing|unique)\b',text,re.M|re.I))

schema=(root/'schema.dbml').read_text(encoding='utf-8')
check('All persistent concepts have tables',all('Table '+name+' {' in schema for name in ['users','accounts','transactions','categories','balance_adjustments','bills','goals']))
check('Only decimal money columns',not re.search(r'\b(balance|amount|target_amount|old_balance|new_balance)\s+(float|double|int)\b',schema,re.I))
check('Protected account number persistence','number_ciphertext varbinary' in schema and 'number_fingerprint binary(32)' in schema and not re.search(r'^\s*account_number_full\s',schema,re.M))
check('Owner-scoped number uniqueness','(user_id, number_fingerprint) [unique' in schema)
check('Goal overlap index is not misrepresented as unique','(user_id, goal_type, category_id, start_date, end_date) [name:' in schema)
for api in ['API-TRANSACTION-CREATE','API-ACCOUNT-UPDATE','API-GOAL-UPDATE']:
    check(api+' version input','### `expected_version`' in (root/'01-inception/api'/b.apifile(api)).read_text(encoding='utf-8'))
check('Delete version header','### `If-Match`' in (root/'01-inception/api/api-account-delete.md').read_text(encoding='utf-8'))

rules=0
for u in b.UCS:
    text=(root/'01-inception/uc'/b.ucfile(u)).read_text(encoding='utf-8')
    blocks=re.findall(r'```ocl\n(.*?)\n```',text,re.S)
    rules+=len(blocks)
    check(b.ucfile(u)+' exact rule set',len(blocks)==len(u['rules']) and len(blocks)>=7)
    check(b.ucfile(u)+' no identity-only frame condition',not re.search(r'(\w+)\.allInstances\(\) = \1\.allInstances\(\)@pre',text))
    # Each block's local receivers are declared with the corresponding field types.
    model=re.search(r'```plantuml\n(.*?)\n```',text,re.S).group(1)
    declared=set(re.findall(r'^(?:class|enum) (\w+) \{',model,re.M))
    primitive={'String','Integer','Real','Boolean','Set','Sequence','Bag','OrderedSet','Tuple'}
    member_lines='\n'.join(line for line in model.splitlines() if line.startswith('  +'))
    type_refs=set(re.findall(r':\s*(\w+)',member_lines))
    check(b.ucfile(u)+' typed local closure',type_refs<=declared|primitive)

check('Rule count matches authoring data',rules==sum(len(u['rules']) for u in b.UCS))
for path in root.rglob('*.md'):
    if 'source' in path.parts:continue
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
        if target.startswith(('https://','http://','#')):continue
        check('Local link '+str(path.relative_to(root))+' -> '+target,(path.parent/target).exists())
report={'scope':'Source preservation and cross-artifact structure; no formal OCL or live database execution.',
        'useCases':len(b.UCS),'apis':len(source_ids),'oclRules':rules,'checks':checks,'failures':failures}
(root/'evidence').mkdir(exist_ok=True)
(root/'evidence/package-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'{"FAIL" if failures else "PASS"}: {len(checks)} checks; {len(b.UCS)} use cases, {len(source_ids)} APIs, {rules} rules.')
if failures:
    print('\n'.join(failures))
    raise SystemExit(1)
