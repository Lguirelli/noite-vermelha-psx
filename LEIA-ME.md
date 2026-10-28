# A Noite Vermelha — Evolução 27

Extraia o ZIP e abra **JOGAR.html** no Chrome ou Edge atualizado. O jogo contém mapa, modelos e texturas incorporados, sem servidor. Os outros arquivos HTML redirecionam para esta mesma versão.

## Personagens enviados
Os quatro protagonistas vêm de Personagens_PSX_UV_Separadas.blend. Foram mantidos os vértices, faces, peças, pesos e mapeamentos UV do arquivo, incluindo a máscara separada de Octávio nos modelos editáveis. O original, sem alterações, está em assets/source.

A versão exportável usa os ossos de deformação do Rigify, com hierarquia simplificada para glTF. O rig de controles completo está preservado no original. Cada GLB em assets/rigged contém pele, texturas incorporadas e duas animações. No HTML, as mesmas deformações são armazenadas em 48 poses e interpoladas pela placa de vídeo. A animação de caminhada avança pela distância percorrida; cada integrante mantém seu movimento independente.

## Animações utilizadas
**Quaternius Universal Animation Library — Standard**, licença CC0: Idle_Loop e Walk_Loop. Biblioteca original em assets/animations, junto da licença. Os demais movimentos da biblioteca estão disponíveis para trabalho posterior; não estão conectados a ações de combate neste jogo.

Fonte oficial: https://quaternius.com/packs/universalanimationlibrary.html
Download oficial: https://quaternius.itch.io/universal-animation-library

A versão gratuita contém uma seleção; a oferta de mais de 120 movimentos refere-se à biblioteca completa. Mixamo também foi considerado, mas não foi necessário enviar os personagens para outro serviço.

## Mapa e texturas
O mapa GLB da versão anterior foi preservado integralmente, com verificação de hash. O shader do atlas de detalhes passou a usar dimensões por material no mundo: tijolos, pedras, madeira e reboco têm escalas distintas. Vitrais e painéis conservam a composição de suas UVs. Isso não substitui uma revisão manual de todas as faces do mapa.

## Avaliação e limites
assets/previa-repouso27.png e assets/previa-caminhada27.png foram renderizadas a partir das poses e UVs exatas incorporadas no HTML. assets/rigged/protagonistas-animados27.blend contém os personagens animados; avaliacao-poses27.blend contém o palco de avaliação da pose de caminhada.

Os testes de lógica de câmera, zoom, colisão, recuperação dos seguidores, mapa e integridade passaram. A interação e a renderização WebGL no navegador ainda precisam de conferência visual; não foram testadas nesta entrega. Não foram acrescentados NPCs ou lendas.
