#!/bin/bash
# This script builds the static site and serves it locally.

# Exit immediately if a command exits with a non-zero status.
set -e

# Get the absolute path of the script's directory
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Change to the script's directory (the project root)
cd "$SCRIPT_DIR"

# --- 1. Build the site ---
echo "
[1;34mBuilding the website...[0m"
python3 build.py

# --- 2. Start the local server ---
echo "
[1;32mBuild complete. Starting server at http://localhost:8000[0m"
echo "(Press Ctrl+C to stop the server)"
cd public
python3 -m http.server 8000
