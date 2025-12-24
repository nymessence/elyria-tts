#!/usr/bin/env python3
"""
Simple test for video_synthesizer.py functionality without API calls
"""

import tempfile
from pathlib import Path
from video_synthesizer import parse_script, create_blank_image
import cv2
import numpy as np
from pydub import AudioSegment


def simple_test():
    print("Testing video_synthesizer functionality...")
    
    # Parse the test script
    segments = parse_script('test_video_script.txt')
    print(f"Parsed {len(segments)} segments")
    
    # Create temporary directory for assets
    temp_dir = Path(tempfile.mkdtemp())
    print(f"Created temp directory: {temp_dir}")
    
    # Create test images using fallback
    width, height = 1280, 720  # 720p resolution
    images = []
    
    for i, segment in enumerate(segments):
        if segment['type'] == 'image':
            print(f"Creating fallback image for: {segment['prompt'][:50]}...")
            img = create_blank_image(width, height, f"IMG {i+1}: {segment['prompt'][:30]}...")
            img_path = temp_dir / f"img_{i}.jpg"
            img.save(img_path)
            images.append(str(img_path))
    
    print(f"Created {len(images)} test images")
    
    # Create simple silent audio for each text segment
    audio_segments = []
    for i, segment in enumerate(segments):
        if segment['type'] == 'text':
            # Create a short silent audio file for the text
            duration_ms = 2000  # 2 seconds per text segment
            silent = AudioSegment.silent(duration=duration_ms)
            audio_path = temp_dir / f"audio_{i}.wav"
            silent.export(audio_path, format="wav")
            audio_segments.append({
                'audio_path': str(audio_path),
                'image_path': images[0] if images else None,  # Use first image
                'text': segment['content']
            })
    
    print(f"Created {len(audio_segments)} audio segments")
    
    # Create a simple video with the images
    if images:
        video_path = Path("output/test_simple_video.mp4")
        video_path.parent.mkdir(parents=True, exist_ok=True)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(str(video_path), fourcc, 1, (width, height))  # 1 FPS for test
        
        # Add each image for a few frames to simulate slideshow
        for img_path in images:
            img = cv2.imread(img_path)
            img = cv2.resize(img, (width, height))
            # Show each image for 30 frames (3 seconds at 10 FPS in final version)
            for _ in range(10):  # 10 frames at 1 FPS for test
                video_writer.write(img)
        
        video_writer.release()
        print(f"Created test video: {video_path}")
    
    print("Test completed successfully!")
    print("Note: This was a functionality test without actual API calls")
    print("The real video_synthesizer.py requires a valid API key to generate images")


if __name__ == "__main__":
    simple_test()