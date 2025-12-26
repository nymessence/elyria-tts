#!/bin/bash
# NoHUP runner for the intelligent image generator
# This script will run in the background after the current process

# Wait for a moment to ensure current process completes
sleep 5

# Run the intelligent image generator with nohup to continue execution
nohup python3 /home/erick/elyria-tts/intelligent_image_generator.py \
  --script /home/erick/elyria-tts/example_script_emotional.txt \
  --api-endpoint "https://api.z.ai/api/paas/v4" \
  --api-key "$Z_AI_API_KEY" \
  --output /home/erick/elyria-tts/example_script_emotional_with_images.txt \
  > /home/erick/elyria-tts/image_generation.log 2>&1 &

echo "Intelligent image generator started with PID $!"
echo "Log file: /home/erick/elyria-tts/image_generation.log"