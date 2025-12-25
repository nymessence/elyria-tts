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

### Accelerator Support

The setup scripts support different hardware accelerators:

#### CPU Setup (default)
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/setup.sh)" cpu
```

#### GPU (CUDA) Setup
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/setup.sh)" gpu
# or
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/setup.sh)" cuda
```

#### TPU Setup
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/setup.sh)" tpu
```

The same options work for the Kaggle setup script:
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/kaggle_setup.sh)" cpu
```

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

### Device Selection

You can specify the device to run inference on using the `--device` parameter:

```bash
# CPU (default)
python voice_synthesizer.py --device cpu [other args...]

# GPU (CUDA)
python voice_synthesizer.py --device cuda [other args...]
python voice_synthesizer.py --device gpu [other args...]  # gpu is an alias for cuda

# TPU (if available)
python voice_synthesizer.py --device tpu [other args...]
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

**Note**: The turbo model requires downloading additional models from Hugging Face. If you encounter token requirements, you can download the models locally first:

```bash
# Download the turbo model manually
huggingface-cli download ResembleAI/chatterbox-turbo --local-dir ./chatterbox-turbo-model
```

Then modify the code to load from the local directory, or set the HF_TOKEN environment variable.

## Video Synthesizer

Create slideshow videos with AI-generated images and voice narration using `video_synthesizer.py`:

```bash
uv run --active video_synthesizer.py \
  --delay 5 \
  --similarity 0.65 \
  --api-endpoint "https://api.z.ai/api/paas/v4" \
  --model "glm-4.6v-flash" \
  --api-key $Z_AI_API_KEY \
  --resolution 1920x1080 \
  --voice voices/nya_elyria.wav \
  --script video_script.txt \
  --output output/video.mp4
```

### Video Script Format

The video script includes special `[IMG: prompt]` tags to generate images:

```
[IMG: Prompt for first image here]

Sentence 1 here.
Sentence 2 here.

[IMG: Prompt for second image here]

Sentence 3 here.
Sentence 4 here.
```

- Images are generated based on the prompts in `[IMG: ...]` tags
- Sentences between image tags are narrated using the voice clone
- 500ms gap between sentences
- 1000ms gap between slides (image + text block)

### Dependencies

The video synthesizer requires additional dependencies:

```bash
pip install opencv-python pillow pydub numpy requests
```

## CPU Performance Notes

This implementation is designed for CPU execution and will run slowly, especially on resource-constrained devices like Raspberry Pi. Keep input scripts short for reasonable processing times.

Conservative defaults are used for CPU inference:
- cfg_weight: 0.5
- exaggeration: 0.5

These values can be adjusted later for more expressive speech or GPU runs.

## Kaggle Setup

For Kaggle environments, we provide a specialized setup script that operates from `kaggle/working` and clones the repository into `/tmp`:

```bash
# Copy and paste this script into a Kaggle notebook cell to set up the environment
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/kaggle_setup.sh)"
```

The `kaggle_setup.sh` script:
- Updates system and installs Python 3.12
- Clones the repository to `/tmp` to avoid committing to Kaggle dataset
- Sets up the Python environment in `/tmp`
- Copies necessary files to `kaggle/working` for user access
- Creates convenience scripts for easy execution
- Installs all required dependencies including video synthesis dependencies

After running the setup script, you can run synthesis commands with outputs saved to `kaggle/working/`.

### Kaggle Usage Methods

#### Method 1: Direct API Access
You can use the voice and video synthesizers directly via the Kaggle API by setting up your notebook with the appropriate accelerator settings:

1. Create a new Kaggle notebook
2. Set accelerator to T4 x2 (for GPU support if needed)
3. Enable internet access in notebook settings
4. Run the setup command in the first cell
5. Use the synthesizers in subsequent cells

#### Method 2: Your Own Notebook
To create your own notebook with the voice synthesizer:

1. Create a new Kaggle notebook
2. In the notebook settings, ensure:
   - Accelerator: T4 x2 (or CPU as needed)
   - Internet: Enabled
   - GPU: Enabled if using GPU mode
3. Add the setup command to a cell:
   ```bash
   !bash -c "$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/kaggle_setup.sh) cpu"
   ```
4. Add your voice synthesis code in subsequent cells:
   ```python
   import sys
   sys.path.append('/tmp/elyria-tts')
   # Now you can use the synthesizer modules
   ```

#### Method 3: Pre-configured Notebook
Use the pre-configured notebook template by forking the repository and adapting it for your specific use case.

## Configuration Options

The setup script supports different accelerator types:

```bash
# CPU only (default, recommended for initial setup)
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/kaggle_setup.sh)" cpu

# GPU (CUDA) for faster inference
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/kaggle_setup.sh)" gpu

# TPU support (if available)
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nymessence/elyria-tts/main/kaggle_setup.sh)" tpu
```

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

For turbo model usage in Kaggle (if token issues occur), you can pre-download the model:

```bash
# Pre-download turbo model in Kaggle
huggingface-cli download ResembleAI/chatterbox-turbo --local-dir ./chatterbox-turbo-model
```

## Future Work

Long-form narration and GPU acceleration will be implemented later on Kaggle.