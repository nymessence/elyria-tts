#!/usr/bin/env python3
"""
Intelligent Infobox and Image Generator for Elyria-TTS
Uses glm-4.6v-flash vision model to generate images with smart prompts
Handles 429 rate limit errors gracefully
"""

import argparse
import json
import os
import re
import time
import requests
from pathlib import Path
from typing import List, Tuple


def generate_smart_prompt(sentence: str, context: str = "") -> str:
    """
    Generate intelligent image prompts based on text content
    """
    sentence_lower = sentence.lower()
    
    # Analyze the sentence to generate an appropriate image prompt
    if any(word in sentence_lower for word in ["happy", "cheerful", "joy", "celebrate", "delighted"]):
        return "A bright, cheerful scene with vibrant colors representing happiness, joyful expressions, and positive emotions"
    elif any(word in sentence_lower for word in ["sad", "melancholy", "depressed", "gloomy", "heartbroken"]):
        return "A muted, melancholic scene with soft lighting representing sadness, thoughtful expressions, and gentle emotions"
    elif any(word in sentence_lower for word in ["exciting", "energetic", "excited", "thrilling", "dynamic"]):
        return "An energetic, dynamic scene with vivid colors representing excitement, motion, and high energy"
    elif any(word in sentence_lower for word in ["tired", "sleepy", "exhausted", "rest", "relax"]):
        return "A cozy, sleepy scene with warm lighting representing rest, relaxation, and peaceful emotions"
    elif any(word in sentence_lower for word in ["surprise", "amazed", "wow", "astonished", "shocked"]):
        return "A scene showing surprise or amazement with dramatic lighting and expressive elements"
    elif any(word in sentence_lower for word in ["love", "affection", "romance", "caring", "affectionate"]):
        return "A warm, loving scene with soft lighting and affectionate elements"
    elif any(word in sentence_lower for word in ["anger", "mad", "furious", "rage", "irate"]):
        return "A scene representing strong emotions with bold colors and intense expressions"
    elif any(word in sentence_lower for word in ["nature", "forest", "mountains", "lake", "river", "garden", "park"]):
        return "Beautiful nature scene with forests, mountains, lakes, and natural elements"
    elif any(word in sentence_lower for word in ["city", "urban", "building", "street", "metropolis", "skyscraper"]):
        return "Modern cityscape with buildings, urban environment, and metropolitan elements"
    elif any(word in sentence_lower for word in ["technology", "computer", "digital", "robot", "ai", "future"]):
        return "Futuristic technology scene with computers, digital interfaces, and high-tech elements"
    elif any(word in sentence_lower for word in ["food", "meal", "restaurant", "cooking", "delicious"]):
        return "Delicious food scene with appetizing presentation and warm lighting"
    elif any(word in sentence_lower for word in ["music", "concert", "song", "instrument", "singing"]):
        return "Musical scene with instruments, concert atmosphere, and rhythmic elements"
    elif any(word in sentence_lower for word in ["sports", "game", "exercise", "competition", "athletic"]):
        return "Sports scene with athletic activity, competition, and dynamic movement"
    else:
        # General prompt based on context
        return f"Scene representing: {sentence}. Context: {context}. Highly detailed, realistic, vibrant colors, professional photography"


def add_infoboxes(input_file: Path, output_file: Path) -> List[str]:
    """
    Add infoboxes to a script file intelligently
    Returns list of generated prompts
    """
    print(f"Analyzing script file: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output_lines = []
    prompts = []
    prev_line_has_image = False
    
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        
        # Skip empty lines and existing IMG tags
        if not stripped_line or '[IMG:' in stripped_line:
            output_lines.append(line)
            if '[IMG:' in stripped_line:
                prev_line_has_image = True
            continue
        
        # If line contains text (sentence), consider adding an image
        if re.search(r'[.!?]', stripped_line) and len(stripped_line) > 10:
            # Don't add images too frequently
            if not prev_line_has_image and i > 0:
                # Generate a smart prompt based on the current sentence
                context = "" if i == 0 else lines[i-1].strip()
                prompt = generate_smart_prompt(stripped_line, context)
                prompts.append(prompt)
                
                # Add an infobox before this line
                output_lines.append(f"[IMG: {prompt}]\n")
                print(f"Added image prompt: {prompt[:50]}...")
            
            prev_line_has_image = False
        
        output_lines.append(line)
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"Infoboxes added to: {output_file}")
    return prompts


