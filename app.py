#!/usr/bin/env python3
"""Servidor local do Esquizofeliz AI Bridge; prepara prompts, nunca executa mídia."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import base64
import json
import os
import re
import urllib.request
import urllib.error

from core.knowledge_loader import load_knowledge, load_shared_rules
from core.prompt_builder import build_messages
from core.validator import validate_result

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = int(os.getenv("BRIDGE_PORT", "8765"))
MAX_IMAGE_BYTES = 6 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp"}


def load_env():
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
API_BASE = os.getenv("BRIDGE_API_BASE", "http://127.0.0.1:11434").rstrip("/")
MODEL = os.getenv("BRIDGE_MODEL", "qwen3.5:9b-q4_K_M")
API_KEY = os.getenv("BRIDGE_API_KEY", "")


def load_catalog():
    items = []
    for path in sorted((ROOT / "models").glob("*.json")):
        with path.open(encoding="utf-8") as handle:
            items.append(json.load(handle))
    return items


CATALOG = load_catalog()
CATALOG_BY_ID = {item["id"]: item for item in CATALOG}


def compact_catalog():
    fields = ("id", "name", "purpose", "inputs", "outputs",
              "supported_tasks", "unsupported_or_unconfirmed", "prompt_guidance")
    return [{key: item[key] for key in fields} for item in CATALOG]


def ask_local_model(user_text, selected_tool, image=None):
    tool = CATALOG_BY_ID.get(selected_tool)
    if selected_tool and not tool:
        raise ValueError("Ferramenta selecionada não existe no catálogo.")
    knowledge = load_shared_rules()
    if tool:
        knowledge += load_knowledge(tool["id"])
    else:
        knowledge += "\n\n" + "\n\n".join(
            load_knowledge(item["id"]) for item in CATALOG
        )
    messages = build_messages(
        user_text, selected_tool, compact_catalog(), knowledge,
        image_present=bool(image),
    )
    if image:
        # Ollama /api/chat recebe imagens base64 no campo images da mensagem.
        messages[-1]["images"] = [image["data"]]

    payload = {
        "model": MODEL,
        "messages": messages,
        "think": False,
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": 2048},
    }
    request = urllib.request.Request(
        API_BASE + "/api/chat",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    if API_KEY:
        request.add_header("Authorization", "Bearer " + API_KEY)
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        if image:
            raise RuntimeError(
                "O endpoint Ollama não aceitou a imagem. Verifique se o modelo "
                "configurado tem visão e aceita imagens em /api/chat. "
                "O Bridge não analisou a referência."
            ) from error
        raise RuntimeError(f"Ollama respondeu HTTP {error.code}: {detail[:800]}") from error

    content = raw.get("message", {}).get("content", "")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("O Ollama não retornou conteúdo textual.")
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    first, last = content.find("{"), content.rfind("}")
    if first < 0 or last < first:
        raise ValueError("O modelo não devolveu um objeto JSON válido.")
    result = json.loads(content[first:last + 1])
    validate_result(result)

    # A validação não delega ao LLM a escolha de uma ferramenta inexistente.
    returned_tool = result.get("tool")
    allowed_names = {item["name"] for item in CATALOG}
    allowed_ids = set(CATALOG_BY_ID)
    if returned_tool not in allowed_names | allowed_ids | {None, ""}:
        raise ValueError("O modelo retornou uma ferramenta ausente do catálogo.")
    if selected_tool and returned_tool not in {selected_tool, tool["name"]}:
        result["status"] = "partially_supported"
        result["limitations"].append(
            "A ferramenta retornada pelo modelo divergiu da ferramenta selecionada; "
            "revise a compatibilidade antes de usar o prompt."
        )
    if image:
        result["assumptions"].append(
            "A imagem foi encaminhada ao endpoint Ollama local para análise; "
            "ela não foi enviada ao FLUX/ComfyUI."
        )
        result["limitations"].append(
            "Anexe manualmente a imagem original ao pipeline de geração/edição."
        )
    return result


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
            self._send(200, (ROOT / "interface" / "index.html").read_bytes(),
                       "text/html; charset=utf-8")
        elif self.path == "/api/catalog":
            self._send(200, json.dumps(compact_catalog(), ensure_ascii=False))
        elif self.path == "/api/health":
            self._send(200, json.dumps({"app": "ok", "model": MODEL, "endpoint": API_BASE}))
        else:
            self._send(404, json.dumps({"error": "Não encontrado."}))

    def do_POST(self):
        if self.path != "/api/prompt":
            self._send(404, json.dumps({"error": "Não encontrado."}))
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 10 * 1024 * 1024:
                raise ValueError("Requisição vazia ou maior que 10 MB.")
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            user_text = str(body.get("text", "")).strip()
            selected_tool = str(body.get("tool", "")).strip()
            if not user_text:
                raise ValueError("Escreva o que deseja criar.")
            if len(user_text) > 12000:
                raise ValueError("O pedido deve ter no máximo 12.000 caracteres.")

            image = None
            image_data = body.get("image")
            if image_data:
                mime = image_data.get("mime_type")
                encoded = image_data.get("data", "")
                if mime not in ALLOWED_IMAGE_TYPES:
                    raise ValueError("Use uma imagem PNG, JPEG ou WEBP.")
                if not isinstance(encoded, str) or len(encoded) > ((MAX_IMAGE_BYTES + 2) // 3) * 4 + 8:
                    raise ValueError("A imagem deve ter no máximo 6 MB.")
                try:
                    decoded = base64.b64decode(encoded, validate=True)
                except (ValueError, base64.binascii.Error) as error:
                    raise ValueError("A imagem enviada não é base64 válida.") from error
                if not decoded or len(decoded) > MAX_IMAGE_BYTES:
                    raise ValueError("A imagem deve ter entre 1 byte e 6 MB.")
                image = {"mime_type": mime, "data": base64.b64encode(decoded).decode("ascii")}

            result = ask_local_model(user_text, selected_tool, image)
            self._send(200, json.dumps(result, ensure_ascii=False))
        except urllib.error.URLError as error:
            self._send(502, json.dumps({
                "error": "Não consegui acessar o Ollama local.",
                "detail": str(error.reason),
            }, ensure_ascii=False))
        except (KeyError, json.JSONDecodeError, ValueError) as error:
            self._send(400, json.dumps({"error": str(error)}, ensure_ascii=False))
        except RuntimeError as error:
            self._send(502, json.dumps({"error": str(error)}, ensure_ascii=False))
        except Exception as error:
            self._send(500, json.dumps({
                "error": "Falha ao preparar o prompt.", "detail": str(error)
            }, ensure_ascii=False))

    def log_message(self, fmt, *args):
        print("[Bridge] " + (fmt % args))


if __name__ == "__main__":
    print(f"Esquizofeliz AI Bridge em http://{HOST}:{PORT}")
    print(f"Modelo local: {MODEL} | endpoint: {API_BASE}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
