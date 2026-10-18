"""Sound design for "NFT: del boom al ajuste", built from the Foley sprite.

Cuts come from audio-src/foley-sprite.wav using the start/duration table in
audio-src/foley-sprite.json (the "Foley Sprite Tester" artifact). Each cut is
placed on the animation's timing. Bars keep the sonification idea: the `ping`
cut is transposed so its pitch follows the bar's value. A light stereo room
glues the cuts together. Deterministic: re-running gives identical output.

Usage: python3 audio-src/build_from_sprite.py   (writes assets/audio/sfx.wav)
"""

import json
import os
import wave

import numpy as np

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "assets", "audio", "sfx.wav")
LENGTH = 31.0
rng = np.random.default_rng(2026)

with wave.open(os.path.join(HERE, "foley-sprite.wav")) as w:
    SR = w.getframerate()
    raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
SPRITE_AUDIO = raw.reshape(-1, 2).astype(np.float64) / 32768.0
with open(os.path.join(HERE, "foley-sprite.json")) as f:
    CUTS = json.load(f)


def cut(name, semitones=0.0, gain=1.0):
    c = CUTS[name]
    seg = SPRITE_AUDIO[int(c["start"] * SR): int((c["start"] + c["duration"]) * SR)]
    if semitones:
        rate = 2 ** (semitones / 12)
        src = np.arange(len(seg))
        dst = np.arange(0, len(seg) - 1, rate)
        seg = np.stack([np.interp(dst, src, seg[:, ch]) for ch in range(2)], axis=1)
    fade = min(len(seg) // 4, int(0.006 * SR))
    seg = seg.copy()
    seg[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return seg * gain


def semis_for(value, vmin, vmax, lo=-5, hi=7):
    return lo + (value - vmin) / (vmax - vmin) * (hi - lo)


def place(track, sound, at):
    i = int(at * SR)
    j = min(len(track), i + len(sound))
    track[i:j] += sound[: j - i]


def room(x, seconds=1.6, wet=0.22):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    out = np.empty_like(x)
    for ch in range(2):
        ir = np.convolve(rng.standard_normal(n), np.ones(16) / 16, mode="same") * np.exp(-t / (seconds / 5))
        ir /= np.sqrt(np.sum(ir ** 2))
        y = np.fft.irfft(np.fft.rfft(x[:, ch], size) * np.fft.rfft(ir, size), size)[: len(x)]
        out[:, ch] = (1 - wet) * x[:, ch] + wet * y * 1.4
    return out


def build():
    x = np.zeros((int(LENGTH * SR), 2))

    # 01 title (0–4s)
    place(x, cut("chime", gain=0.8), 0.4)
    place(x, cut("glide", gain=0.35), 1.1)
    place(x, cut("swoosh", gain=0.3), 3.55)

    # 02 global (4–14s): ping per bar, pitch = annual volume
    for i, v in enumerate([18.3, 21.9, 8.7, 8.9, 5.6, 1.9]):
        place(x, cut("ping", semis_for(v, 1.9, 21.9), gain=0.55), 4 + 1.1 + i * 0.4)
    place(x, cut("switch", gain=0.5), 4 + 4.6)   # peak turns dark gray
    place(x, cut("switch", -3, gain=0.5), 4 + 5.2)  # 2025 turns orange
    place(x, cut("drop", gain=0.65), 4 + 5.8)    # "−74 %" note
    place(x, cut("swoosh", gain=0.3), 13.55)

    # 03 categories (14–22s)
    place(x, cut("tap", gain=0.6), 14 + 1.1)     # art 2021
    place(x, cut("drop", -2, gain=0.6), 14 + 2.2)  # art 2025 collapse
    place(x, cut("ping", 7, gain=0.5), 14 + 3.7)   # sports +337 %
    place(x, cut("ping", 4, gain=0.5), 14 + 4.15)  # PFP +187 %
    place(x, cut("drop", gain=0.5), 14 + 4.6)    # gaming −17 %
    place(x, cut("swoosh", gain=0.3), 21.55)

    # 04 regions (22–28s): ping pitch = market share
    for i, share in enumerate([34.3, 24.8, 6.5]):
        place(x, cut("ping", semis_for(share, 0, 34.3), gain=0.5), 22 + 1.0 + i * 0.35)
    place(x, cut("swoosh", gain=0.3), 27.55)

    # 05 close (28–31s)
    place(x, cut("complete", gain=0.75), 28.3)

    return room(x)


def write(path, audio, peak_db=-6):
    audio = audio / (np.max(np.abs(audio)) + 1e-9) * 10 ** (peak_db / 20)
    fade = int(0.01 * SR)
    audio[-fade:] *= np.linspace(1, 0, fade)[:, None]
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    write(OUT, build())
    print("wrote", os.path.abspath(OUT))
