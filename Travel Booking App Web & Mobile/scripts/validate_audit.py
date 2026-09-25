"""Additional static checks for this package; not a full OCL type checker."""
from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
errors=[]

total=0
for p in sorted((root/'uc').glob('uc-*.md')):
    text=p.read_text(encoding='utf-8'); uc=p.name[3:5]
    uml_section=re.search(r'### UML Model\s*(.*?)\s*### Business Rules',text,re.S)
    uml_blocks=re.findall(r'```plantuml\n(.*?)```',uml_section[1],re.S) if uml_section else []
    if len(uml_blocks)!=1:
        errors.append(f'{p.name}: expected exactly one local UML model')
        model=''
    else:
        model=uml_blocks[0]
    classifiers={}
    for kind,name,body in re.findall(r'^(class|enum) (\w+)\s*\{(.*?)^\}',model,re.M|re.S):
        members={}
        for line in body.splitlines():
            line=re.sub(r'^\+','',line.strip())
            line=re.sub(r'^\{static\}\s*','',line)
            m=re.match(r'(\w+)\s*:\s*(\w+)',line)
            if m: members[m[1]]=m[2]
            op=re.match(r'(\w+)\(',line)
            if op: members[op[1]]='operation'
            if kind=='enum' and line: members[line]=name
        classifiers[name]=members
    blocks=re.findall(r'```ocl\n(.*?)```',text,re.S)
    ids=[re.search(r'^-- (BR-UC-\d+-\d+)',b,re.M)[1] for b in blocks]
    expected=[f'BR-UC-{uc}-{i:02}' for i in range(1,len(blocks)+1)]
    if ids!=expected or len(ids)<7: errors.append(f'{p.name}: rule sequence or minimum count')
    interaction=text.split('### Trigger',1)[1].split('### UML Model',1)[0]
    if re.search(r'BR-UC-|Business Rules?|```ocl|\b(?:threshold|idempotency|ownership|eligibility)\b|>=|<=',interaction,re.I):
        errors.append(f'{p.name}: policy reference in conditions/flows')
    normalized=[]
    for block in blocks:
        rid=re.search(r'-- (BR-UC-\d+-\d+)',block)[1]
        body=re.sub(r'--[^\n]*','',block)
        tokens=re.sub(r"'(?:''|[^'])*'", "''",body)
        stack=[]
        for ch in tokens:
            if ch in '({[': stack.append(ch)
            if ch in ')}]':
                if not stack or stack.pop()!=dict(zip(')}]','({['))[ch]:
                    errors.append(f'{rid}: unbalanced closing delimiter'); break
        if stack: errors.append(f'{rid}: unclosed delimiters {stack}')
        for cls,member in re.findall(r'\b(\w+)::(\w+)',body):
            if cls not in classifiers or member not in classifiers[cls]: errors.append(f'{rid}: unresolved {cls}::{member}')
        for cls in re.findall(r'\b(\w+)\.allInstances\(',body):
            if cls not in classifiers: errors.append(f'{rid}: unknown classifier {cls}')
        env={}
        ctx=re.search(r'context (\w+)(?:::\w+\((.*?)\): ([^\n]+))?',body)
        if ctx:
            env['self']=ctx[1]
            if ctx[2]: env.update(dict(re.findall(r'(\w+): (\w+)',ctx[2])))
            if ctx[3] and ctx[3] in classifiers: env['result']=ctx[3]
        for path in re.findall(r'\b(?:self|result|criteria|command)(?:\.\w+)+',body):
            parts=path.split('.'); typ=env.get(parts[0])
            for member in parts[1:]:
                if member in {'oclIsNew','oclIsUndefined','oclIsInvalid','oclIsKindOf','oclIsTypeOf','oclAsType'}: break
                if not typ or typ not in classifiers: break
                if member not in classifiers[typ]:
                    errors.append(f'{rid}: unknown property {typ}.{member} in {path}'); break
                typ=classifiers[typ][member]
                if typ=='operation': break
        constraint=re.split(r'\b(?:pre|post|inv) BR_\w+:',body)[-1]
        normalized.append(re.sub(r'\s+','',constraint))
    if len(normalized)!=len(set(normalized)): errors.append(f'{p.name}: duplicate rule body')
    total+=len(blocks)
    print(f'UC-{uc}: {len(blocks)} BR')

for p in (root/'api').glob('api-*.md'):
    text=p.read_text(encoding='utf-8')
    if re.search(r'BR-UC-|```(?:ocl|plantuml)',text): errors.append(f'{p.name}: domain policy artifact in API')

for p in root.rglob('*.md'):
    text=p.read_text(encoding='utf-8-sig')
    if len(re.findall(r'^```',text,re.M))%2: errors.append(f'{p.name}: unmatched fence')
    for href in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
        if not href.startswith(('http:','https:','#')) and not (p.parent/href.split('#')[0]).exists(): errors.append(f'{p.name}: broken link {href}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {total} rule blocks; minimum count, sequence, delimiter balance, qualified names, direct property paths, policy references, duplicate bodies and links.')
print('LIMIT: no full OCL parser, theorem prover, live Figma comparison or database execution is performed by this checker.')
