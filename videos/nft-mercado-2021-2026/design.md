# NFT: del boom al ajuste — design spec

Concepto: un informe financiero nocturno. Cada número tiene una barra que le da peso; el color dice si sube o baja.

## Paleta
- bg `#0D1321` (fondo, todas las escenas) · panel `#1D2D44` · muted `#9AAAC4` · fg `#F0EBD8`
- acento `#FCA311` (ámbar: pico, remates, cifra clave)
- suba `#2EC4B6` (teal) · baja `#E5383B` (rojo)

## Tipografía (embebidas)
- Display / cifras: Oswald 700 (uppercase en títulos)
- Datos, etiquetas, fuentes: IBM Plex Mono 400/700, `tabular-nums`

## Composición
- Márgenes 120px laterales, 96px arriba/abajo. Fuente siempre abajo a la izquierda, mono 20px muted.
- Fondo: grilla fina de puntos (data), glow ámbar tenue detrás del foco, número fantasma del año al 4 %.
- Sin pie charts, sin gridlines ni leyendas.
