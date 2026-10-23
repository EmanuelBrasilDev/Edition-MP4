import {spawnSync} from 'node:child_process';
import {existsSync} from 'node:fs';

for (const [tool, args] of [
  ['node', ['--version']], ['npm', ['--version']], ['python3', ['--version']],
  ['ffmpeg', ['-version']], ['ffprobe', ['-version']],
  [process.env.REMOTION_BROWSER_EXECUTABLE ?? '/usr/bin/chromium', ['--version']],
]) {
  const result = spawnSync(tool, args, {encoding: 'utf8'});
  if (result.error || result.status !== 0) throw new Error(`Ferramenta indisponível: ${tool}`);
  console.log(`${tool}: ${result.stdout.trim().split('\n')[0]}`);
}
for (const directory of ['public/videos', 'public/logos', 'public/musicas', 'public/imagens',
  'src/components', 'src/compositions', 'src/config', 'scripts', 'previews', 'exports', 'docs']) {
  if (!existsSync(directory)) throw new Error(`Diretório ausente: ${directory}`);
}
console.log('Ferramentas e estrutura disponíveis. Nenhuma credencial externa necessária.');
