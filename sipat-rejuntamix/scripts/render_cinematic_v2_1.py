#!/usr/bin/env python3
"""Revisão pontual: encurta em 0,5 s a pausa entre as falas, preservando a v2."""
import argparse,json,sys
sys.dont_write_bytecode=True
from pathlib import Path
import render_cinematic_v2 as engine

p=argparse.ArgumentParser();p.add_argument('mode',choices=['sample','final']);args=p.parse_args()
cfg=json.loads((engine.ROOT/'src/config/cinematic-v2-1.json').read_text())
oldbase=engine.BASE
engine.BASE=engine.ROOT/'previews/cinematic-v2-1';engine.BASE.mkdir(exist_ok=True)
a,b=cfg['intro_pause_removed'];old_end=cfg['intro_end']+b-a
assert engine.digest(engine.ROOT/cfg['source'])==cfg['source_sha256']
engine.make_gradients();titles=engine.make_titles(cfg)
# Renderiza a introdução diretamente do original; a retrospectiva reutiliza os planos da v2.
intro=engine.BASE/'intro-720.mp4'
if not intro.exists():
    graph=(f'[0:v]split[x][y];[x]trim=start=0:end={a},setpts=PTS-STARTPTS[x1];'
           f'[y]trim=start={b}:end={old_end},setpts=PTS-STARTPTS[y1];'
           '[x1][y1]concat=n=2:v=1:a=0,fps=30,scale=720:1280:flags=lanczos,setsar=1,'
           'eq=contrast=1.035:saturation=1.025:gamma=1.015,unsharp=3:3:0.15,format=yuv420p[v]')
    engine.run(['ffmpeg','-hide_banner','-nostdin','-n','-i',str(engine.ROOT/cfg['source']),'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-an','-t',str(cfg['intro_end']),'-c:v','libx264','-crf','15','-preset','fast','-threads','2','-video_track_timescale','90000',str(intro)],engine.BASE/'intro.log')
voice=engine.BASE/'voz-master.wav'
if not voice.exists():
    graph=(f'[0:a]asplit[x][y];[x]atrim=end={a},asetpts=PTS-STARTPTS,afade=t=out:st={a-.005}:d=0.005[x1];'
           f'[y]atrim=start={b}:end={old_end},asetpts=PTS-STARTPTS,afade=t=in:d=0.005[y1];'
           '[x1][y1]concat=n=2:v=0:a=1[a]')
    engine.run(['ffmpeg','-hide_banner','-nostdin','-n','-i',str(oldbase/'voz-master.wav'),'-filter_complex',graph,'-map','[a]','-c:a','pcm_s24le',str(voice)],engine.BASE/'voz.log')
shots=[{'duration':cfg['intro_end']}]+cfg['shots']
paths=[intro]+[oldbase/'planos-720'/(s['id']+'.mp4') for s in cfg['shots']]
audio=[voice,oldbase/'musica-master.wav']
if args.mode=='sample':
    engine.join(cfg,shots,paths,audio,720,titles,engine.BASE/'amostra-juncao.mp4',seek=5.5,length=5)
else:
    engine.join(cfg,shots,paths,audio,720,titles,engine.ROOT/'exports/sipat-rejuntamix-cinematic-v2-1.mp4')
assert engine.digest(engine.ROOT/cfg['source'])==cfg['source_sha256']
