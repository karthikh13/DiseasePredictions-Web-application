#!/usr/bin/env bash
echo "⚙️ Using custom build script"

# Set Python version manually
echo "python-3.10.12" > runtime.txt

# Install dependencies manually
pip install -r requirements.txt
