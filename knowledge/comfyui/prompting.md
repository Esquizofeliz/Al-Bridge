# Como preparar prompts para ComfyUI

Não existe formato universal de prompt ComfyUI: o texto é consumido pelos nós conectados no workflow.

- Identifique checkpoint/modelo e nós de condicionamento.
- Determine qual campo recebe prompt positivo e se existe negativo.
- Verifique se usa CLIP, T5, conditioning específico ou entrada multimodal.
- Só sugerir sampler, scheduler, steps, CFG, seed, resolução ou LoRA se esses campos existirem no workflow fornecido.
- Sem workflow, gerar prompt genérico e marcar parâmetros como não verificados.

ComfyUI não é sinônimo de FLUX, LTX ou KugelAudio; cada modelo tem seus requisitos.
