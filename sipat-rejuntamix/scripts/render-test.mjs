import {spawnSync} from 'node:child_process';
import {mkdtempSync} from 'node:fs';
import {join} from 'node:path';

const output = mkdtempSync(join(process.cwd(), 'previews/remotion-test-'));
for (const [composition, format] of [['TesteHorizontal', '16:9'], ['TesteVertical', '9:16']]) {
  const file = join(output, `${composition}.mp4`);
  const result = spawnSync(process.execPath, ['node_modules/@remotion/cli/remotion-cli.js',
    'render', 'src/index.ts', composition, file, '--log=error'], {stdio: 'inherit'});
  if (result.status !== 0) process.exit(result.status ?? 1);
  const check = spawnSync('python3', ['scripts/media.py', 'verify', file, '--format', format], {stdio: 'inherit'});
  if (check.status !== 0) process.exit(check.status ?? 1);
}
console.log(`Renders sintéticos validados em ${output}`);
