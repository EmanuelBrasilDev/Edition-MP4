#!/usr/bin/env python3
"""Edição SIPAT v1: títulos, movimentos sutis e voz priorizada, sem música nova.
Requer apenas Python 3 e FFmpeg/FFprobe. Execute a partir de qualquer diretório.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'public/videos/WhatsApp Video 2026-10-23 at 16.22.38 (1).mp4'
WORK = ROOT / 'previews/edicao-v1'
OUTPUT = ROOT / 'exports/SIPAT_RejuntaMix_Instagram_v1.mp4'
# Mantém todos os clipes e toda a fala. Nenhum corte editorial de conteúdo.
DURATION = 137.1


def run(args, **kw):
    return subprocess.run(args, check=True, **kw)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while block := f.read(1024 * 1024):
            h.update(block)
    return h.hexdigest()


def overlays():
    # Títulos de seção, não legendas de falas. Área segura para a interface Reels.
    header = '''[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,DejaVu Sans,52,&H00FFFFFF,&H00FFFFFF,&H00101010,&H70000000,-1,0,0,0,100,100,1,0,1,1,1,7,0,0,0,1
Style: Small,DejaVu Sans,26,&H00FFFFFF,&H00FFFFFF,&H00101010,&H70000000,0,0,0,0,100,100,0,0,1,1,1,7,0,0,0,1
Style: Chapter,DejaVu Sans,27,&H00FFFFFF,&H00FFFFFF,&H00101010,&H70000000,-1,0,0,0,100,100,0,0,1,1,1,7,0,0,0,1
Style: Shape,DejaVu Sans,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    def event(start, end, style, text, layer=1):
        return f'Dialogue: {layer},{start},{end},{style},,0,0,0,,{text}\n'
    lines = [header]
    # Painel com fade sincronizado ao título, sem esconder a apresentadora.
    lines += [event('0:00:00.35','0:00:04.30','Shape',r'{\pos(48,120)\fad(250,350)\1c&H101010&\1a&H35&\p1}m 0 0 l 365 0 l 365 166 l 0 166',0),
              event('0:00:00.35','0:00:04.30','Shape',r'{\pos(48,120)\fad(250,350)\1c&H2082F5&\p1}m 0 0 l 5 0 l 5 166 l 0 166',1),
              event('0:00:00.35','0:00:04.30','Title',r'{\move(57,138,72,138,0,250)\fad(250,350)}SIPAT'),
              event('0:00:00.35','0:00:04.30','Small',r'{\move(57,208,72,208,0,250)\fad(250,350)\b1}REJUNTAMIX'),
              event('0:00:00.35','0:00:04.30','Small',r'{\pos(72,246)\fs21\fad(250,350)}Retrospectiva')]
    for start,end,text in [
        ('0:00:31.95','0:00:35.55','Momentos de aprendizado'),
        ('0:01:07.15','0:01:10.75','Troca de experiências'),
    ]:
        lines.append(event(start,end,'Shape',r'{\pos(48,970)\fad(200,300)\1c&H101010&\1a&H35&\p1}m 0 0 l 575 0 l 575 70 l 0 70',0))
        lines.append(event(start,end,'Shape',r'{\pos(48,970)\fad(200,300)\1c&H2082F5&\p1}m 0 0 l 5 0 l 5 70 l 0 70'))
        lines.append(event(start,end,'Chapter',r'{\move(57,989,70,989,0,200)\fad(200,300)}'+text))
    # Encerramento sobre a última foto, sem nova tela nem logomarca.
    lines += [event('0:02:13.35','0:02:16.60','Shape',r'{\pos(48,940)\fad(250,400)\1c&H101010&\1a&H35&\p1}m 0 0 l 575 0 l 575 115 l 0 115',0),
              event('0:02:13.35','0:02:16.60','Chapter',r'{\pos(70,957)\fad(250,400)\1c&H2082F5&}SIPAT · REJUNTAMIX'),
              event('0:02:13.35','0:02:16.60','Small',r'{\pos(70,1000)\fad(250,400)}Cuidado e segurança, juntos.')]
    path = WORK / 'titulos.ass'
    path.write_text(''.join(lines), encoding='utf-8')
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true', help='Apenas os primeiros 8 segundos')
    args = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    target = WORK / 'abertura-preview.mp4' if args.preview else OUTPUT
    if target.exists():
        raise SystemExit(f'Saída já existe, não será sobrescrita: {target}')
    digest = sha(SOURCE)
    ass = overlays()
    # Redução leve de ruído, remoção de graves e presença; sem alterar pitch/velocidade.
    voice = ('highpass=f=75,afftdn=nr=5:nf=-42,'
             'equalizer=f=2600:t=q:w=1.1:g=1.5,'
             'acompressor=threshold=0.125:ratio=2:attack=15:release=180:makeup=1')
    measurement = WORK / 'loudness-medicao.json'
    if not measurement.exists():
        result = run(['ffmpeg','-hide_banner','-nostdin','-i',str(SOURCE),'-t',str(DURATION),
                      '-vn','-af',voice+',loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json',
                      '-f','null','-'], capture_output=True, text=True)
        match = re.findall(r'\{\s*"input_i".*?\}', result.stderr, flags=re.S)
        if not match:
            raise RuntimeError('FFmpeg não forneceu medição de loudness')
        measurement.write_text(match[-1])
    loud = json.loads(measurement.read_text())
    normalize = (f'loudnorm=I=-16:TP=-1.5:LRA=7:measured_I={loud["input_i"]}:'
                 f'measured_TP={loud["input_tp"]}:measured_LRA={loud["input_lra"]}:'
                 f'measured_thresh={loud["input_thresh"]}:offset={loud["target_offset"]}:'
                 'linear=false:print_format=json')
    # Movimento suave de até 2,5%; nunca acelera a gravação ou a voz.
    zoom = "1+0.025*pow(sin(PI*mod(it,10)/10),2)"
    video = ("fps=30,scale=720:1280:flags=lanczos,setsar=1,"
             f"zoompan=z='{zoom}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=720x1280:fps=30,"
             'eq=contrast=1.02:saturation=1.02:gamma=1.005,'
             'unsharp=3:3:0.2,'
             f"ass=filename='{ass}':fontsdir=/usr/share/fonts/truetype/dejavu,"
             'fade=t=in:st=0:d=0.15,fade=t=out:st=136.5:d=0.6,format=yuv420p')
    audio = voice + ',' + normalize + ',aresample=48000,afade=t=out:st=129.09:d=0.1'
    command = ['ffmpeg','-hide_banner','-nostdin','-n','-i',str(SOURCE),
               '-map','0:v:0','-map','0:a:0','-t',str(8 if args.preview else DURATION),
               '-vf',video,'-af',audio,'-c:v','libx264','-preset','medium','-crf','20',
               '-pix_fmt','yuv420p','-threads','2','-filter_threads','2',
               '-c:a','aac','-b:a','192k','-ar','48000',
               '-movflags','+faststart','-map_metadata','-1',
               '-metadata','title=SIPAT RejuntaMix — Retrospectiva',str(target)]
    (WORK / ('comando-preview.json' if args.preview else 'comando-render.json')).write_text(
        json.dumps(command, indent=2, ensure_ascii=False))
    with (WORK / ('preview.log' if args.preview else 'render.log')).open('w') as log:
        run(command, stdout=log, stderr=subprocess.STDOUT)
    assert sha(SOURCE) == digest, 'Integridade do original não confere'
    info = json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(target)],
                          capture_output=True,text=True).stdout)
    (WORK / ('preview-ffprobe.json' if args.preview else 'export-ffprobe.json')).write_text(
        json.dumps(info,indent=2,ensure_ascii=False))
    print(f'Exportado: {target}', flush=True)
    print(f'Original preservado: SHA-256 {digest}', flush=True)


if __name__ == '__main__':
    main()
