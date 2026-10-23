# SIPAT RejuntaMix — edição cinematográfica v2

## Resultado e direção

Montagem de **79,70 segundos**, preservando a introdução completa do novo
arquivo, seguida por 13 planos selecionados em ordem cronológica. Saída final:
`exports/sipat-rejuntamix-cinematic-v2.mp4`, vertical 720 × 1280, 30 fps,
H.264/yuv420p e AAC estéreo a 48 kHz, com faststart.

Composição editável: `src/config/cinematic-v2.json`.
Implementação: `scripts/render_cinematic_v2.py`.
Direção permanente atualizada em `AGENTS.md`; pedido completo preservado em
`docs/DIRECAO_CRIATIVA_V2.md`. A primeira edição e os dois arquivos originais
foram preservados.

## Análise crítica da v1

A v1 mantinha praticamente todo o consolidado de 137 segundos, incluindo
panorâmicas hesitantes, paredes e repetições de enquadramento. Aplicava o mesmo
zoom periódico sobre o vídeo inteiro, pequenas correções uniformes e caixas de
título semelhantes, sem uma curva de ritmo. Não havia estrutura musical.
As fotos finais mantinham grandes áreas vazias no quadro vertical.

A v2 faz seleção editorial de planos, encurta a montagem e muda de linguagem ao
fim da apresentação. Usa o envolvimento da plateia, gestos da palestrante,
planos de contexto e fotos originais como pontos narrativos. A revisão da
primeira prévia da v2 levou à substituição de trechos em que a câmera perdia a
palestrante ou apontava para a parede. As imagens continuam na ordem original.

A análise foi feita com folhas de contato, quadros pontuais, detecção de cenas,
metadados, reconhecimento automático de fala e medições de áudio. Isso não é
uma declaração de audição humana integral do conteúdo.

## Falas e áudio

No novo arquivo, a troca entre as duas tomadas de apresentação ocorre em
**8,00 s**. A troca da segunda tomada para o evento acontece em **23,70 s**.
O reconhecimento da segunda fala inclui seu encerramento sobre o tema
"Mente tranquila e trabalho seguro" antes dessa troca; como a transcrição tem
erros em nomes e palavras, ela não foi usada para fabricar legendas.

Preservamos o intervalo completo **0,00–23,70 s**. Portanto, a edição não corta
palavras no interior das duas tomadas. O limite de 23,70 s é o corte visual do
consolidado, não uma alegação de precisão fonética do reconhecimento.

A voz recebe redução leve de ruído, remoção moderada de graves, presença e
normalização em duas passagens. A faixa de introdução tem exatamente
1.137.600 amostras a 48 kHz; a música começa na amostra seguinte, sem sobrepor
as falas. Não há efeito sonoro adicional.

Todos os planos são renderizados com **`-an`**. A mixagem final concatena apenas
`voz-master.wav` (23,70 s) e `musica-master.wav` (56 s). Nenhuma fala, conversa
ou ambiente original dos demais vídeos participa do áudio final.

## Música e ritmo

**Inspired — Kevin MacLeod**, ISRC **USUAN1600022**.
Instrumental de guitarra, sintetizadores e percussão, **120 BPM**, obtido
no site oficial do compositor. Licença **Creative Commons BY 4.0**; nenhuma
compra ou serviço pago foi necessário.

- Fonte: https://incompetech.com/music/royalty-free/mp3-royaltyfree/Inspired.mp3
- Catálogo: https://incompetech.com/music/royalty-free/pieces.json
- Termos: https://incompetech.com/music/royalty-free/licenses/
- Licença: https://creativecommons.org/licenses/by/4.0/

Trecho musical contínuo de **48,033–104,033 s**, sem mudança de velocidade,
com entrada curta para evitar clique e fade-out de 2,4 s no encerramento.
Os créditos, o link da licença e a indicação de trecho editado aparecem no
encerramento e nos metadados. O texto para a descrição da publicação está em
`docs/CREDITOS_TRILHA_V2.txt`; mantenha a atribuição ao compartilhar.

A análise de ataques por fluxo espectral confirma pulsação aproximadamente a
cada 0,5 s. Os cortes foram distribuídos em frases de 2, 4, 6 e 8 segundos,
não em todas as batidas. O trecho de maior energia por volta de 80 s na música
coincide com a passagem por planos mais curtos na montagem. A variação de energia
da faixa é discreta, não uma grande mudança orquestral. Dados e distância dos
cortes aos ataques detectados estão em `docs/ANALISE_MUSICAL_V2.json`.

## Montagem e recursos visuais

- Tipografia sem caixas constantes, animações suaves e acentos em laranja.
- Uma passagem geométrica breve marca a entrada musical; sem flashes ou glitches.
- Corte direto como base, com quatro dissolvências pontuais para mudanças de
  enquadramento e desaceleração rumo às fotos.
