import json
import unittest
from pathlib import Path

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
        ids = []
        for path in (ROOT / "models").glob("*.json"):
            ids.append(json.loads(path.read_text(encoding="utf-8"))["id"])
        self.assertEqual(len(ids), len(set(ids)))

if __name__ == "__main__":
    unittest.main()