def generate_images(prompts: List[str], api_endpoint: str, api_key: str, max_retries: int = 3) -> List[str]:
    """
    Generate images using glm-4.6v-flash API
    """
    print(f"Generating images for {len(prompts)} prompts...")
    image_urls = []
    
    for i, prompt in enumerate(prompts):
        print(f"Generating image {i+1}/{len(prompts)}: {prompt[:50]}...")
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "model": "glm-4.6v-flash",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "response_format": "url"
        }
        
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = requests.post(f"{api_endpoint}/images/generations", 
                                       headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data and len(data['data']) > 0:
                        image_url = data['data'][0].get('url', '')
                        if image_url:
                            image_urls.append(image_url)
                            print(f"✓ Image generated successfully")
                            break
                    else:
                        print(f"✗ No image data returned in response")
                        break
                elif response.status_code == 429:
                    print(f"⚠️  Rate limit (429) error, waiting before retry...")
                    # Exponential backoff
                    time.sleep(2 ** retry_count * 10)  # Wait 10, 20, 40 seconds
                    retry_count += 1
                else:
                    print(f"✗ Error {response.status_code} generating image: {response.text}")
                    break
            except requests.exceptions.Timeout:
                print(f"⚠️  Request timed out, retrying...")
                retry_count += 1
                time.sleep(10)
            except requests.exceptions.RequestException as e:
                print(f"✗ Request error: {e}")
                break
        
        if retry_count >= max_retries:
            print(f"✗ Failed to generate image after {max_retries} retries")
            image_urls.append(None)  # Placeholder for failed generation
    
    return image_urls


def main():
    parser = argparse.ArgumentParser(description="Intelligent Infobox and Image Generator for Elyria-TTS")
    parser.add_argument("--script", required=True, help="Input script file path")
    parser.add_argument("--api-endpoint", help="API endpoint for image generation")
    parser.add_argument("--api-key", help="API key for image generation service")
    parser.add_argument("--output", help="Output script file path")
    
    args = parser.parse_args()
    
    input_script = Path(args.script)
    if not input_script.exists():
        raise FileNotFoundError(f"Input script not found: {args.script}")
    
    output_script = Path(args.output) if args.output else input_script.with_name(
        input_script.stem + "_with_infoboxes.txt"
    )
    
    print("Starting Intelligent Infobox and Image Generator...")
    print("This script will intelligently add infoboxes and generate images using glm-4.6v-flash vision model")
    
    # Add infoboxes to the script
    prompts = add_infoboxes(input_script, output_script)
    
    # If API endpoint and key are provided, generate images
    if args.api_endpoint and args.api_key:
        print("API credentials detected, proceeding with image generation...")
        image_urls = generate_images(prompts, args.api_endpoint, args.api_key)
        
        # Create a report of generated images
        report_path = output_script.with_name(output_script.stem + "_image_report.txt")
        with open(report_path, 'w') as f:
            f.write("Generated Images Report\n")
            f.write("=======================\n\n")
            for i, (prompt, url) in enumerate(zip(prompts, image_urls)):
                f.write(f"Image {i+1}:\n")
                f.write(f"  Prompt: {prompt}\n")
                f.write(f"  URL: {url if url else 'FAILED'}\n\n")
        
        print(f"Image generation report saved to: {report_path}")
    else:
        print("No API credentials provided, skipping image generation (dry run mode)")
        print("429 errors would normally occur during image generation if API key was provided")
        print(f"Generated {len(prompts)} image prompts for potential generation")
    
    print("Intelligent Infobox and Image Generation complete!")
    print(f"Output saved to: {output_script}")


if __name__ == "__main__":
    main()