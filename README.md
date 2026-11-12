# Esquizofeliz AI Bridge

**Engenheiro local de prompts, não executor de mídia.** Recebe uma ideia em português, consulta uma biblioteca técnica versionada e devolve prompts/instruções para o usuário executar manualmente no software escolhido.

## Princípios
- Local-first: sem API paga, nuvem ou telemetria.
- Ollama local como provedor de linguagem.
- Documentação upstream como fonte de verdade; o LLM não deve inventar capacidades.
- Nenhum workflow é enviado e nenhum modelo de geração é executado.
- Imagem de referência opcional pode ser analisada pelo Qwen3.5 local; ela não é enviada ao FLUX pelo Bridge.

## Requisitos
- Python 3.10+; sem dependências Python externas.
- Ollama com modelo compatível com a API /api/chat.
- Para análise de imagem, o modelo configurado precisa ter visão e o servidor Ollama precisa aceitar imagens no campo images.
- FLUX.2 Klein 9B tem licença não comercial e pode exigir recursos acima dos disponíveis em GPUs de 8 GB.

## Configuração
Copie .env.example para .env e ajuste:
```env
BRIDGE_API_BASE=http://127.0.0.1:11434
BRIDGE_MODEL=qwen3.5:9b-q4_K_M
BRIDGE_API_KEY=
BRIDGE_PORT=8765
```
O Bridge carrega .env automaticamente. Não publique segredos.

## Executar
```bash
python3 app.py
```
Abra http://127.0.0.1:8765

## Ferramentas documentadas
- FLUX.2 Klein 9B — texto-imagem e edição com referências.
- KugelAudio Open — texto-fala; vozes pré-codificadas; português com qualidade variável.
- LTX-2.3 — pipelines locais específicos para T2V, I2V, A2V e tarefas especializadas.
- ComfyUI — workflows por nós; compatibilidade depende do JSON e dos nós instalados.

Leia knowledge/SOURCES.md e knowledge/DOCUMENTATION_RULES.md antes de alterar capacidades.

## Imagem de referência
A interface aceita PNG, JPEG ou WEBP de até 6 MB. O arquivo é enviado em base64 somente à API Ollama local configurada, para análise visual. O Bridge não o armazena em disco, não o envia ao FLUX/ComfyUI e não chama serviços remotos. O prompt resultante inclui instruções de edição, mas o usuário ainda precisa selecionar a imagem original no software gerador. Se o endpoint não suportar imagens, a requisição falha claramente; o Bridge não finge ter visto a referência.

## Testes
```bash
python3 -m unittest discover -s tests -v
```

## Licenças
O Bridge é MIT. Cada modelo, peso, nó customizado e checkpoint mantém seus próprios termos. Em particular, FLUX.2 Klein 9B é não comercial; não confundir com Klein 4B Apache-2.0.
