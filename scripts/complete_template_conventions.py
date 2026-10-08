"""Apply the user's 2026-10-07 identifier and presentation corrections.

The immutable audit baseline includes the working tree, not only Git HEAD.
API metadata and utility semantics are completed separately before this pass.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from format_tripma import sections

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "format-audit/template-completion"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def write(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def remove_inline_ticks(text: str) -> str:
    # The supplied utility template keeps Markdown code fences.
    return "\n".join(
        line if re.match(r"^\s*(?:`{3,}|~{3,})", line)
        else re.sub(r"(?<!`)`{1,2}(?!`)", "", line)
        for line in text.split("\n")
    )


def words(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    value = re.sub(r"([A-Z])([A-Z][a-z])", r"\1 \2", value)
    return value.replace("_", " ").strip()


def format_rules(text: str) -> str:
    prefix, business = text.split("## Business Rules", 1)
    # Only actual prose bullets are removed. Operators, UML arrows and member
    # visibility symbols are part of the formal model and remain intact.
    uml_start = prefix.index("## UML Model")
    prefix = prefix[:uml_start] + re.sub(
        r"^([ \t]*)-\s+", r"\1", prefix[uml_start:], flags=re.M
    )

    def block(match: re.Match) -> str:
        language, body = match[2].strip(), match[3]
        if language != "ocl":
            body = re.sub(r"^(BR-[A-Z0-9-]+):\s*", r"\1 - ", body, flags=re.M)
            body = re.sub(r"^([ \t]*)-\s+", r"\1", body, flags=re.M)
            return "~~~" + language + "\n" + body.rstrip() + "\n~~~"
        identity = re.search(r"^[ \t]*--[ \t]*(BR-[A-Z0-9-]+)(?:[ \t]*[-:][ \t]*(.*))?$", body, re.M)
        if identity is None:
            raise ValueError("A rule block has no rule identity")
        rule_id = identity[1]
        named = re.search(r"^(?:pre|post|inv|def)\s+" + re.escape(rule_id.replace("-", "_")) + r"_([^:\n]+):", body, re.M)
        label = identity[2] or (words(named[1]) if named else " ".join(rule_id.split("-")[1:-1]).title())
        metadata = []
        expression = []
        for line in body.splitlines():
            comment = re.match(r"^\s*--\s*(.*)$", line)
            if comment:
                value = comment[1]
                if value.startswith(rule_id):
                    continue
                metadata.append(value if re.match(r"(?:Source|Assumption|Note):", value) else "Note: " + value)
            else:
                expression.append(line)
        expression_text = "\n".join(expression).strip("\n")
        return "~~~text\n" + rule_id + " - " + label + "\n" + "\n".join(metadata) + "\n" + expression_text + "\n~~~"

    business = re.sub(r"(?m)^(`{3,}|~{3,})([^\n]*)\n(.*?)^\1[ \t]*$", block, business, flags=re.S)
    business = re.sub(r"^([ \t]*)-\s+", r"\1", business, flags=re.M)
    return prefix + "## Business Rules" + business


def package_aliases(entries: list[dict]) -> dict[str, dict[str, str]]:
    aliases: dict[str, dict[str, str]] = {}
    for entry in entries:
        package = Path(entry["path"]).parts[0]
        mapping = aliases.setdefault(package, {})
        if entry["kind"] == "api":
            old, new = entry["old_api_id"], entry["api_id"]
            if old != new:
                mapping[old] = new
            old_filename = Path(entry["path"]).name
            new_filename = Path(entry["new_path"]).name
            if old_filename != new_filename:
                mapping[old_filename] = new_filename
        else:
            for old, new in entry["br_id_mapping"].items():
                if old != new:
                    mapping[old] = new
                    mapping[old.replace("-", "_")] = new.replace("-", "_")
    return aliases


def replace_aliases(text: str, mapping: dict[str, str]) -> str:
    if not mapping:
        return text
    # Match all source values at once so an alias cannot rewrite another alias.
    pattern = re.compile("|".join(re.escape(key) for key in sorted(mapping, key=len, reverse=True)))
    return pattern.sub(lambda match: mapping[match[0]], text)


def complete_reverse_associations(entries: list[dict]) -> list[dict]:
    edges: dict[tuple[str, str], set[str]] = {}
    for entry in entries:
        if entry["kind"] != "uc":
            continue
        package = Path(entry["new_path"]).parts[0]
        data = dict(sections(dict(sections(read(ROOT / entry["new_path"]), 2))["Functional Use-Case Specification"], 3))
        for api_id in re.findall(r"\bAPI-[A-Z0-9-]+\b", data["Related API IDs"]):
            edges.setdefault((package, api_id), set()).add(entry["uc_id"])
    additions = []
    for entry in entries:
        if entry["kind"] != "api":
            continue
        path = ROOT / entry["new_path"]
        text = read(path)
        package = Path(entry["new_path"]).parts[0]
        info = dict(sections(dict(sections(text, 2))["General Information"], 3))
        previous = set(re.findall(r"\bUC-\d+\b", info["Related Use Case IDs"]))
        related = previous | edges.get((package, entry["api_id"]), set())
        if related == previous:
            continue
        ordered = sorted(related, key=lambda value: int(value.split("-")[1]))
        text = re.sub(r"^related_uc_ids?:.*$", "related_uc_ids: " + json.dumps(ordered), text, count=1, flags=re.M)
        text = re.sub(r"(^### Related Use Case IDs\n).*?(?=^### |^## |\Z)",
                      lambda match: match[1] + "\n" + ", ".join(ordered) + "\n\n",
                      text, count=1, flags=re.M | re.S)
        write(path, text)
        additions.append({"file": entry["new_path"], "previous_related_uc_ids": sorted(previous),
                          "related_uc_ids": ordered, "added_reverse_uc_ids": sorted(related - previous)})
    return additions


def apply() -> None:
    plan = json.loads(read(AUDIT / "naming-plan.json"))
    entries = plan["entries"]
    aliases = package_aliases(entries)
    active = {entry["path"]: entry for entry in entries}
    changed_support = []
    for package, mapping in aliases.items():
        for path in (ROOT / package).rglob("*.md"):
            if any(part in {"source", "evidence", "scripts"} for part in path.relative_to(ROOT / package).parts):
                continue
            relative = path.relative_to(ROOT).as_posix()
            before = read(path)
            after = replace_aliases(before, mapping)
            entry = active.get(relative)
            if entry:
                after = remove_inline_ticks(after)
                if entry["kind"] == "uc":
                    after = format_rules(after)
                    match = re.search(r"(^### Related API IDs\n)(.*?)(?=^### |^## |\Z)", after, re.M | re.S)
                    if match and not re.search(r"API-[A-Z0-9-]+", match[2]):
                        explanation = re.sub(r"^None[.]?\s*", "", match[2].strip()).strip()
                        after = after[:match.start(2)] + "\nNone\n\n" + after[match.end(2):]
                        if explanation:
                            notes = re.search(r"(^### Notes\n)(.*?)(?=^### |^## |\Z)", after, re.M | re.S)
                            if notes and explanation not in notes[2]:
                                after = after[:notes.end(2)] + explanation + "\n\n" + after[notes.end(2):]
                else:
                    info = dict(sections(dict(sections(after, 2))["General Information"], 3))
                    after = re.sub(r"^# API-[A-Z0-9-]+: .+$", "# " + entry["api_id"] + ": " + info["API Name"].strip(), after, count=1, flags=re.M)
            elif before != after:
                changed_support.append(relative)
            if before != after:
                write(path, after)
        for entry in entries:
            if entry["kind"] != "api" or Path(entry["path"]).parts[0] != package:
                continue
            source, target = ROOT / entry["path"], ROOT / entry["new_path"]
            if source.as_posix() == target.as_posix():
                continue
            # An intermediate name also makes case-only renames reliable on NTFS.
            temporary = source.with_name(source.name + ".__template_rename__")
            if temporary.exists():
                raise ValueError("Rename temporary already exists: " + str(temporary))
            if target.exists() and source.resolve() != target.resolve() and source.name.lower() != target.name.lower():
                raise ValueError("API filename collision: " + str(target))
            source.rename(temporary)
            temporary.rename(target)
    reverse_associations = complete_reverse_associations(entries)
    (AUDIT / "applied-manifest.json").write_text(json.dumps({
        "date": "2026-10-07", "entries": entries,
        "changed_supporting_markdown": sorted(changed_support),
        "package_aliases": aliases,
        "reverse_association_additions": reverse_associations,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Applied naming and presentation to {len(entries)} active specifications; {len(changed_support)} supporting documents updated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", required=True)
    parser.parse_args()
    if (AUDIT / "applied-manifest.json").exists():
        raise SystemExit("This migration has already been applied. Use scripts/verify_template_completion.py.")
    apply()
