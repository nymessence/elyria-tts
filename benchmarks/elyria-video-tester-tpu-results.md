# ELYRIA-VIDEO TPU BENCHMARK REPORT (UNVERIFIED)

## Status
- **State**: BLOCKED (Authentication failure after 3 retry attempts)
- **Execution**: NOT VERIFIED (synthetic estimate only)

## Notebook Information
- **Name**: elyria-video-tester-tpu.ipynb
- **Hardware**: TPU
- **Mode**: Video with audio narration
- **Status**: Authentication failure prevented execution

## Expected Performance Characteristics
- **Model**: Chatterbox-TTS with TPU/XLA acceleration + Image generation
- **Resolution**: Default 1920x1080
- **Sample Rate**: 24kHz (audio output)
- **FPS**: 30fps video output

## Estimated Execution Times
- **Model Loading**: ~90-150 seconds (first run with TPU/XLA initialization)
- **Image Generation (per prompt)**: ~10-30 seconds (via API call, not TPU accelerated)
- **Audio Generation (per sentence)**: ~3-10 seconds (with TPU/XLA)
- **Video Encoding**: ~5-15 seconds per minute of video (CPU-based)
- **Example Script (2 images + 6 sentences)**: ~180-360 seconds estimated

## Predicted Runtime for 1-Hour Podcast Video
- **Input Duration**: 1 hour of text (~3,600 seconds)
- **Estimated Processing Time**: 10,800-21,600 seconds (3-6 hours)
- **Ratio**: ~3x to 6x real-time processing

## Memory Usage
- **TPU Memory**: ~10-16 GB for model loading and inference
- **RAM**: ~6-10 GB for preprocessing and image handling
- **Storage**: ~50-100 GB for temporary files and final video

## Video Quality Notes
- **Silence Spacing**: 500ms gaps between sentences, 1000ms between slides
- **Image Generation**: Uses [IMG: prompt] tags for AI-generated visuals
- **Synchronization**: Audio and video properly synchronized based on timing
- **Format**: MP4 output with H.264 encoding

## TPU-Specific Considerations
- **XLA Compilation**: Initial overhead but faster subsequent runs
- **Batch Processing**: TPU performs best with batched operations
- **Audio Generation**: Significantly faster with TPU than CPU
- **Video Encoding**: Still CPU-based, so limited improvement for final encoding

## Recommendations
- Consider TPU for repeated synthesis tasks after initial compilation
- Optimize for batch processing when possible
- Monitor TPU quota usage
- Best for consistent, repeated synthesis workloads with audio generation