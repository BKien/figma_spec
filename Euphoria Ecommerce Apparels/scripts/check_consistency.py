from pathlib import Path
import json, re
from urllib.parse import unquote
from decimal import Decimal

ROOT=Path(__file__).resolve().parents[1]
errors=[]
def check(condition,message):
    if not condition: errors.append(message)

common=(ROOT/'api/common-contract.md').read_text(encoding='utf-8')
schemas={}
for section in re.split(r'(?m)^## ',common)[1:]:
    name=section.splitlines()[0].strip()
    fields={}
    for match in re.finditer(r'(?ms)^### `([^`]+)`\n(.*?)(?=^### |\Z)',section):
        meta={m.group(1):m.group(2).rstrip('.') for m in re.finditer(r'^- (Type|Required|Nullable|Description|Example): (.+)$',match[2],re.M)}
        fields[match[1]]=meta
    if fields: schemas[name]=fields

def validate(value,typ,where,nullable=False):
    if value is None:
        check(nullable,where+': unexpected null')
        return
    if typ.endswith('[]'):
        check(isinstance(value,list),where+': expected array')
        if isinstance(value,list):
            for i,item in enumerate(value): validate(item,typ[:-2],f'{where}[{i}]')
        return
    primitives={'string':str,'integer':int,'number':(int,float),'boolean':bool,'object':dict}
    if typ in primitives:
        expected=primitives[typ]
        check(isinstance(value,expected) and not (typ in ('integer','number') and isinstance(value,bool)),where+': incorrect primitive type')
        return
    check(typ in schemas,where+': unknown schema '+typ)
    if typ not in schemas:return
    check(isinstance(value,dict),where+': expected object')
    if not isinstance(value,dict): return
    fields=schemas[typ]
    check(not (set(value)-set(fields)),where+': unexpected properties')
    for name,meta in fields.items():
        if meta['Required']=='Yes': check(name in value,where+': missing '+name)
        if name in value:
            validate(value[name],meta['Type'],where+'.'+name,meta['Nullable']=='Yes')
            enum=re.search(r'Public enum: ([A-Z_, ]+)',meta.get('Description',''))
            if enum: check(value[name] in [s.strip() for s in enum[1].split(',')],where+'.'+name+': invalid enum')
    if typ=='Money':
        try: Decimal(value['amount'])
        except Exception: check(False,where+': invalid decimal')
        check(bool(re.fullmatch('[A-Z]{3}',value.get('currency',''))),where+': invalid currency code')
    if typ=='Cart':
        subtotal=sum(Decimal(x['lineTotal']['amount']) for x in value['items'])
        check(subtotal==Decimal(value['subtotal']['amount']),where+': subtotal mismatch')
        check(subtotal+Decimal(value['shippingEstimate']['amount'])==Decimal(value['totalEstimate']['amount']),where+': total mismatch')
    if typ=='CheckoutPreview':
        check(Decimal(value['subtotal']['amount'])-Decimal(value['discount']['amount'])+Decimal(value['shipping']['amount'])==Decimal(value['total']['amount']),where+': checkout total mismatch')
    if typ=='CartLine':
        check(value['quantity']*Decimal(value['unitPrice']['amount'])==Decimal(value['lineTotal']['amount']),where+': line total mismatch')

for name,fields in schemas.items():
    for field,meta in fields.items():
        example=meta.get('Example','').strip('`')
        try: validate(json.loads(example),meta['Type'],name+'.'+field,meta['Nullable']=='Yes')
        except Exception as ex: check(False,f'{name}.{field}: example parse failed: {ex}')

ucs={};apis={};example_count=0
for p in (ROOT/'uc').glob('uc-*.md'):
    text=p.read_text(encoding='utf-8');uid=re.search(r'^# (UC-\d+)',text)[1]
    ucs[uid]=(p,set(re.findall(r'API-[A-Z0-9-]+',text)))
for p in (ROOT/'api').glob('api-*.md'):
    text=p.read_text(encoding='utf-8');aid=re.search(r'^# (API-[A-Z0-9-]+)',text)[1]
    apis[aid]=(p,set(re.findall(r'`(UC-\d+)`',text)))
    for section in re.split(r'(?m)^## ',text):
        blocks=re.findall(r'(?s)```json\n(.*?)\n```',section)
        if not blocks: continue
        name='body' if section.startswith('Request Body') else 'data'
        typ=re.search(r'### `'+name+r'`\n.*?- Type: ([^.\n]+)',section,re.S)
        check(typ is not None,f'{p.name}: no schema for example')
        if not typ: continue
        for block in blocks:
            payload=json.loads(block)
            if name=='data':
                check(set(payload)=={'data','requestId'},f'{p.name}: invalid envelope')
                check(isinstance(payload.get('requestId'),str),f'{p.name}: invalid requestId')
                payload=payload['data']
            validate(payload,typ[1],p.name)
            example_count+=1
