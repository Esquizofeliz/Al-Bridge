# Esquizofeliz AI Bridge

**Engenheiro local de prompts, não executor de mídia.** Recebe uma ideia em português, consulta uma biblioteca técnica versionada e devolve prompts/instruções para o usuário executar manualmente no software escolhido.

## Princípios
- Local-first: sem API paga, nuvem ou telemetria.
- Ollama local como provedor de linguagem.
- Documentação upstream como fonte de verdade; o LLM não deve inventar capacidades.
- Nenhum workflow é enviado e nenhum modelo de geração é executado.
- Imagem de referência opcional pode orientar a interpretação do pedido para qualquer ferramenta, mas é enviada somente ao Ollama local, nunca diretamente ao gerador.

## Requisitos
- Python 3.10+; sem dependências Python externas.
- Ollama com modelo compatível com a API /api/chat.
- Para análise de imagem, o modelo configurado precisa ter visão e aceitar imagens no campo images.
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
- FLUX.2 Klein 9B — texto-imagem e edição com uma ou mais referências, conforme o pipeline.
- KugelAudio Open — texto-fala; vozes pré-codificadas; português com qualidade variável.
- LTX-2.3 — pipelines locais específicos para T2V, I2V, A2Vid e tarefas especializadas.

Leia knowledge/SOURCES.md e knowledge/DOCUMENTATION_RULES.md antes de alterar capacidades.

## Imagem de referência
A interface aceita PNG, JPEG ou WEBP de até 6 MB, independentemente da ferramenta selecionada. A imagem é enviada em base64 somente à API Ollama local configurada, para servir de contexto visual ao planejamento do prompt. Ela não é enviada ao FLUX, KugelAudio ou LTX pelo Bridge e não é armazenada em disco. Se o endpoint não suportar imagens, a requisição falha claramente; o Bridge não finge ter visto a referência.

O suporte da ferramenta de destino continua específico:
- FLUX.2 Klein 9B: edição com imagem(ns) depende do pipeline/checkpoint usado.
- LTX-2.3: imagem é entrada em pipelines image-to-video compatíveis.
- KugelAudio Open: não recebe imagem como entrada; uma imagem pode apenas contextualizar o texto/roteiro solicitado.

Quando a ferramenta aceitar imagem, anexe o arquivo original manualmente no software/pipeline de geração.

## Testes
```bash
python3 -m unittest discover -s tests -v
```

## Licenças
O Bridge é MIT. Cada modelo, peso, nó customizado e checkpoint mantém seus próprios termos. Em particular, FLUX.2 Klein 9B é não comercial; não confundir com Klein 4B Apache-2.0.
