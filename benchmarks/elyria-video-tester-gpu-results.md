# ELYRIA-VIDEO GPU BENCHMARK REPORT (UNVERIFIED)

## Status
- **State**: BLOCKED (Authentication failure after 3 retry attempts)
- **Execution**: NOT VERIFIED (synthetic estimate only)

## Notebook Information
- **Name**: elyria-video-tester-gpu.ipynb
- **Hardware**: GPU (CUDA/T4 x2)
- **Mode**: Video with audio narration
- **Status**: Authentication failure prevented execution

## Expected Performance Characteristics
- **Model**: Chatterbox-TTS with CUDA acceleration + Image generation
- **Resolution**: Default 1920x1080
- **Sample Rate**: 24kHz (audio output)
- **FPS**: 30fps video output

## Estimated Execution Times
- **Model Loading**: ~60-90 seconds (first run with CUDA initialization)
- **Image Generation (per prompt)**: ~5-15 seconds (with GPU acceleration)
- **Audio Generation (per sentence)**: ~2-8 seconds (with CUDA)
- **Video Encoding**: ~2-8 seconds per minute of video (with CUDA)
- **Example Script (2 images + 6 sentences)**: ~120-240 seconds estimated

## Predicted Runtime for 1-Hour Podcast Video
- **Input Duration**: 1 hour of text (~3,600 seconds)
- **Estimated Processing Time**: 7,200-14,400 seconds (2-4 hours)
- **Ratio**: ~2x to 4x real-time processing

## Memory Usage
- **VRAM**: ~6-10 GB for model loading and inference
- **RAM**: ~4-8 GB for preprocessing and image handling
- **Storage**: ~50-100 GB for temporary files and final video

## Video Quality Notes
- **Silence Spacing**: 500ms gaps between sentences, 1000ms between slides
- **Image Generation**: Uses [IMG: prompt] tags for AI-generated visuals
- **Synchronization**: Audio and video properly synchronized based on timing
- **Format**: MP4 output with H.264 encoding

## GPU-Specific Considerations
- **CUDA Acceleration**: Significantly faster audio processing than CPU
- **VRAM Management**: May need attention for large models
- **Video Encoding**: GPU-accelerated video encoding possible

## Recommendations
- Use GPU for optimal performance
- Monitor VRAM usage during processing
- Consider chunking longer videos into segments
- Plan for substantial storage requirements