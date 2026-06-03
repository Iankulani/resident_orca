#!/bin/bash

# Quick Deployment Script for Resident Orca
# One-command setup and run

set -e

echo "🐋 Deploying Resident Orca..."

# Clone or copy files
if [ ! -f "resident_orca.py" ]; then
    echo "Error: resident_orca.py not found in current directory"
    exit 1
fi

# Run installer
chmod +x install.sh
./install.sh

# Start Orca
echo "Starting Resident Orca..."
./run_orca.sh