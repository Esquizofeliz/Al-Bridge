# ComfyUI — ficha técnica

ComfyUI é interface e runtime de workflows baseados em nós; não é um único modelo de IA.

- Workflow representa nós, entradas, saídas e conexões.
- Formato de workflow/API e nomes de nós dependem da versão e extensões instaladas.
- Nós customizados acrescentam parâmetros e dependências que podem não existir no núcleo.

## Escopo do Bridge
O Bridge prepara prompts e instruções textuais. Não chama /prompt, não envia arquivos, não consulta fila e não executa workflows. Para afirmar que um parâmetro serve a um workflow específico, é necessário conhecer JSON do workflow e versões dos nós.

Documentação: https://docs.comfy.org/
Repositório: https://github.com/Comfy-Org/ComfyUI
