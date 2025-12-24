#!/usr/bin/env python3
"""
Video Synthesizer - Creates slideshow videos with AI-generated images and voice narration
"""

import argparse
import asyncio
import json
import os
import re
import tempfile
import time
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
from pydub import AudioSegment
import torchaudio


def generate_image_with_api(prompt, api_endpoint, model, api_key, resolution):
    """
    Generate an image using the Z.AI API with glm-4.6v-flash model
    """
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        width, height = resolution.split('x')
        width, height = int(width), int(height)

        # The glm-4.6v-flash model may support image generation through
        # a vision/image generation endpoint. Try the standard image generation API first.
        payload = {
            "model": model,  # glm-4.6v-flash
            "prompt": prompt,
            "n": 1,
            "size": f"{width}x{height}",
            "response_format": "url"
        }

        response = requests.post(f"{api_endpoint}/images/generations",
                               headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            # Extract image URL from response (structure may vary by API)
            if 'data' in data and len(data['data']) > 0:
                if 'url' in data['data'][0]:
                    image_url = data['data'][0]['url']
                    # Download the image
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        # Save to temporary file
                        temp_img = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                        temp_img.write(img_response.content)
                        temp_img.close()
                        return temp_img.name
                elif 'b64_json' in data['data'][0]:
                    import base64
                    img_data = base64.b64decode(data['data'][0]['b64_json'])
                    temp_img = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                    temp_img.write(img_data)
                    temp_img.close()
                    return temp_img.name
        else:
            print(f"Primary API call failed: {response.status_code} - {response.text}")

        # If the standard images/generations endpoint doesn't work with glm-4.6v-flash,
        # we could potentially use the chat endpoint for a vision model that generates image descriptions
        # but for now we'll just return None to trigger the fallback

    except requests.exceptions.RequestException as e:
        print(f"Network error during image generation: {e}")
    except Exception as e:
        print(f"Error during image generation: {e}")

    return None


def create_blank_image(width, height, text="Image Generation Failed"):
    """
    Create a blank image with text as fallback
    """
    img = Image.new('RGB', (width, height), color=(73, 109, 137))
    d = ImageDraw.Draw(img)

    # Try to use a default font
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 36)
    except:
        font = ImageFont.load_default()

    # Calculate text position (center)
    # Use textbbox instead of textsize (which is deprecated)
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    d.text((x, y), text, fill=(255, 255, 255), font=font)
    return img


def parse_script(script_path):
    """
    Parse the script file to extract images and text segments
    """
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by image tags
    segments = re.split(r'\[IMG:\s*(.*?)\]', content)
    
    # First element is text before first image (if any)
    parsed_segments = []
    
    for i, segment in enumerate(segments):
        segment = segment.strip()
        if i == 0:
            # First segment is text before any image
            if segment:
                parsed_segments.append({
                    'type': 'text',
                    'content': segment
                })
        else:
            # Alternating: image prompt, then text
            if i % 2 == 1:  # This is an image prompt
                if segment:  # Make sure it's not empty
                    parsed_segments.append({
                        'type': 'image',
                        'prompt': segment
                    })
            else:  # This is text after an image
                if segment:
                    parsed_segments.append({
                        'type': 'text',
                        'content': segment
                    })
    
    return parsed_segments


def synthesize_voice(text, voice_path, output_path, device="cpu"):
    """
    Use the existing voice synthesizer functionality to generate audio
    """
    try:
        from chatterbox import ChatterboxTTS
        import perth
        
        # Initialize model
        tts = ChatterboxTTS.from_pretrained(device=device)
        
        # Handle watermarker
        if perth.PerthImplicitWatermarker is None:
            tts.watermarker = perth.DummyWatermarker()
        
        # Prepare conditionals
        tts.prepare_conditionals(str(voice_path), exaggeration=0.5)
        
        # Generate audio
        audio = tts.generate(
            text=text,
            cfg_weight=0.5,
            exaggeration=0.5
        )
        
        # Save using torchaudio
        torchaudio.save(str(output_path), audio, tts.sr)
        
    except Exception as e:
        print(f"Error synthesizing voice: {e}")
        # Create a silent audio file as fallback
        silence = AudioSegment.silent(duration=1000)  # 1 second of silence
        silence.export(output_path, format="wav")


