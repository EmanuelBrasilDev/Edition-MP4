# Evidências de preparação — 23/10/2026

## Ferramentas

- Debian GNU/Linux 13, Linux x86_64.
- Node.js 24.19.0 e npm 11.9.0 existentes, sem atualização global.
- Python 3.12.14 existente, usado apenas com biblioteca padrão.
- FFmpeg e FFprobe 7.1.5 existentes, com libx264 e AAC.
- Chromium 154.0.8037.57 existente em `/usr/bin/chromium`.
- Remotion CLI, renderer e biblioteca 4.0.538; React/React DOM 19.2.3.
- Dependências locais fixadas por `package-lock.json`.

## Testes executados

- Verificação das ferramentas e diretórios: passou.
- ESLint e TypeScript: passaram.
- FFmpeg: arquivo único e concatenação na ordem informada; clipes de proporções
  diferentes, com áudio e sem áudio; MP4 H.264/AAC 16:9 e 9:16; decode integral;
  originais byte a byte intactos e recusa de sobrescrita: passaram.
- Remotion: renders sintéticos completos de dois segundos (60 frames) em
  1920x1080 e 1080x1920, H.264/yuv420p; FFprobe e decode integral: passaram.
- Studio: servidor iniciou na porta 3000; Chromium carregou ambas as rotas e
  confirmou o texto da composição no DOM: passou.
- Reinstalação reproduzível com `bash scripts/install.sh` (`npm ci`, doctor e
  lint/TypeScript): passou. Studio reiniciado e as duas composições verificadas
  novamente após reinstalar: passaram.
- Bundle de produção com `npm run build`, gravado em `previews/bundle`: passou.

Instruções completas de instalação (`install_script`) e reinício/validação
(`start_skill`) foram persistidas no rascunho da configuração do ambiente,
assim como os dois domínios de documentação. O usuário deve revisar e salvar
nas configurações e publicar o ambiente. Publicação e restauração em uma tarefa
nova não foram executadas nem verificadas nesta sessão.

Resultados sintéticos estão em subpastas únicas de `previews/`, ignoradas pelo
Git. Não representam a retrospectiva final.

## Dificuldades resolvidas e limites

- Cache padrão npm fora da área gravável: configurado cache em
  `/workspace/.cache/npm`, sem modificar o ambiente global.
- `create-video@4.0.538 --yes --blank --no-tailwind` falhou por DNS em seu acesso
  direto; obtido o mesmo template `remotion-dev/template-empty` pelo Git HTTPS
  da plataforma, sem copiar seu `.git`.
- Primeiro render produziu faixa de cor completa (`yuvj420p`). Configuração
  BT.709 explícita corrigiu para `yuv420p`; ambos os renders foram repetidos
  com sucesso após a correção.
- Site `www.remotion.dev` respondeu com bloqueio do proxy. Documentação e
  licença foram consultadas nas fontes oficiais via GitHub e no pacote
  instalado. Os domínios `www.remotion.dev` e `remotion.dev` foram adicionados
  ao rascunho da política de rede, sem presumir aplicação imediata.
- Não há visualização web integrada nesta interface de onboarding. O Studio
  foi validado internamente em Chromium; acesso visual pelo usuário depende
  de encaminhamento de porta oferecido pelo cliente ou execução local.
- Nenhum arquivo real foi analisado; qualidade do áudio, legendas, HDR,
  enquadramento e duração reais ainda não podem ser validados.
- Licença comercial Remotion pendente de enquadramento; consultar
  `LICENCIAMENTO.md`. FFmpeg funciona de modo independente.

## Origem dos recursos oficiais

- Template: `https://github.com/remotion-dev/template-empty`, commit
  `bad1be9984b08a9ee3f3eee1df98765caa04ca11`.
- Agent Skills: `https://github.com/remotion-dev/skills`, commit
  `6c67adcd9cdbe6eb84d76342da89b225f9161cb2`, copiadas integralmente para
  `.agents/skills/` a partir do diretório oficial `skills/`.
- Documentação: `https://github.com/remotion-dev/remotion`, commit
  `1c7c484efbbbe96d9ecd0abb4440af54222d4874`.

As skills ficam locais ao projeto; nenhum agente adicional foi iniciado.
