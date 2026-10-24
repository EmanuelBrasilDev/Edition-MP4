#!/usr/bin/env python3
"""Montagem cinematográfica reproduzível em FFmpeg, sem dependência de Remotion."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'src/config/cinematic-v2.json'
BASE = ROOT / 'previews/cinematic-v2'
FPS = 30


def run(args, log):
    with Path(log).open('w') as f:
        p = subprocess.run(args, stdout=f, stderr=subprocess.STDOUT)
    if p.returncode:
        raise RuntimeError(Path(log).read_text()[-7000:])


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        while block := f.read(1024 * 1024): h.update(block)
    return h.hexdigest()


def stamp(t):
    cs = round(t * 100)
    return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'



def make_gradients():
    # PNG RGBA gerado com biblioteca padrão: independente de Pillow/NumPy.
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    for name in ['top','bottom']:
        rows=[]
        for y in range(1280):
            alpha=(max(0,1-y/440)**1.4*145 if name=='top' else min(1,max(0,(y-560)/520))*155)
            row=bytearray(720*4)
            for x in range(720):
                weight=min(1,max(0,(680-x)/420)) if name=='top' else 1
                row[x*4+3]=int(alpha*weight)
            rows.append(bytes([0])+row)
        data=bytes([137,80,78,71,13,10,26,10])
        data+=chunk(b'IHDR',struct.pack('>IIBBBBB',720,1280,8,6,0,0,0))
        data+=chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b'')
        (BASE/f'gradient-{name}.png').write_bytes(data)

def make_titles(cfg):
    s = '''[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hero,DejaVu Sans,57,&H00FFFFFF,&H00FFFFFF,&H65000000,&H80000000,-1,0,0,0,100,100,0,0,1,1,1,7,0,0,0,1
Style: Label,DejaVu Sans,23,&H00FFFFFF,&H00FFFFFF,&H65000000,&H80000000,0,0,0,0,100,100,3,0,1,1,1,7,0,0,0,1
Style: Text,DejaVu Sans,38,&H00FFFFFF,&H00FFFFFF,&H65000000,&H80000000,-1,0,0,0,100,100,0,0,1,1,1,7,0,0,0,1
Style: Credit,DejaVu Sans,16,&H00FFFFFF,&H00FFFFFF,&H80000000,&H90000000,0,0,0,0,100,100,0,0,1,0.5,0,8,0,0,0,1
Style: Shape,DejaVu Sans,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    def add(a,b,style,text,layer=2):
        nonlocal s
        s += f'Dialogue: {layer},{stamp(a)},{stamp(b)},{style},,0,0,0,,{text}\n'
    # Tipografia livre de caixas; sombra local e linha laranja em movimento.
    add(.45,4.8,'Label',r'{\move(61,127,61,112,0,350)\fad(350,500)}REJUNTAMIX')
    add(.65,4.8,'Hero',r'{\move(57,177,57,157,0,420)\fad(350,500)}SIPAT')
    add(.85,4.8,'Shape',r'{\pos(61,237)\1c&H2082F5&\fscx0\t(0,450,\fscx100)\fad(150,500)\p1}m 0 0 l 118 0 l 118 4 l 0 4')
    t = cfg['intro_end']
    # Uma única passagem geométrica na mudança de linguagem, sem flashes.
    add(t,t+.6,'Shape',r'{\move(-260,0,980,0,0,600)\1c&H2082F5&\p1}m 0 0 l 70 0 l 330 1280 l 260 1280',5)
    add(t,t+.6,'Shape',r'{\move(-275,0,965,0,0,600)\1c&HFFFFFF&\1a&H55&\p1}m 0 0 l 5 0 l 265 1280 l 260 1280',6)
    add(t+.65,t+3.75,'Text',r'{\move(56,839,56,815,0,400)\fad(400,400)\fs43}Mente tranquila.')
    add(t+1.0,t+3.75,'Text',r'{\move(56,905,56,877,0,400)\fad(400,400)\fs40}Trabalho seguro.')
    # Três palavras aparecem em sequência; permanece longo intervalo sem texto.
    a = cfg['shots'][4]['timeline_in'] + .5
    for delay,y,text in [(0,150,'Aprender.'),(.45,210,'Prevenir.'),(.9,270,'Proteger.')]:
        add(a+delay,a+4.7,'Text',r'{\move(56,'+str(y+18)+',56,'+str(y)+r',0,400)\fad(350,500)\fs43}'+text)
    end = cfg['shots'][-1]['timeline_in']
    add(end+.35,end+5.7,'Label',r'{\pos(56,157)\fad(450,500)\1c&H2082F5&}REJUNTAMIX')
    add(end+.6,end+5.7,'Hero',r'{\move(52,223,52,205,0,400)\fad(450,500)\fs65}SIPAT')
    add(end+1,end+5.7,'Shape',r'{\pos(56,302)\1c&H2082F5&\fscx0\t(0,400,\fscx100)\fad(200,500)\p1}m 0 0 l 110 0 l 110 3 l 0 3')
    add(end+1,end+5.7,'Text',r'{\pos(56,935)\fad(450,500)\fs33}Juntos por um\Nambiente mais seguro.')
    add(end+.65,end+5.7,'Credit',r'{\pos(360,1063)\fad(350,500)}Música: "Inspired" — Kevin MacLeod (incompetech.com)\NCC BY 4.0 · Trecho editado\Ncreativecommons.org/licenses/by/4.0/')
    path = BASE/'titulos-v2.ass';path.write_text(s,encoding='utf-8');return path


def prepare_audio(cfg):
    source = ROOT/cfg['source'];music = ROOT/cfg['music']
    voice = 'highpass=f=75,afftdn=nr=5:nf=-42,equalizer=f=2600:t=q:w=1.1:g=1.3'
    results = []
    for name,media,start,duration,filters,lufs in [
        ('voz',source,0,cfg['intro_end'],voice,-16),
        ('musica',music,cfg['music_start'],cfg['music_duration'],'anull',-17),
    ]:
        out=BASE/f'{name}-master.wav'
        if not out.exists():
            cmd=['ffmpeg','-hide_banner','-nostdin','-ss',str(start),'-i',str(media),'-t',str(duration),'-vn','-af',filters+f',loudnorm=I={lufs}:TP=-1.8:LRA=9:print_format=json','-f','null','-']
            p=subprocess.run(cmd,capture_output=True,text=True,check=True)
            m=json.loads(re.findall(r'\{\s*"input_i".*?\}',p.stderr,re.S)[-1]);(BASE/f'{name}-medicao.json').write_text(json.dumps(m,indent=2))
            ln=(f'loudnorm=I={lufs}:TP=-1.8:LRA=9:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:'
                f'measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true')
            fade='' if name=='voz' else f',afade=t=in:d=0.04,afade=t=out:st={duration-2.4}:d=2.4'
            af=filters+','+ln+',aresample=48000'+fade+f',asetpts=PTS-STARTPTS,apad=whole_len={round(duration*48000)},atrim=end_sample={round(duration*48000)},asetpts=N/SR/TB'
            run(['ffmpeg','-hide_banner','-nostdin','-n','-ss',str(start),'-i',str(media),'-vn','-af',af,'-ar','48000','-ac','2','-c:a','pcm_s24le',str(out)],BASE/f'{name}-master.log')
        results.append(out)
    return results


def segment(cfg,shot,width,cache):
    height=width*16//9;duration=shot['duration'];tail=shot.get('transition_out',0)
    out=cache/(shot['id']+'.mp4');log=cache/(shot['id']+'.log')
    if out.exists() and out.stat().st_size>1000:return out
    frames=round((duration+tail)*FPS)
    prefix=['ffmpeg','-hide_banner','-nostdin','-n']
    if shot['motion']=='closing':
        still=BASE/'foto-equipe.png'
        if not still.exists():
            run(prefix+['-ss',str(shot['source_in']),'-i',str(ROOT/cfg['source']),'-frames:v','1','-vf','crop=478:358:0:246',str(still)],BASE/'foto-equipe.log')
        # A foto inteira fica nítida; o mesmo registro desfocado preenche o 9:16.
        fg=round(width*.9)//2*2;fh=round(fg*358/478)//2*2
        vf=(f'[0:v]split[bg][fg];[bg]scale={width}:{height}:force_original_aspect_ratio=increase,'
            f'crop={width}:{height},gblur=sigma={18*width/720},eq=saturation=0.75,colorchannelmixer=rr=0.38:gg=0.38:bb=0.38[back];'
            f'[fg]scale={fg}:{fh}:flags=lanczos[front];'
            rf'[back][front]overlay=x=(W-w)/2:y={height*.31:.3f}-{height*.006:.3f}*min(t/6\,1),'
            f'fps=30,setsar=1,format=yuv420p[v]')
        cmd=prefix+['-loop','1','-framerate','30','-i',str(still),'-filter_complex_threads','1','-filter_complex',vf,'-map','[v]']
    else:
        speed=(shot['source_out']-shot['source_in'])/duration
        grade={
            'intro':'eq=contrast=1.035:saturation=1.025:gamma=1.015',
            'day':'eq=contrast=1.045:saturation=1.035:gamma=1.015',
            'warm':'colorbalance=bs=0.012:bm=0.008,eq=contrast=1.035:saturation=1.015:gamma=1.025',
            'indoor':'colorbalance=rs=0.009:gm=-0.006,eq=contrast=1.045:saturation=1.025:gamma=1.035',
            'neutral':'eq=contrast=1.02:saturation=1.01',
        }[shot['grade']]
        vf=f'trim=duration={shot["source_out"]-shot["source_in"]},setpts=(PTS-STARTPTS)/{speed},fps=30,scale={width}:{height}:flags=lanczos,setsar=1'
        if shot['motion'] in ['push','pull']:
            p=rf'min(on/{max(round(duration*30)-1,1)}\,1)'
            ease=f'(0.5-0.5*cos(PI*{p}))'
            z='1+0.025*'+ease if shot['motion']=='push' else '1.025-0.025*'+ease
            vf+=f",zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={width}x{height}:fps=30"
        vf+=','+grade+f',unsharp=3:3:0.15,tpad=stop_mode=clone:stop_duration={tail+.15},trim=duration={duration+tail},format=yuv420p'
        cmd=prefix+['-ss',str(shot['source_in']),'-threads','1','-i',str(ROOT/cfg['source']),'-vf',vf]
    cmd+=['-an','-frames:v',str(frames),'-c:v','libx264','-preset','fast','-crf','15' if width==720 else '20','-threads','2','-filter_threads','1','-video_track_timescale','90000',str(out)]
    run(cmd,log);print('Plano pronto:',shot['id'],width,flush=True);return out


def join(cfg,shots,paths,audio,width,titles,out,seek=None,length=None):
    if out.exists():raise RuntimeError(f'Saída existente, não será sobrescrita: {out}')
    cmd=['ffmpeg','-hide_banner','-nostdin','-n']
    for p in paths:cmd+=['-threads','1','-i',str(p)]
    for p in audio:cmd+=['-i',str(p)]
    for name in ['gradient-top.png','gradient-bottom.png']:
        cmd+=['-loop','1','-framerate','30','-i',str(BASE/name)]
    graph=[]
    for i in range(len(paths)):graph.append(f'[{i}:v]settb=AVTB,setpts=PTS-STARTPTS,fps=30,settb=AVTB[v{i}]')
    current='v0';cursor=shots[0]['duration']
    for i in range(1,len(paths)):
        label=f'j{i}';fade=shots[i-1].get('transition_out',0)
        if fade:
            graph.append(f'[{current}][v{i}]xfade=transition=fade:duration={fade}:offset={cursor},fps=30,settb=AVTB[{label}]')
        else:
            graph.append(f'[{current}][v{i}]concat=n=2:v=1:a=0,fps=30,settb=AVTB[{label}]')
        current=label;cursor+=shots[i]['duration']
    # Gradiente discreto sob os textos, sem cobrir rostos com caixas.
    # Títulos ASS e faixa de transição usam coordenadas 720x1280 e escalam no preview.
    gi=len(paths)+2
    h=width*16//9
    middle=cfg['shots'][4]['timeline_in']+.5
    graph += [
        f'[{gi}:v]scale={width}:{h},format=rgba,split=2[gt0][gt1]',
        '[gt0]fade=t=in:st=0.4:d=0.35:alpha=1,fade=t=out:st=4.3:d=0.5:alpha=1[ga]',
        f'[gt1]fade=t=in:st={middle}:d=0.35:alpha=1,fade=t=out:st={middle+4.2}:d=0.5:alpha=1[gb]',
        f'[{gi+1}:v]scale={width}:{h},format=rgba,fade=t=in:st={cfg["intro_end"]}:d=0.4:alpha=1,fade=t=out:st={cfg["intro_end"]+3.35}:d=0.4:alpha=1[gc]',
        f'[{current}][ga]overlay=shortest=1[shade1]',
        '[shade1][gb]overlay=shortest=1[shade2]',
        '[shade2][gc]overlay=shortest=1[shaded]',
    ]
    graph.append(f"[shaded]ass=filename='{titles}':fontsdir=/usr/share/fonts/truetype/dejavu,fade=t=out:st={cfg['duration']-.6}:d=0.6,format=yuv420p[v]")
    n=len(paths)
    graph.append(f'[{n}:a][{n+1}:a]concat=n=2:v=0:a=1,atrim=duration={cfg["duration"]},asetpts=PTS-STARTPTS[a]')
    script=out.with_suffix('.ffgraph');script.write_text(';\n'.join(graph))
    cmd+=['-filter_complex_threads','1','-filter_complex_script',str(script),'-map','[v]','-map','[a]']
    if seek is not None:cmd+=['-ss',str(seek)]
    cmd+=['-t',str(length if length is not None else cfg['duration']),'-c:v','libx264','-preset','fast','-crf','19' if width==720 else '23','-threads','2','-c:a','aac','-b:a','192k','-ar','48000','-pix_fmt','yuv420p','-movflags','+faststart','-map_metadata','-1','-metadata','title=SIPAT RejuntaMix — Cinematic v2','-metadata','comment=Music: Inspired by Kevin MacLeod (incompetech.com). CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ — excerpt edited.',str(out)]
    run(cmd,out.with_suffix('.log'));print('Exportado:',out,flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['samples','preview','final']);args=p.parse_args()
    cfg=json.loads(CONFIG.read_text());BASE.mkdir(parents=True,exist_ok=True)
    assert digest(ROOT/cfg['source'])==cfg['source_sha256'],'Fonte foi alterada'
    make_gradients()
    titles=make_titles(cfg);audio=prepare_audio(cfg)
    width=720 if args.mode=='final' else 360
    cache=BASE/f'planos-{width}';cache.mkdir(exist_ok=True)
    intro={'id':'00_intro','source_in':0,'source_out':cfg['intro_end'],'duration':cfg['intro_end'],'motion':'none','grade':'intro'}
    shots=[intro]+cfg['shots']
    if args.mode=='samples':
        paths=[segment(cfg,s,width,cache) for s in shots[:2]]
        join(cfg,shots[:2],paths,audio,width,titles,BASE/'amostra-transicao.mp4',seek=21.7,length=6)
        closing=segment(cfg,shots[-1],width,cache)
        start=shots[-1]['timeline_in'];out=BASE/'amostra-encerramento.mp4'
        vf=f"setpts=PTS+{start}/TB,ass=filename='{titles}':fontsdir=/usr/share/fonts/truetype/dejavu,setpts=PTS-STARTPTS,fade=t=out:st=5.4:d=0.6"
        run(['ffmpeg','-hide_banner','-nostdin','-n','-i',str(closing),'-ss','50','-i',str(audio[1]),'-vf',vf,'-map','0:v','-map','1:a','-t','6','-c:v','libx264','-preset','fast','-crf','23','-threads','2','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],BASE/'amostra-encerramento.log')
        print('Amostras completas.',flush=True)
    else:
        paths=[segment(cfg,s,width,cache) for s in shots]
        out=BASE/'previa-completa-v2.mp4' if args.mode=='preview' else ROOT/'exports/sipat-rejuntamix-cinematic-v2.mp4'
        join(cfg,shots,paths,audio,width,titles,out)
    assert digest(ROOT/cfg['source'])==cfg['source_sha256'],'Original não foi preservado'


if __name__=='__main__':main()
