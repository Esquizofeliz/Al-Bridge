# FLUX.2 Klein 9B — ficha técnica

**Evidência:** CONFIRMED para geração texto-imagem e edição com referências no repositório oficial BFL. Variante tratada: FLUX.2 [klein] 9B distilled, não 4B, 9B Base ou 9B KV.

## Capacidades
- Texto para imagem.
- Edição com uma imagem de referência.
- Edição com múltiplas imagens de referência, conforme pipeline.
- A referência precisa ser entregue ao pipeline FLUX, não apenas mencionada no prompt.

## Entradas e saídas
- Texto: descrição ou instrução de edição.
- Imagem(ns): referência visual conforme CLI/pipeline.
- Saída: imagem.

## Variantes e licença
- Klein 9B e Klein 9B KV: FLUX Non-Commercial License.
- Klein 4B: Apache-2.0; não misturar as licenças.
- 9B KV é checkpoint distinto, otimizado por KV cache.
- A escolha 9B não implica caber em 8 GB VRAM. Quantização/offload dependem de implementação e precisam ser testados.

## Papel da imagem no Bridge
O navegador envia a imagem ao servidor local; o servidor encaminha base64 ao endpoint Ollama local para análise visual. A imagem não é enviada ao FLUX nem a serviço remoto pelo Bridge. O usuário deve anexar a mesma referência manualmente ao pipeline gerador.

Fonte: https://github.com/black-forest-labs/flux2
