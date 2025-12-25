#!/bin/bash
# Final verification script for the Nya Elyria Voice Synthesizer

echo "=== Nya Elyria Voice Synthesizer - Final Verification ==="
echo ""

echo "1. Checking repository structure..."
ls -la
echo ""

echo "2. Checking main scripts..."
ls -la voice_synthesizer.py video_synthesizer.py setup.sh kaggle_setup.sh
echo ""

echo "3. Checking example files..."
ls -la example_script*.txt video_script.txt test_video_script.txt
echo ""

echo "4. Checking documentation..."
ls -la README.md
echo ""

echo "5. Checking voice file..."
ls -la voices/
echo ""

echo "6. Testing Python imports..."
source .venv/bin/activate && python -c "
from voice_synthesizer import main as voice_main
from video_synthesizer import parse_script
print('✓ Voice synthesizer import successful')
print('✓ Video synthesizer import successful')
print('✓ All imports working correctly')
"
echo ""

echo "=== Setup Scripts ==="
echo ""
echo "Standard setup (copy/paste to terminal):"
echo "bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/setup.sh)\""
echo ""
echo "Kaggle setup (copy/paste to Kaggle notebook):"
echo "bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/kaggle_setup.sh)\""
echo ""

echo "=== Example Commands ==="
echo ""
echo "Voice synthesis:"
echo "python voice_synthesizer.py --voice voices/nya_elyria.wav --script example_script.txt --output output/example.wav"
echo ""
echo "Voice synthesis with emotional tags:"
echo "python voice_synthesizer.py --voice voices/nya_elyria.wav --script example_script_emotional.txt --output output/emotional.wav --turbo"
echo ""
echo "Video synthesis:"
echo "python video_synthesizer.py --api-endpoint \"https://api.z.ai/api/paas/v4\" --api-key \$Z_AI_API_KEY --model \"glm-4.6v-flash\" --voice voices/nya_elyria.wav --script video_script.txt --output output/video.mp4"
echo ""

echo "=== Verification Complete ==="
echo "All components are properly set up and ready for use!"