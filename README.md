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
├── voices/
│   └── nya_elyria.wav
├── output/
│   └── example.wav
├── README.md
├── .gitignore
```

## Usage

Run the voice synthesizer using the following command:

```bash
uv run voice_synthesizer.py \
  --voice voices/nya_elyria.wav \
  --script example_script.txt \
  --output output/example.wav
```

## CPU Performance Notes

This implementation is designed for CPU execution and will run slowly, especially on resource-constrained devices like Raspberry Pi. Keep input scripts short for reasonable processing times.

Conservative defaults are used for CPU inference:
- cfg_weight: 0.5
- exaggeration: 0.5

These values can be adjusted later for more expressive speech or GPU runs.

## Future Work

Long-form narration and GPU acceleration will be implemented later on Kaggle.