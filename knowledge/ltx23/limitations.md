# Limitações — LTX-2.3

- LTX-2.3 22B é pesado. Não prometer execução adequada em GPU de 8 GB; requisitos dependem de quantização, offload, resolução, pipeline e RAM.
- A2Vid é específico; não extrapolar capacidade para workflows genéricos.
- Dub-It não deve ser anunciado como validado para português: idiomas documentados são inglês, francês, espanhol, alemão e russo.
- Não prometer sincronização labial perfeita apenas com prompt.
- Não confundir adicionar áudio em edição posterior com condicionar geração pelo áudio.
- Negative prompt e parâmetros variam por pipeline/template.
- API hospedada é serviço separado; Bridge prioriza uso local/open-source.