def create_video(segments, voice_path, output_path, api_endpoint, model, api_key, resolution, delay, similarity):
    """
    Create the final video from segments
    """
    width, height = map(int, resolution.split('x'))

    # Create temporary directory for assets
    temp_dir = Path(tempfile.mkdtemp())

    # Process each segment
    images = []
    audio_segments = []
    sentence_idx = 0  # Track sentence index globally

    for i, segment in enumerate(segments):
        if segment['type'] == 'image':
            print(f"Generating image {i+1}: {segment['prompt'][:50]}...")

            # Generate image
            img_path = generate_image_with_api(
                segment['prompt'],
                api_endpoint,
                model,
                api_key,
                resolution
            )

            if img_path:
                img = Image.open(img_path)
                img = img.resize((width, height), Image.LANCZOS)
                img_path = temp_dir / f"img_{i}.jpg"
                img.save(img_path)
                images.append(str(img_path))
            else:
                # Create fallback image
                img = create_blank_image(width, height, f"Failed to generate: {segment['prompt'][:30]}...")
                img_path = temp_dir / f"img_{i}.jpg"
                img.save(img_path)
                images.append(str(img_path))

        elif segment['type'] == 'text':
            # Find all sentences in the text
            sentences = [s.strip() for s in segment['content'].split('.') if s.strip()]
            sentences = [s + '.' if s and not s.endswith('.') else s for s in sentences if s]

            # Use the most recent image for these sentences
            current_image = images[-1] if images else None
            if not current_image:
                # Create a default image if no images were generated yet
                img = create_blank_image(width, height, "Default Slide")
                img_path = temp_dir / f"default_img_{i}.jpg"
                img.save(img_path)
                images.append(str(img_path))
                current_image = str(img_path)

            for j, sentence in enumerate(sentences):
                sentence = sentence.strip()
                if not sentence:
                    continue

                print(f"Synthesizing audio for sentence {sentence_idx + 1}: {sentence[:50]}...")

                # Create audio for this sentence
                audio_path = temp_dir / f"audio_{sentence_idx}.wav"
                synthesize_voice(sentence, voice_path, audio_path)

                # Add this sentence audio with its corresponding image
                audio_segments.append({
                    'audio_path': str(audio_path),
                    'image_path': current_image,
                    'sentence': sentence
                })

                sentence_idx += 1

                # Add 500ms gap between sentences
                audio_segments.append({
                    'audio_path': None,  # Silent gap
                    'image_path': current_image,
                    'sentence': '[SILENCE_GAP]'
                })

    # Now create the video
    if not audio_segments:
        print("No audio segments to process")
        return

    # Combine all audio segments with gaps
    final_audio = AudioSegment.empty()

    for seg in audio_segments:
        if seg['audio_path'] and seg['sentence'] != '[SILENCE_GAP]':
            # Add the sentence audio
            sentence_audio = AudioSegment.from_wav(seg['audio_path'])
            final_audio += sentence_audio
        elif seg['sentence'] == '[SILENCE_GAP]':
            # Add 500ms gap between sentences
            final_audio += AudioSegment.silent(duration=500)

    # Create video frames based on timing
    fps = 30
    frame_duration_ms = 1000 / fps  # Duration of each frame in milliseconds

    # Calculate when each image should be shown based on audio timing
    video_frames = []
    current_time_ms = 0

    for seg in audio_segments:
        if seg['sentence'] == '[SILENCE_GAP]':
            # Add frames for 500ms gap
            gap_frames = int(500 / frame_duration_ms)
            image = cv2.imread(seg['image_path'])
            image = cv2.resize(image, (width, height))

            for _ in range(gap_frames):
                video_frames.append(image.copy())

            current_time_ms += 500
        else:
            # Get duration of this audio segment
            sentence_audio = AudioSegment.from_wav(seg['audio_path'])
            audio_duration_ms = len(sentence_audio)

            # Calculate number of frames for this audio
            num_frames = int(audio_duration_ms / frame_duration_ms)

            # Load and resize the image
            image = cv2.imread(seg['image_path'])
            image = cv2.resize(image, (width, height))

            # Add frames for this image
            for _ in range(num_frames):
                video_frames.append(image.copy())

            current_time_ms += audio_duration_ms

    if not video_frames:
        print("No video frames to process")
        return

    # Write the video file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

    for frame in video_frames:
        video_writer.write(frame)

    video_writer.release()

    # Export final audio
    audio_output_path = output_path.with_name(output_path.stem + "_audio.wav")
    final_audio.export(audio_output_path, format="wav")

    # Combine video and audio using ffmpeg (if available)
    try:
        import subprocess
        final_output_path = output_path.with_name(output_path.stem + "_final.mp4")

        # Use ffmpeg to combine video and audio
        cmd = [
            'ffmpeg', '-y',  # -y to overwrite output file
            '-i', str(output_path),  # input video
            '-i', str(audio_output_path),  # input audio
            '-c:v', 'copy',  # copy video stream
            '-c:a', 'aac',  # encode audio as AAC
            '-strict', 'experimental',
            str(final_output_path)
        ]

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"Final video with audio created: {final_output_path}")
        # Remove intermediate files
        os.remove(output_path)
        os.remove(audio_output_path)

    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Video created: {output_path}")
        print(f"Audio created: {audio_output_path}")
        print("Note: To combine video and audio, install ffmpeg and run:")
        print(f"ffmpeg -i {output_path} -i {audio_output_path} -c:v copy -c:a aac output/final_video.mp4")

    # Cleanup temp files
    import shutil
    shutil.rmtree(temp_dir)


