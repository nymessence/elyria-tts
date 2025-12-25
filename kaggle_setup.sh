#!/bin/bash

# Kaggle Setup Script for Nya Elyria Voice Synthesizer
# This script is designed to be copy/pasted and run from inside Kaggle
# It clones the repository to /tmp but sets up for use in kaggle/working

set -e  # Exit on any error

# Default to CPU for Kaggle
ACCELERATOR_TYPE=${1:-cpu}
echo "Setting up Nya Elyria Voice Synthesizer in Kaggle environment with $ACCELERATOR_TYPE support..."

# Clone the main repository to /tmp to avoid committing to Kaggle dataset
if [ ! -d "/tmp/elyria-tts" ]; then
    echo "Cloning main repository to /tmp..."
    git clone https://github.com/nymessence/elyria-tts.git /tmp/elyria-tts
fi

# Change to the cloned repository in /tmp
cd /tmp/elyria-tts

# Initialize and update submodules (if any)
echo "Initializing submodules..."
git submodule init
git submodule update --recursive

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    pip install uv
fi

# Create Python 3.11 virtual environment in /tmp
echo "Creating Python 3.11 virtual environment in /tmp..."
uv venv --python 3.11 /tmp/elyria-tts/.venv

# Activate virtual environment
source /tmp/elyria-tts/.venv/bin/activate

# Install Chatterbox-TTS from source
if [ ! -d "/tmp/elyria-tts/chatterbox" ]; then
    echo "Cloning Chatterbox-TTS to /tmp..."
    git clone https://github.com/resemble-ai/chatterbox.git /tmp/elyria-tts/chatterbox
fi

echo "Installing Chatterbox-TTS from source with compatibility fixes..."
cd /tmp/elyria-tts/chatterbox

# Install with specific numpy version to avoid build issues
pip install numpy>=1.26.0 --force-reinstall --no-cache-dir

# Install core dependencies first based on accelerator type
case $ACCELERATOR_TYPE in
    "cpu")
        echo "Installing CPU version of PyTorch..."
        pip install torch==2.8.0+cpu torchaudio==2.8.0+cpu --index-url https://download.pytorch.org/whl/cpu --force-reinstall --no-cache-dir
        ;;
    "cuda"|"gpu")
        echo "Installing CUDA version of PyTorch..."
        pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118 --force-reinstall --no-cache-dir
        ;;
    "tpu")
        echo "Installing TPU version of PyTorch..."
        pip install torch==2.8.0+cpu torchaudio==2.8.0+cpu --index-url https://download.pytorch.org/whl/cpu --force-reinstall --no-cache-dir  # TPU support via XLA
        ;;
    *)
        echo "Unknown accelerator type: $ACCELERATOR_TYPE. Defaulting to CPU."
        pip install torch==2.8.0+cpu torchaudio==2.8.0+cpu --index-url https://download.pytorch.org/whl/cpu --force-reinstall --no-cache-dir
        ;;
esac

# Verify torch installation
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"

# Install chatterbox without its dependencies to avoid conflicts
pip install -e . --no-build-isolation --no-deps
cd /tmp/elyria-tts

# Install additional dependencies for video synthesizer
echo "Installing video synthesis dependencies..."
uv pip install opencv-python pillow pydub numpy requests

# Copy necessary files to kaggle/working for user access
echo "Setting up kaggle/working directory..."
mkdir -p kaggle/working
cp -f voice_synthesizer.py kaggle/working/
cp -f video_synthesizer.py kaggle/working/
cp -f example_script.txt kaggle/working/
cp -f example_script_paralinguistic.txt kaggle/working/
cp -f example_script_emotional.txt kaggle/working/
cp -f video_script.txt kaggle/working/
cp -f test_video_script.txt kaggle/working/

# Create a convenience script in kaggle/working
cat > kaggle/working/run_voice_synthesis.sh << 'EOF'
#!/bin/bash
# Convenience script to run voice synthesis in Kaggle

cd /tmp/elyria-tts
source .venv/bin/activate

# Example usage:
# python voice_synthesizer.py --voice voices/nya_elyria.wav --script example_script.txt --output kaggle/working/output.wav

echo "Voice synthesizer ready!"
echo "Usage: python voice_synthesizer.py --voice voices/nya_elyria.wav --script example_script.txt --output kaggle/working/output.wav"
EOF

chmod +x kaggle/working/run_voice_synthesis.sh

cat > kaggle/working/run_video_synthesis.sh << 'EOF'
#!/bin/bash
# Convenience script to run video synthesis in Kaggle

cd /tmp/elyria-tts
source .venv/bin/activate

# Example usage:
# python video_synthesizer.py --api-endpoint "https://api.z.ai/api/paas/v4" --api-key $Z_AI_API_KEY --model "glm-4.6v-flash" --voice voices/nya_elyria.wav --script video_script.txt --output kaggle/working/video.mp4

echo "Video synthesizer ready!"
echo "Usage: python video_synthesizer.py --api-endpoint 'https://api.z.ai/api/paas/v4' --api-key \$Z_AI_API_KEY --model 'glm-4.6v-flash' --voice voices/nya_elyria.wav --script video_script.txt --output kaggle/working/video.mp4"
EOF

chmod +x kaggle/working/run_video_synthesis.sh

echo "Setup complete!"
echo ""
echo "To run voice synthesis:"
echo "  cd /tmp/elyria-tts"
echo "  source .venv/bin/activate"
echo "  python voice_synthesizer.py --voice voices/nya_elyria.wav --script example_script.txt --output kaggle/working/output.wav"
echo ""
echo "To run video synthesis:"
echo "  cd /tmp/elyria-tts"
echo "  source .venv/bin/activate"
echo "  python video_synthesizer.py --api-endpoint 'https://api.z.ai/api/paas/v4' --api-key \$Z_AI_API_KEY --model 'glm-4.6v-flash' --voice voices/nya_elyria.wav --script video_script.txt --output kaggle/working/video.mp4"
echo ""
echo "Convenience scripts are available in kaggle/working/:"
echo "  - run_voice_synthesis.sh"
echo "  - run_video_synthesis.sh"
echo ""
echo "Example scripts and voice files are available in kaggle/working/ for reference."