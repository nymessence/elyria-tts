#!/bin/bash

# Setup script for Nya Elyria Voice Synthesizer
# Repository: https://github.com/nymessence/elyria-tts.git

set -e  # Exit on any error

# Default to CPU
ACCELERATOR_TYPE=${1:-cpu}
echo "Setting up Nya Elyria Voice Synthesizer with $ACCELERATOR_TYPE support..."

# Clone the main repository
if [ ! -d "elyria-tts" ]; then
    echo "Cloning main repository..."
    git clone https://github.com/nymessence/elyria-tts.git
fi

cd elyria-tts

# Initialize and update submodules (if any)
echo "Initializing submodules..."
git submodule init
git submodule update --recursive

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    pip install uv
fi

# Create Python 3.11 virtual environment
echo "Creating Python 3.11 virtual environment..."
uv venv --python 3.11

# Activate virtual environment
source .venv/bin/activate

# Install Chatterbox-TTS from source
if [ ! -d "chatterbox" ]; then
    echo "Cloning Chatterbox-TTS..."
    git clone https://github.com/resemble-ai/chatterbox.git
fi

echo "Installing Chatterbox-TTS from source with compatibility fixes..."
cd chatterbox
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
cd ..

# Install any additional dependencies from pyproject.toml
if [ -f "pyproject.toml" ]; then
    echo "Installing project dependencies..."
    uv pip install -e .
fi

echo "Setup complete!"
echo ""
echo "To run the voice synthesizer:"
echo "  cd elyria-tts"
echo "  source .venv/bin/activate"
echo "  python voice_synthesizer.py --voice voices/nya_elyria.wav --script example_script.txt --output output/example.wav"
echo ""
echo "For paralinguistic tags support:"
echo "  python voice_synthesizer.py --voice voices/nya_elyria.wav --script example_script_paralinguistic.txt --output output/example_turbo.wav --turbo"