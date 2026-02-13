#!/bin/bash

# Alatoo CTF Setup & Run Script

# Configuration
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
SERVER_SCRIPT="server.py"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[CTF-SETUP]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    error "Python 3 is not installed."
    echo "Run: sudo apt update && sudo apt install python3"
    exit 1
fi

# 2. Check if the venv module is available
# On some Debian/Ubuntu/Raspberry Pi OS versions, you need 'python3-venv' specifically.
if ! python3 -m venv --help &> /dev/null; then
    error "Python 3 venv module is missing."
    echo "Run: sudo apt install python3-venv"
    exit 1
fi

# 3. Create Virtual Environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    log "Creating virtual environment in ./$VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        error "Failed to create virtual environment."
        exit 1
    fi
else
    log "Using existing virtual environment."
fi

# 4. Activate Virtual Environment
log "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# 5. Install Dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
    log "Installing/Updating requirements..."
    pip install -r "$REQUIREMENTS_FILE"
    if [ $? -ne 0 ]; then
        error "Failed to install dependencies."
        exit 1
    fi
else
    error "$REQUIREMENTS_FILE not found!"
    exit 1
fi

# 6. Run the Server
log "Starting CTF Server..."
python "$SERVER_SCRIPT"
