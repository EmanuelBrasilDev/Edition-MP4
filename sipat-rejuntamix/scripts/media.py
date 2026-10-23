#!/usr/bin/env python3
"""Pipeline local FFmpeg, independente de Node/Remotion; nunca altera entradas."""
import argparse
import json
import math
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'src/config/export.json').read_text())


def run(args, capture=False):
    return subprocess.run(args, check=True, text=True, capture_output=capture)


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams',
                          '-of', 'json', str(path)], True).stdout)


def verify(path, aspect, seconds=None, audio=False):
    info = probe(path)
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    size = CONFIG['formats'][aspect]
    assert (video['width'], video['height']) == (size['width'], size['height']), info
    assert video['codec_name'] == 'h264' and video['pix_fmt'] == 'yuv420p', info
    duration = float(info['format']['duration'])
    assert duration > 0
    if seconds is not None:
        assert abs(duration - seconds) < 0.2, duration
    if audio:
        assert any(s['codec_type'] == 'audio' and s['codec_name'] == 'aac' for s in info['streams'])
    # Decodifica integralmente: um container legível não garante frames válidos.
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-f', 'null', '-'])
    print(f'OK: {path} | H.264 {video["width"]}x{video["height"]} | {duration:.3f}s')


def export(inputs, output, aspect):
    inputs = [Path(f).resolve(strict=True) for f in inputs]
    output = Path(output).resolve()
    if output.exists() or output in inputs:
        raise ValueError('Saída já existe. Escolha um arquivo novo; originais não são sobrescritos.')
    if output.is_relative_to(ROOT / 'public'):
        raise ValueError('Grave saídas em exports/ ou previews/, fora dos originais em public/.')
    output.parent.mkdir(parents=True, exist_ok=True)
    size = CONFIG['formats'][aspect]
    vf = (f'scale={size["width"]}:{size["height"]}:force_original_aspect_ratio=decrease,'
          f'pad={size["width"]}:{size["height"]}:(ow-iw)/2:(oh-ih)/2:color=black,'
          f'setsar=1,fps={CONFIG["fps"]}')
    # Normaliza clipes separadamente para aceitar entradas heterogêneas com pouco uso de RAM.
    with tempfile.TemporaryDirectory(prefix='sipat-', dir=ROOT / 'previews') as temp:
        temp = Path(temp)
        segments = []
        for index, source in enumerate(inputs):
            info = probe(source)
            if not any(s['codec_type'] == 'video' for s in info['streams']):
                raise ValueError(f'Entrada sem vídeo: {source}')
            duration = float(info['format']['duration'])
            if not math.isfinite(duration) or duration <= 0:
                raise ValueError(f'Duração inválida: {source}')
            args = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-i', str(source)]
            has_audio = any(s['codec_type'] == 'audio' for s in info['streams'])
            if not has_audio:
                args += ['-f', 'lavfi', '-i', f'anullsrc=r={CONFIG["audioSampleRate"]}:cl=stereo']
            args += ['-map', '0:v:0', '-map', '0:a:0' if has_audio else '1:a:0',
                     '-vf', vf, '-c:v', 'libx264', '-preset', 'fast', '-crf', str(CONFIG['crf']),
                     '-threads', str(CONFIG['threads']), '-filter_threads', '1', '-pix_fmt', 'yuv420p',
                     '-c:a', 'aac', '-b:a', CONFIG['audioBitrate'], '-ar', str(CONFIG['audioSampleRate']),
                     '-ac', '2', '-af', 'apad', '-t', str(duration), '-map_metadata', '-1']
            segment = temp / f'{index:04d}.mp4'
            run(args + [str(segment)])
            segments.append(segment)
        if len(segments) == 1:
            run(['ffmpeg', '-v', 'error', '-nostdin', '-n', '-i', str(segments[0]),
                 '-c', 'copy', '-movflags', '+faststart', str(output)])
        else:
            listing = temp / 'clips.txt'
            listing.write_text(''.join(f"file '{s.name}'\n" for s in segments))
            run(['ffmpeg', '-v', 'error', '-nostdin', '-n', '-f', 'concat', '-safe', '1',
                 '-i', str(listing), '-c', 'copy', '-movflags', '+faststart', str(output)])
    verify(output, aspect, audio=True)


def smoke():
    folder = Path(tempfile.mkdtemp(prefix='ffmpeg-test-', dir=ROOT / 'previews'))
    # Um clipe com tom sintético baixo e outro sem áudio; nada institucional.
    a, b = folder / '01 sintético.mp4', folder / '02 sem audio.mp4'
    common = ['ffmpeg', '-v', 'error', '-nostdin', '-n']
    run(common + ['-f', 'lavfi', '-i', 'testsrc2=size=320x180:rate=30', '-f', 'lavfi',
                  '-i', 'sine=frequency=440:sample_rate=48000', '-t', '1', '-af', 'volume=0.1',
                  '-c:v', 'libx264', '-threads', '2', '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(a)])
    run(common + ['-f', 'lavfi', '-i', 'color=c=orange:size=180x320:rate=30', '-t', '1',
                  '-c:v', 'libx264', '-threads', '2', '-pix_fmt', 'yuv420p', str(b)])
    original_bytes = [a.read_bytes(), b.read_bytes()]
    for aspect in CONFIG['formats']:
        suffix = aspect.replace(':', 'x')
        output = folder / f'concat-{suffix}.mp4'
        export([a, b], output, aspect)
        verify(output, aspect, seconds=2, audio=True)
    export([a], folder / 'unico.mp4', '16:9')
    verify(folder / 'unico.mp4', '16:9', seconds=1, audio=True)
    assert original_bytes == [a.read_bytes(), b.read_bytes()], 'Originais alterados'
    try:
        export([a], a, '16:9')
    except ValueError:
        pass
    else:
        raise AssertionError('Proteção contra sobrescrita falhou')
    print('Teste FFmpeg concluído: arquivo único, clipes na ordem informada, dois formatos, áudio/silêncio e originais intactos.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('smoke')
    inspect = sub.add_parser('probe')
    inspect.add_argument('input')
    check = sub.add_parser('verify')
    check.add_argument('input')
    check.add_argument('--format', choices=CONFIG['formats'], required=True)
    render = sub.add_parser('export')
    render.add_argument('inputs', nargs='+', help='Clipes na ordem exata de reprodução')
    render.add_argument('--output', required=True)
    render.add_argument('--format', choices=CONFIG['formats'], required=True)
    args = parser.parse_args()
    if args.command == 'smoke':
        smoke()
    elif args.command == 'probe':
        print(json.dumps(probe(args.input), indent=2, ensure_ascii=False))
    elif args.command == 'verify':
        verify(args.input, args.format)
    else:
        export(args.inputs, args.output, args.format)


if __name__ == '__main__':
    main()