def main():
    parser = argparse.ArgumentParser(description="Video Synthesizer - Creates slideshow videos with AI-generated images and voice narration")
    parser.add_argument("--delay", type=float, default=5.0, help="Delay between slides in seconds")
    parser.add_argument("--similarity", type=float, default=0.65, help="Similarity threshold for image generation")
    parser.add_argument("--api-endpoint", required=True, help="API endpoint for image generation")
    parser.add_argument("--model", default="glm-4.6v-flash", help="Model to use for image generation")
    parser.add_argument("--api-key", required=True, help="API key for image generation service")
    parser.add_argument("--resolution", default="1920x1080", help="Video resolution (default: 1920x1080)")
    parser.add_argument("--voice", required=True, help="Path to the voice reference WAV file")
    parser.add_argument("--script", required=True, help="Path to the script file")
    parser.add_argument("--output", default="output/video.mp4", help="Output video path")
    
    args = parser.parse_args()
    
    # Validate inputs
    voice_path = Path(args.voice)
    script_path = Path(args.script)
    
    if not voice_path.exists():
        raise FileNotFoundError(f"Voice file not found: {args.voice}")
    
    if not script_path.exists():
        raise FileNotFoundError(f"Script file not found: {args.script}")
    
    # Parse the script
    print("Parsing script...")
    segments = parse_script(script_path)
    
    # Create output directory if it doesn't exist
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create the video
    print("Creating video...")
    create_video(
        segments=segments,
        voice_path=voice_path,
        output_path=output_path,
        api_endpoint=args.api_endpoint,
        model=args.model,
        api_key=args.api_key,
        resolution=args.resolution,
        delay=args.delay,
        similarity=args.similarity
    )
    
    print(f"Video creation complete: {output_path}")


if __name__ == "__main__":
    main()