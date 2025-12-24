# Nya Elyria Voice Synthesizer

A minimal, reliable voice synthesis CLI using **Chatterbox-TTS** to clone the **Nya Elyria** voice.

## Installation

This system is designed to run on Raspberry Pi using CPU only. Python 3.11 is required.

### Option 1: Install from source

```bash
# Install uv if not already installed
pip install uv

# Create a Python 3.11 virtual environment
uv venv --python 3.11

# Activate the virtual environment
source .venv/bin/activate

# Clone and install Chatterbox-TTS
git clone https://github.com/resemble-ai/chatterbox.git
cd chatterbox
pip install -e .
```

Note: Chatterbox was developed and tested on Python 3.11 and Debian 11, and dependencies are pinned in `pyproject.toml`.

## Project Structure

```
.
├── voice_synthesizer.py
├── example_script.txt
├── example_script_paralinguistic.txt
├── voices/
│   └── nya_elyria.wav
├── output/
│   └── example.wav
├── README.md
├── .gitignore
```

## Usage

### Basic Voice Cloning

Run the voice synthesizer using the following command:

```bash
uv run voice_synthesizer.py \
  --voice voices/nya_elyria.wav \
  --script example_script.txt \
  --output output/example.wav
```

### Paralinguistic Tags Support

The Chatterbox-TTS Turbo model supports paralinguistic tags for expressive speech. Use the `--turbo` flag to enable support for tags like `[cough]`, `[laugh]`, `[chuckle]`:

```bash
uv run voice_synthesizer.py \
  --voice voices/nya_elyria.wav \
  --script example_script_paralinguistic.txt \
  --output output/example_turbo.wav \
  --turbo
```

**Note**: The turbo model requires downloading additional models from Hugging Face and may require authentication.

## CPU Performance Notes

This implementation is designed for CPU execution and will run slowly, especially on resource-constrained devices like Raspberry Pi. Keep input scripts short for reasonable processing times.

Conservative defaults are used for CPU inference:
- cfg_weight: 0.5
- exaggeration: 0.5

These values can be adjusted later for more expressive speech or GPU runs.

## Kaggle Usage

For Kaggle deployment, the repository will be cloned into `/tmp` but output should be saved to `kaggle/working`:

```bash
# Clone to /tmp
cd /tmp
git clone https://github.com/nymessence/elyria-tts.git
cd elyria-tts

# Setup (same as above)
uv venv --python 3.11
source .venv/bin/activate
git clone https://github.com/resemble-ai/chatterbox.git
pip install -e chatterbox/

# Run with output to kaggle/working
python voice_synthesizer.py \
  --voice voices/nya_elyria.wav \
  --script example_script.txt \
  --output kaggle/working/output.wav
```

The setup script also works in Kaggle environments:

```bash
# In Kaggle
cd /tmp
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/setup.sh)"
cd elyria-tts
source .venv/bin/activate
python voice_synthesizer.py --voice voices/nya_elyria.wav --script example_script.txt --output kaggle/working/output.wav
```

## Future Work

Long-form narration and GPU acceleration will be implemented later on Kaggle.