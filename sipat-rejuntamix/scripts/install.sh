#!/usr/bin/env bash
set -euo pipefail
cd /workspace/Edition-MP4/sipat-rejuntamix
# Ferramentas do sistema vêm na imagem preparada; não usa sudo ou instalação global.
for tool in node npm python3 ffmpeg ffprobe; do
  command -v "$tool" >/dev/null || { echo "Ferramenta ausente: $tool" >&2; exit 1; }
done
test -x "${REMOTION_BROWSER_EXECUTABLE:-/usr/bin/chromium}"
npm ci --no-audit --no-fund
npm run doctor
npm run lint
