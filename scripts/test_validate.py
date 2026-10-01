#!/usr/bin/env python3
"""Negative security tests for the dependency-free package validator."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path


VALIDATOR_PATH = Path(__file__).with_name("validate.py")
SPEC = importlib.util.spec_from_file_location("skill_validator", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load package validator")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidatorSecurityTests(unittest.TestCase):
    def assert_rejected(self, callback) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                callback()
        self.assertEqual(raised.exception.code, 1)

    def test_rejects_invalid_openai_yaml(self) -> None:
        self.assert_rejected(lambda: VALIDATOR.parse_openai_interface("interface: [\n"))

    def test_rejects_missing_interface_mapping(self) -> None:
        self.assert_rejected(
            lambda: VALIDATOR.parse_openai_interface(
                'unrelated:\n  display_name: "Not an interface"\n'
            )
        )

    def test_rejects_duplicate_interface_key(self) -> None:
        self.assert_rejected(
            lambda: VALIDATOR.parse_openai_interface(
                'interface:\n  display_name: "One"\n  display_name: "Two"\n'
            )
        )

    def test_rejects_boolean_description(self) -> None:
        raw = VALIDATOR.parse_scalar_yaml_mapping(
            "name: valid-name\ndescription: false"
        )
        self.assert_rejected(
            lambda: VALIDATOR.decode_yaml_string(raw["description"], "description")
        )

    def test_rejects_mutable_action_tag(self) -> None:
        original_read_text = VALIDATOR.read_text
        workflow = original_read_text(".github/workflows/validate.yml")
        insecure = workflow.replace(
            "actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
            "actions/checkout@v4",
        )
        VALIDATOR.read_text = (
            lambda relative: insecure
            if relative == ".github/workflows/validate.yml"
            else original_read_text(relative)
        )
        try:
            self.assert_rejected(VALIDATOR.validate_workflow_security)
        finally:
            VALIDATOR.read_text = original_read_text

    def test_rejects_pull_request_target(self) -> None:
        original_read_text = VALIDATOR.read_text
        workflow = original_read_text(".github/workflows/validate.yml")
        insecure = workflow.replace("  pull_request:\n", "  pull_request_target:\n")
        VALIDATOR.read_text = (
            lambda relative: insecure
            if relative == ".github/workflows/validate.yml"
            else original_read_text(relative)
        )
        try:
            self.assert_rejected(VALIDATOR.validate_workflow_security)
        finally:
            VALIDATOR.read_text = original_read_text

    def test_rejects_unsupported_frontmatter(self) -> None:
        original_read_text = VALIDATOR.read_text
        valid_skill = original_read_text("SKILL.md")
        invalid_skill = valid_skill.replace(
            "\n---\n", "\nmetadata: [\n---\n", 1
        )
        VALIDATOR.read_text = (
            lambda relative: invalid_skill
            if relative == "SKILL.md"
            else original_read_text(relative)
        )
        try:
            self.assert_rejected(VALIDATOR.validate_skill)
        finally:
            VALIDATOR.read_text = original_read_text

    @unittest.skipIf(os.name == "nt", "symlink permissions vary on Windows")
    def test_rejects_symbolic_links(self) -> None:
        original_root = VALIDATOR.ROOT
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "target.txt").write_text("safe", encoding="utf-8")
            (root / "linked.txt").symlink_to(root / "target.txt")
            VALIDATOR.ROOT = root
            try:
                self.assert_rejected(VALIDATOR.validate_public_hygiene)
            finally:
                VALIDATOR.ROOT = original_root

    def test_scans_validator_source_for_secrets(self) -> None:
        original_root = VALIDATOR.ROOT
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake_token = "gh" + "p_" + ("A" * 24)
            (root / "validate.py").write_text(fake_token, encoding="utf-8")
            VALIDATOR.ROOT = root
            try:
                self.assert_rejected(VALIDATOR.validate_public_hygiene)
            finally:
                VALIDATOR.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
