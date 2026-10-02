from __future__ import annotations

import math
import shutil
import struct
import subprocess
import wave
from pathlib import Path


def generate_chime_wav(output_path: Path) -> None:
    """Synthesize a dual-tone soothing chime WAV using standard Python math & wave."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        return

    sample_rate = 44100
    duration_tone1 = 0.4
    duration_tone2 = 0.8
    total_samples = int(sample_rate * (duration_tone1 + duration_tone2))

    # Notes: D5 (587.33 Hz) -> A5 (880.00 Hz)
    freq1 = 587.33
    freq2 = 880.00

    frames = bytearray()
    split_sample = int(sample_rate * duration_tone1)

    for i in range(total_samples):
        if i < split_sample:
            t = i / sample_rate
            freq = freq1
            # Exponential decay envelope
            envelope = math.exp(-3.5 * t)
        else:
            t = (i - split_sample) / sample_rate
            freq = freq2
            envelope = math.exp(-2.5 * t)

        # Dual harmonic for rich bell-like tone
        val = 0.7 * math.sin(2.0 * math.pi * freq * t) + 0.3 * math.sin(
            4.0 * math.pi * freq * t
        )
        sample = int(val * envelope * 32767 * 0.4)
        sample = max(-32768, min(32767, sample))
        frames.extend(struct.pack("<h", sample))

    with wave.open(str(output_path), "wb") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(frames)


class SoundManager:
    """Manages audio chime generation and non-blocking playback."""

    def __init__(self) -> None:
        self.cache_dir = Path.home() / ".cache" / "pomodoro"
        self.wav_path = self.cache_dir / "chime.wav"
        self._player = self._find_player()
        self._ensure_chime()

    def _find_player(self) -> str | None:
        for player in ("pw-play", "paplay", "aplay"):
            if shutil.which(player):
                return player
        return None

    def _ensure_chime(self) -> None:
        try:
            generate_chime_wav(self.wav_path)
        except Exception:
            pass

    def play_chime(self) -> None:
        """Play chime in a fire-and-forget non-blocking process."""
        self._ensure_chime()
        if self._player and self.wav_path.exists():
            try:
                cmd = (
                    [self._player, "-q", str(self.wav_path)]
                    if self._player == "aplay"
                    else [self._player, str(self.wav_path)]
                )
                subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return
            except Exception:
                pass

        # Fallback to terminal bell
        print("\a", end="", flush=True)