for uid,(p,refs) in ucs.items():
    for aid in refs: check(aid in apis and uid in apis[aid][1],f'{uid}: missing reciprocal API link {aid}')
for aid,(p,refs) in apis.items():
    for uid in refs:check(uid in ucs and aid in ucs[uid][1],f'{aid}: missing reciprocal UC link {uid}')

inventory=json.loads((ROOT/'evidence/screen-inventory.json').read_text())
node_ids={n['id'].replace(':','-') for n in inventory}
model=(ROOT/'uc/shared-domain-model.md').read_text(encoding='utf-8')
model+='\n'.join(p.read_text(encoding='utf-8') for p,_ in ucs.values())
classes=set(re.findall(r'(?m)^(?:class|enum) (\w+)',model))
rule_count=0
rules_per_uc={}
interaction_checks=0
check(17 <= len(ucs) <= 20, 'Expected between 17 and 20 use cases.')
for uid,(p,refs) in ucs.items():
    text=p.read_text(encoding='utf-8')
    nodes=re.findall(r'node-id=([\d-]+)',text)
    check(bool(nodes),uid+': no source nodes')
    check(set(nodes)<=node_ids,uid+': unknown source node')
    blocks=re.findall(r'(?s)```ocl\n(.*?)\n```',text)
    rules_per_uc[uid]=len(blocks)
    check(len(blocks)>=7,uid+': fewer than seven business rules')
    bodies=[re.sub(r'\s+',' ',re.sub(r'(?m)^--.*$','',b).split(':\n',1)[-1]).strip() for b in blocks]
    check(len(bodies)==len(set(bodies)),uid+': duplicate predicates within the use case')
    interactions=re.search(r'(?s)### Trigger\n(.*?)### UML Model',text)
    check(interactions is not None,uid+': missing interaction boundary')
    if interactions:
        interaction_checks+=1
        prose=interactions[1]
        leak=r'(?i)\bBR[-_]|business rules?|>=|<=|::|allInstances|isUnique|\b(?:predicate|threshold|formula|eligibility|authorization|ownership|normalization|idempotency|concurrency|must|only if|provided that|belongs to|owned by|at least|at most|no more than|sum of|multiplied by|divided by)\b'
        check(re.search(leak,prose) is None,uid+': business policy disclosed in conditions or flows')
        check(re.search(r'\b\d+\s+(?:minutes?|hours?|days?|characters?|items?)\b',prose,re.I) is None,uid+': policy threshold disclosed in conditions or flows')
    rule_ids=re.findall(r'(?m)^-- (BR-UC-\d{2}-\d{2})$',text)
    check(rule_ids==[f'BR-{uid}-{i:02}' for i in range(1,len(blocks)+1)],uid+': malformed rule namespace or sequence')
    for block in blocks:
        rule_count+=1
        ctx=re.search(r'^context (\w+)(?:::(\w+)\()? ',block,re.M)
        if ctx is None: ctx=re.search(r'^context (\w+)(?:::(\w+)\()?',block,re.M)
        check(ctx is not None,uid+': missing context')
        if ctx:
            check(ctx[1] in classes,uid+': unmodeled context '+ctx[1])
            if ctx[2]: check(bool(re.search(r'\+'+ctx[2]+r'\(',model)),uid+': unmodeled operation '+ctx[2])

for p in ROOT.rglob('*.md'):
    text=p.read_text(encoding='utf-8')
    check(len(re.findall(r'^```',text,re.M))%2==0,str(p)+': unbalanced fences')
    for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
        if link.startswith(('http:','https:','#')):continue
        target=(p.parent/unquote(link.split('#')[0])).resolve()
        check(target.exists(),f'{p.name}: broken local link {link}')
        check(target.is_relative_to(ROOT),f'{p.name}: link escapes package')

summary={'use_cases':len(ucs),'apis':len(apis),'ocl_rules':rule_count,'rules_per_uc':dict(sorted(rules_per_uc.items())),'minimum_rules_per_uc':min(rules_per_uc.values()),'policy_neutral_interaction_sections':interaction_checks,'wire_schemas':len(schemas),'json_examples':example_count,'source_frames':len(inventory),'errors':errors}
(ROOT/'evidence/consistency-results.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
raise SystemExit(1 if errors else 0)
