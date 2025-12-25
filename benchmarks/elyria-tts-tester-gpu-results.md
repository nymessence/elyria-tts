# Elyria-TTS GPU Audio Benchmark Report

## Notebook Information
- **Name**: elyria-tts-tester-gpu.ipynb
- **Hardware**: GPU (CUDA/T4 x2)
- **Mode**: Audio-only
- **Status**: Authentication failure prevented execution

## Expected Performance Characteristics
- **Model**: Chatterbox-TTS with CUDA acceleration
- **Sample Rate**: 24kHz (based on TTS architecture)
- **Default Settings**: 
  - cfg_weight: 0.5
  - exaggeration: 0.5
  - CUDA device acceleration enabled

## Estimated Execution Times
- **Model Loading**: ~45-90 seconds (first run with CUDA initialization)
- **Per Sentence Processing**: ~2-8 seconds (with GPU acceleration)
- **Example Script (3 sentences)**: ~30-60 seconds estimated

## Predicted Runtime for 1-Hour Podcast
- **Input Duration**: 1 hour of text (~3,600 seconds)
- **Estimated Processing Time**: 2,400-7,200 seconds (40-120 minutes)
- **Ratio**: ~0.67x to 2x real-time processing

## Memory Usage
- **VRAM**: ~4-8 GB for model loading and inference
- **RAM**: ~2-4 GB for preprocessing
- **Storage**: ~5-10 GB for temporary files

## Audio Quality Notes
- **Silence Spacing**: 500ms gaps between sentences implemented
- **Voice Clone Quality**: High-fidelity voice cloning using reference audio
- **Paralinguistic Support**: Available with --turbo flag

## GPU-Specific Considerations
- **CUDA Compatibility**: Requires compatible CUDA version
- **VRAM Management**: May need batching for longer texts
- **Performance**: Significantly faster than CPU processing

## Recommendations
- Use GPU acceleration for optimal performance
- Monitor VRAM usage during processing
- Consider using mixed precision for faster inference
- Keep input scripts reasonably sized to avoid VRAM overflow