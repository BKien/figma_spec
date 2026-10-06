"""Project each active use-case UML onto its own unchanged business rules.

Source archives, APIs, persistence models, and the excluded 100ms package are
not rewritten. Run with --apply once, then --verify to audit the saved result.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = ROOT / "100ms Video Conferencing and Live Streaming"
REPORT = ROOT / "format-audit" / "local-uml" / "report.json"
FENCE = re.compile(r"(?ms)^(~~~|```)plantuml\n(.*?)\n\1")
DECL = re.compile(r"(?ms)^(class|enum) (\w+)([^\n{]*)\{\n(.*?)^\}")
MEMBER = re.compile(r"^\s*(?:\{static\}\s*)?[+#-]?(?:\{static\}\s*)?([A-Za-z_]\w*|<=|>=|<|>)\s*(\(|:)")
TOKEN = re.compile(r"@pre|->|::|<=|>=|<>|[A-Za-z_]\w*|\d+(?:\.\d+)?|[^\s]")
PRIMITIVES = {"String", "Boolean", "Integer", "Real", "Decimal", "UUID", "Binary", "Date", "DateTime", "OclAny", "OclVoid"}
COLLECTIONS = {"Set", "Sequence", "Bag", "OrderedSet", "Collection", "Tuple"}
BOOL_OPS = {"exists", "one", "forAll", "isUnique", "includes", "excludes", "includesAll", "excludesAll", "isEmpty", "notEmpty", "oclIsUndefined", "oclIsInvalid", "oclIsNew", "oclIsTypeOf", "oclIsKindOf"}
ITERATORS = {"select", "reject", "collect", "collectNested", "sortedBy", "any", "exists", "one", "forAll", "isUnique"}


def read(path):
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def frozen_hashes(directory):
    return {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in sorted(directory.rglob("*")) if p.is_file()}


def uc_files():
    return sorted(p for p in ROOT.glob("*/01-inception/*/uc-*.md") if EXCLUDED not in p.parents)


@dataclass
class Classifier:
    kind: str
    name: str
    suffix: str
    members: dict[str, str]
    body: str


def declarations(model):
    result = {}
    for match in DECL.finditer(model):
        kind, name, suffix, body = match.groups()
        members = {}
        current = None
        depth = 0
        for line in body.splitlines():
            if current and depth:
                members[current] += "\n" + line
                depth += line.count("(") - line.count(")")
                continue
            member = MEMBER.match(line)
            if member:
                current = member[1]
                members[current] = line
                depth = line.count("(") - line.count(")")
            elif current and line.strip():
                members[current] += "\n" + line
        if name in result:
            previous = result[name]
            members = {**previous.members, **members}
            body = previous.body + "\n" + body
        result[name] = Classifier(kind, name, suffix.rstrip(), members, body.rstrip())
    return result


def member_types(line):
    # Parameter and return types are both part of an operation's vocabulary.
    return set(re.findall(r":\s*([A-Za-z_]\w*)", line)) | set(re.findall(r"\b(?:Set|Sequence|Bag|OrderedSet|Collection)\((\w+)\)", line))


def output_types(line):
    tail = line.rsplit("):", 1)[-1] if "):" in line else line.split(":", 1)[-1]
    words = re.findall(r"\b[A-Za-z_]\w*\b", tail)
    return {w for w in words[:2] if w not in COLLECTIONS and w not in {"query", "ordered"}}


def clean_ocl(text):
    text = re.sub(r"(?m)^\s*--.*$", "", text)
    # Literals cannot introduce classifier/member dependencies.
    return re.sub(r"'(?:[^'\\]|\\.|'')*'|\"(?:[^\"\\]|\\.)*\"", "''", text)


def analyze(rules, classes):
    used = defaultdict(set)
    roots = set()
    unresolved = set()
    clean = clean_ocl(rules)
    # Process each context independently: 'result', 'self' and iterator names
    # can have different types in different rules in the same document.
    chunks = re.split(r"(?m)(?=^context\s)", clean)
    for chunk in chunks:
        context = re.match(r"context\s+(\w+)(?:::([A-Za-z_]\w*)\s*\((.*?)\)\s*:\s*([^\n]+))?", chunk, re.S)
        if not context:
            continue
        cls, operation, parameters, returns = context.groups()
        roots.add(cls)
        if operation:
            used[cls].add(operation)
        env = defaultdict(set)
        env["self"].add(cls)
        if returns:
            env["result"].update(re.findall(r"\b\w+\b", returns))
            env["result"].difference_update(COLLECTIONS)
        for variable, typ, element in re.findall(r"\b(\w+)\s*:\s*(\w+)(?:\((\w+)\))?", parameters or ""):
            env[variable].add(element or typ)
        for variable, typ, element in re.findall(r"\blet\s+(\w+)\s*:\s*(\w+)(?:\((\w+)\))?", chunk):
            env[variable].add(element or typ)
        tokens = TOKEN.findall(chunk)
        pairs = {}
        stack = []
        for index, token in enumerate(tokens):
            if token in {"(", "{"}:
                stack.append(index)
            elif token in {")", "}"} and stack:
                start = stack.pop()
                pairs[start] = index
                pairs[index] = start
        types = defaultdict(set)
        for _ in range(12):
            changed = False
            for index, token in enumerate(tokens):
                inferred = set()
                if re.fullmatch(r"[A-Za-z_]\w*", token):
                    if index and tokens[index - 1] in {".", "::", "->"}:
                        owners = types[index - 2] if index >= 2 else set()
                        for owner in owners:
                            definition = classes.get(owner)
                            if definition and token in definition.members:
                                used[owner].add(token)
                                inferred.update(output_types(definition.members[token]))
                            elif definition and definition.kind == "enum":
                                inferred.add(owner)
                        if token == "allInstances":
                            inferred.update(owners)
                        elif token in BOOL_OPS:
                            inferred.add("Boolean")
                        elif token in {"size", "count", "indexOf"}:
                            inferred.add("Integer")
                        elif token not in {"collect", "collectNested"} and not inferred:
                            inferred.update(owners)
                        if token in ITERATORS and index + 1 in pairs:
                            end = pairs[index + 1]
                            interior = tokens[index + 2:end]
                            if "|" in interior:
                                bar = interior.index("|")
                                for variable in interior[:bar]:
                                    if re.fullmatch(r"[a-z_]\w*", variable) and not owners <= env[variable]:
                                        env[variable].update(owners)
                                        changed = True
                            elif interior and interior[0] not in {"(", "{"}:
                                for owner in owners:
                                    definition = classes.get(owner)
                                    if definition and interior[0] in definition.members:
                                        used[owner].add(interior[0])
                    else:
                        inferred.update(env[token])
                        if token in classes:
                            inferred.add(token)
                        if token in {"true", "false"}:
                            inferred.add("Boolean")
                        # Invariants allow implicit self navigation.
                        if token in classes.get(cls, Classifier("", "", "", {}, "")).members and not (index + 1 < len(tokens) and tokens[index + 1] == ":"):
                            used[cls].add(token)
                            inferred.update(output_types(classes[cls].members[token]))
                elif token == "@pre":
                    inferred.update(types[index - 1])
                elif token in {"<", "<=", ">", ">="}:
                    for owner in types[index - 1] | types[index + 1]:
                        definition = classes.get(owner)
                        if definition and token in definition.members:
                            used[owner].add(token)
                elif token in {")", "}"} and index in pairs:
                    start = pairs[index]
                    fn_index = start - 1
                    fn = tokens[fn_index] if fn_index >= 0 else ""
                    if fn in {"collect", "collectNested"}:
                        interior = tokens[start + 1:index]
                        if "|" in interior:
                            inferred.update(types[index - 1])
                        elif interior:
                            owners = types[fn_index - 2]
                            for owner in owners:
                                definition = classes.get(owner)
                                if definition and interior[0] in definition.members:
                                    inferred.update(output_types(definition.members[interior[0]]))
                    elif fn in COLLECTIONS:
                        for j in range(start + 1, index):
                            inferred.update(types[j])
                    elif fn_index >= 0 and re.fullmatch(r"[A-Za-z_]\w*", fn):
                        inferred.update(types[fn_index])
                    else:
                        inferred.update(types[index - 1])
                if not inferred <= types[index]:
                    types[index].update(inferred)
                    changed = True
                # Infer untyped let bindings from the complete RHS chain.
                if token == "let" and index + 2 < len(tokens):
                    variable = tokens[index + 1]
                    try:
                        equal = tokens.index("=", index + 2)
                    except ValueError:
                        continue
                    endpoint = equal + 1
                    j = endpoint
                    while j < len(tokens):
                        if tokens[j] in {"(", "{"} and j in pairs:
                            j = pairs[j]
                        endpoint = j
                        if j + 1 >= len(tokens) or tokens[j + 1] not in {".", "->", "::", "@pre", "("}:
                            break
                        j += 1
                    if not types[endpoint] <= env[variable]:
                        env[variable].update(types[endpoint])
                        changed = True
            if not changed:
                break
        # Explicit type declarations and static calls are unambiguous roots.
        roots.update(set(re.findall(r"\b\w+\b", chunk)) & set(classes))
        # Unqualified helpers in legacy OCL still need their declared operation.
        for match in re.finditer(r"(?<![.\w:>])\b(\w+)\s*\(", chunk):
            name = match[1]
            if name in COLLECTIONS or name in {"if", "context"}:
                continue
            for owner, definition in classes.items():
                if name in definition.members and "(" in definition.members[name]:
                    used[owner].add(name)
                    roots.add(owner)
        # Retain ambiguous navigation conservatively, but only on classifiers
        # reachable from this UC. Record it for review rather than guessing.
        for index, token in enumerate(tokens):
            if index and tokens[index - 1] in {".", "->", "::"}:
                owners = types[index - 2]
                if not any(owner in classes and token in classes[owner].members for owner in owners):
                    if token not in BOOL_OPS | ITERATORS | {"size", "count", "allInstances", "at", "asSet", "asSequence"} and any(token in definition.members for definition in classes.values()):
                        unresolved.add(token)
    return roots, used, unresolved


def project(model, rules, pool, shared_model=""):
    local = declarations(model)
    classes = {**pool, **local}
    roots, used, unresolved = analyze(rules, classes)
    needed = roots & set(classes)
    # Standard scalar names need a class body only when the BR uses operations
    # provided by that body's declaration, not merely as a field's scalar type.
    needed -= {name for name in PRIMITIVES if not used[name]}
    while True:
        previous = (set(needed), {key: set(value) for key, value in used.items()})
        for name in list(needed):
            definition = classes[name]
            # A value object used as a complete argument/equality operand needs
            # its complete value shape. Opaque entity equality needs identity.
            if "<<value>>" in definition.suffix:
                used[name].update(definition.members)
            elif not used[name] and "id" in definition.members:
                used[name].add("id")
            used[name].update(unresolved & set(definition.members))
            for member in used[name]:
                if member not in definition.members:
                    continue
                for typ in member_types(definition.members[member]):
                    if typ in classes and (typ not in PRIMITIVES or used[typ]):
                        needed.add(typ)
        if previous == (needed, dict(used)):
            break
    order = [name for name in local if name in needed] + sorted(needed - set(local))
    blocks = []
    for name in order:
        definition = classes[name]
        body = definition.body if definition.kind == "enum" else "\n".join(line for member, line in definition.members.items() if member in used[name])
        if not body:
            body = "  ' Only the type is referenced by this use case's Business Rules."
        blocks.append(f"{definition.kind} {name}{definition.suffix} {{\n{body}\n}}")
    # Preserve original relation kinds and cardinalities whenever the retained
    # vocabulary uses that relation. Add typed property edges missing in legacy
    # models, without introducing any node outside this UC's vocabulary.
    edges = []
    covered = set()
    for line in (model + "\n" + shared_model).splitlines():
        edge = re.match(r'^(\w+)(?:\s+"[^"]*")?\s+([.o*<|>-]+)(?:\s+"[^"]*")?\s+(\w+)(?:\s*:\s*(.*))?$', line)
        if not edge:
            continue
        left, relation, right, label = edge.groups()
        if left not in needed or right not in needed:
            continue
        matching = []
        for owner, target in ((left, right), (right, left)):
            for member in used[owner]:
                declaration = classes[owner].members.get(member, "")
                if target in member_types(declaration):
                    matching.append((owner, member, target))
        if not matching and ".." not in relation:
            continue
        if label and any(label == member for owner, member, target in matching):
            matching = [(owner, member, target) for owner, member, target in matching if member == label]
        if line not in edges:
            edges.append(line)
        covered.update(matching)
    for name in order:
        definition = classes[name]
        for member, line in definition.members.items():
            if member not in used[name] or MEMBER.match(line)[2] != ":":
                continue
            for typ in sorted(member_types(line) & needed - PRIMITIVES):
                if typ != name and (name, member, typ) not in covered:
                    multiplicity = re.search(r"\[([^]]+)\]", line)
                    cardinality = multiplicity[1] if multiplicity else "0..*" if re.search(r"\b(?:Set|Sequence|Bag|OrderedSet|Collection)\(", line) else "1"
                    edges.append(f'{name} --> "{cardinality}" {typ} : {member}')
    # Keep notes only when their attached class and named members survive.
    notes = []
    for note in re.finditer(r"(?ms)^note (?:right|left|top|bottom) of (\w+)\n.*?^end note", model):
        owner = note[1]
        if owner in needed and not (set(re.findall(r"\b\w+\b", note[0])) & set(classes[owner].members) - used[owner]):
            notes.append(note[0])
    if "CalendarDate" in needed and "ordinal" in used["CalendarDate"]:
        notes.append('note right of CalendarDate\n  ordinal is the calendar-day index in Asia/Saigon.\nend note')
    output = "@startuml\nhide empty members\n\n" + "\n\n".join(blocks)
    if edges:
        output += "\n\n" + "\n".join(edges)
    if notes:
        output += "\n\n" + "\n\n".join(notes)
    output += "\n\n@enduml"
    return output, local, declarations(output), sorted(unresolved)


def non_uml(text):
    text = re.sub(r"(?m)^Vocabulary imports:.*\n\n", "", text)
    return FENCE.sub("<LOCAL UML>", text)


def verify():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    errors = []
    if report["excluded_hashes"] != frozen_hashes(EXCLUDED):
        errors.append("The excluded 100ms package changed.")
    for item in report["use_cases"]:
        path = ROOT / item["path"]
        text = read(path)
        if sha(non_uml(text).encode()) != item["non_uml_sha256"]:
            errors.append(f"{item['path']}: behavior/BR content changed")
        matches = list(FENCE.finditer(text))
        if len(matches) != 1:
            errors.append(f"{item['path']}: expected exactly one UML block")
            continue
        model = matches[0][2]
        classes = declarations(model)
        rules = text.split("## Business Rules", 1)[1]
        roots, used, unresolved = analyze(rules, classes)
        if re.search(r"(?i)shared[- ]domain[- ]model|!include", text):
            errors.append(f"{item['path']}: external UML dependency")
        for name in roots - set(classes) - PRIMITIVES - COLLECTIONS:
            errors.append(f"{item['path']}: missing classifier {name}")
        for reference in re.finditer(r"\b(\w+)(?:\.allInstances\(\)|::(\w+))", clean_ocl(rules)):
            name, member = reference.groups()
            if name not in classes:
                errors.append(f"{item['path']}: undefined explicit OCL classifier {name}")
            elif member == "allInstances":
                continue
            elif member and classes[name].kind == "enum":
                if not re.search(rf"(?m)^\s*{re.escape(member)}\s*$", classes[name].body):
                    errors.append(f"{item['path']}: undefined enum literal {name}::{member}")
            elif member and member not in classes[name].members:
                errors.append(f"{item['path']}: undefined explicit OCL member {name}::{member}")
        for name, definition in classes.items():
            if definition.kind == "enum":
                continue
            for member, line in definition.members.items():
                for typ in member_types(line) - PRIMITIVES - COLLECTIONS - set(classes):
                    errors.append(f"{item['path']}: missing member type {typ}")
            for member in used[name] - set(definition.members):
                errors.append(f"{item['path']}: missing operation/member {name}.{member}")
        if sha(model.encode()) != item["uml_sha256"]:
            errors.append(f"{item['path']}: UML differs from reviewed projection")
    for path in report["deleted"]:
        if (ROOT / path).exists():
            errors.append(f"Removed specification artifact exists: {path}")
    for path, digest in report["preserved_hashes"].items():
        if not (ROOT / path).is_file() or sha((ROOT / path).read_bytes()) != digest:
            errors.append(f"Unrelated artifact changed: {path}")
    if errors:
        raise SystemExit("\n".join(errors))
    counts = Counter(Path(item["path"]).parts[0] for item in report["use_cases"])
    print(json.dumps({"verified_use_cases": sum(counts.values()), "projects": dict(counts), "deleted_spec_artifacts": len(report["deleted"]), "100ms_unchanged": True, "BR_and_behavior_unchanged": True}, indent=2))


def apply():
    files = uc_files()
    pools = defaultdict(dict)
    shared_models = defaultdict(str)
    for path in files:
        for match in FENCE.finditer(read(path)):
            for name, definition in declarations(match[2]).items():
                pools[path.parts[len(ROOT.parts)]].setdefault(name, definition)
    shared = [p for p in ROOT.glob("*/01-inception/**/shared-domain-model.md") if EXCLUDED not in p.parents]
    for path in shared:
        for match in FENCE.finditer(read(path)):
            pools[path.parts[len(ROOT.parts)]].update(declarations(match[2]))
            shared_models[path.parts[len(ROOT.parts)]] += "\n" + match[2]
    excluded_hashes = frozen_hashes(EXCLUDED)
    changed = set(files)
    deleted = shared + [p for p in ROOT.glob("*/01-inception/**/README.md") if EXCLUDED not in p.parents]
    changed.update(deleted)
    docs = [p for p in ROOT.glob("*/*.md") if EXCLUDED not in p.parents]
    reference_updates = {}
    for path in docs:
        original = read(path)
        text = re.sub(r"(01-inception/(?:uc|api|use-cases|api-constracts)/)README\.md", r"\1", original)
        text = text.replace(', [shared UML model](01-inception/uc/shared-domain-model.md), and', ' and')
        text = text.replace(' and `shared-domain-model.md`', '')
        text = text.replace('described in the shared model', 'described in each use case\'s local UML model')
        if text != original:
            reference_updates[path] = text
            changed.add(path)
    projects = {p.parents[2] for p in files}
    preserved = {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for project in projects for p in project.rglob("*") if p.is_file() and p not in changed}
    report = {"excluded_hashes": excluded_hashes, "preserved_hashes": preserved, "deleted": [p.relative_to(ROOT).as_posix() for p in deleted], "use_cases": [], "reference_updates": [p.relative_to(ROOT).as_posix() for p in reference_updates]}
    rewritten = {}
    for path in files:
        text = read(path)
        matches = list(FENCE.finditer(text))
        if len(matches) != 1 or "## Business Rules" not in text:
            raise ValueError(f"Unsupported UC structure: {path}")
        model = matches[0][2]
        rules = text.split("## Business Rules", 1)[1]
        project_name = path.parts[len(ROOT.parts)]
        output, before, after, unresolved = project(model, rules, pools[project_name], shared_models[project_name])
        updated = text[:matches[0].start(2)] + output + text[matches[0].end(2):]
        updated = re.sub(r"(?m)^Vocabulary imports:.*\n\n", "", updated)
        assert non_uml(text) == non_uml(updated), path
        rewritten[path] = updated
        report["use_cases"].append({"path": path.relative_to(ROOT).as_posix(), "non_uml_sha256": sha(non_uml(text).encode()), "uml_sha256": sha(output.encode()), "classifiers_before": len(before), "classifiers_after": len(after), "members_before": sum(len(c.members) for c in before.values() if c.kind == "class"), "members_after": sum(len(c.members) for c in after.values() if c.kind == "class"), "conservative_member_names": unresolved})
    # Compute and validate all projections before writing any UC.
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for path, text in {**rewritten, **reference_updates}.items():
        path.write_text(text, encoding="utf-8", newline="\n")
    for path in deleted:
        resolved = path.resolve()
        assert resolved.is_relative_to(ROOT) and not resolved.is_relative_to(EXCLUDED)
        path.unlink()
    verify()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--apply", action="store_true")
    group.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    apply() if args.apply else verify()
