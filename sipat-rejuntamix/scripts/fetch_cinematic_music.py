#!/usr/bin/env python3
"""Obtém a trilha escolhida da fonte oficial e confere o SHA-256 registrado."""
import hashlib
import json
from pathlib import Path
import urllib.request

root = Path(__file__).resolve().parents[1]
metadata = json.loads((root / 'docs/TRILHA_V2.json').read_text())
path = root / 'public/musicas/Inspired-Kevin-MacLeod.mp3'
path.parent.mkdir(parents=True, exist_ok=True)
if path.exists():
    if hashlib.sha256(path.read_bytes()).hexdigest() != metadata['sha256']:
        raise SystemExit('O arquivo existente difere da trilha validada; não será sobrescrito.')
else:
    temporary = path.with_suffix('.mp3.part')
    with urllib.request.urlopen(metadata['source_url'], timeout=60) as response, temporary.open('wb') as f:
        while block := response.read(1024 * 1024):
            f.write(block)
    if hashlib.sha256(temporary.read_bytes()).hexdigest() != metadata['sha256']:
        temporary.unlink()
        raise SystemExit('A fonte retornou um arquivo diferente; checksum não confere.')
    temporary.rename(path)
print('Trilha íntegra:', path)
print('Inspired — Kevin MacLeod (incompetech.com), CC BY 4.0. Manter os créditos.')
