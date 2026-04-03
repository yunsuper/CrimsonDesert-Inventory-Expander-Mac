#!/bin/bash

# Crimson Desert Mac Inventory Patcher
# Created by yunsuper1

clear
echo "==============================================="
echo "   Crimson Desert Inventory Expander (Mac Native)"
echo "   Target: 180 Starting Slots / 999 Max Slots"
echo "==============================================="
echo ""

# Check for lz4 module (Required for Python decompression)
python3 -c "import lz4.block" &> /dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing the required 'lz4' module..."
    python3 -m pip install lz4
fi

# Run Python patch script (patch_inventory_mac.py in the same folder)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python3 "$DIR/patch_inventory_mac.py"

# Proceed with macOS quarantine removal only if Python script succeeds
if [ $? -eq 0 ]; then
    APP_PATH="$HOME/Library/Application Support/Steam/steamapps/common/Crimson Desert/CrimsonDesert_Steam.app"
    echo ""
    echo "3. Removing macOS Quarantine (Mac login password required)..."
    sudo xattr -cr "$APP_PATH"
    echo "==============================================="
    echo "   🎉 Patch and Quarantine Removal Completed Successfully!"
else
    echo "==============================================="
    echo "   ❌ An error occurred during the patching process."
fi

echo "==============================================="
read -p "Press any key to exit..."