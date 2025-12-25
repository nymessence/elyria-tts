#!/usr/bin/env python3
"""
Voice Synthesizer CLI using Chatterbox-TTS
"""

import argparse
import torch
from pathlib import Path
import torchaudio as ta
import perth


def main():
    parser = argparse.ArgumentParser(description="Nya Elyria Voice Synthesizer using Chatterbox-TTS")
    parser.add_argument("--voice", required=True, help="Path to the voice reference WAV file")
    parser.add_argument("--script", required=True, help="Path to the text script file")
    parser.add_argument("--output", required=True, help="Path for the output WAV file")
    parser.add_argument("--turbo", action="store_true", help="Use ChatterboxTurboTTS model for paralinguistic tags support")
    parser.add_argument("--device", choices=["cpu", "cuda", "gpu", "tpu"], default="cpu", help="Device to run inference on (cpu, cuda/gpu, or tpu)")

    args = parser.parse_args()

    # Map gpu alias to cuda
    device = args.device
    if device == "gpu":
        device = "cuda"

    print(f"Using device: {device}")

    # Check if required files exist
    voice_path = Path(args.voice)
    script_path = Path(args.script)

    if not voice_path.exists():
        raise FileNotFoundError(f"Voice file not found: {args.voice}")

    if not script_path.exists():
        raise FileNotFoundError(f"Script file not found: {args.script}")

    # Read the script content
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = f.read().strip()

    print(f"Synthesizing speech for: {script_text[:50]}...")

    # Import and initialize ChatterboxTTS or ChatterboxTurboTTS
    if args.turbo:
        try:
            from chatterbox.tts_turbo import ChatterboxTurboTTS
            print("Loading ChatterboxTurboTTS model (with paralinguistic tags support)...")
            tts = ChatterboxTurboTTS.from_pretrained(device=device)
        except ImportError:
            raise ImportError("ChatterboxTurboTTS not found. Please install chatterbox-tts.")
    else:
        try:
            from chatterbox import ChatterboxTTS
            print("Loading ChatterboxTTS model...")
            tts = ChatterboxTTS.from_pretrained(device=device)

            # Handle the case where watermarker is not available
            if perth.PerthImplicitWatermarker is None:
                print("Warning: Perth watermarker not available, using dummy watermarker")
                tts.watermarker = perth.DummyWatermarker()
        except ImportError:
            raise ImportError("ChatterboxTTS not found. Please install chatterbox-tts.")

    # Conservative defaults suitable for CPU inference
    cfg_weight = 0.5
    exaggeration = 0.5

    # Generate the audio using the voice reference
    print("Generating audio...")
    if args.turbo:
        # For turbo model, use audio prompt path in generate method
        audio = tts.generate(
            text=script_text,
            audio_prompt_path=str(voice_path),
            cfg_weight=cfg_weight,
            exaggeration=exaggeration
        )
    else:
        # For regular model, prepare conditionals first
        tts.prepare_conditionals(str(voice_path), exaggeration=exaggeration)
        audio = tts.generate(
            text=script_text,
            cfg_weight=cfg_weight,
            exaggeration=exaggeration
        )

    # Save the output using torchaudio
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ta.save(str(output_path), audio, tts.sr)

    print(f"Audio saved to: {args.output}")


if __name__ == "__main__":
    main()