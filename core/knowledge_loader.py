"""Carrega documentação Markdown local para contexto técnico."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"

def load_knowledge(tool_id: str) -> str:
    folder = KNOWLEDGE / tool_id
    if not folder.is_dir():
        return ""
    parts = []
    for name in ("technical.md", "prompting.md", "examples.md", "limitations.md"):
        path = folder / name
        if path.is_file():
            parts.append(f"\n\n## DOCUMENTO: {tool_id}/{name}\n" + path.read_text(encoding="utf-8"))
    return "".join(parts)

def load_shared_rules() -> str:
    parts = []
    for name in ("DOCUMENTATION_RULES.md", "SOURCES.md"):
        path = KNOWLEDGE / name
        if path.is_file():
            parts.append(f"\n\n## {name}\n" + path.read_text(encoding="utf-8"))
    return "".join(parts)
