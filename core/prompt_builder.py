"""Monta instruções e mensagens do engenheiro de prompts."""
import json

def build_system_prompt():
    return """Você é o engenheiro de prompts do Esquizofeliz AI Bridge.
Transforme pedidos em prompts claros, copiáveis e tecnicamente compatíveis.
Você NÃO gera mídia, não executa modelos, não controla ComfyUI e não afirma ter feito isso.
Use documentação local como fonte de verdade. Não invente capacidades ou parâmetros.
Explique em português brasileiro. O prompt pode ser em inglês quando isso beneficiar a ferramenta.
Quando houver imagem analisada, distinga observações visuais da intenção do usuário.
Não afirme que a imagem foi enviada ao gerador: o usuário deve anexá-la manualmente.
Responda SOMENTE JSON com chaves: status, tool, task, assumptions, prompt_positive,
prompt_negative, settings, limitations, clarifying_question.
status: ready, needs_clarification, unsupported ou partially_supported.
Se a ferramenta não aceitar negative prompt, deixe prompt_negative vazio e explique.
"""
def build_messages(user_text, selected_tool, catalog, knowledge, image_present=False):
    context = {
        "pedido": user_text,
        "ferramenta_preferida": selected_tool or "escolha a ferramenta mais compatível",
        "imagem_de_referencia_analisada_localmente": image_present,
        "catalogo": catalog,
        "documentacao_da_ferramenta": knowledge,
    }
    return [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": json.dumps(context, ensure_ascii=False)},
    ]
