#!/usr/bin/env python3
"""Validate the public Tilda migration skill without third-party packages."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "SKILL.md",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "PUBLISHING.md",
    "agents/openai.yaml",
    "examples/migration-config.example.yaml",
    "references/phase-gates.md",
    "references/project-adapter.md",
    "scripts/validate.py",
    ".github/workflows/validate.yml",
)
TEXT_SUFFIXES = {"", ".md", ".py", ".yaml", ".yml", ".txt"}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(relative_path: str) -> str:
    path = ROOT / relative_path
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        fail(f"cannot read {relative_path}: {exc}")


def parse_scalar_yaml_mapping(text: str) -> dict[str, str]:
    """Parse key/value lines while preserving raw scalar syntax."""
    result: dict[str, str] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([A-Za-z0-9_-]+):\s*(.*)", line)
        if not match:
            fail(f"unsupported frontmatter syntax on line {line_number}")
        key, raw_value = match.groups()
        if key in result:
            fail(f"duplicate frontmatter key: {key}")
        result[key] = raw_value.strip()
    return result


def decode_yaml_string(raw_value: str, key: str, *, allow_plain: bool = False) -> str:
    """Decode the narrow YAML string subset accepted by this package."""
    if raw_value.startswith('"'):
        try:
            value = json.loads(raw_value)
        except json.JSONDecodeError as exc:
            fail(f"invalid quoted value for {key}: {exc}")
        if not isinstance(value, str):
            fail(f"{key} must be a string")
        return value

    if not allow_plain:
        fail(f"{key} must be a quoted string")

    lowered = raw_value.casefold()
    yaml_non_strings = {
        "",
        "~",
        "null",
        "true",
        "false",
        "yes",
        "no",
        "on",
        "off",
    }
    if lowered in yaml_non_strings or raw_value[0] in "[{!&*|>":
        fail(f"{key} must be an unambiguous string")
    if re.fullmatch(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", raw_value):
        fail(f"{key} must not be numeric")
    return raw_value


def validate_skill() -> None:
    content = read_text("SKILL.md")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", content, re.DOTALL)
    if not match:
        fail("SKILL.md must start with valid YAML frontmatter")

    raw_frontmatter = parse_scalar_yaml_mapping(match.group(1))
    allowed = {"name", "description"}
    unexpected = set(raw_frontmatter) - allowed
    if unexpected:
        fail(f"unexpected SKILL.md frontmatter keys: {sorted(unexpected)}")

    if "name" not in raw_frontmatter or "description" not in raw_frontmatter:
        fail("SKILL.md requires name and description")
    name = decode_yaml_string(raw_frontmatter["name"], "name", allow_plain=True)
    description = decode_yaml_string(raw_frontmatter["description"], "description")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail("skill name must use lowercase hyphen-case")
    if len(name) > 64:
        fail("skill name exceeds 64 characters")
    if not description.strip():
        fail("skill description is required")
    if len(description) > 1024 or "<" in description or ">" in description:
        fail("skill description violates length or character constraints")
    if "[TODO:" in content:
        fail("SKILL.md contains an unfinished scaffold placeholder")


def parse_openai_interface(content: str) -> dict[str, str]:
    """Validate the exact interface-only openai.yaml schema used here."""
    lines = [line for line in content.splitlines() if line.strip()]
    if not lines or lines[0] != "interface:":
        fail("agents/openai.yaml must start with an interface mapping")

    allowed = {
        "display_name",
        "short_description",
        "default_prompt",
        "icon_small",
        "icon_large",
        "brand_color",
    }
    interface: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:], start=2):
        match = re.fullmatch(r"  ([a-z_]+):\s*(.+)", line)
        if not match:
            fail(f"invalid interface mapping on openai.yaml line {line_number}")
        key, raw_value = match.groups()
        if key not in allowed:
            fail(f"unexpected interface key: {key}")
        if key in interface:
            fail(f"duplicate interface key: {key}")
        interface[key] = decode_yaml_string(raw_value, f"interface.{key}")
    return interface


def validate_openai_metadata() -> None:
    interface = parse_openai_interface(read_text("agents/openai.yaml"))
    required = {"display_name", "short_description", "default_prompt"}
    missing = required - set(interface)
    if missing:
        fail(f"agents/openai.yaml is missing interface keys: {sorted(missing)}")
    if not 25 <= len(interface["short_description"]) <= 64:
        fail("interface.short_description must contain 25 to 64 characters")
    if "$tilda-v4-migration" not in interface["default_prompt"]:
        fail("interface.default_prompt must mention $tilda-v4-migration")


def validate_links() -> None:
    markdown_link = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        for raw_target in markdown_link.findall(content):
            target = raw_target.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(f"link escapes the package: {path.relative_to(ROOT)} -> {raw_target}")
            if not resolved.exists():
                fail(f"broken link: {path.relative_to(ROOT)} -> {raw_target}")


def validate_public_hygiene() -> None:
    high_confidence_secret_patterns = {
        "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
        "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
        "Slack token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    }
    local_path_patterns = (
        re.compile(r"/(?:Users|Volumes)/[^\s`]+"),
        re.compile(r"[A-Za-z]:\\Users\\[^\s`]+"),
    )

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            fail(f"unexpected non-text artifact: {path.relative_to(ROOT)}")
        content = path.read_text(encoding="utf-8")
        for label, pattern in high_confidence_secret_patterns.items():
            if pattern.search(content):
                fail(f"possible {label} in {path.relative_to(ROOT)}")
        for pattern in local_path_patterns:
            if pattern.search(content):
                fail(f"absolute local path in {path.relative_to(ROOT)}")


def main() -> None:
    missing = [relative for relative in REQUIRED_FILES if not (ROOT / relative).is_file()]
    if missing:
        fail(f"missing required files: {', '.join(missing)}")

    validate_skill()
    validate_openai_metadata()
    validate_links()
    validate_public_hygiene()

    if os.name != "nt" and not os.access(ROOT / "scripts/validate.py", os.X_OK):
        fail("scripts/validate.py must be executable")

    print("PASS: public skill package is structurally valid")


if __name__ == "__main__":
    main()
