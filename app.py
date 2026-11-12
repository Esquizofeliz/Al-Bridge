#!/usr/bin/env python3
"""Servidor local do Esquizofeliz AI Bridge."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import json
import os
import re
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = int(os.getenv("BRIDGE_PORT", "8765"))


def load_env():
    """Carrega configurações do .env sem dependências externas."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()

API_BASE = os.getenv(
    "BRIDGE_API_BASE", "http://127.0.0.1:11434"
).rstrip("/")
MODEL = os.getenv("BRIDGE_MODEL", "qwen3.5:9b-q4_K_M")
API_KEY = os.getenv("BRIDGE_API_KEY", "")

def load_catalog():
    catalog = []
    for path in sorted((ROOT / "models").glob("*.json")):
        with path.open(encoding="utf-8") as f:
            catalog.append(json.load(f))
    return catalog


CATALOG = load_catalog()


def compact_catalog():
    return [{
        "id": item["id"],
        "name": item["name"],
        "purpose": item["purpose"],
        "inputs": item["inputs"],
        "outputs": item["outputs"],
        "supported_tasks": item["supported_tasks"],
        "unsupported_or_unconfirmed": item["unsupported_or_unconfirmed"],
        "prompt_guidance": item["prompt_guidance"],
    } for item in CATALOG]


def build_system_prompt():
    return """Você é o engenheiro de prompts do Esquizofeliz AI Bridge.
Sua única função é transformar o pedido do usuário em prompts claros e tecnicamente compatíveis.
Você NÃO gera nem executa mídia, não chama ferramentas e não deve alegar que executou algo.

REGRAS OBRIGATÓRIAS:
1. Use somente capacidades e tarefas presentes no catálogo fornecido.
2. Se a combinação solicitada não estiver documentada, marque como "unsupported" ou "unconfirmed"; nunca invente suporte.
3. Se faltar uma informação essencial, faça no máximo uma pergunta objetiva. Caso contrário, faça suposições razoáveis e declare-as.
4. Escreva o prompt principal em inglês quando isso for apropriado à ferramenta, mas explique tudo em português brasileiro.
5. Não invente parâmetros numéricos específicos. Se não houver parâmetro documentado no catálogo, escreva "não especificado no registro".
6. Não confunda adicionar uma faixa de áudio ao vídeo na edição com condicionar a geração do vídeo pelo áudio.
7. Não presuma sincronização labial.
8. Retorne SOMENTE JSON válido, sem markdown, neste formato:
{
 "status":"ready|needs_clarification|unsupported|partially_supported",
 "tool":"nome ou null",
 "task":"descrição curta",
 "assumptions":["..."],
 "prompt_positive":"...",
 "prompt_negative":"...",
 "settings":["..."],
 "limitations":["..."],
 "clarifying_question":""
}
Se a tarefa não for compatível, não produza um prompt enganoso. Explique a limitação em limitations e proponha apenas uma alternativa que esteja documentada.
"""


def ask_local_model(user_text, selected_tool):
    catalog = compact_catalog()

    messages = [
        {"role": "system", "content": build_system_prompt()},
        {
            "role": "system",
            "content": "CATÁLOGO TÉCNICO LOCAL (fonte de verdade):\n"
            + json.dumps(catalog, ensure_ascii=False),
        },
        {
            "role": "user",
            "content": json.dumps({
                "pedido": user_text,
                "ferramenta_preferida": selected_tool or
                "escolha a ferramenta mais compatível",
            }, ensure_ascii=False),
        },
    ]

    payload = {
        "model": MODEL,
        "messages": messages,
        "think": False,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 2048,
        },
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    if API_KEY:
        headers["Authorization"] = "Bearer " + API_KEY

    req = urllib.request.Request(
        API_BASE + "/api/chat",
        data=data,
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Ollama respondeu HTTP {e.code}: {detail[:1000]}"
        ) from e

    content = raw.get("message", {}).get("content", "")

    if not isinstance(content, str) or not content.strip():
        raise ValueError("O Ollama não retornou conteúdo textual.")

    content = re.sub(
        r"<think>.*?</think>", "", content, flags=re.DOTALL
    ).strip()

    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

    first, last = content.find("{"), content.rfind("}")

    if first < 0 or last < first:
        raise ValueError("O modelo não devolveu um objeto JSON válido.")

    return json.loads(content[first:last + 1])


class Handler(BaseHTTPRequestHandler):

    def _send(self, status, body, content_type="application/json; charset=utf-8"):
        encoded = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(
                200,
                (ROOT / "interface" / "index.html").read_bytes(),
                "text/html; charset=utf-8",
            )
        elif self.path == "/api/catalog":
            self._send(200, json.dumps(compact_catalog(), ensure_ascii=False))
        elif self.path == "/api/health":
            self._send(200, json.dumps({
                "app": "ok",
                "model": MODEL,
                "endpoint": API_BASE,
            }))
        else:
            self._send(404, json.dumps({"error": "Não encontrado."}))

    def do_POST(self):
        if self.path != "/api/prompt":
            self._send(404, json.dumps({"error": "Não encontrado."}))
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))

            if length <= 0 or length > 20000:
                raise ValueError("Envie um pedido de texto de até 20 KB.")

            body = json.loads(self.rfile.read(length).decode("utf-8"))
            user_text = str(body.get("text", "")).strip()
            selected_tool = str(body.get("tool", "")).strip()

            if not user_text:
                raise ValueError("Escreva o que deseja criar.")

            if len(user_text) > 12000:
                raise ValueError("O pedido deve ter no máximo 12.000 caracteres.")

            result = ask_local_model(user_text, selected_tool)

            required = {
                "status", "tool", "task", "assumptions",
                "prompt_positive", "prompt_negative",
                "settings", "limitations", "clarifying_question",
            }

            if not isinstance(result, dict) or not required.issubset(result):
                raise ValueError(
                    "O modelo não retornou a estrutura esperada. Tente novamente."
                )

            if result["status"] not in {
                "ready", "needs_clarification",
                "unsupported", "partially_supported",
            }:
                raise ValueError("O modelo retornou um status inválido.")

            self._send(200, json.dumps(result, ensure_ascii=False))

        except urllib.error.URLError as e:
            self._send(502, json.dumps({
                "error": "Não consegui acessar o Ollama local.",
                "detail": str(e.reason),
            }, ensure_ascii=False))

        except (KeyError, IndexError, json.JSONDecodeError, ValueError) as e:
            self._send(400, json.dumps({"error": str(e)}, ensure_ascii=False))

        except Exception as e:
            self._send(500, json.dumps({
                "error": "Falha ao preparar o prompt.",
                "detail": str(e),
            }, ensure_ascii=False))

    def log_message(self, fmt, *args):
        print("[Bridge] " + (fmt % args))


if __name__ == "__main__":
    print(f"Esquizofeliz AI Bridge em http://{HOST}:{PORT}")
    print(f"Modelo local: {MODEL} | endpoint: {API_BASE}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
