# Regras de criação e correção — A Noite Vermelha

## Fonte de verdade e versões
1. Partir sempre do pacote de maior evolução validada. Para a próxima alteração, a base é a evolução 25.
2. JOGAR.html é a única entrada real. Atalhos devem encaminhar para ele; não distribuir uma campanha antiga como se fosse a versão atual.
3. Nunca reconstruir a entrega executando scripts de etapas 20/21/22 sobre uma pasta atual. Gerar uma pasta nova e aplicar mudanças incrementais sobre a base declarada no manifesto.
4. Antes de editar, registrar SHA-256 do mapa e da navegação, lista de marcos E21/E22 e recursos incorporados. Mudanças de fonte, interface ou câmera não podem alterar o mapa.
5. O mapa dentro do HTML deve ser byte a byte idêntico ao GLB em assets. Falha dessa verificação bloqueia o empacotamento.
6. Preservar os 49 detalhes E21 e 65 detalhes E22, salvo alteração explicitamente documentada. Não usar apenas contagem total: conferir nomes dos marcos e hash quando a geometria não mudou.

## Construções
7. Priorizar os locais narrativos: bar, casa de Helena, registro civil, consultório, igreja/arquivo, cela, fazenda, moinho e pontos de investigação.
8. Casa secundária permanece fechada, com exterior completo; não criar interiores vazios visíveis ou portas falsas abertas.
9. Novos acessos devem reservar ao menos 1,4 m de vão e corredores principais de 1,8 m. Essas medidas são metas para alterações futuras, não uma certificação retroativa de todo o mapa.
10. Mobiliário deve ter função e orientação: cadeiras voltadas à mesa, bancos ao altar, prateleiras contra paredes. Não inserir adereços no percurso obrigatório nem diante de pistas.
11. Toda alteração sólida deve atualizar colisões; validar entrada, saída, escadas e acesso à pista. Objetos devem apoiar no terreno ou piso local.

## Materiais e câmera
12. UV com correção de perspectiva. Proibir interpolação afim e quantização de vértices em tela enquanto causarem deslizamento de textura.
13. Texturas projetadas devem usar coordenadas de mundo/objeto estáveis, nunca posição da câmera. Conferir escala e sangramento entre células do atlas.
14. Preservar clipping da água e repetição de textura sem alongamento.
15. Scroll altera a distância da câmera; normalizar deltaMode e funcionar sob captura de cursor. Rolagem de menu não pode mover a câmera.
16. Colisão da câmera é independente da cápsula do personagem. Obstáculo real pode limitar a distância e deve ser indicado na interface.
17. Usar Bilaby em títulos e Electro em interface, com complemento para caracteres ausentes e licenças anexadas.

## Grupo e animação
18. Quatro personagens têm posições e ciclos independentes. Preservar separação, trajeto do líder, distância máxima de 12 m e recuperação após bloqueio de 2,4 s.
19. Recuperação deve escolher posição livre; não atravessar paredes durante a caminhada. Verificar pisos, água e diferenças de altura.
20. Caminhada acompanha deslocamento real, parada usa idle e giro tem limite. Não anunciar IK ou rig novo quando apenas ciclos amostrados foram ajustados.

## Validação e entrega
21. Rodar testes de entrada canônica, integridade do mapa, câmera, scroll, paredes, recuperação e referências da interface.
22. Registrar separadamente testes de lógica, importação 3D e teste visual no navegador. Uma categoria não substitui a outra; informar verificações pendentes.
23. Gerar ZIP numerado e manifesto a cada evolução. Conferir o ZIP reaberto, não apenas a pasta de origem.
24. Guardar versões anteriores intactas fora do novo pacote. Não apresentar uma campanha antiga como atualização do mapa.

25. Unidade do projeto: 1 unidade = 1 metro. Validar alturas dos protagonistas (1,78–2,04 m), folga de portas e altura de móveis antes de alterar a escala do cenário.
26. Alterações em HTML com dados base64 devem atuar em trechos identificados; proibir substituições genéricas sobre o arquivo inteiro. Validar descompressão do mapa, imagens, fontes e poses antes de empacotar.
