# Preparação editorial — SIPAT RejuntaMix

Etapa atual: somente preparação técnica. Não existe retrospectiva final nem
material oficial importado. Os testes usam padrões, cores e tom sintéticos.

## Quando o material chegar

1. Guardar os originais em `public/videos/` e manter cópia de segurança fora
   deste ambiente. Não sobrescrever, renomear ou converter o único original.
2. Inspecionar resolução, orientação, duração, codecs e áudio com `media.py probe`.
3. Se vier um MP4 montado, preservar sua sequência. Se vierem clipes separados,
   registrar a ordem explicitamente; o pipeline usa a ordem dos argumentos,
   sem ordenar nomes automaticamente.
4. Escolher 16:9 ou 9:16 somente após analisar os arquivos. Os presets de teste
   não determinam duração, FPS ou formato final da retrospectiva.
5. Adicionar a introdução da apresentadora, títulos e transições somente com
   material aprovado. A paleta provisória é laranja, preto e branco. Não criar
   uma logomarca: usar exclusivamente o arquivo oficial fornecido depois.

## Vozes, música e efeitos — orientação do usuário

- Em qualquer trecho com fala, inclusive ao trocar de quadro, não usar música.
- Priorizar a voz de quem fala, elevando e destacando sua presença sem clipping.
  Ajustar os ganhos após ouvir e medir o material, sem aumentos arbitrários agora.
- Efeitos sonoros, se usados, devem ser discretos, em nível de som ambiente.
- Legendas podem ser criadas, mas precisam de sincronização e revisão humana.
- Música somente onde apropriado e autorizado, fora dos trechos com fala.
- O pipeline básico não adiciona música, efeitos nem altera ganho da fala;
  apenas recodifica o áudio. Não há serviço de transcrição automática instalado.

## Extensões futuras, sem implementação nesta etapa

O Remotion permite títulos animados, mídia local via `staticFile()`, camadas de
logomarca, legendas e transições. Instalar pacotes adicionais apenas quando
necessários, com a mesma versão dos demais pacotes Remotion.

O FFmpeg permite filtros de texto/legendas, correção moderada de imagem e áudio,
mixagem e montagem sem Remotion. Essas decisões exigem análise dos originais;
nenhum desses tratamentos foi aplicado a material real nesta preparação.

O pipeline preparado preserva o enquadramento com barras quando necessário,
sem corte automático. HDR, rotação, VFR e gerenciamento de cor de arquivos reais
exigem inspeção antes da exportação definitiva.
