# Biblioteca de conhecimento

Esta pasta é a referência técnica local do Bridge. O modelo de linguagem interpreta a intenção; esta biblioteca delimita o que pode ser afirmado.

Cada ferramenta possui quatro documentos: technical.md (interfaces e funcionamento), prompting.md (como redigir), examples.md (casos de uso) e limitations.md (limites e incertezas).

A documentação descreve capacidades upstream, não garante que estejam instaladas localmente. Versão, checkpoint, pipeline e dependências precisam ser conferidos separadamente.

O Bridge não executa inferência e não faz upload de mídia para geradores. A imagem de referência opcional é enviada somente ao endpoint Ollama local para análise visual e elaboração do prompt; o usuário anexa o original manualmente ao gerador quando o pipeline aceitar imagem.
