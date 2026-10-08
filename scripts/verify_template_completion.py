"""Read-only checks for the user-requested template completion.

The immutable baseline and naming plan define the authorized presentation
changes. This checker does not call validators for superseded templates and
does not claim to parse or execute OCL.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import json
import posixpath
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "format-audit/template-completion"
UNSPECIFIED = re.compile(r"\bnot[ _-]+specified\b", re.I)
FENCE_LINE = re.compile(r"^[ \t]*(`{3,}|~{3,})([^\n]*)$")
RULE_LINE = re.compile(r"^(?:--\s*)?(BR-[A-Z0-9]+(?:-[A-Z0-9]+)*)(?=\s|:|$)", re.M)
LABELS = ("Type", "Format", "Required", "Nullable", "Trigger", "Description",
          "Example", "Note", "Notes", "Default", "Allowed value", "Allowed values",
          "Validation")


def decode(data):
    return data.decode("utf-8-sig").replace("\r\n", "\n")


def metadata(text):
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    return match[1] if match else ""


def meta_value(text, name):
    match = re.search(r"^" + re.escape(name) + r":\s*(.*)$", metadata(text), re.M)
    return match[1].strip().strip('"') if match else ""


def heading_value(text, name):
    match = re.search(r"^### " + re.escape(name) + r"\s*\n(.*?)(?=^#{1,3} |\Z)",
                      text, re.M | re.S)
    return match[1].strip() if match else ""


def fenced_blocks(text):
    blocks = []
    current = None
    body = []
    for line in text.splitlines():
        match = FENCE_LINE.fullmatch(line)
        if current is None:
            if match:
                current = (match[1][0], len(match[1]), match[2].strip())
                body = []
        elif match and match[1][0] == current[0] and len(match[1]) >= current[1] and not match[2].strip():
            blocks.append((current[2], "\n".join(body)))
            current = None
        else:
            body.append(line)
    return blocks, current is None


def section(text, name):
    match = re.search(r"^## " + re.escape(name) + r"\s*\n(.*?)(?=^## |\Z)",
                      text, re.M | re.S)
    return match[1].strip() if match else ""


def compact(text):
    """Ignore layout whitespace while keeping quoted literal contents intact."""
    pieces = re.split(r"('(?:''|[^'])*'|\"(?:\\.|[^\"\\])*\")", text)
    return "".join(piece if index % 2 else re.sub(r"\s+", "", piece)
                   for index, piece in enumerate(pieces))


def plain(text):
    return " ".join(text.replace("`", "").split())


def rule_chunks(text):
    body = section(text, "Business Rules")
    matches = list(RULE_LINE.finditer(body))
    return [(match[1], body[match.start():matches[index + 1].start()
                          if index + 1 < len(matches) else len(body)])
            for index, match in enumerate(matches)]


def formal_rule(chunk):
    # Rule names, provenance, general OCL comments, and technical prose are
    # presentation/prose. Compare the context and expression tokens themselves.
    lines = [line for line in chunk.splitlines()
             if not FENCE_LINE.fullmatch(line) and not re.match(r"^\s*--", line)]
    body = "\n".join(lines)
    context = re.search(r"^context\b", body, re.M)
    if not context:
        return ""
    body = body[context.start():]
    body = re.split(r"^\s*Technical constraints(?:\s*\([^\n]*\))?\s*:",
                    body, maxsplit=1, flags=re.M)[0]
    return compact(body.replace("`", ""))


def provenance_lines(chunk):
    """Retain provenance/comment meanings while allowing comments to move."""
    result = []
    before_context = True
    for line in chunk.splitlines():
        if re.match(r"^context\b", line):
            before_context = False
        stripped = line.strip()
        old_comment = re.match(r"^--\s*(.*)$", stripped)
        if old_comment:
            value = old_comment[1]
            if value.startswith("BR-"):
                continue
            if not re.match(r"^(?:Source|Assumption|Note):", value):
                value = "Note: " + value
            result.append(plain(value))
        elif before_context and re.match(r"^(?:Source|Assumption|Note):", stripped):
            result.append(plain(stripped))
    return Counter(result)


def technical_prose(chunk):
    match = re.search(r"^\s*Technical constraints(?:\s*\([^\n]*\))?\s*:", chunk, re.M)
    if not match:
        return ""
    lines = [re.sub(r"^\s*-\s+", "", line)
             for line in chunk[match.start():].splitlines()
             if not FENCE_LINE.fullmatch(line)]
    return plain("\n".join(lines))


def full_rule_prose(chunk):
    lines = []
    for line in chunk.splitlines():
        if FENCE_LINE.fullmatch(line):
            continue
        line = re.sub(r"^\s*-\s+", "", line)
        line = re.sub(r"^(BR-[A-Z0-9-]+):\s*", r"\1 - ", line)
        lines.append(line)
    return plain("\n".join(lines))


def field_values(text):
    """Collect sequential metadata, preserving repeated heading/label identity."""
    chunks = re.split(r"(?m)^(#{2,3}) (.+)\n", text)
    parent = ""
    occurrence = Counter()
    values = {}
    for offset in range(1, len(chunks), 3):
        level, heading, body = chunks[offset:offset + 3]
        heading = heading.replace("`", "").strip()
        if level == "##":
            parent = heading
        key = (parent, heading)
        occurrence[key] += 1
        # The core metadata may share a line. Split only before a recognized
        # next label, so punctuation inside a value remains part of that value.
        label_pattern = "|".join(re.escape(label) for label in LABELS)
        body = re.sub(r";[ \t]+(?=(?:" + label_pattern + r"):)", "\n", body)
        labels = list(re.finditer(r"^(" + label_pattern + r"):[ \t]*(.*)$", body, re.M))
        label_occurrence = Counter()
        for index, match in enumerate(labels):
            label = match[1]
            label_occurrence[label] += 1
            value = body[match.start(2):labels[index + 1].start()
                         if index + 1 < len(labels) else len(body)].strip()
            values[(parent, heading, occurrence[key], label, label_occurrence[label])] = value
    return values


def run():
    plan = json.loads((AUDIT / "naming-plan.json").read_text(encoding="utf-8"))
    with zipfile.ZipFile(AUDIT / "baseline.zip") as archive:
        baseline = {name: archive.read(name) for name in archive.namelist() if not name.endswith("/")}
    entries = plan["entries"]
    failures = []
    checks = Counter()
    texts = {}
    packages = defaultdict(lambda: {"uc": {}, "api": {}, "br_ids": []})
    aliases = defaultdict(dict)
    filename_aliases = defaultdict(dict)
    canonical_api_paths = {}
    canonical_api_filenames = defaultdict(dict)
    for entry in entries:
        package = entry["path"].split("/", 1)[0]
        if entry["kind"] == "api":
            aliases[package][entry["old_api_id"]] = entry["api_id"]
            filename_aliases[package][Path(entry["path"]).name] = Path(entry["new_path"]).name
            canonical_api_paths[entry["new_path"].lower()] = entry["new_path"]
            for name in (Path(entry["path"]).name, Path(entry["new_path"]).name):
                canonical_api_filenames[package][name.lower()] = Path(entry["new_path"]).name
        else:
            aliases[package].update(entry["br_id_mapping"])
            aliases[package].update({old.replace("-", "_"): new.replace("-", "_")
                                     for old, new in entry["br_id_mapping"].items()})

    def require(condition, path, message):
        checks["assertions"] += 1
        if not condition:
            failures.append({"path": path, "message": message})

    def translated(text, package):
        for old, new in sorted({**aliases[package], **filename_aliases[package]}.items(),
                               key=lambda item: -len(item[0])):
            text = text.replace(old, new)
        return text.replace("`", "")

    # The completion repairs missing reverse associations using existing UC
    # edges only. It may not introduce a new UC -> API relation or discard an
    # original API -> UC relation.
    original_api_related = {}
    expected_api_related = {}
    for entry in entries:
        if entry["kind"] != "api" or entry["path"] not in baseline:
            continue
        package = entry["path"].split("/", 1)[0]
        related = set(re.findall(r"\bUC-\d+\b", heading_value(decode(baseline[entry["path"]]),
                                                                "Related Use Case IDs")))
        original_api_related[(package, entry["api_id"])] = related
        expected_api_related[(package, entry["api_id"])] = set(related)
    for entry in entries:
        if entry["kind"] != "uc" or entry["path"] not in baseline:
            continue
        package = entry["path"].split("/", 1)[0]
        related = set(re.findall(r"\bAPI-[A-Z0-9-]+\b", translated(
            heading_value(decode(baseline[entry["path"]]), "Related API IDs"), package)))
        for aid in related:
            expected_api_related.setdefault((package, aid), set()).add(entry["uc_id"])

    def links(text, path):
        for match in re.finditer(r"(?<!!)\[[^\]\n]*\]\(([^\n)]+)\)", text):
            target = match[1].strip()
            if target.startswith("<") and ">" in target:
                target = target[1:target.index(">")]
            else:
                target = re.split(r'\s+["\']', target, maxsplit=1)[0]
            if not target or target.startswith("#") or urlsplit(target).scheme:
                continue
            target = unquote(target.split("#", 1)[0].split("?", 1)[0])
            resolved = (ROOT / Path(path).parent / target).resolve()
            require(resolved.exists(), path, "Unresolved local link: " + target)
            relative = posixpath.normpath(posixpath.join(posixpath.dirname(path), target.replace("\\", "/")))
            canonical = canonical_api_paths.get(relative.lower())
            if canonical:
                require(relative == canonical, path, "API link must use exact planned filename casing: " + target)
            checks["local_links"] += 1

    def api_filename_references(text, path):
        package = path.split("/", 1)[0]
        for match in re.finditer(r"\bAPI-[A-Z0-9]+(?:-[A-Z0-9]+)*\.md\b", text, re.I):
            actual = match[0]
            canonical = canonical_api_filenames[package].get(actual.lower())
            if canonical:
                require(actual == canonical, path,
                        "API filename reference must use planned name/casing: " + actual + " -> " + canonical)
                checks["api_filename_references"] += 1

    require(Counter(entry["kind"] for entry in entries) == Counter({"uc": 168, "api": 243}),
            "naming-plan.json", "Expected 168 UCs and 243 APIs in the nine packages")
    for entry in entries:
        old_path, path = entry["path"], entry["new_path"]
        package = old_path.split("/", 1)[0]
        file = ROOT / path
        require(old_path in baseline, old_path, "Specification is absent from the immutable baseline")
        require(file.is_file(), path, "Expected final specification is missing")
        if old_path not in baseline or not file.is_file():
            continue
        old = decode(baseline[old_path])
        text = decode(file.read_bytes())
        texts[path] = text
        blocks, balanced = fenced_blocks(text)
        require(balanced, path, "Unbalanced Markdown fence")
        require(not UNSPECIFIED.search(text), path, "Not specified marker remains")
        require(not any("`" in line for line in text.splitlines() if not FENCE_LINE.fullmatch(line)),
                path, "Inline backtick remains")
        require(meta_value(text, "status") == "Frozen", path, "Lifecycle status must be Frozen")
        require(not re.search(r"\b(?:API|BR)-UC-\d+", text), path, "Generic UC-derived API or BR identity remains")
        links(text, path)
        api_filename_references(text, path)
        title = next((line for line in text.splitlines() if line.startswith("# ")), "")
        if entry["kind"] == "api":
            aid = entry["api_id"]
            require(file.name == aid + ".md", path, "API filename must match the uppercase API ID")
            require(meta_value(text, "api_id") == aid and heading_value(text, "API ID") == aid,
                    path, "API identity differs between plan, frontmatter, and API ID section")
            require(title == f"# {aid}: {heading_value(text, 'API Name')}", path,
                    "API title must contain its ID and API Name")
            for name in ("API Name", "Method", "Path", "Description",
                         "Authentication", "Authorization"):
                value = heading_value(old, name)
                if value and not UNSPECIFIED.search(value):
                    require(plain(translated(value, package)) == plain(heading_value(text, name)),
                            path, "Known General Information value changed: " + name)
            old_responses = re.findall(r"^## (?:Success|Error) Response[^\n]*", old, re.M)
            new_responses = re.findall(r"^## (?:Success|Error) Response[^\n]*", text, re.M)
            require(old_responses == new_responses, path, "HTTP response status sections changed")
            previous_values = field_values(old)
            current_values = field_values(text)
            for key, value in previous_values.items():
                if value and not UNSPECIFIED.search(value):
                    require(key in current_values and plain(translated(value, package)) == plain(current_values[key]),
                            path, "Known API metadata changed: " + " / ".join(map(str, key)))
                    checks["known_api_values"] += 1
            related = set(re.findall(r"\bUC-\d+\b", heading_value(text, "Related Use Case IDs")))
            previous_related = original_api_related.get((package, aid), set())
            require(previous_related.issubset(related), path, "An original related UC association was removed")
            require(related == expected_api_related.get((package, aid), set()), path,
                    "API related UCs must exactly match original associations plus baseline UC reverse edges")
            checks["added_reverse_associations"] += len(related - previous_related)
            meta_related = set(re.findall(r"\bUC-\d+\b", metadata(text)))
            require(related == meta_related, path, "API frontmatter and Related Use Case IDs disagree")
            require(aid not in packages[package]["api"], path, "Duplicate API ID within package")
            packages[package]["api"][aid] = (path, related)
            checks["api_documents"] += 1
        else:
            uid = entry["uc_id"]
            require(re.fullmatch(r"uc-\d+-[a-z0-9-]+\.md", file.name) is not None,
                    path, "UC filename must be uc-ordinal-function-name.md")
            require(meta_value(text, "uc_id") == uid and heading_value(text, "Use Case ID") == uid,
                    path, "UC identity differs between plan, frontmatter, and UC ID section")
            require(title == f"# {uid}: {heading_value(text, 'Use Case Name')}", path,
                    "UC title must contain its ID and Use Case Name")
            for name in ("Use Case Name", "Description", "Actor(s)", "Trigger", "Pre-Condition(s)",
                         "Post-Condition(s)", "Basic Flow", "Alternative Flow", "Exception Flow", "Related UI"):
                value = heading_value(old, name)
                if value and not UNSPECIFIED.search(value):
                    require(plain(translated(value, package)) == plain(heading_value(text, name)),
                            path, "Existing UC content changed: " + name)
                    checks["uc_sections_preserved"] += 1
            old_uml = [body for language, body in fenced_blocks(section(old, "UML Model"))[0] if language == "plantuml"]
            new_uml = [body for language, body in fenced_blocks(section(text, "UML Model"))[0] if language == "plantuml"]
            require(len(old_uml) == len(new_uml) and len(new_uml) == 1,
                    path, "UC must retain exactly one UML model")
            if old_uml and new_uml:
                require(compact(translated(old_uml[0], package)) == compact(new_uml[0]),
                        path, "UML declaration, member, or relationship changed")
                require("@startuml" in new_uml[0] and "@enduml" in new_uml[0],
                        path, "UML start/end markers missing")
                checks["uml_models_preserved"] += 1
            old_rules, new_rules = rule_chunks(old), rule_chunks(text)
            old_ids = [entry["br_id_mapping"].get(rid, rid) for rid, _ in old_rules]
            new_ids = [rid for rid, _ in new_rules]
            require(old_ids == new_ids, path, "Business Rule identity/order/count differs from naming plan")
            numbers = [int(rid.rsplit("-", 1)[1]) for rid in new_ids]
            require(numbers == list(range(1, len(numbers) + 1)), path, "BR local sequence is not gap-free")
            require(len(new_ids) >= 7, path, "Use case has fewer than seven Business Rules")
            require(all(rid.startswith(entry["br_prefix"]) for rid in new_ids),
                    path, "BR prefix does not match the shortened UC name")
            for (old_id, old_chunk), (new_id, new_chunk) in zip(old_rules, new_rules):
                require(re.match(re.escape(new_id) + r" - \S", new_chunk) is not None,
                        path, "Business Rule must start with bare ID - Rule Name: " + new_id)
                previous_formal = formal_rule(translated(old_chunk, package))
                current_formal = formal_rule(new_chunk)
                require(previous_formal == current_formal, path,
                        "Formal OCL context/expression changed: " + new_id)
                if previous_formal:
                    checks["ocl_rules_preserved"] += 1
                else:
                    require(full_rule_prose(translated(old_chunk, package)) == full_rule_prose(new_chunk),
                            path, "Existing prose-only Business Rule content changed: " + new_id)
                    checks["prose_only_rules_preserved"] += 1
                require(provenance_lines(translated(old_chunk, package)) == provenance_lines(new_chunk),
                        path, "Business Rule provenance or comment content changed: " + new_id)
                require(technical_prose(translated(old_chunk, package)) == technical_prose(new_chunk),
                        path, "Business Rule technical prose changed: " + new_id)
                old_name = re.match(re.escape(old_id) + r"\s*(?::|-)\s*(\S.*)$", old_chunk.splitlines()[0])
                if old_name:
                    require(new_chunk.splitlines()[0] == new_id + " - " + translated(old_name[1], package),
                            path, "Existing Business Rule name changed: " + new_id)
                checks["business_rules_preserved"] += 1
                checks["rule_prose_preserved"] += 1
            br_blocks, _ = fenced_blocks(section(text, "Business Rules"))
            require(bool(br_blocks) and all(language == "text" for language, _ in br_blocks),
                    path, "Business Rules must use text fences from the supplied template")
            for name in ("UML Model", "Business Rules"):
                body = section(text, name)
                require(not re.search(r"^\s*-\s+", body, re.M), path, "Prose bullet remains in " + name)
            require(not re.search(r"^\s*--\s+", section(text, "Business Rules"), re.M),
                    path, "OCL dash-prefixed metadata comment remains")
            related_text = heading_value(text, "Related API IDs")
            related = set(re.findall(r"\bAPI-[A-Z0-9-]+\b", related_text))
            require(bool(related) or related_text == "None", path, "UC with no API must contain exactly None")
            baseline_related = set(re.findall(r"\bAPI-[A-Z0-9-]+\b",
                                               translated(heading_value(old, "Related API IDs"), package)))
            require(related == baseline_related, path, "UC/API associations changed")
            require(uid not in packages[package]["uc"], path, "Duplicate UC ID within package")
            packages[package]["uc"][uid] = (path, related)
            packages[package]["br_ids"].extend(new_ids)
            checks["uc_documents"] += 1

    for package, data in packages.items():
        require(len(data["br_ids"]) == len(set(data["br_ids"])), package, "Duplicate BR ID within package")
        for uid, (path, related) in data["uc"].items():
            for aid in related:
                require(aid in data["api"], path, "Related API does not exist: " + aid)
                if aid in data["api"]:
                    require(uid in data["api"][aid][1], path, "API lacks reverse UC association: " + aid)
                checks["uc_api_edges"] += 1
        for aid, (path, related) in data["api"].items():
            require(bool(related), path, "API has no Related Use Case IDs")
            for uid in related:
                require(uid in data["uc"], path, "Related UC does not exist: " + uid)
                if uid in data["uc"]:
                    require(aid in data["uc"][uid][1], path, "UC lacks reverse API association: " + uid)

    planned_paths = set(entry["new_path"] for entry in entries)
    actual_paths = set()
    for package in packages:
        for file in (ROOT / package / "01-inception").rglob("*.md"):
            text = decode(file.read_bytes())
            if meta_value(text, "artifact_type") in {"api-contract", "business-use-case-specification"}:
                actual_paths.add(file.relative_to(ROOT).as_posix())
    require(actual_paths == planned_paths, "01-inception", "Active UC/API inventory differs from the 411 planned specifications")

    # Active supporting documents may link to renamed files. Source/evidence
    # archives and old executable validators remain historical/protected inputs.
    for package in packages:
        for file in (ROOT / package).rglob("*.md"):
            path = file.relative_to(ROOT).as_posix()
            parts = {part.lower() for part in file.relative_to(ROOT / package).parts[:-1]}
            if parts.intersection({"source", "evidence", "scripts"}) or path in planned_paths:
                continue
            text = decode(file.read_bytes())
            links(text, path)
            api_filename_references(text, path)
            checks["supporting_documents"] += 1

    utility_paths = [path for path in baseline if Path(path).name == "OCL-UTILITY-DEFINITIONS.md"]
    require(len(utility_paths) == 8, "OCL-UTILITY-DEFINITIONS.md", "Baseline should contain eight utility documents")
    for path in utility_paths:
        file = ROOT / path
        require(file.is_file(), path, "OCL utility document is missing")
        if not file.is_file():
            continue
        text = decode(file.read_bytes())
        require(metadata(text).splitlines() == ["artifact_type: ocl-utility-definitions", "status: Frozen"],
                path, "OCL frontmatter must contain exactly artifact_type and Frozen status")
        require("\n# OCL Utility Definitions\n" in text and "\n## Utility Classes\n" in text,
                path, "OCL catalog headings differ from supplied template")
        blocks, balanced = fenced_blocks(text)
        require(balanced and len(blocks) == 2 and all(language == "text" for language, _ in blocks),
                path, "Utility document must have exactly two balanced text fences")
        require(not UNSPECIFIED.search(text), path, "Not specified marker remains in utility catalog")
        require(not any("`" in line for line in text.splitlines() if not FENCE_LINE.fullmatch(line)),
                path, "Inline backtick remains in utility catalog")
        if len(blocks) == 2:
            definitions = {(match[1], match[2], compact(match[3]), compact(match[4]))
                           for match in re.finditer(r"^(\w+)(?:\.|::)(\w+)\((.*)\):\s*(.+)$", blocks[0][1], re.M)}
            methods = set()
            for match in re.finditer(r"^class (\w+)(?:\s+<<\w+>>)?\s*\{(.*?)^\}", blocks[1][1], re.M | re.S):
                for method in re.finditer(r"^\s*\+(\w+)\((.*)\):\s*(.+)$", match[2], re.M):
                    methods.add((match[1], method[1], compact(method[2]), compact(method[3])))
            require(bool(definitions) and definitions == methods, path,
                    "Utility definitions and class method signatures differ: " +
                    str({"missing_class_methods": sorted(definitions - methods), "extra_class_methods": sorted(methods - definitions)}))
            checks["utility_methods"] += len(definitions)
        links(text, path)
        checks["utility_documents"] += 1

    # Supplied examples may be intentional shorthand. Only new examples created
    # by this completion must be JSON values of their declared top-level type.
    decisions_file = AUDIT / "metadata-decisions.json"
    require(decisions_file.is_file(), "metadata-decisions.json", "Metadata decision evidence is missing")
    if decisions_file.is_file():
        decisions = json.loads(decisions_file.read_text(encoding="utf-8"))
        final_path_by_old = {entry["path"]: entry["new_path"] for entry in entries}
        generated = [(decision["file"], replacement)
                     for decision in decisions.get("decisions", [])
                     for replacement in decision.get("replacements", [])
                     if replacement.get("label") == "Example"]
        require(len(generated) == decisions.get("counts", {}).get("Example"),
                "metadata-decisions.json", "Generated example decision count is inconsistent")
        example_values = {path: field_values(text) for path, text in texts.items()}
        for old_path, replacement in generated:
            path = final_path_by_old.get(old_path, old_path)
            values = example_values.get(path, {})
            matching = [key for key in values
                        if key[0] == replacement["section"] and key[1] == replacement["field"].replace("`", "")
                        and key[3] == "Example"]
            require(len(matching) == 1, path,
                    "New example cannot be located uniquely: " + replacement["section"] + " / " + replacement["field"])
            if len(matching) != 1:
                continue
            key = matching[0]
            raw = values[key]
            require(plain(raw) == plain(replacement["value"]), path,
                    "New example differs from recorded decision: " + replacement["field"])
            try:
                value = json.loads(raw)
            except (ValueError, TypeError) as error:
                require(False, path, "New example is not valid JSON: " + replacement["field"] + " / " + str(error))
                continue
            declared_type = values.get((*key[:3], "Type", 1), "").lower().strip()
            nullable = values.get((*key[:3], "Nullable", 1), "").lower().strip()
            if value is None:
                type_matches = nullable.rstrip(".") in {"yes", "true"}
            elif re.search(r"\barray\b", declared_type):
                type_matches = isinstance(value, list)
            elif declared_type.startswith("object") or "object" in declared_type or declared_type.startswith("money"):
                type_matches = isinstance(value, dict)
            elif declared_type.startswith(("integer", "int32", "int64", "long")):
                type_matches = type(value) is int
            elif declared_type.startswith(("number", "real", "decimal", "float", "double", "numeric")):
                type_matches = type(value) in {int, float}
            elif declared_type.startswith("string"):
                type_matches = isinstance(value, str)
            elif declared_type.startswith(("boolean", "bool")):
                type_matches = type(value) is bool
            else:
                type_matches = False
            require(type_matches, path, "New example JSON type disagrees with Type/Nullable: " +
                    replacement["field"] + " / " + declared_type)
            checks["new_json_examples"] += 1

    for path, contents in baseline.items():
        file_path = Path(path)
        protected = ("source" in file_path.parts or file_path.suffix.lower() in {".dbml", ".sql"}
                     or "SCHEMA" in file_path.name.upper())
        if protected:
            file = ROOT / path
            require(file.is_file() and file.read_bytes() == contents, path, "Protected source or schema bytes changed")
            checks["protected_files"] += 1

    failures = list({(item["path"], item["message"]): item for item in failures}.values())
    report = {"status": "PASS" if not failures else "FAIL", "checks": dict(checks),
              "failures": failures,
              "limits": ["Static presentation, traceability, and baseline preservation checks; no OCL execution or proof.",
                         "Utility signature equivalence is checked; utility semantic assertions are not executed."]}
    (AUDIT / "verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{report['status']}: {checks['uc_documents']} UCs, {checks['api_documents']} APIs, "
          f"{checks['business_rules_preserved']} Business Rules, {checks['utility_documents']} utility catalogs; "
          f"{len(failures)} failures.")
    for failure in failures[:60]:
        print(f"{failure['path']}: {failure['message']}")
    if len(failures) > 60:
        print(f"See verification.json for the remaining {len(failures) - 60} failures.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(run())
