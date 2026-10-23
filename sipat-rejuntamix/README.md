# SIPAT — RejuntaMix: ambiente de edição

A reedição cinematográfica v2 está documentada em [docs/CINEMATIC_V2.md](docs/CINEMATIC_V2.md),
com timeline editável, trilha licenciada e comandos de renderização.
As instruções abaixo registram a preparação técnica inicial.

Na preparação inicial, foram usados somente testes técnicos sintéticos.
As edições posteriores usam os vídeos enviados pelo usuário; a v2 tem trilha
licenciada e preserva os originais e a primeira edição.

## Ferramentas e instalação

Validadas em Debian 13 x86_64: Node.js 24.19.0, npm 11.9.0, Python 3.12.14,
FFmpeg/FFprobe 7.1.5 e Chromium 154.0.8037.57, já existentes no ambiente.
Instalados localmente: Remotion 4.0.538 (CLI e renderer), React 19.2.3 e ferramentas
TypeScript/ESLint do template oficial Blank. As Agent Skills oficiais estão em
`.agents/skills/`. Não houve instalação global, sudo, compra ou API externa.

Para reproduzir a instalação neste ambiente:

```bash
cd /workspace/Edition-MP4/sipat-rejuntamix
bash scripts/install.sh
```

O script usa `npm ci` e o lockfile. O cache npm fica em `/workspace/.cache/npm`.
Em outra máquina, instale primeiro Node compatível com `package.json`, Python 3,
FFmpeg/FFprobe com libx264/AAC e Chromium. Ajuste o cache em `.npmrc` se necessário.
Se Chromium estiver em outro caminho, use `REMOTION_BROWSER_EXECUTABLE` nos
comandos Remotion. Não é necessário baixar navegador pelo Remotion.

## Iniciar e visualizar

```bash
cd /workspace/Edition-MP4/sipat-rejuntamix
npm run dev
```

O Studio escuta na porta 3000. Em máquina local, abra no navegador o endereço
impresso pelo comando. Na nuvem, o acesso visual depende do encaminhamento de
porta disponibilizado pelo cliente; a interface de onboarding não oferece
preview web integrado. Não há link público criado. O processo precisa ser
reiniciado em cada sessão; não faz parte do snapshot.

Escolha `TesteHorizontal` ou `TesteVertical`: composições sintéticas de dois
segundos, em laranja, preto e branco. Esses presets **não definem o formato ou a
duração do vídeo real**. Em outro terminal, valide o Studio:

```bash
npm run test:studio
```

## Onde colocar os arquivos

| Material | Diretório relativo ao projeto |
| --- | --- |
| MP4 já montado ou clipes originais | `public/videos/` |
| Logomarca oficial, a fornecer | `public/logos/` |
| Músicas com autorização de uso | `public/musicas/` |
| Imagens autorizadas | `public/imagens/` |
| Testes e arquivos intermediários | `previews/` |
| Exportações aprovadas | `exports/` |

Não altere os originais. Guarde também uma cópia de segurança fora do ambiente.
Essas pastas de mídia, renders, dependências e caches são ignoradas pelo Git.
Não coloque credenciais no projeto. O fluxo atual não requer nenhuma.

## Testar

```bash
npm run doctor         # ferramentas e diretórios
npm run lint           # ESLint + TypeScript
npm run test:ffmpeg     # MP4 único, clipes heterogêneos, áudio/silêncio e dois formatos
npm run test:remotion   # dois renders sintéticos de 2 segundos + FFprobe e decode
npm test               # todos os anteriores, sem exigir Studio ligado
npm run test:studio    # exige npm run dev em outro terminal
npm run build          # bundle local em previews/bundle
```

Os testes criam subpastas únicas em `previews/` e não sobrescrevem arquivos.
A renderização usa dois workers, sem exigir GPU. Consulte
[docs/VALIDACAO.md](docs/VALIDACAO.md) para resultados e limitações.

## Exportar no futuro — somente depois da análise dos originais

O pipeline FFmpeg é independente de Node, npm e Remotion. Usa apenas Python 3
com biblioteca padrão, FFmpeg e FFprobe. Inspecione primeiro:

```bash
python3 scripts/media.py probe public/videos/sipat.mp4
```

Exemplos **para a etapa futura**, não executados com material institucional:

```bash
# Um MP4 já montado: mantém a sequência e o áudio, sem acrescentar música.
python3 scripts/media.py export public/videos/sipat.mp4 \
  --format 16:9 --output exports/sipat-horizontal.mp4

# Clipes separados: a ordem é exatamente a dos argumentos.
python3 scripts/media.py export public/videos/01.mp4 public/videos/02.mp4 \
  --format 9:16 --output exports/sipat-vertical.mp4
```

Escolha explicitamente o formato após analisar o material. O script prepara
H.264, yuv420p, CRF 18, AAC 192 kb/s, 48 kHz, MP4 com faststart, enquadramento
inteiro com barras quando necessário e sem cortes automáticos. Os clipes são
normalizados em arquivos temporários antes da concatenação. Clipes sem áudio
recebem silêncio. O ganho da fala não é alterado automaticamente. Saídas
existentes são recusadas e nada é gravado em `public/` pelo pipeline.

Configurações centralizadas: `src/config/export.json`. FPS 30 e resolução Full HD
são presets iniciais de teste, sujeitos à análise dos vídeos reais. A exportação
recodifica e pode usar espaço temporário proporcional à duração do material.

Para repetir apenas os renders técnicos Remotion, use `npm run test:remotion`.
As composições atuais não incluem os vídeos reais; a composição definitiva será
criada somente em etapa posterior.

## Orientações editoriais e pendências

- Sem música durante falas, inclusive nas trocas de quadro. Priorizar e destacar
  as vozes sem distorção; efeitos sonoros baixos, em nível ambiente. Legendas
  poderão ser criadas e revisadas após receber o material.
- Aguardar vídeos, logomarca oficial, músicas autorizadas e escolha do formato.
  Nenhuma transcrição, correção de imagem ou mixagem real foi feita.
- **Licença Remotion:** empresas com fins lucrativos com mais de três funcionários
  precisam de Company License. Confirmar o enquadramento da RejuntaMix antes do
  uso comercial; nenhuma licença foi presumida ou adquirida. Os testes atuais
  são avaliação técnica. O fluxo FFmpeg permanece independente.
- O site Remotion foi bloqueado pelo proxy; fontes oficiais foram consultadas
  pelo GitHub e pela licença incluída no pacote. Domínios foram salvos no
  rascunho de rede; salvar o rascunho não aplica nem publica a configuração.

Detalhes: [projeto e áudio](docs/PROJETO.md),
[licenciamento](docs/LICENCIAMENTO.md), [validação](docs/VALIDACAO.md).
