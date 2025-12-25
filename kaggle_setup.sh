#!/bin/bash
# Kaggle Setup Script (HARD-LOCKED)
# Python 3.12 + uv only, no pip leakage, CPU-safe PyTorch

set -euo pipefail

PYTHON_VERSION="3.12"
ACCELERATOR_TYPE="${1:-cpu}"
ROOT="/tmp/elyria-tts"

echo "=== Nya Elyria Voice Synthesizer (locked uv / py${PYTHON_VERSION}) ==="
echo "Accelerator: ${ACCELERATOR_TYPE}"

# ----------------------------
# Clean preinstalled packages that might conflict
# ----------------------------
echo "Removing conflicting preinstalled packages..."
pip uninstall -y torch torchaudio torchvision tensorflow keras 2>/dev/null || true
pip uninstall -y chatterbox chatterbox-tts 2>/dev/null || true

# ----------------------------
# System Python 3.12
# ----------------------------
apt update
apt install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-venv

python${PYTHON_VERSION} --version

# Install pip for Python 3.12
python${PYTHON_VERSION} -m ensurepip --upgrade

# ----------------------------
# Install uv bound to Python 3.12
# ----------------------------
python${PYTHON_VERSION} -m pip install --upgrade pip
python${PYTHON_VERSION} -m pip install --upgrade uv

uv --version
uv python install ${PYTHON_VERSION}
uv python pin ${PYTHON_VERSION}

# ----------------------------
# Clone repo
# ----------------------------
if [ ! -d "${ROOT}" ]; then
  git clone https://github.com/nymessence/elyria-tts.git "${ROOT}"
fi

cd "${ROOT}"

git submodule init
git submodule update --recursive

# ----------------------------
# uv hard lock config
# ----------------------------
cat > .uv.toml <<EOF
[python]
requires = "==${PYTHON_VERSION}.*"
EOF

# ----------------------------
# Create venv (FORCED 3.12)
# ----------------------------
rm -rf .venv
uv venv --python ${PYTHON_VERSION} .venv
source .venv/bin/activate

python --version

# ----------------------------
# Base deps (NUMPY CAPPED)
# ----------------------------
pip install \
  "numpy>=1.26,<2.5" \
  packaging typing-extensions

# ----------------------------
# PyTorch (CPU default, Kaggle-safe)
# ----------------------------
if python -c "import torch; print(torch.__version__)" 2>/dev/null; then
  echo "Torch already present in venv"
else
  case "${ACCELERATOR_TYPE}" in
    cpu)
      pip install torch torchaudio
      ;;
    cuda|gpu)
      # Kaggle CUDA stacks are fragile; use only if you know the image
      pip install \
        torch torchaudio \
        --index-url https://download.pytorch.org/whl/cu118
      ;;
    tpu)
      pip install torch torchaudio
      ;;
    *)
      pip install torch torchaudio
      ;;
  esac
fi

# ----------------------------
# Verify torch binding (use direct python call, not heredoc)
# ----------------------------
echo ""
echo "=== Verifying PyTorch Installation ==="
${ROOT}/.venv/bin/python -c "import sys, torch; print('Python:', sys.version); print('Executable:', sys.executable); print('Torch:', torch.__version__); print('Torch path:', torch.__file__)"
echo ""

# ----------------------------
# Chatterbox (source install, no deps)
# ----------------------------
if [ ! -d "${ROOT}/chatterbox" ]; then
  git clone https://github.com/resemble-ai/chatterbox.git "${ROOT}/chatterbox"
fi

cd chatterbox
pip install -e . --no-build-isolation --no-deps
cd "${ROOT}"

# ----------------------------
# App deps
# ----------------------------
pip install \
  opencv-python pillow pydub requests

# ----------------------------
# Kaggle working files
# ----------------------------
mkdir -p kaggle/working
cp -f voice_synthesizer.py kaggle/working/ 2>/dev/null || echo "Note: voice_synthesizer.py not found"
cp -f video_synthesizer.py kaggle/working/ 2>/dev/null || echo "Note: video_synthesizer.py not found"
cp -f example_script*.txt kaggle/working/ 2>/dev/null || echo "Note: example scripts not found"
cp -f video_script.txt kaggle/working/ 2>/dev/null || true
cp -f test_video_script.txt kaggle/working/ 2>/dev/null || true

# ----------------------------
# Convenience runners
# ----------------------------
cat > kaggle/working/run_voice_synthesis.sh <<'EOF'
#!/bin/bash
cd /tmp/elyria-tts
source .venv/bin/activate
python voice_synthesizer.py \
  --voice voices/nya_elyria.wav \
  --script example_script.txt \
  --output kaggle/working/output.wav
EOF
chmod +x kaggle/working/run_voice_synthesis.sh

cat > kaggle/working/run_video_synthesis.sh <<'EOF'
#!/bin/bash
cd /tmp/elyria-tts
source .venv/bin/activate
python video_synthesizer.py \
  --api-endpoint "https://api.z.ai/api/paas/v4" \
  --api-key "$Z_AI_API_KEY" \
  --model "glm-4.6v-flash" \
  --voice voices/nya_elyria.wav \
  --script video_script.txt \
  --output kaggle/working/video.mp4
EOF
chmod +x kaggle/working/run_video_synthesis.sh

echo ""
echo "=== SETUP COMPLETE ==="
echo "Python: $(python --version)"
echo "PyTorch: $(python -c 'import torch; print(torch.__version__)')"
echo ""
echo "IMPORTANT: Virtual environment activation is required for all operations:"
echo "  source /tmp/elyria-tts/.venv/bin/activate"
echo ""
echo "Run voice synthesis:"
echo "  source /tmp/elyria-tts/.venv/bin/activate && bash kaggle/working/run_voice_synthesis.sh"
echo ""
echo "Run video synthesis:"
echo "  source /tmp/elyria-tts/.venv/bin/activate && bash kaggle/working/run_video_synthesis.sh"
