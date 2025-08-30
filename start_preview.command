#!/bin/bash
# This script builds the static site and starts a local server.

echo ">>> Building static site..."
python3 build.py

echo ">>> Starting local server in 'public' directory..."
echo ">>> Access the site at http://localhost:8080"
echo ">>> Press Ctrl+C to stop the server."

cd public
python3 -m http.server 8080
