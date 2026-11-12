# Esquizofeliz AI Bridge

**Um engenheiro local de prompts.** O Bridge recebe uma descrição em português, interpreta a intenção com um modelo local e devolve prompts prontos para copiar. Ele **não gera nem executa** imagens, vídeos ou áudios.

## Princípios

- Local-first: sem APIs pagas ou serviços em nuvem.
- O usuário controla a execução: o Bridge apenas prepara o texto.
- O registro técnico é a fonte de verdade sobre capacidades e limitações.
- O modelo de linguagem interpreta; não inventa suporte técnico.
- Nenhum arquivo ou modelo do computador é alterado por este projeto.

## Requisitos

- Ubuntu/Linux, Python 3.10 ou superior.
- Um servidor local compatível com a API OpenAI Chat Completions.
- Configuração inicial sugerida para o ambiente conhecido: `http://127.0.0.1:8338/v1`, modelo `qwen3-8b`.
- O servidor/modelo precisa estar iniciado separadamente.

Não instala nem baixa modelos.

## Iniciar

```bash
cd esquizofeliz-ai-bridge
python3 app.py
```

Abra `http://127.0.0.1:8765`.

Configurações opcionais por variáveis de ambiente:

```bash
BRIDGE_API_BASE=http://127.0.0.1:8338/v1
BRIDGE_MODEL=qwen3-8b
BRIDGE_API_KEY=
BRIDGE_PORT=8765
```

A chave é opcional e deve ser usada somente se o servidor local exigir autenticação. Não coloque chaves de serviços externos.

## O que a primeira versão faz

1. Recebe somente texto digitado.
2. Consulta o catálogo local de capacidades.
3. Pede ao modelo local um plano de prompt estruturado.
4. Valida se a ferramenta escolhida possui suporte documentado para o tipo de tarefa.
5. Exibe prompt positivo, negativo, parâmetros sugeridos e ressalvas.
6. Não envia mídia, não executa workflows e não chama ferramentas de geração.

## Catálogo inicial

Os registros em `models/` são um ponto de partida conservador, baseado na documentação oficial consultada para este projeto. Verifique versões e workflows antes de atualizar as afirmações. Em especial:

- LTX-2.3: geração conjunta de áudio/vídeo e workflows específicos; não presumir que áudio externo arbitrário condicione vídeo.
- FLUX.2: imagem a partir de texto e referências visuais; não é gerador de áudio/vídeo.
- KugelAudio Open: texto para fala; a versão pública não deve ser tratada como clonagem livre a partir de qualquer WAV.
- ComfyUI não está integrado para execução nesta versão.

## Privacidade

O texto digitado é enviado apenas ao endpoint local configurado. O aplicativo não possui telemetria, analytics ou chamadas remotas. Se você configurar um endpoint remoto, essa garantia deixa de valer.

## Testes

```bash
python3 -m unittest discover -s tests -v
```

## Próximos passos possíveis

- Melhorar a cobertura de workflows por versão.
- Adicionar exportação `.txt` e histórico local opt-in.
- Criar perfis de prompt por ferramenta.
- Incluir testes com prompts reais e avaliação manual.

## Licença

MIT. Consulte `LICENSE`.
