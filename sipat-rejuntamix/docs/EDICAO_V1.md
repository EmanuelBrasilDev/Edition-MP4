# Edição SIPAT RejuntaMix — versão 1

Preparada a partir do vídeo recebido em 23/10/2026. Nenhuma logomarca nova,
trilha, efeito sonoro ou material de terceiros foi acrescentado.

## Análise do original

- MP4 H.264, 478 × 850, aproximadamente 60 fps, áudio AAC estéreo a 44,1 kHz.
- Duração: 137,122 segundos, já em formato vertical próximo a 9:16.
- Abertura com apresentadora até aproximadamente 24,63 s, seguida de registros
  do evento, palestras e imagens/fotos finais a partir de 129,07 s.
- Cortes visuais encontrados por diferença de cena: 8,93; 24,63; 31,60; 38,07;
  46,57; 62,27; 66,80; 76,00; 92,17; 103,67; 113,90; 129,07 e 133,07 s.
  Parte dessas diferenças corresponde a movimentos de câmera; não se deve
  interpretá-las automaticamente como mudança de assunto.
- Loudness original: -18,12 LUFS integrados, pico verdadeiro de -0,78 dBTP
  e faixa de variação de 12,10 LU. Esses valores são medições, não avaliação
  auditiva subjetiva de cada fala.
- Fonte de baixa resolução e áudio de ambientes diferentes; o processamento
  não recupera detalhes ou palavras ausentes na gravação.

## Decisões de edição

1. Preservar a sequência fornecida e toda a fala. Não acelerar vozes nem retirar
   frases com base em reconhecimento automático.
2. Usar títulos animados curtos: abertura, dois marcadores de seção e fechamento
   sobre a foto original. São títulos editoriais, não legendas de fala.
3. Movimentos de enquadramento limitados a 2,5%, centrados; contraste, saturação
   e nitidez ajustados com moderação, sem cortes agressivos de pessoas.
4. Priorizar fala: filtro de graves, redução leve de ruído, presença, compressão
   moderada e normalização de loudness em duas passagens, alvo -16 LUFS,
   limite de pico -1,5 dBTP antes da codificação AAC.
5. Não acrescentar música ou efeitos nas falas ou transições. A trilha já mixada
   no arquivo original é tratada como um único áudio; não houve separação de
   voz e música ou remoção garantida de música preexistente.
6. Manter aproximadamente 2min17s: a mudança de ritmo vem dos títulos, movimentos
   leves e continuidade sonora, sem resumir ou reordenar depoimentos.
7. Exportar em 720 × 1280, 30 fps constantes, MP4 H.264/yuv420p, CRF 20,
   AAC estéreo 192 kb/s a 48 kHz, faststart. A ampliação adapta o quadro ao
   formato, sem prometer recuperar detalhes do original.

## Legendas e análise local

Foram testados modelos Whisper tiny e small em execução local, obtidos do
repositório oficial k2-fsa/sherpa-onnx. O áudio não foi enviado a um serviço
externo de transcrição. O reconhecimento apresentou erros de palavras e
repetições; não foi usado para redigir legendas, identificar pessoas ou cortar
frases. Os resultados automáticos ficam apenas em `previews/edicao-v1/`, fora
Git, e não são uma transcrição revisada do evento.

## Reproduzir

Requer Python 3 e FFmpeg/FFprobe com libx264, AAC, libass e as fontes DejaVu
Sans existentes neste ambiente. Não usa Remotion nem sua licença.

```bash
cd /workspace/Edition-MP4/sipat-rejuntamix
python3 scripts/edit_sipat.py --preview  # 8 segundos, apenas se a saída não existir
python3 scripts/edit_sipat.py            # versão completa; recusa sobrescrever saída
```

O script gera os títulos ASS e mede loudness em `previews/edicao-v1/`;
para recalcular a medição após mudar os filtros de áudio, remova somente
`previews/edicao-v1/loudness-medicao.json` antes de renderizar novamente.
A composição, o vídeo e a medição desta versão usam o arquivo original
especificado no script. A exportação não depende dos modelos de transcrição.

Saída: `exports/SIPAT_RejuntaMix_Instagram_v1.mp4`.
Originais, previews e exportações não são versionados. O original permanece
idêntico à cópia enviada, conferido por SHA-256:
`94f7531d2f18f915dadd533e2ff1b69d35ff11c37b6a29123e9946d58e09ecf8`.

## Validação da exportação

- Decodificação integral de vídeo e áudio com `ffmpeg -xerror`: passou.
- 720 × 1280, H.264/yuv420p, 30 fps, 4112 frames; vídeo 137,067 s, áudio
  137,100 s (diferença inferior a um frame de 30 fps).
- Loudness medido do AAC final: -16,00 LUFS integrados, -1,44 dBTP de pico
  verdadeiro e faixa dinâmica de 7,50 LU; sem pico em 0 dBFS.
- Inspeção visual de frames da abertura, dos dois marcadores e do encerramento:
  títulos legíveis, fora dos rostos; ausência de nova logomarca.
- Tamanho final: 51.850.193 bytes (aproximadamente 52 MB).
- Conferência SHA-256 confirmou o original intacto.

A verificação do áudio foi técnica e por reconhecimento automático; não equivale
a uma audição humana integral para julgar inteligibilidade ou música já mixada.
