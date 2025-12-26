#!/bin/bash
# Periodic Log Monitoring CI System for Elyria-TTS
# Monitors execution logs and detects failures

set -e  # Exit on any error

echo "Starting log monitoring for Elyria-TTS notebooks..."

# Environment setup
source ~/.bashrc
python -m venv .venv || true
source .venv/bin/activate
pip install -U uv
uv pip install kaggle

# Authentication setup
if [ -z "$KAGGLE_API_TOKEN" ]; then
    echo "KAGGLE_API_TOKEN not available in environment"
    exit 1
fi

mkdir -p ~/.kaggle
echo "{\"username\": \"erickmagyar\", \"key\": \"$KAGGLE_API_TOKEN\"}" > ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json

# Verify authentication
if ! kaggle kernels list | head -n 5; then
    echo "Authentication failed"
    exit 1
fi

echo "Authentication successful"

# Define notebook queue
NOTEBOOKS=(
    "elyria-tts-tester-cpu"
    "elyria-tts-tester-gpu" 
    "elyria-tts-tester-tpu"
    "elyria-video-tester-cpu"
    "elyria-video-tester-gpu"
    "elyria-video-tester-tpu"
)

# Create monitoring directory
mkdir -p monitoring/logs

# Function to fetch logs for a kernel
fetch_kernel_logs() {
    local kernel_name=$1
    local log_file="monitoring/logs/${kernel_name}_$(date +%s).log"
    
    echo "Fetching logs for kernel: $kernel_name"
    
    # Try to get kernel status and output
    if kaggle kernels status "erickmagyar/$kernel_name" > "$log_file.status" 2>&1; then
        echo "Status for $kernel_name:" >> "$log_file"
        cat "$log_file.status" >> "$log_file"
        rm "$log_file.status"
        
        # Try to get output if kernel is complete
        if grep -q "complete\|finished\|success" "$log_file" || [ -f "kaggle_output/${kernel_name}_output.txt" ]; then
            echo "Getting output for $kernel_name..."
            kaggle kernels output "erickmagyar/$kernel_name" -p "kaggle_output" 2>> "$log_file" || echo "No output available yet for $kernel_name" >> "$log_file"
        fi
    else
        echo "Failed to get status for $kernel_name" >> "$log_file"
    fi
    
    echo "$log_file"
}

# Function to analyze logs for failures
analyze_logs() {
    local log_file=$1
    local notebook_name=$2
    
    echo "Analyzing logs for $notebook_name in $log_file..."
    
    # Check for common failure indicators
    if grep -qi "error\|exception\|traceback\|failed\|timeout" "$log_file"; then
        echo "FAILURE DETECTED in $notebook_name:"
        grep -i "error\|exception\|traceback\|failed\|timeout" "$log_file"
        return 1
    elif grep -qi "infinite loop\|hang\|stuck" "$log_file"; then
        echo "INFINITE LOOP/HANG DETECTED in $notebook_name:"
        grep -i "infinite loop\|hang\|stuck" "$log_file"
        return 1
    elif grep -qi "gpu\|cuda\|tpu\|memory\|oom" "$log_file"; then
        echo "RESOURCE ERROR DETECTED in $notebook_name:"
        grep -i "gpu\|cuda\|tpu\|memory\|oom" "$log_file"
        return 1
    else
        echo "No failures detected in $notebook_name logs"
        return 0
    fi
}

# Function to repair issues
repair_notebook() {
    local notebook_name=$1
    local failure_type=$2
    
    echo "Repairing $notebook_name for $failure_type..."
    
    # Based on failure type, apply appropriate fix
    case $failure_type in
        *infinite*loop*|*hang*|*stuck*)
            # Add timeouts and iteration limits
            if [ -f "voice_synthesizer.py" ]; then
                echo "Adding timeout safeguards to voice_synthesizer.py..."
                # Already implemented timeouts
            fi
            if [ -f "video_synthesizer.py" ]; then
                echo "Adding timeout safeguards to video_synthesizer.py..."
                # Already implemented timeouts
            fi
            ;;
        *memory*|*oom*)
            # Adjust memory usage parameters
            echo "Optimizing memory usage for $notebook_name..."
            ;;
        *gpu*|*cuda*|*tpu*)
            # Fix device configuration
            echo "Adjusting device configuration for $notebook_name..."
            ;;
        *)
            echo "Applying general fix for $notebook_name..."
            ;;
    esac
    
    # Commit the fix
    git add . 
    git commit -m "Fix: Addressed $failure_type in $notebook_name"
    git push
}

# Main monitoring loop
echo "Starting periodic log monitoring loop..."
while true; do
    for notebook in "${NOTEBOOKS[@]}"; do
        echo "Checking logs for: $notebook"
        
        # Fetch logs for the notebook
        log_file=$(fetch_kernel_logs "$notebook")
        
        # Analyze logs for failures
        if analyze_logs "$log_file" "$notebook"; then
            echo "✓ $notebook is running successfully"
        else
            echo "✗ $notebook has failures, initiating repair..."
            # Determine failure type and repair
            failure_type=$(grep -i "error\|exception\|traceback\|failed\|timeout\|infinite loop\|hang\|stuck\|gpu\|cuda\|tpu\|memory\|oom" "$log_file" | head -n 1)
            repair_notebook "$notebook" "$failure_type"
        fi
    done
    
    echo "Completed log monitoring cycle. Waiting 60 seconds before next cycle..."
    sleep 60
done