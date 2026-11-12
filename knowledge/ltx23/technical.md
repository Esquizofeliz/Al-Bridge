# LTX-2.3 — ficha técnica

Evidência: CONFIRMED para pipelines listados no repositório oficial Lightricks. Esta ficha trata do projeto local/open-source, não da API hospedada.

## Pipelines
- Texto/imagem para vídeo: pipelines TI2Vid com condicionamento de imagem.
- Áudio para vídeo: A2VidPipelineTwoStage, com áudio de entrada e condicionamento de imagem opcional.
- Interpolação de keyframes: TI2VidTwoStagesPipeline com imagens guia e índices de frame.
- Dub-It: pipeline especializado de redublagem, com restrições próprias.

## Imagens
A API usa ImageConditioningInput e bindings como ImageReplace e ImageGuide. Índices de frame são índices em pixels na linha temporal, começando em zero; não converter manualmente para índice latente.

## Áudio
A2Vid recebe arquivo de áudio, codifica o áudio e mantém a forma de onda original na saída. É capacidade específica do pipeline A2Vid, não garantia para qualquer workflow ComfyUI.