- Ajustes leves de cor e contraste por condição de luz; tons de pele preservados.
- Movimento simulado de até 2,5% apenas em planos selecionados. Não há zoom
  oscilatório uniforme nem aceleração de vozes. Variações moderadas de velocidade
  são aplicadas somente a imagens cujo áudio foi descartado.
- Texto apenas na abertura, entrada da retrospectiva, uma passagem da palestra
  e fechamento. Sem nomes, datas ou atividades inventadas.
- A foto final é exibida inteira, sobre uma versão ampliada, desfocada e
  escurecida da própria imagem; não se cortam pessoas para preencher o 9:16.

| Tempo na v2 | Intervalo no novo original | Conteúdo selecionado |
| --- | --- | --- |
| 0,00–23,70 s | 0,00–23,70 s | As duas falas completas |
| 23.70–27.70 s | 24.05–27.65 s | Chegada e estrutura de atendimento |
| 27.70–31.70 s | 32.30–36.30 s | Plateia reunida |
| 31.70–35.70 s | 37.30–40.80 s | Participação coletiva, mãos levantadas |
| 35.70–39.70 s | 46.00–49.40 s | Palestrante em plano claro |
| 39.70–45.70 s | 55.00–58.80 s | Gestos e presença da palestrante |
| 45.70–47.70 s | 63.00–65.30 s | Plateia em outro enquadramento |
| 47.70–49.70 s | 68.50–71.20 s | Plano geral do público |
| 49.70–55.70 s | 79.00–83.80 s | Palestrante e projeção em outro ambiente |
| 55.70–57.70 s | 85.00–87.40 s | Pessoas na plateia |
| 57.70–61.70 s | 104.90–108.70 s | Plano mais próximo da palestra |
| 61.70–69.70 s | 118.00–123.40 s | Vista ampla do encontro, desaceleração antes das fotos |
| 69.70–73.70 s | 128.20–131.80 s | Registro fotográfico já presente no original |
| 73.70–79.70 s | 133.20–133.20 s | Foto final da equipe, preservada integralmente |

## Reproduzir e revisar

As dependências são Python 3 (biblioteca padrão), FFmpeg/FFprobe com libx264,
AAC e libass, e as fontes DejaVu Sans instaladas. Não usa Remotion, API externa,
modelo de geração ou licença empresarial Remotion para renderizar.

```bash
cd /workspace/Edition-MP4/sipat-rejuntamix
python3 scripts/fetch_cinematic_music.py
python3 scripts/render_cinematic_v2.py samples
python3 scripts/render_cinematic_v2.py preview
python3 scripts/render_cinematic_v2.py final
```

O arquivo novo enviado pelo usuário precisa estar em `public/videos/`, com o
nome e o SHA-256 registrados na configuração. O script confere sua integridade
antes e depois de renderizar. O download da trilha verifica o SHA-256 registrado
em `docs/TRILHA_V2.json`, mantendo a verificação TLS.

Amostras iniciais: `previews/cinematic-v2/amostra-transicao.mp4` e
`amostra-encerramento.mp4`. Prévia completa revisada:
`previews/cinematic-v2/previa-completa-v2.mp4` (360 × 640).
Folhas de contato, medições, logs e fontes ASS ficam na mesma pasta.

Os scripts recusam sobrescrever vídeos de saída. Ao revisar a montagem,
preserve a exportação anterior com outro nome antes de repetir. Ao modificar
seleções/velocidades/cores, renove somente os clipes gerados em
`previews/cinematic-v2/planos-360/` e `planos-720/`; ao modificar áudio, renove
`voz-master.wav` e `musica-master.wav`. Nunca apague arquivos de `public/videos/`.

## Limitações

A única fonte visual fornecida é um MP4 já comprimido, com 478 × 850 pixels,
movimentos de celular, exposição variável e alguns trechos fora de foco.
A saída 720 × 1280 padroniza a entrega, sem recuperar detalhe inexistente.
Não foi adicionada logomarca porque não há arquivo oficial separado.

## Validação do arquivo entregue

Render final: 2.391 quadros, vídeo e áudio com 79,700 s, 35.649.819 bytes.
Decodificação integral com FFmpeg sem erros. A comparação do áudio decodificado
com os masters resultou em correlação 0,99975 na introdução e 0,99993 na
montagem musical, com diferenças compatíveis com a codificação AAC.
Loudness integrado: -16.82 LUFS; pico verdadeiro: -1.80 dBTP.
Quadros revisados para texto, enquadramento e encerramento; original novo e v1
conferidos por hash. Relatório e hash final em `VALIDACAO_CINEMATIC_V2.json`.
