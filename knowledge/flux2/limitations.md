# Limitações — FLUX.2 Klein 9B

- Não gera áudio ou vídeo.
- O prompt não substitui o envio da imagem ao pipeline de edição.
- O campo de referência do Bridge serve para análise local; não encaminha a imagem ao FLUX.
- A análise depende de modelo Ollama com visão e endpoint que aceite images.
- Não afirmar que Qwen interpretou a imagem se o endpoint rejeitar a entrada.
- Não anunciar 9B como adequado a GPU de 8 GB sem teste. O upstream recomenda 4B para GPUs de consumo.
- A licença do Klein 9B é não comercial. Conferir os termos oficiais.
- Preservação exata de rosto, texto, logotipo ou pixels não é garantida.
