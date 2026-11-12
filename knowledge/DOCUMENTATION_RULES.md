# Regras de documentação e evidência

## Estados
- CONFIRMED: consta diretamente em documentação oficial, código oficial ou model card da variante identificada.
- PARTIALLY_CONFIRMED: depende de versão, workflow, checkpoint, extensão ou configuração.
- UNCONFIRMED: não foi possível verificar em fonte primária suficiente.
- UNSUPPORTED: a fonte oficial exclui a capacidade ou a interface descrita não a implementa.

## Regras
1. Priorizar repositório, documentação, model card e código mantidos pelo projeto original.
2. Registrar URL exata, componente, versão/commit quando disponível e data em SOURCES.md.
3. Não transformar exemplos de API hospedada em prova de suporte local/offline.
4. Separar capacidade do modelo, pipeline, workflow e implementação efetiva do Bridge.
5. Não inventar valores de resolução, FPS, duração, CFG, steps, sampler, formatos ou parâmetros.
6. Marcar como dependente de workflow qualquer função que exija nós customizados ou pipelines específicos.
7. Registrar conflitos entre documentação antiga e atual.
8. Não declarar sincronização labial, clonagem de voz ou análise visual sem evidência e implementação compatíveis.
9. A imagem no Bridge é analisada localmente; o usuário anexa a imagem original manualmente ao software gerador.
10. Atualizar data de verificação ao revisitar fontes.
