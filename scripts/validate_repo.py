#!/usr/bin/env python3
"""Deterministic checks for the focused SA plugin."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {"architect", "adr", "hld", "flow", "interface", "data", "review", "method"}
EXPECTED_STANDARDS = {
    "adr.md",
    "core-flow.md",
    "data.md",
    "deployment-view.md",
    "diagrams.md",
    "hld.md",
    "interface.md",
    "operating-guardrails.md",
    "quality-bar.md",
    "review.md",
    "runtime-flow.md",
    "tailoring.md",
    "workflow.md",
}
EXPECTED_EXAMPLE_FILES = {
    "architecture-brief.md",
    "decisions/ADR-0001-async-order-intake.md",
    "hld/container-orders.puml",
    "hld/container-orders-catalogue.md",
    "flows/client-submit-express-order.puml",
    "interfaces/order-intake-api.yaml",
    "interfaces/order-intake-events.yaml",
    "data/data-design.md",
    "reviews/design-review-2026-03-14.md",
    "sa-config.yaml",
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def frontmatter_name(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"\A---\s*\n.*?^name:\s*([^\n]+)\n.*?^---\s*$", text, re.M | re.S)
    return match.group(1).strip() if match else None


def walk_values(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from walk_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_values(child)
    else:
        yield value


def resolve_json_pointer(document, pointer: str) -> bool:
    current = document
    for raw_part in pointer.removeprefix("#/").split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False
    return True


def main() -> int:
    errors: list[str] = []

    manifest_path = ROOT / ".claude-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid plugin manifest: {exc}", errors)
        manifest = {}

    if manifest.get("name") != "sa":
        fail("plugin name must be 'sa'", errors)
    if manifest.get("version") != "3.0.0":
        fail("plugin version must be 3.0.0", errors)

    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    actual_skills = {path.parent.name for path in skill_files}
    if actual_skills != EXPECTED_SKILLS:
        fail(
            f"skill surface mismatch: expected {sorted(EXPECTED_SKILLS)}, got {sorted(actual_skills)}",
            errors,
        )

    for path in skill_files:
        name = frontmatter_name(path)
        if name != path.parent.name:
            fail(f"{path.relative_to(ROOT)} frontmatter name is {name!r}", errors)

        text = path.read_text(encoding="utf-8")
        for raw_ref in re.findall(r"`(\.\./[^`]+\.(?:md|yaml))`", text):
            target = (path.parent / raw_ref).resolve()
            if not target.exists():
                fail(f"broken reference in {path.relative_to(ROOT)}: {raw_ref}", errors)

    standards_root = ROOT / "skills" / "method" / "standards"
    actual_standards = {path.name for path in standards_root.glob("*.md")}
    if actual_standards != EXPECTED_STANDARDS:
        missing = sorted(EXPECTED_STANDARDS - actual_standards)
        extra = sorted(actual_standards - EXPECTED_STANDARDS)
        fail(f"standards mismatch: missing={missing}, extra={extra}", errors)

    example_root = ROOT / "examples" / "express-lane"
    actual_example_files = {
        str(path.relative_to(example_root))
        for path in example_root.rglob("*")
        if path.is_file()
    }
    if actual_example_files != EXPECTED_EXAMPLE_FILES:
        missing = sorted(EXPECTED_EXAMPLE_FILES - actual_example_files)
        extra = sorted(actual_example_files - EXPECTED_EXAMPLE_FILES)
        fail(f"example mismatch: missing={missing}, extra={extra}", errors)

    review = example_root / "reviews" / "design-review-2026-03-14.md"
    review_text = review.read_text(encoding="utf-8")
    for referenced in re.findall(
        r"`((?:architecture-brief\.md|(?:decisions|hld|flows|interfaces|data)/[^`]+\.(?:md|puml|yaml)))`",
        review_text,
    ):
        if not (example_root / referenced).exists():
            fail(f"review references missing example file: {referenced}", errors)

    for diagram in example_root.rglob("*.puml"):
        text = diagram.read_text(encoding="utf-8")
        if text.count("@startuml") != 1 or text.count("@enduml") != 1:
            fail(f"unbalanced PlantUML markers: {diagram.relative_to(ROOT)}", errors)

    for markdown_path in ROOT.rglob("*.md"):
        if ".git" in markdown_path.parts:
            continue
        markdown_text = markdown_path.read_text(encoding="utf-8")
        for raw_link in re.findall(r"\]\(([^)]+)\)", markdown_text):
            link = raw_link.split("#", 1)[0].strip()
            if not link or "://" in link or link.startswith("mailto:"):
                continue
            target = (markdown_path.parent / link).resolve()
            if not target.exists():
                fail(
                    f"broken Markdown link in {markdown_path.relative_to(ROOT)}: {raw_link}",
                    errors,
                )

    try:
        import yaml  # type: ignore
    except ImportError:
        yaml = None
    if yaml is not None:
        for skill_path in skill_files:
            skill_text = skill_path.read_text(encoding="utf-8")
            frontmatter = skill_text.split("---", 2)[1]
            try:
                metadata = yaml.safe_load(frontmatter)
            except Exception as exc:
                fail(f"invalid frontmatter {skill_path.relative_to(ROOT)}: {exc}", errors)
                continue
            if not isinstance(metadata, dict) or not metadata.get("description"):
                fail(f"missing skill description: {skill_path.relative_to(ROOT)}", errors)

        for yaml_path in example_root.rglob("*.yaml"):
            try:
                document = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
            except Exception as exc:  # PyYAML exposes several parser exception types.
                fail(f"invalid YAML {yaml_path.relative_to(ROOT)}: {exc}", errors)
                continue
            for value in walk_values(document):
                if isinstance(value, str) and value.startswith("#/"):
                    if not resolve_json_pointer(document, value):
                        fail(
                            f"unresolved local reference {value} in {yaml_path.relative_to(ROOT)}",
                            errors,
                        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        f"OK: {len(skill_files)} skills, {len(actual_standards)} standards, plugin manifest, references, "
        f"{len(actual_example_files)} example files, diagrams and YAML"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
