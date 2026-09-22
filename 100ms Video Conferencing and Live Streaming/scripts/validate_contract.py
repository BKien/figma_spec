"""Targeted package checks; not a complete OCL parser or model checker."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

shared = (ROOT / 'uc/shared-domain-model.md').read_text(encoding='utf-8-sig')
class_bodies = dict(re.findall(r'class (\w+) \{\n(.*?)\n\}', shared, re.S))
enums = {n: set(re.findall(r'\b[A-Z][A-Z_]+\b', b)) for n, b in re.findall(r'enum (\w+) \{\n(.*?)\n\}', shared, re.S)}
properties = {p for b in class_bodies.values() for p in re.findall(r'^\s*(?:\{static\}\s*)?(\w+):', b, re.M)}
assumptions = (ROOT / 'ASSUMPTIONS.md').read_text(encoding='utf-8-sig')
api_texts = {p.stem[4:].upper(): p.read_text(encoding='utf-8-sig') for p in (ROOT / 'api').glob('api-*.md')}
uc_texts = {}
contexts = 0
for path in sorted((ROOT / 'uc').glob('uc-*.md')):
    text = path.read_text(encoding='utf-8-sig')
    number = path.name[3:5]
    uc_texts[int(number)] = text
    rule_ids = re.findall(r'^-- BR-UC-(\d{2})-(\d{2})$', text, re.M)
    require(rule_ids == [(number, f'{n:02}') for n in range(1, len(rule_ids)+1)], path.name + ': rule IDs must be gap-free')
    for block in re.findall(r'```ocl\n(.*?)\n```', text, re.S):
        ctx = re.search(r'^context (.+)$', block, re.M).group(1)
        contexts += 1
        if '::' in ctx:
            classifier, operation = ctx.split('::', 1)
            require(classifier in class_bodies and operation in class_bodies.get(classifier, ''), path.name + ': undeclared operation ' + ctx)
        else:
            require(ctx in class_bodies, path.name + ': undeclared invariant classifier ' + ctx)
        a = re.search(r'^-- Assumption: (A-\d{2})$', block, re.M)
        require(a is not None and ('## ' + a.group(1) + ' ') in assumptions, path.name + ': unresolved assumption')
        for enum, literal in re.findall(r'\b(\w+)::([A-Z][A-Z_]+)\b', block):
            if enum in enums:
                require(literal in enums[enum], path.name + ': unknown enum literal ' + enum + '::' + literal)
        for token in re.finditer(r'\.([a-zA-Z]\w*)', block):
            prop = token.group(1)
            rest = block[token.end():].lstrip()
            if not rest.startswith('('):
                require(prop in properties, path.name + ': undeclared property ' + prop)
        require(not re.search(r'(?<![.\w])\w+@pre\.', block), path.name + ': pre-state suffix applied before property access')
        require(not re.search(r'\b(\w+)\s*=\s*\1@pre\b', block), path.name + ': identity equality used as frame condition')
    for api in set(re.findall(r'API-([A-Z0-9-]+)', text)):
        require(api in api_texts and f'`UC-{number}`' in api_texts.get(api, ''), path.name + ': missing API reverse edge ' + api)

common = (ROOT / 'api/common-contract.md').read_text(encoding='utf-8-sig')
representations = set(re.findall(r'^## (\w+)$', common, re.M))
for name, text in api_texts.items():
    for typ in re.findall(r'^- Type: (?:object|array) \((\w+)\)', text, re.M):
        require(typ in representations, name + ': unknown wire object ' + typ)
    require('common-contract.md' in text, name + ': missing common envelope inheritance')
    for status in [401, 403]:
        require(f'## Error Response — HTTP {status}' in text, name + ': missing auth outcome')

preference = api_texts['PREFERENCES-UPDATE']
for field in ['focusedParticipantId', 'sidePanel', 'microphoneDeviceId', 'virtualBackgroundId']:
    require(f'### `{field}`' in preference, 'Preferences cannot carry ' + field)
for name in ['layout', 'pictureInPicture']:
    body = re.search(r'### `' + name + r'`\n(.*?)(?=\n##|\Z)', preference, re.S).group(1)
    require('- Nullable: No' in body, name + ': nullable request contradicts storage')
for n, token in [(3, 'stream.status = StreamStatus::STARTING'), (4, 'stream.status = StreamStatus::ENDED'), (7, 'p.role = ParticipantRole::STAGE_PARTICIPANT'), (18, 'session.status = SessionStatus::ENDED')]:
    require(token in uc_texts[n], f'UC-{n:02}: missing primary lifecycle effect')
require('SessionService::leave(' in uc_texts[17] and 'SessionService::end(' in uc_texts[18], 'Departure operations are not separated')
require('SessionService::depart(' not in shared, 'Ambiguous departure operation remains')
for n in [3,4]:
    require('stream.version@pre + 1' in uc_texts[n], f'UC-{n:02}: version increment is not relative to pre-state')
require('command.principalId = session.designatedHostPrincipalId' in uc_texts[2], 'Join lacks designated-principal role mapping')
require('request.sessionId = session.id' in uc_texts[7], 'Stage decision target is not session-bound')
require('result.reactions->size() <= 50' in uc_texts[8], 'Reaction page bound missing')
for field in ['data.nextCursor']:
    require(f'### `{field}`' in api_texts['PARTICIPANT-LIST'], 'Participant pagination has no continuation')
require('## Reaction' in common and '`CLAP`' in common, 'Reaction wire enum not defined')
schema = (ROOT / 'schema.dbml').read_text(encoding='utf-8-sig')
for name in ['one_joined_membership','one_joined_host','one_pending_stage_request','one_active_share','one_active_recording']:
    require("name: '" + name + "'" in schema, 'Missing conditional unique index: ' + name)
require('(principal_id, session_id, operation, idempotency_key) [unique]' in schema, 'Idempotency is not scoped before participant creation')
for path in ROOT.rglob('*.md'):
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text(encoding='utf-8-sig')):
        if not target.startswith(('http:', 'https:', '#')):
            require((path.parent / target).exists(), str(path.relative_to(ROOT)) + ': broken link ' + target)
if errors:
    raise SystemExit('\n'.join(sorted(set(errors))))
print(f'PASS: {contexts} OCL contexts/assumption links, wire shapes, lifecycle regression checks, persistence guards and Markdown links')
