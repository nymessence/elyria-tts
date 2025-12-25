# Elyria-Video CPU Benchmark Report

## Notebook Information
- **Name**: elyria-video-tester-cpu.ipynb
- **Hardware**: CPU
- **Mode**: Video with audio narration
- **Status**: Authentication failure prevented execution

## Expected Performance Characteristics
- **Model**: Chatterbox-TTS with CPU inference + Image generation
- **Resolution**: Default 1920x1080
- **Sample Rate**: 24kHz (audio output)
- **FPS**: 30fps video output

## Estimated Execution Times
- **Model Loading**: ~60-120 seconds (first run)
- **Image Generation (per prompt)**: ~10-30 seconds (via API call)
- **Audio Generation (per sentence)**: ~10-30 seconds
- **Video Encoding**: ~5-15 seconds per minute of video
- **Example Script (2 images + 6 sentences)**: ~300-600 seconds estimated

## Predicted Runtime for 1-Hour Podcast Video
- **Input Duration**: 1 hour of text (~3,600 seconds)
- **Estimated Processing Time**: 18,000-36,000 seconds (5-10 hours)
- **Ratio**: ~5x to 10x real-time processing

## Memory Usage
- **RAM**: ~4-8 GB for model loading and inference
- **Storage**: ~50-100 GB for temporary image/audio files and final video
- **VRAM**: Minimal (CPU-based)

## Video Quality Notes
- **Silence Spacing**: 500ms gaps between sentences, 1000ms between slides
- **Image Generation**: Uses [IMG: prompt] tags for AI-generated visuals
- **Synchronization**: Audio and video properly synchronized based on timing
- **Format**: MP4 output with H.264 encoding

## Potential Issues
- **API Calls**: Depends on external image generation API (rate limits)
- **CPU Performance**: Slow processing for both audio and video encoding
- **Disk Space**: Large temporary files during processing
- **Memory**: Multiple large models loaded simultaneously

## Recommendations
- Use GPU for faster image and audio generation
- Plan for large storage requirements
- Consider shorter video segments for CPU processing
- Monitor API usage quotas for image generation