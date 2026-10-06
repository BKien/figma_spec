"""Apply Tripma's document presentation with a verifiable, lossless baseline.

Only active UC/API Markdown is rewritten. Domain expressions and all other
package files are frozen. The audit compares each section independently, so
moving Related UI/APIs/Notes ahead of UML cannot hide a missing section.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote
import zipfile

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "format-audit" / "tripma-format"
UC_NAMES = {
    "Actors": "Actor(s)",
    "Preconditions": "Pre-Condition(s)",
    "Postconditions": "Post-Condition(s)",
    "Alternative Flows": "Alternative Flow",
    "Exception Flows": "Exception Flow",
    "Related APIs": "Related API IDs",
}
API_NAMES = {
    "Request Headers": "Request Header(s)",
    "Path Parameters": "Path Parameter(s)",
    "Query Parameters": "Query Parameter(s)",
}
UC_ORDER = [
    "Description", "Actors", "Priority", "Trigger", "Preconditions",
    "Postconditions", "Basic Flow", "Alternative Flows", "Exception Flows",
    "Related UI", "Related APIs", "Notes", "UML Model", "Business Rules",
]
API_GENERAL = [
    "API ID", "API Name", "Related Use Case IDs", "Method", "Path",
    "Description", "Authentication", "Authorization",
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode(data: bytes) -> str:
    return data.decode("utf-8-sig").replace("\r\n", "\n")


def sections(text: str, level: int) -> list[tuple[str, str]]:
    """Read headings outside fences; never interpret code as document structure."""
    found = []
    fence = None
    offset = 0
    for line in text.splitlines(keepends=True):
        fence_match = re.match(r"^(`{3,}|~{3,})(.*)$", line.rstrip("\n"))
        if fence_match:
            marker = fence_match.group(1)
            if fence is None:
                fence = marker[0]
            elif marker[0] == fence:
                fence = None
        elif fence is None:
            match = re.match(r"^" + "#" * level + r" (.+)\n?$", line)
            if match:
                found.append((match.group(1), offset, offset + len(line)))
        offset += len(line)
    return [(name, text[start:(found[i+1][1] if i+1 < len(found) else len(text))].strip("\n"))
            for i, (name, _, start) in enumerate(found)]


def title(text: str) -> tuple[str, str]:
    match = re.search(r"^# ((?:UC|API)-[A-Z0-9-]+)(?: — |: )(.+)$", text, re.M)
    if not match:
        raise ValueError("Unrecognized specification title")
    return match.group(1), match.group(2)


def fences(text: str) -> list[tuple[str, str]]:
    result = []
    language = None
    marker = None
    body = []
    for line in text.splitlines(keepends=True):
        match = re.match(r"^(`{3,}|~{3,})([^\n]*)\n?$", line)
        if language is None and match:
            marker = match.group(1)[0]
            language = match.group(2).strip()
            body = []
        elif language is not None and match and match.group(1)[0] == marker:
            result.append((language, "".join(body)))
            language = None
        elif language is not None:
            body.append(line)
    if language is not None:
        raise ValueError("Unclosed Markdown fence")
    return result


def tripma_fences(text: str) -> str:
    # Preserve fence language and every body byte, changing only the delimiter.
    return re.sub(r"^```([^\n]*)$", r"~~~\1", text, flags=re.M)


def encode_formatted(original: bytes, text: str) -> bytes:
    """Preserve even mixed original line endings inside code block bodies."""
    newline = "\r\n" if b"\r\n" in original else "\n"
    encoded = text.replace("\n", newline).encode("utf-8")
    pattern = re.compile(
        rb"^(?P<marker>`{3,}|~{3,})(?P<language>[^\r\n]*)\r?\n"
        rb"(?P<body>.*?)(?P<closing>^(?P=marker)[ \t]*\r?$)",
        re.M | re.S,
    )
    before = list(pattern.finditer(original))
    after = list(pattern.finditer(encoded))
    if len(before) != len(after):
        raise ValueError("Code block count changed during byte preservation")
    for old, new in reversed(list(zip(before, after))):
        if old["language"].strip() != new["language"].strip():
            raise ValueError("Code block language changed")
        if old["body"].replace(b"\r\n", b"\n") != new["body"].replace(b"\r\n", b"\n"):
            raise ValueError("Code block content changed")
        encoded = encoded[:new.start("body")] + old["body"] + encoded[new.end("body"):]
    if original.startswith(b"\xef\xbb\xbf"):
        encoded = b"\xef\xbb\xbf" + encoded
    return encoded


def uc_body(name: str, body: str, aliases: list[dict], uc_id: str) -> str:
    if name == "Trigger":
        def trigger(match):
            aliases.append({"old": match.group(1), "new": f"{uc_id}/Trigger"})
            return ""
        body = re.sub(r"\*\*(TRG-UC-\d{2}-\d{2})\*\* — ", trigger, body)
    elif name in ("Preconditions", "Postconditions"):
        def condition(match):
            old, kind, number = match.group(1), match.group(2), int(match.group(3))
            new = f"{kind}-{number}"
            aliases.append({"old": old, "new": new})
            return new + ": "
        body = re.sub(r"^- \*\*((PRE|POST)-UC-\d{2}-(\d{2}))\*\* — ", condition, body, flags=re.M)
    elif name in ("Alternative Flows", "Exception Flows"):
        def flow(match):
            old, kind, number = match.group(1), match.group(2), int(match.group(3))
            new = f"{kind}-{number}"
            aliases.append({"old": old, "new": new})
            # The source supplies no branch name or Basic Flow anchor.
            # Do not invent either; retain every original activity number.
            return new + ":"
        body = re.sub(r"^#### ((AF|EF)-UC-\d{2}-(\d{2}))$", flow, body, flags=re.M)
    return tripma_fences(body)


def format_uc(text: str) -> tuple[str, list[dict]]:
    uc_id, name = title(text)
    data = dict(sections(text, 3))
    if set(data) - set(UC_ORDER) or not (set(UC_ORDER) - {"Notes"}) <= set(data):
        raise ValueError(f"Unexpected UC sections: {uc_id}")
    aliases = []
    output = ["---", "artifact_type: business-use-case-specification", 'status: "Draft"',
              f"uc_id: {uc_id}", f"uc_name: {json.dumps(name, ensure_ascii=False)}", "---", "",
              f"# {uc_id}: {name}", "", "## Functional Use-Case Specification", "",
              "### Use Case ID", "", uc_id, "", "### Use Case Name", "", name, ""]
    for section in UC_ORDER:
        if section not in data:
            continue
        level = "##" if section in ("UML Model", "Business Rules") else "###"
        output += [f"{level} {UC_NAMES.get(section, section)}", "",
                   uc_body(section, data[section], aliases, uc_id), ""]
    return "\n".join(output).rstrip() + "\n", aliases


def api_body(body: str) -> str:
    result = []
    fenced = False
    for line in body.splitlines():
        if re.match(r"^(`{3,}|~{3,})", line):
            fenced = not fenced
            line = re.sub(r"^```", "~~~", line)
        elif not fenced:
            line = re.sub(r"^### `([^`]+)`$", r"### \1", line)
            # Field metadata is rendered as plain sequential labels by Tripma.
            line = re.sub(r"^- ((?:Type|Format|Required|Nullable|Default|Allowed values?|Validation|Trigger|Description|Example|Note):)", r"\1", line)
        result.append(line)
    return "\n".join(result)


def format_api(text: str) -> str:
    api_id, name = title(text)
    data = sections(text, 2)
    if [name for name, _ in data[:8]] != API_GENERAL:
        raise ValueError(f"Unexpected API general information: {api_id}")
    related = sorted(set(re.findall(r"\bUC-\d{2}\b", dict(data)["Related Use Case IDs"])))
    related_meta = (f"related_uc_id: {related[0]}" if len(related) == 1
                    else "related_uc_ids: " + json.dumps(related))
    output = ["---", "artifact_type: api-contract", "status: Draft", f"api_id: {api_id}",
              related_meta, "---", "", f"# {api_id}: {name}", "", "## General Information", ""]
    for index, (section, body) in enumerate(data):
        level = "###" if index < 8 else "##"
        output += [f"{level} {API_NAMES.get(section, section)}", "", api_body(body), ""]
    return "\n".join(output).rstrip() + "\n"


def payload(text: str) -> str:
    """Ignore known presentation markers, never whitespace/characters in code."""
    result = []
    fenced = False
    for line in text.splitlines():
        if re.match(r"^(`{3,}|~{3,})", line):
            fenced = not fenced
            result.append(re.sub(r"^(`{3,}|~{3,})", "~~~", line))
            continue
        if not fenced:
            if not line.strip():
                continue
            line = re.sub(r"^\*\*TRG-UC-\d{2}-\d{2}\*\* — ", "", line)
            line = re.sub(r"^- \*\*(PRE|POST)-UC-\d{2}-(\d{2})\*\* — ", lambda m: f"{m[1]}-{int(m[2])}: ", line)
            line = re.sub(r"^#### (AF|EF)-UC-\d{2}-(\d{2})$", lambda m: f"{m[1]}-{int(m[2])}:", line)
            line = re.sub(r"^### `([^`]+)`$", r"### \1", line)
            line = re.sub(r"^- ((?:Type|Format|Required|Nullable|Default|Allowed values?|Validation|Trigger|Description|Example|Note):)", r"\1", line)
        result.append(line)
    return "\n".join(result)


def semantic_sections(text: str, kind: str, formatted: bool) -> list[tuple[str, str]]:
    if kind == "uc":
        data = sections(text, 3)
        if formatted:
            data = [(name, body) for name, body in data if name not in ("Use Case ID", "Use Case Name")]
            # H3 Notes ends where the next H2 UML starts, rather than at another H3.
            functional = sections(text, 2)[0][1]
            data = sections(functional, 3)
            data = [(name, body) for name, body in data if name not in ("Use Case ID", "Use Case Name")]
            data += [(name, body) for name, body in sections(text, 2) if name in ("UML Model", "Business Rules")]
        reverse = {new: old for old, new in UC_NAMES.items()}
        return sorted((reverse.get(name, name), payload(body)) for name, body in data)
    data = sections(text, 2)
    if formatted:
        data = sections(data[0][1], 3) + data[1:]
    reverse = {new: old for old, new in API_NAMES.items()}
    return [(reverse.get(name, name), payload(body)) for name, body in data]


def broken_links(path: Path, text: str) -> list[str]:
    links = re.findall(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)", text)
    missing = []
    for target in links:
        if re.match(r"^[a-z]+://|^#", target, re.I):
            continue
        target_path = unquote(target.split("#", 1)[0]).strip("<>")
        if target_path and not (path.parent / target_path).exists():
            missing.append(target)
    return missing


def active_specs(packages: list[Path]) -> list[Path]:
    return sorted([f for package in packages
                   for pattern in ("01-inception/uc/uc-*.md", "01-inception/api/api-*.md")
                   for f in package.glob(pattern)])


def verify(manifest: dict) -> dict:
    checks = Counter()
    package_counts = {}
    failures = []
    with zipfile.ZipFile(AUDIT / "before.zip") as archive:
        for relative, record in manifest["files"].items():
            path = ROOT / relative
            before_bytes = archive.read(relative)
            if sha(before_bytes) != record["sha256_before"]:
                failures.append(f"Baseline hash mismatch: {relative}")
            if not path.is_file():
                failures.append(f"Missing file: {relative}")
                continue
            current = path.read_bytes()
            if "kind" not in record:
                if sha(current) != record["sha256_before"]:
                    failures.append(f"Protected file changed: {relative}")
                else:
                    checks["unchanged_files"] += 1
                continue
            before, after = decode(before_bytes), decode(current)
            kind = record["kind"]
            if title(before) != title(after):
                failures.append(f"Specification identity changed: {relative}")
            if semantic_sections(before, kind, False) != semantic_sections(after, kind, True):
                failures.append(f"Section content changed: {relative}")
            if fences(before_bytes.decode("utf-8-sig")) != fences(current.decode("utf-8-sig")):
                failures.append(f"Code block content changed: {relative}")
            if Counter(broken_links(path, before)) != Counter(broken_links(path, after)):
                failures.append(f"Relative link regression: {relative}")
            expected = format_uc(before)[0] if kind == "uc" else format_api(before)
            if expected != after:
                failures.append(f"Tripma presentation mismatch: {relative}")
            if sha(current) != record["sha256_after"]:
                failures.append(f"Formatted file hash mismatch: {relative}")
            checks[kind] += 1
            checks["code_blocks"] += len(fences(before))
            checks["business_rules"] += len(re.findall(r"^-- BR-UC-\d{2}-\d{2}$", before, re.M))
            counts = package_counts.setdefault(Path(relative).parts[0], Counter())
            counts[kind] += 1
    if failures:
        raise ValueError("\n".join(failures))
    checks["id_aliases"] = sum(len(record.get("aliases", [])) for record in manifest["files"].values())
    return {"status": "PASS", "checks": dict(checks),
            "packages": {name: dict(count) for name, count in sorted(package_counts.items())}}


def apply() -> None:
    if (AUDIT / "manifest.json").exists():
        raise ValueError("A baseline already exists. Use --verify; never replace the original baseline.")
    packages = sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "01-inception").is_dir())
    specs = active_specs([p for p in packages if p.name != "Tripma"])
    planned = {}
    # Build and compare every result before any package file is written.
    for path in specs:
        before = decode(path.read_bytes())
        kind = "uc" if path.name.startswith("uc-") else "api"
        after, aliases = format_uc(before) if kind == "uc" else (format_api(before), [])
        if semantic_sections(before, kind, False) != semantic_sections(after, kind, True):
            raise ValueError(f"Pre-write section preservation failed: {path}")
        if fences(before) != fences(after):
            raise ValueError(f"Pre-write code preservation failed: {path}")
        planned[path] = (after, kind, aliases)
    files = sorted(f for package in packages for f in package.rglob("*") if f.is_file())
    manifest = {"baseline": "Current workspace; includes pre-existing uncommitted changes.",
                "reference": "Tripma/01-inception", "created_local": datetime.now(timezone(timedelta(hours=7))).isoformat(timespec="seconds"),
                "files": {}}
    AUDIT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(AUDIT / "before.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            original = path.read_bytes()
            archive.writestr(relative, original)
            record = {"sha256_before": sha(original)}
            if path in planned:
                after, kind, aliases = planned[path]
                encoded = encode_formatted(original, after)
                record.update(kind=kind, aliases=aliases, sha256_after=sha(encoded))
                planned[path] = (encoded, kind, aliases)
            manifest["files"][relative] = record
    # Save the complete original snapshot and manifest before touching specs.
    (AUDIT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for path, (encoded, _, _) in planned.items():
        path.write_bytes(encoded)
    result = verify(manifest)
    (AUDIT / "verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.apply == args.verify:
        parser.error("Choose exactly one of --apply or --verify")
    if args.apply:
        apply()
    else:
        print(json.dumps(verify(json.loads((AUDIT / "manifest.json").read_text(encoding="utf-8"))), indent=2))
