# Revisão pontual v2.1 — continuidade da apresentação

Pedido: encurtar a pausa entre a primeira e a segunda fala, sem alterar a montagem restante.

Removido o intervalo 7,60–8,10 s da introdução original, com corte conjunto de
imagem e áudio. Foram retirados 0,50 s ao redor da troca de tomada aos 8 s.
A escolha usa quadros do movimento da boca e medição da energia do áudio;
não constitui alegação de audição humana integral. As frases foram mantidas,
com microfades de 5 ms no áudio na junção para evitar estalos.

A retrospectiva mantém os mesmos planos, durações, textos, transições e música.
Sua entrada passa de 23,70 s para 23,20 s. Duração final: 79,20 s.
Formato mantido: 720 × 1280, 30 fps, H.264/AAC. A v2 anterior permanece intacta.

Configuração: `src/config/cinematic-v2-1.json`.
Render: `scripts/render_cinematic_v2_1.py`.
Saída: `exports/sipat-rejuntamix-cinematic-v2-1.mp4`.

Após preparar/renderizar a v2 para gerar seus planos intermediários e masters:

```bash
python3 scripts/render_cinematic_v2_1.py sample
python3 scripts/render_cinematic_v2_1.py final
```

A introdução é renderizada diretamente do original; os demais planos reutilizam
os intermediários de alta qualidade da v2. O vídeo final da v2 não é recodificado
como fonte. O ajuste do renderizador base apenas parametriza o tempo do gradiente
pela entrada musical, preservando os mesmos valores quando usado com a v2.
