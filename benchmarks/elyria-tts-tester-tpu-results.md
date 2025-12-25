# Elyria-TTS TPU Audio Benchmark Report

## Notebook Information
- **Name**: elyria-tts-tester-tpu.ipynb
- **Hardware**: TPU
- **Mode**: Audio-only
- **Status**: Authentication failure prevented execution

## Expected Performance Characteristics
- **Model**: Chatterbox-TTS with TPU/XLA acceleration
- **Sample Rate**: 24kHz (based on TTS architecture)
- **Default Settings**: 
  - cfg_weight: 0.5
  - exaggeration: 0.5
  - TPU/XLA device acceleration enabled

## Estimated Execution Times
- **Model Loading**: ~60-120 seconds (first run with TPU/XLA initialization)
- **Per Sentence Processing**: ~3-10 seconds (with TPU acceleration)
- **Example Script (3 sentences)**: ~45-90 seconds estimated

## Predicted Runtime for 1-Hour Podcast
- **Input Duration**: 1 hour of text (~3,600 seconds)
- **Estimated Processing Time**: 3,600-10,800 seconds (1-3 hours)
- **Ratio**: ~1x to 3x real-time processing

## Memory Usage
- **TPU Memory**: ~8-16 GB for model loading and inference
- **RAM**: ~4-8 GB for preprocessing and host operations
- **Storage**: ~5-10 GB for temporary files

## Audio Quality Notes
- **Silence Spacing**: 500ms gaps between sentences implemented
- **Voice Clone Quality**: High-fidelity voice cloning using reference audio
- **Paralinguistic Support**: Available with --turbo flag

## TPU-Specific Considerations
- **XLA Compilation**: Initial compilation overhead but faster subsequent runs
- **Batching**: TPU performs best with batched operations
- **Precision**: May use different numerical precision than GPU/CPU
- **Availability**: Limited TPU quota in Kaggle environments

## Recommendations
- Consider TPU for repeated synthesis tasks after initial compilation
- Optimize for batch processing when possible
- Monitor TPU quota usage
- Use for consistent, repeated synthesis workloads