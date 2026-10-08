"""Apply the supplied UC/API presentation and preserve the current content.

Snapshot first, then apply once. --verify checks against that immutable snapshot,
including model/rule bytes, API field values, activity text and protected files.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote
import zipfile

sys.dont_write_bytecode = True
from format_tripma import encode_formatted, fences, sections, title

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "format-audit/template-format"
TEMPLATE = Path("D:/000-template/template.zip")
MANIFEST = AUDIT / "manifest.json"
GENERAL = ["API ID", "API Name", "Related Use Case IDs", "Method", "Path",
           "Description", "Authentication", "Authorization"]
UC_SECTIONS = ["Use Case ID", "Use Case Name", "Description", "Actor(s)",
               "Priority", "Trigger", "Pre-Condition(s)", "Post-Condition(s)",
               "Basic Flow", "Alternative Flow", "Exception Flow", "Related UI",
               "Related API IDs", "Notes"]
LABEL = re.compile(r"^(Type|Format|Required|Nullable|Trigger|Description|Example|"
                   r"Note|Notes|Default|Allowed values?|Validation):[ \t]*(.*)$")
CORE = ["Type", "Format", "Required", "Nullable"]
UNSPECIFIED = "Not specified."


def decode(data):
    return data.decode("utf-8-sig").replace("\r\n", "\n")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def relative(path):
    return path.relative_to(ROOT).as_posix()


def packages():
    return sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "01-inception").is_dir())


def kind(path):
    if path.name == "OCL-UTILITY-DEFINITIONS.md":
        return "ocl"
    if "01-inception" in path.parts and re.match(r"(?i)^uc-\d{2}-.+\.md$", path.name):
        return "uc"
    if "01-inception" in path.parts and re.match(r"(?i)^api-[a-z0-9-]+\.md$", path.name):
        return "api"
    return None


def metadata_header(text):
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    return (match.group(1), text[match.end():].lstrip("\n")) if match else ("", text)


def frozen(text):
    header, body = metadata_header(text)
    if not header or not re.search(r"^status:", header, re.M):
        raise ValueError("UC/API metadata has no lifecycle status")
    header = re.sub(r"^status:.*$", "status: Frozen", header, flags=re.M)
    return f"---\n{header}\n---\n\n{body}"


def squash(text):
    return "\n".join(line.rstrip() for line in text.splitlines() if line.strip())


def letter(index):
    result = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(97 + remainder) + result
    return result


def branch_blocks(body):
    found = list(re.finditer(r"^(AF|EF)-(\d+):[ \t]*(.*)$", body, re.M))
    if not found:
        return []
    if body[:found[0].start()].strip():
        raise ValueError("Unrecognized content before the first branch")
    return [(f"{m[1]}-{m[2]}", m[3].strip(),
             body[m.end():found[i + 1].start() if i + 1 < len(found) else len(body)].strip())
            for i, m in enumerate(found)]


def uc_functional(text):
    return dict(sections(dict(sections(text, 2))["Functional Use-Case Specification"], 3))


def format_uc(text, mapping):
    text = frozen(text)
    data = uc_functional(text)
    basic = re.findall(r"^(\d+)\. ", data["Basic Flow"], re.M)
    if [int(n) for n in basic] != list(range(1, len(basic) + 1)):
        raise ValueError("Basic Flow is not a consecutive numbered list")
    used = Counter()
    output = []
    for name, body in sections(text, 2):
        if name != "Functional Use-Case Specification":
            output += [f"## {name}", "", body, ""]
            continue
        output += [f"## {name}", ""]
        for heading in UC_SECTIONS:
            if heading not in data and heading != "Notes":
                raise ValueError(f"Missing UC section {heading}")
            value = data.get(heading, "None.")
            if heading in ("Alternative Flow", "Exception Flow"):
                formatted = []
                for flow_id, old_title, activities in branch_blocks(value):
                    anchored = re.findall(r"^(\d+)([a-z]+)[.:] ", activities, re.M)
                    if anchored:
                        if not old_title:
                            raise ValueError(f"Existing anchored branch needs a title: {flow_id}")
                        activities = re.sub(r"^(\d+[a-z]+)\. ", r"\1: ", activities, flags=re.M)
                        activities = re.sub(r"\n+(?=\d+[a-z]+: )", "\n\n", activities)
                        formatted += [f"{flow_id}: {old_title}", "", activities, ""]
                        continue
                    entry = mapping[flow_id]
                    anchor = entry["anchor"]
                    if not 1 <= anchor <= len(basic):
                        raise ValueError(f"Invalid branch anchor: {flow_id} -> {anchor}")
                    def replace(match):
                        code = f"{anchor}{letter(used[anchor])}"
                        used[anchor] += 1
                        return code + ": "
                    activities = re.sub(r"^\d+\. ", replace, activities, flags=re.M)
                    activities = re.sub(r"\n+(?=\d+[a-z]+: )", "\n\n", activities)
                    if not re.search(r"^\d+[a-z]+: ", activities, re.M):
                        raise ValueError(f"Branch has no activities: {flow_id}")
                    formatted += [f"{flow_id}: {old_title or entry['title']}", "", activities, ""]
                if formatted:
                    value = "\n".join(formatted).rstrip()
            if heading in ("Pre-Condition(s)", "Post-Condition(s)"):
                value = re.sub(r"\n+(?=(?:PRE|POST)-\d+:)", "\n\n", value)
            output += [f"### {heading}", "", value, ""]
    prefix = text[:text.index("## Functional Use-Case Specification")]
    return prefix + "\n".join(output).rstrip() + "\n"


def field_parts(body):
    # Split only the four core labels; semicolons inside enums/examples survive.
    body = re.sub(r";[ \t]*(?=(?:Type|Format|Required|Nullable):)", "\n", body)
    metadata = {}
    preamble = []
    current = None
    fence = None
    for line in body.splitlines():
        mark = re.match(r"^(`{3,}|~{3,})", line)
        match = LABEL.match(line) if fence is None and not mark else None
        if match:
            current = match[1]
            if current in metadata:
                raise ValueError(f"Duplicate field metadata: {current}")
            metadata[current] = [match[2]]
        elif current is None:
            preamble.append(line)
        else:
            metadata[current].append(line)
        if mark:
            fence = None if fence == mark[1][0] else mark[1][0]
    return squash("\n".join(preamble)), {key: "\n".join(value).strip() for key, value in metadata.items()}


def format_field(body, section):
    preamble, metadata = field_parts(body)
    if "Type" not in metadata:
        raise ValueError("API field has no Type metadata")
    required = ["Type"] + (["Format"] if section == "Request Header(s)" or "Format" in metadata else []) + ["Required", "Nullable"]
    first = "; ".join(f"{label}: {metadata.get(label, UNSPECIFIED)}" for label in required)
    output = [first, ""]
    if preamble:
        output += [preamble, ""]
    requested = ["Trigger", "Description", "Example"]
    if section == "Request Header(s)" or section.startswith("Error Response"):
        requested.append("Note")
    for label in requested:
        output += [f"{label}: {metadata.get(label, UNSPECIFIED)}", ""]
    for label, value in metadata.items():
        if label not in CORE + requested:
            output += [f"{label}: {value}", ""]
    return "\n".join(output).rstrip()


def field_name(name, section):
    prefix = {"Request Header(s)": "headers.", "Path Parameter(s)": "path.",
              "Query Parameter(s)": "query."}.get(section)
    name = name.strip("`")
    return prefix + name if prefix and not name.startswith(prefix) else name


def format_api(text):
    text = frozen(text)
    data = sections(text, 2)
    if "Path Parameter(s)" not in dict(data):
        location = next(i for i, (name, _) in enumerate(data) if name in ("Query Parameter(s)", "Request Body"))
        data.insert(location, ("Path Parameter(s)", "None."))
    if [name for name, _ in sections(data[0][1], 3)] != GENERAL:
        raise ValueError("Unexpected API General Information structure")
    output = []
    for section, body in data:
        output += [f"## {section}", ""]
        if section in ("General Information", "Notes"):
            output += [body, ""]
            continue
        fields = sections(body, 3)
        if not fields:
            output += [body or "None.", ""]
            continue
        prefix = body[:body.index("### ")].strip()
        if prefix:
            output += [prefix, ""]
        for name, values in fields:
            output += [f"### {field_name(name, section)}", "", format_field(values, section), ""]
    return text[:text.index("## General Information")] + "\n".join(output).rstrip() + "\n"


def format_ocl(text):
    header, body = metadata_header(text)
    body = re.sub(r"^# OCL Utility Semantics$", "# OCL Utility Definitions", body, count=1, flags=re.M)
    source = [line for line in header.splitlines() if not line.startswith(("artifact_type:", "status:"))]
    output = "---\nartifact_type: ocl-utility-definitions\nstatus: Frozen\n---\n\n" + body.rstrip() + "\n"
    if source:
        output += "\n## Source Metadata\n\n~~~yaml\n" + "\n".join(source) + "\n~~~\n"
    return output


def maps():
    merged = {}
    for path in sorted(AUDIT.glob("branch-map-*.json")):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if merged.keys() & data.keys():
            raise ValueError("Branch mapping files overlap")
        merged.update(data)
    return merged


def links(text):
    return Counter(re.findall(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)", text))


def compare_uc(before, after):
    old, new = uc_functional(before), uc_functional(after)
    if set(new) != set(UC_SECTIONS):
        raise ValueError("UC section set differs from the supplied template")
    for heading, value in old.items():
        if heading not in ("Alternative Flow", "Exception Flow"):
            if squash(value) != squash(new[heading]):
                raise ValueError(f"UC content changed in {heading}")
            continue
        old_flows, new_flows = branch_blocks(value), branch_blocks(new[heading])
        if not old_flows and squash(value) != squash(new[heading]):
            raise ValueError(f"Empty branch section changed: {heading}")
        if len(old_flows) != len(new_flows):
            raise ValueError("UC branch count changed")
        for (old_id, old_title, old_body), (new_id, new_title, new_body) in zip(old_flows, new_flows):
            if old_id != new_id or (old_title and old_title != new_title):
                raise ValueError("UC branch identity changed")
            activities = lambda body: squash(re.sub(r"^\d+[a-z]*[.:] ", "", body, flags=re.M))
            if activities(old_body) != activities(new_body):
                raise ValueError("UC branch activity text changed")
            if re.search(r"^\d+\. ", new_body, re.M) or not new_title:
                raise ValueError("UC branch does not follow the supplied format")
            basic_count = len(re.findall(r"^\d+\. ", new["Basic Flow"], re.M))
            if any(not 1 <= int(n) <= basic_count for n in re.findall(r"^(\d+)[a-z]+: ", new_body, re.M)):
                raise ValueError("UC branch points outside Basic Flow")
    if "Notes" not in old and new["Notes"] != "None.":
        raise ValueError("An added Notes section must state None.")
    for section in ("UML Model", "Business Rules"):
        if dict(sections(before, 2))[section] != dict(sections(after, 2))[section]:
            raise ValueError(f"{section} content changed")


def compare_api(before, after):
    old, new = sections(before, 2), sections(after, 2)
    if "Path Parameter(s)" not in dict(old):
        location = next(i for i, (name, _) in enumerate(old) if name in ("Query Parameter(s)", "Request Body"))
        old.insert(location, ("Path Parameter(s)", "None."))
    if [name for name, _ in old] != [name for name, _ in new]:
        raise ValueError("API sections/status codes changed")
    for (section, old_body), (_, new_body) in zip(old, new):
        if section in ("General Information", "Notes") or not sections(old_body, 3):
            if squash(old_body) != squash(new_body):
                raise ValueError(f"API section content changed: {section}")
            continue
        old_fields, new_fields = sections(old_body, 3), sections(new_body, 3)
        if squash(old_body[:old_body.index("### ")]) != squash(new_body[:new_body.index("### ")]):
            raise ValueError("API section introductory content changed")
        if len(old_fields) != len(new_fields):
            raise ValueError("API field count changed")
        for (old_name, old_value), (new_name, new_value) in zip(old_fields, new_fields):
            if field_name(old_name, section) != new_name:
                raise ValueError("API field identity changed")
            old_text, old_meta = field_parts(old_value)
            new_text, new_meta = field_parts(new_value)
            if old_text != new_text or any(new_meta.get(key) != value for key, value in old_meta.items()):
                raise ValueError(f"API field values changed: {section}/{old_name}")
            if any(value != UNSPECIFIED for key, value in new_meta.items() if key not in old_meta):
                raise ValueError("An added API label invents a value")
            if not {"Type", "Required", "Nullable", "Trigger", "Description", "Example"} <= new_meta.keys():
                raise ValueError("API field lacks a required template label")


def compare_ocl(before, after):
    old_header, old_body = metadata_header(before)
    old_body = re.sub(r"^# OCL Utility Semantics$", "# OCL Utility Definitions", old_body, count=1, flags=re.M)
    new_header, new_body = metadata_header(after)
    if new_header != "artifact_type: ocl-utility-definitions\nstatus: Frozen":
        raise ValueError("OCL header differs from the screenshot")
    source = [line for line in old_header.splitlines() if not line.startswith(("artifact_type:", "status:"))]
    suffix = "\n## Source Metadata\n\n~~~yaml\n" + "\n".join(source) + "\n~~~\n" if source else ""
    if new_body != old_body.rstrip() + "\n" + suffix:
        raise ValueError("OCL utility content or source provenance changed")


def compare(path, before_bytes, after_bytes, document_kind):
    before, after = decode(before_bytes), decode(after_bytes)
    if document_kind in ("uc", "api"):
        if title(before) != title(after):
            raise ValueError("Specification identity changed")
        old_header, _ = metadata_header(before)
        new_header, _ = metadata_header(after)
        if re.sub(r"^status:.*$", "status: Frozen", old_header, flags=re.M) != new_header:
            raise ValueError("Non-status specification metadata changed")
        if fences(before_bytes.decode("utf-8-sig")) != fences(after_bytes.decode("utf-8-sig")):
            raise ValueError("Code block language/body bytes changed")
        (compare_uc if document_kind == "uc" else compare_api)(before, after)
    else:
        compare_ocl(before, after)
    if links(before) != links(after):
        raise ValueError("Reference targets changed")


def snapshot():
    if MANIFEST.exists():
        raise ValueError("The baseline already exists; it must not be replaced")
    AUDIT.mkdir(parents=True, exist_ok=True)
    records = {}
    with zipfile.ZipFile(AUDIT / "before.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for package in packages():
            for path in sorted(package.rglob("*")):
                if not path.is_file():
                    continue
                data = path.read_bytes()
                records[relative(path)] = {"sha256_before": sha(data), "kind": kind(path)}
                archive.writestr(relative(path), data)
    manifest = {"created_local": "2026-10-07", "template": str(TEMPLATE),
                "template_sha256": sha(TEMPLATE.read_bytes()), "files": records}
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"snapshot_files": len(records), "active_documents": sum(bool(r["kind"]) for r in records.values())}))


def plan(manifest):
    branch_map = maps()
    planned = {}
    with zipfile.ZipFile(AUDIT / "before.zip") as archive:
        for name, record in manifest["files"].items():
            document_kind = record["kind"]
            if not document_kind:
                continue
            path = ROOT / name
            original = archive.read(name)
            before = decode(original)
            if document_kind == "uc":
                formatted = format_uc(before, branch_map.get(name, {}))
            else:
                formatted = (format_api if document_kind == "api" else format_ocl)(before)
            if document_kind == "ocl":
                newline = "\r\n" if b"\r\n" in original else "\n"
                encoded = formatted.replace("\n", newline).encode("utf-8")
                if original.startswith(b"\xef\xbb\xbf"):
                    encoded = b"\xef\xbb\xbf" + encoded
            else:
                encoded = encode_formatted(original, formatted)
            try:
                compare(path, original, encoded, document_kind)
            except ValueError as error:
                raise ValueError(f"{name}: {error}") from error
            planned[name] = encoded
    return planned


def verify(manifest):
    counts = Counter()
    per_package = defaultdict(Counter)
    baseline_broken_links = []
    with zipfile.ZipFile(AUDIT / "before.zip") as archive:
        for name, record in manifest["files"].items():
            path = ROOT / name
            original = archive.read(name)
            current = path.read_bytes()
            if sha(original) != record["sha256_before"]:
                raise ValueError(f"Snapshot hash mismatch: {name}")
            if not record["kind"]:
                if sha(current) != record["sha256_before"]:
                    raise ValueError(f"Protected file changed: {name}")
                counts["protected_files"] += 1
                continue
            compare(path, original, current, record["kind"])
            if sha(current) != record.get("sha256_after"):
                raise ValueError(f"Formatted hash mismatch: {name}")
            counts[record["kind"]] += 1
            per_package[Path(name).parts[0]][record["kind"]] += 1
            if record["kind"] == "uc":
                counts["preserved_uml_and_rule_blocks"] += len(fences(decode(original)))
                counts["formatted_branches"] += sum(len(branch_blocks(uc_functional(decode(current))[section])) for section in ("Alternative Flow", "Exception Flow"))
            for target in links(decode(current)):
                if re.match(r"^[a-z]+://|^#", target, re.I):
                    continue
                target_path = unquote(target.split("#", 1)[0]).strip("<>")
                if target_path and not (path.parent / target_path).exists():
                    baseline_broken_links.append({"file": name, "target": target})
    result = {"status": "PASS", "checks": dict(counts),
              "packages": {name: dict(values) for name, values in sorted(per_package.items())},
              "pre_existing_missing_link_targets": baseline_broken_links,
              "scope": "Template presentation and source preservation; no domain-policy or database changes."}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--snapshot", action="store_true")
    action.add_argument("--check-plan", action="store_true")
    action.add_argument("--apply", action="store_true")
    action.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.snapshot:
        snapshot()
        return
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if sha(TEMPLATE.read_bytes()) != manifest["template_sha256"]:
        raise ValueError("The supplied template changed after the snapshot")
    if args.check_plan or args.apply:
        planned = plan(manifest)
        if args.check_plan:
            print(json.dumps({"planned_documents": len(planned), "status": "PASS"}))
            return
        for name, data in planned.items():
            record = manifest["files"][name]
            if sha((ROOT / name).read_bytes()) not in {record["sha256_before"], record.get("sha256_after")}:
                raise ValueError(f"File changed since snapshot; cannot overwrite: {name}")
        for name, data in planned.items():
            (ROOT / name).write_bytes(data)
            manifest["files"][name]["sha256_after"] = sha(data)
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = verify(manifest)
    (AUDIT / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
