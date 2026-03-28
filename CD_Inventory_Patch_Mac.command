#!/bin/bash

# Crimson Desert Mac Inventory Patcher
# Created by yunsuper1 (Cherry) for macOS Support

clear
echo "======================================================="
echo "   Crimson Desert Inventory Expander (macOS Native)"
echo "   Target: Base 200 / Max 240 Slots"
echo "======================================================="
echo ""

# Game Path Configuration
TARGET_PATH="$HOME/Library/Application Support/Steam/steamapps/common/Crimson Desert/CrimsonDesert_Steam.app/Contents/Resources/packages/0008/0.paz"
APP_PATH="$HOME/Library/Application Support/Steam/steamapps/common/Crimson Desert/CrimsonDesert_Steam.app"

if [ ! -f "$TARGET_PATH" ]; then
    echo "❌ Error: Game file (0.paz) not found."
    echo "Please ensure the game is installed in the default Steam library path."
    exit 1
fi

echo "1. Backing up original file..."
cp "$TARGET_PATH" "$TARGET_PATH.bak"
echo "✅ Backup completed: 0.paz.bak"

echo "2. Patching inventory data..."
python3 -c "
import os
path = '$TARGET_PATH'
sig = b'\x02\x00\x09\x00\x00\x00Character\x00\x01'
try:
    with open(path, 'r+b') as f:
        data = f.read()
        off = data.find(sig)
        if off != -1:
            f.seek(off + 17)
            f.write(b'\xc8\x00\xf0\x00')
            print('✅ Data patching successful!')
        else:
            print('❌ Error: Signature pattern not found.')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo "3. Removing macOS Quarantine (Requires sudo password)..."
sudo xattr -cr "$APP_PATH"

echo ""
echo "======================================================="
echo "   🎉 Patch Complete! You can now launch the game."
echo "======================================================="
read -p "Press any key to exit..."