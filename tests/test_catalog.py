import json
import unittest
from pathlib import Path

from core.knowledge_loader import load_knowledge, load_shared_rules
from core.validator import validate_result

ROOT = Path(__file__).resolve().parents[1]

class CatalogTests(unittest.TestCase):
    def test_each_model_has_required_fields(self):
        for path in (ROOT / "models").glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            for key in ("id", "name", "purpose", "inputs", "outputs",
                        "supported_tasks", "unsupported_or_unconfirmed",
                        "prompt_guidance", "source", "license_note"):
                self.assertIn(key, data, f"{path.name}: falta {key}")
            self.assertTrue(data["supported_tasks"])
            self.assertTrue(data["unsupported_or_unconfirmed"])

    def test_no_duplicate_ids(self):
        ids = [json.loads(path.read_text(encoding="utf-8"))["id"]
               for path in (ROOT / "models").glob("*.json")]
        self.assertEqual(len(ids), len(set(ids)))

    def test_flux_variant_and_license_are_explicit(self):
        data = json.loads((ROOT / "models/flux2.json").read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "FLUX.2 Klein 9B")
        self.assertIn("Non-Commercial", data["license_note"])

    def test_knowledge_documents_exist_for_all_tools(self):
        for model in (ROOT / "models").glob("*.json"):
            tool_id = json.loads(model.read_text(encoding="utf-8"))["id"]
            docs = load_knowledge(tool_id)
            for expected in ("technical.md", "prompting.md", "examples.md", "limitations.md"):
                self.assertIn(expected, docs)

    def test_shared_rules_are_loaded(self):
        docs = load_shared_rules()
        self.assertIn("DOCUMENTATION_RULES.md", docs)
        self.assertIn("SOURCES.md", docs)

    def test_validator_accepts_valid_result(self):
        result = {
            "status": "ready", "tool": "flux2", "task": "image",
            "assumptions": [], "prompt_positive": "A prompt",
            "prompt_negative": "", "settings": [], "limitations": [],
            "clarifying_question": ""
        }
        self.assertIs(validate_result(result), result)

    def test_validator_rejects_missing_fields(self):
        with self.assertRaises(ValueError):
            validate_result({"status": "ready"})

if __name__ == "__main__":
    unittest.main()
