from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import yaml

from scripts.validate import FORBIDDEN_MARKDOWN


ROOT = Path(__file__).resolve().parents[1]
TECHNIQUE_PATH = (
    ROOT
    / "matrix/tactics/TA0043-reconnaissance/techniques"
    / "NJT-0001-active-scanning/technique.yaml"
)
CHILD_ROOT = TECHNIQUE_PATH.parent / "subtechniques"

COMMON_FIELDS = {
    "schema_version",
    "type",
    "id",
    "name",
    "summary",
    "aliases",
    "definition_and_concept",
    "stealth_characteristics",
    "scope_boundary_definition",
    "application_scenarios_and_threat_model",
    "stealth_mechanisms",
    "defense",
    "evidence",
    "research",
    "lifecycle",
}


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class AuthoringContractTest(unittest.TestCase):
    def test_parent_and_child_schemas_share_the_common_contract(self) -> None:
        technique_schema = json.loads(
            (ROOT / "schemas/technique.schema.json").read_text(encoding="utf-8")
        )
        child_schema = json.loads(
            (ROOT / "schemas/subtechnique.schema.json").read_text(encoding="utf-8")
        )
        for field in COMMON_FIELDS:
            self.assertIn(field, technique_schema["properties"])
            self.assertIn(field, child_schema["properties"])
            self.assertIn(field, technique_schema["required"])
            self.assertIn(field, child_schema["required"])
        self.assertIn("classification", technique_schema["required"])
        self.assertIn("subtechnique_taxonomy", technique_schema["required"])
        self.assertIn("parent_ref", child_schema["required"])
        self.assertIn("lineage", child_schema["required"])

    def test_njt_0001_is_the_canonical_structural_exemplar(self) -> None:
        technique = load_yaml(TECHNIQUE_PATH)
        self.assertEqual(technique["schema_version"], "2.0.0")
        self.assertEqual(technique["id"], "NJT-0001")
        self.assertEqual(
            set(technique),
            COMMON_FIELDS | {"classification", "subtechnique_taxonomy"},
        )
        child_refs = technique["subtechnique_taxonomy"]["subtechnique_refs"]
        self.assertEqual(
            child_refs,
            [
                "NJS-0001-001",
                "NJS-0001-002",
                "NJS-0001-003",
                "NJS-0001-004",
                "NJS-0001-005",
            ],
        )

        children = {
            value["id"]: value
            for value in (
                load_yaml(path)
                for path in sorted(CHILD_ROOT.glob("*/subtechnique.yaml"))
            )
        }
        self.assertEqual(set(children), set(child_refs))
        for child_id, child in children.items():
            self.assertRegex(child_id, r"^NJS-0001-\d{3}$")
            self.assertEqual(child["parent_ref"], "NJT-0001")
            self.assertEqual(
                set(child),
                COMMON_FIELDS | {"parent_ref", "lineage"},
            )
            first = child["stealth_characteristics"]["paragraphs"][0]
            self.assertTrue(first["zh"].startswith(child["name"]["zh"]))
            self.assertTrue(first["en"].startswith(child["name"]["en"]))

        self.assertEqual(
            list(TECHNIQUE_PATH.parent.rglob("*.md")),
            [],
        )

    def test_mechanism_summaries_and_evidence_follow_the_contract(self) -> None:
        subjects = [load_yaml(TECHNIQUE_PATH)] + [
            load_yaml(path)
            for path in sorted(CHILD_ROOT.glob("*/subtechnique.yaml"))
        ]
        for subject in subjects:
            reference_refs = set(subject["evidence"]["reference_refs"])
            mechanism_refs = []
            for mapping in subject["stealth_mechanisms"]:
                mechanism_refs.append(mapping["mechanism_ref"])
                self.assertNotRegex(mapping["summary"]["zh"], r"[。！？.!?]$")
                self.assertNotRegex(mapping["summary"]["en"], r"[。！？.!?]$")
                self.assertTrue(set(mapping["evidence_refs"]).issubset(reference_refs))
            self.assertEqual(len(mechanism_refs), len(set(mechanism_refs)))

    def test_core_templates_match_required_schema_fields(self) -> None:
        pairs = [
            ("technique.schema.json", "templates/technique/technique.yaml"),
            ("subtechnique.schema.json", "templates/subtechnique/subtechnique.yaml"),
            ("detection.schema.json", "templates/detection.yaml"),
            ("analytic.schema.json", "templates/analytic.yaml"),
            ("mitigation.schema.json", "templates/mitigation.yaml"),
        ]
        for schema_name, template_name in pairs:
            schema = json.loads(
                (ROOT / "schemas" / schema_name).read_text(encoding="utf-8")
            )
            template = load_yaml(ROOT / template_name)
            self.assertFalse(schema["additionalProperties"])
            self.assertEqual(set(template), set(schema["properties"]))
            self.assertEqual(set(template), set(schema["required"]))
            self.assertEqual(template["schema_version"], "2.0.0")

    def test_fragmented_markdown_lists_are_rejected(self) -> None:
        self.assertIsNotNone(FORBIDDEN_MARKDOWN.search("- 碎片化正文"))
        self.assertIsNotNone(FORBIDDEN_MARKDOWN.search("1. Fragmented prose"))
        self.assertIsNone(FORBIDDEN_MARKDOWN.search("这是一段完整的自然表述。"))

    def test_defense_exemplars_are_connected_and_complete(self) -> None:
        strategies = {
            value["id"]: value
            for value in (
                load_yaml(path) for path in sorted((ROOT / "detections").glob("*.yaml"))
            )
        }
        analytics = {
            value["id"]: value
            for value in (
                load_yaml(path) for path in sorted((ROOT / "analytics").glob("*.yaml"))
            )
        }
        mitigations = {
            value["id"]: value
            for value in (
                load_yaml(path) for path in sorted((ROOT / "mitigations").glob("*.yaml"))
            )
        }
        self.assertTrue(
            {"DET-000001", "DET-000002", "DET-000003", "DET-000004"}
            .issubset(strategies)
        )
        self.assertTrue(
            {"NJA-000001", "NJA-000002", "NJA-000003", "NJA-000004"}
            .issubset(analytics)
        )
        self.assertTrue(
            {"MIT-000001", "MIT-000002", "MIT-000003"}
            .issubset(mitigations)
        )
        self.assertGreaterEqual(len(strategies), 4)
        self.assertGreaterEqual(len(analytics), 4)
        self.assertGreaterEqual(len(mitigations), 3)

        for strategy_id, strategy in strategies.items():
            self.assertEqual(strategy["type"], "detection-strategy")
            self.assertGreaterEqual(len(strategy["analytic_refs"]), 1)
            for analytic_id in strategy["analytic_refs"]:
                analytic = analytics[analytic_id]
                self.assertEqual(analytic["strategy_ref"], strategy_id)
                self.assertGreaterEqual(len(analytic["data_requirements"]), 1)
                self.assertGreaterEqual(len(analytic["false_positives"]), 1)
                self.assertGreaterEqual(len(analytic["blind_spots"]), 1)

        for mitigation in mitigations.values():
            self.assertGreaterEqual(len(mitigation["measures"]), 1)
            targets = [
                application["target_ref"]
                for application in mitigation["applications"]
            ]
            self.assertEqual(len(targets), len(set(targets)))


if __name__ == "__main__":
    unittest.main()
