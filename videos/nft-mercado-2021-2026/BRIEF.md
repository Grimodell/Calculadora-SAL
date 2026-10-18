---
workflow: general-video
flow: automation
storyboard: yes
message: "El mercado NFT pasó del boom de 2021–2022 a un ajuste profundo: cayó más de 70 % desde el pico"
aspect: 1920x1080
language: es
length: 30s
angle: data-viz
---

## Intent

Gráfico animado (data-viz) con las subas y bajas del mercado NFT en los últimos
5 años (2021–2026), por país y por rubro. Pedido del usuario: "un gráfico animado
que tenga la información de la suba y la baja del precio del NFT en los últimos
5 años, por país y por rubro". Sin narración, en español, 16:9, ~30 s.

## Customizations

- Métrica: volumen de ventas anual en USD (no precio unitario).
- Datos investigados de fuentes públicas, fuente citada en pantalla.
- Rubros: hitos verificados (no serie anual inventada).
- Países: cuota por región de un año, marcada como estimación de consultora.

- Sonido pedido por el usuario: "sonidos efectivos, modernos pero elegantes, del estilo de Designing with Sound (Amber Case, Aaron Day)". Sintetizado en audio-src/generate_sound.py: barras sonificadas (altura = valor), tonos suaves en los cambios de color, respiración en los cambios de escena, acorde final y colchón ambiental muy bajo.
- Ajuste del usuario: "más suaves, más reverb con armónicos, sumar el estilo sobrio de Apple productos" → tonos de cristal con armónicos, ataque lento, reverb estéreo larga (3,4 s), sin soplidos en los cambios de escena, volumen más bajo.

## Notes

- Estilo pedido por el usuario: "un estilo como el Cole Nussbaumer Knaflic, tipografía del estilo de Ellen Lupton, fondo blanco" (ver design.md).

- Volumen global: CryptoSlam (2021 18,3 · 2022 21,9 · 2023 8,7 · 2024 8,9 · 2025 5,63 · 2026 1,92 hasta 22-sep; miles de M USD).
- Rubros (DappRadar): Arte 2021 US$2.900 M → US$23,8 M (dato mar-2025); 3T-2025: PFP +187 % a US$544 M (vía CryptoPotato), Deportes +337 % a US$71,1 M, Gaming −17 % (único rubro en baja).
- Regiones: Norteamérica 34,3 % (2024, Market.us; EE. UU. US$7.380 M); Asia-Pacífico 24,8 % y China 6,5 % (2023, Grand View Research). Metodología de consultoras ≠ volumen on-chain: mostrar solo como cuotas, con aclaración.
- No inventar cifras. Toda cifra lleva fuente y período.
