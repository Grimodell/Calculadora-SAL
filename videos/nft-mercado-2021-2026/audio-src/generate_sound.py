"""Sound design for "NFT: del boom al ajuste".

Approach after Amber Case & Aaron Day, *Designing with Sound*: few sounds,
short and soft, each one carrying information. Bars are sonified (pitch
follows the value), so the rise and fall can be heard; colour changes get a
gentle tone; scene changes get a quiet breath. Everything is synthesized and
deterministic (seeded noise), so a re-run produces identical files.

Usage: python3 audio-src/generate_sound.py   (writes assets/audio/*.wav)
"""

import os
import wave

import numpy as np

SR = 48000
LENGTH = 31.0
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "audio")
rng = np.random.default_rng(2026)

# C major pentatonic, C4..A5 — any two notes sound consonant together.
SCALE = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25, 783.99, 880.00]


def pitch_for(value, vmin, vmax):
    idx = round((value - vmin) / (vmax - vmin) * (len(SCALE) - 1))
    return SCALE[max(0, min(len(SCALE) - 1, idx))]


def env(n, attack, tau):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1)
    return a * np.exp(-t / tau)


def pluck(freq, dur=0.9, tau=0.22, gain=1.0):
    """Soft marimba-like pluck: fundamental plus a quiet 4x partial."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * freq * t) + 0.18 * np.sin(2 * np.pi * freq * 4 * t) * np.exp(-t / 0.05)
    return gain * tone * env(n, 0.004, tau)


def bell(freqs, dur=2.2, tau=0.7, gain=1.0):
    """Gentle chime: a few sine partials with a slow decay."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    tone = sum(np.sin(2 * np.pi * f * t) * (0.8 ** i) for i, f in enumerate(freqs))
    return gain * tone / len(freqs) * env(n, 0.012, tau)


def breath(dur=0.5, gain=1.0):
    """Quiet filtered-noise swell for scene changes."""
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    kernel = np.ones(220) / 220  # crude low-pass
    soft = np.convolve(noise, kernel, mode="same")
    shape = np.sin(np.pi * np.arange(n) / n) ** 2
    return gain * soft * shape


def place(track, sound, at):
    i = int(at * SR)
    j = min(len(track), i + len(sound))
    track[i:j] += sound[: j - i]


def reverb(x, seconds=1.4, wet=0.18):
    n = int(seconds * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / (seconds / 5))
    ir /= np.sqrt(np.sum(ir ** 2))
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return (1 - wet) * x + wet * y


def write(path, mono, peak_db):
    mono = mono / (np.max(np.abs(mono)) + 1e-9) * 10 ** (peak_db / 20)
    fade = int(0.01 * SR)
    mono[-fade:] *= np.linspace(1, 0, fade)
    stereo = np.repeat((mono * 32767).astype(np.int16)[:, None], 2, axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())


def build_sfx():
    x = np.zeros(int(LENGTH * SR))

    # 01 title (0–4s): opening chime, a tick for the rule
    place(x, bell([392.00, 587.33, 783.99], gain=0.55), 0.4)
    place(x, pluck(1046.5, dur=0.3, tau=0.05, gain=0.18), 1.1)

    # 02 global (4–14s): one pluck per bar, pitch = annual volume
    volumes = [18.3, 21.9, 8.7, 8.9, 5.6, 1.9]
    for i, v in enumerate(volumes):
        place(x, pluck(pitch_for(v, 1.9, 21.9), gain=0.55), 4 + 1.1 + i * 0.4)
    place(x, bell([523.25, 783.99], dur=1.4, tau=0.4, gain=0.35), 4 + 4.6)  # peak turns dark gray
    place(x, bell([293.66, 440.00], dur=1.4, tau=0.4, gain=0.38), 4 + 5.2)  # 2025 turns orange
    place(x, pluck(392.00, gain=0.45), 4 + 5.8)  # "−74 %": falling fifth
    place(x, pluck(261.63, dur=1.4, tau=0.45, gain=0.5), 4 + 6.05)

    # 03 categories (14–22s): art falls; diverging bars rise / fall
    place(x, pluck(659.25, gain=0.5), 14 + 1.1)
    place(x, pluck(261.63, dur=1.2, tau=0.35, gain=0.5), 14 + 2.2)
    for i, (f, g) in enumerate([(880.00, 0.5), (783.99, 0.48), (293.66, 0.45)]):
        place(x, pluck(f, gain=g), 14 + 3.7 + i * 0.45)

    # 04 regions (22–28s): pitch = market share
    for i, share in enumerate([34.3, 24.8, 6.5]):
        place(x, pluck(pitch_for(share, 0, 34.3), gain=0.5), 22 + 1.0 + i * 0.35)

    # 05 close (28–31s): resolving chord
    place(x, bell([261.63, 392.00, 523.25, 587.33], dur=2.7, tau=0.9, gain=0.6), 28.3)

    # scene changes: quiet breath
    for at in (3.55, 13.55, 21.55, 27.55):
        place(x, breath(gain=0.06), at)

    return reverb(x)


def build_pad():
    """Very low ambient bed: an open fifth on A with slow movement."""
    t = np.arange(int(LENGTH * SR)) / SR
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.08 * t)
    pad = (np.sin(2 * np.pi * 110.0 * t) + 0.6 * np.sin(2 * np.pi * 164.81 * t)
           + 0.25 * np.sin(2 * np.pi * 220.0 * t + 0.3) * lfo)
    shape = np.clip(t / 2.0, 0, 1) * np.clip((LENGTH - t) / 2.5, 0, 1)
    return pad * shape * (0.85 + 0.15 * lfo)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    write(os.path.join(OUT_DIR, "sfx.wav"), build_sfx(), peak_db=-6)
    write(os.path.join(OUT_DIR, "pad.wav"), build_pad(), peak_db=-26)
    print("wrote", os.path.abspath(OUT_DIR))
