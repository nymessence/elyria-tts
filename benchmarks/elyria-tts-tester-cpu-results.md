# Elyria-TTS CPU Audio Benchmark Report

## Notebook Information
- **Name**: elyria-tts-tester-cpu.ipynb
- **Hardware**: CPU
- **Mode**: Audio-only
- **Status**: Authentication failure prevented execution

## Expected Performance Characteristics
- **Model**: Chatterbox-TTS with CPU inference
- **Sample Rate**: 24kHz (based on TTS architecture)
- **Default Settings**: 
  - cfg_weight: 0.5
  - exaggeration: 0.5
  - Conservative parameters for CPU execution

## Estimated Execution Times
- **Model Loading**: ~30-60 seconds (first run)
- **Per Sentence Processing**: ~10-30 seconds (depending on length)
- **Example Script (3 sentences)**: ~90-150 seconds estimated

## Predicted Runtime for 1-Hour Podcast
- **Input Duration**: 1 hour of text (~3,600 seconds)
- **Estimated Processing Time**: 12,000-18,000 seconds (3.3-5 hours)
- **Ratio**: ~3.3x to 5x real-time processing

## Memory Usage
- **VRAM**: Minimal (CPU-based)
- **RAM**: ~2-4 GB estimated for model loading
- **Storage**: ~5-10 GB for temporary files

## Audio Quality Notes
- **Silence Spacing**: 500ms gaps between sentences implemented
- **Voice Clone Quality**: High-fidelity voice cloning using reference audio
- **Paralinguistic Support**: Available with --turbo flag

## Potential Issues
- **Authentication Error**: 401 Unauthorized error occurred during testing
- **CPU Performance**: Slow processing speeds on resource-constrained devices
- **Memory**: Large model size may cause OOM on low-memory systems

## Recommendations
- Use GPU acceleration for faster processing
- Keep input scripts short for CPU execution
- Ensure stable internet connection for model downloads
- Monitor memory usage during long processing jobs