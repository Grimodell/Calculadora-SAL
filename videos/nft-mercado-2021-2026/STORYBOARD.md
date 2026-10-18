---
format: 1920x1080
duration: 30s
message: "El mercado NFT pasó del boom de 2021–2022 a un ajuste profundo: cayó más de 70 % desde el pico"
arc: Hook → Evolución global → Rubros → Regiones → Cierre
audience: público general / redes y presentaciones, en español
mode: collaborative
---

## Frame 1 — Título

- scene: "NFT: del boom al ajuste" + "Volumen de ventas 2021–2026"
- duration: 4s
- transition_in: cut
- status: built
- src: compositions/frames/01-titulo.html
- blueprint: titlecard-reveal

Apertura limpia: título grande, subtítulo con el período y la métrica. Un único movimiento (slide-up + fade), luego quieto.

## Frame 2 — Evolución global

- scene: Barras por año 2021→2026* que crecen con contador; pico 2022 marcado; remate "−74 % desde el pico"
- duration: 10s
- transition_in: crossfade
- status: built
- src: compositions/frames/02-global.html
- blueprint: dataviz-countup

Barras (miles de M USD): 2021 18,3 · 2022 21,9 (pico) · 2023 8,7 · 2024 8,9 · 2025 5,63 · 2026* 1,92 (hasta 22-sep, barra rayada/parcial).
Flechas ▲/▼ con % interanual sobre cada barra. Remate: −74 % (2025 vs 2022). Fuente: CryptoSlam.

## Frame 3 — Por rubro

- scene: 4 tarjetas con flecha de suba/baja: Arte, PFP, Deportes, Gaming
- duration: 8s
- transition_in: crossfade
- status: built
- src: compositions/frames/03-rubros.html
- blueprint: grid-card-assemble

- Arte ▼ US$2.900 M (2021) → US$23,8 M (dato mar-2025)
- PFP (avatares) ▲ +187 % → US$544 M (3T 2025)
- Deportes ▲ +337 % → US$71,1 M (3T 2025)
- Gaming ▼ −17 % (3T 2025), único rubro en baja
Fuente: DappRadar.

## Frame 4 — Por región

- scene: Barras horizontales de cuota: Norteamérica 34,3 %, Asia-Pacífico 24,8 %, China 6,5 %
- duration: 6s
- transition_in: crossfade
- status: built
- src: compositions/frames/04-regiones.html
- blueprint: dataviz-countup

Norteamérica 34,3 % (2024; EE. UU. US$7.380 M) — Market.us. Asia-Pacífico 24,8 %, China 6,5 % (2023) — Grand View Research.
Nota al pie: "Estimaciones de consultoras; metodología distinta al volumen on-chain".

## Frame 5 — Cierre

- scene: "−74 % de volumen desde el pico de 2022 · precio promedio por venta: US$124 → US$96 (2024→2025)" + fuentes
- duration: 3s
- transition_in: crossfade
- status: built
- src: compositions/frames/05-cierre.html
- blueprint: titlecard-reveal

Conclusión y lista de fuentes (CryptoSlam, DappRadar, Market.us, Grand View Research).
