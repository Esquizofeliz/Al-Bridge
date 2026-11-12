# KugelAudio Open — ficha técnica

Evidência: CONFIRMED para síntese texto-fala no repositório público.

## Entradas e saídas
- Entrada principal: texto.
- Seleção de voz por embeddings/vozes pré-codificadas disponibilizadas pelo projeto.
- Saída: fala sintetizada; README demonstra salvar WAV por processor.save_audio(...).

## Idiomas
O README lista 24 idiomas europeus, incluindo português (pt). A documentação alerta que a qualidade varia; inglês, francês, espanhol e alemão têm cobertura mais forte. Português deve ser testado, sem promessa de prosódia perfeita.

## Vozes e clonagem
O repositório lista vozes pré-codificadas e declara que clonagem de voz a partir de áudio bruto não é suportada nesta versão open-source.

## Parâmetros
O README apresenta cfg_scale e max_new_tokens como argumentos de geração. Não sugerir valores sem contexto/versionamento; exemplos upstream não são presets universais.

## Licença
O repositório declara MIT. Verificar separadamente termos dos pesos/checkpoints.
