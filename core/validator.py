"""Validação determinística da estrutura e dos limites de saída."""
REQUIRED = {
    "status", "tool", "task", "assumptions", "prompt_positive",
    "prompt_negative", "settings", "limitations", "clarifying_question",
}
STATUSES = {"ready", "needs_clarification", "unsupported", "partially_supported"}

def validate_result(result):
    if not isinstance(result, dict):
        raise ValueError("A resposta do modelo não é um objeto JSON.")
    missing = REQUIRED - result.keys()
    if missing:
        raise ValueError("Campos ausentes: " + ", ".join(sorted(missing)))
    if result["status"] not in STATUSES:
        raise ValueError("Status inválido.")
    for key in ("assumptions", "settings", "limitations"):
        if not isinstance(result[key], list):
            raise ValueError(f"O campo {key} deve ser uma lista.")
    for key in ("task", "prompt_positive", "prompt_negative", "clarifying_question"):
        if not isinstance(result[key], str):
            raise ValueError(f"O campo {key} deve ser texto.")
    return result
