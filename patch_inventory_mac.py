"""
Crimson Desert - Inventory Expander v2.2.0 (Mac Native)
- Updated: Slot values 180 / 999 
- Fixed: Added Auto-Search for 0.papgt to prevent path errors
- Fixed: Added detailed debug logging for integrity updates
"""

import struct
import shutil
import os
import sys

try:
    import lz4.block
except ImportError:
    print("❌ ERROR: lz4 module is not installed. Run 'pip3 install lz4' in the terminal.")
    sys.exit(1)

VERSION = "2.2.0 (Mac)"
PAZ_SUBDIR = "0008"
PAZ_FILE = "0.paz"
PAMT_FILE = "0.pamt"

NEW_DEFAULT = 180
NEW_MAX = 999

VANILLA_DEFAULT = 50
VANILLA_MAX = 240
INTEGRITY_SEED = 0xC5EDE
CHAR_SIG = struct.pack('<HI', 2, 9) + b'Character\x00'

# ── Bob Jenkins hashlittle ───────────────────────────────────────────
def _rot(v, k): return ((v << k) | (v >> (32 - k))) & 0xFFFFFFFF

def hashlittle(data: bytes, initval: int = 0) -> int:
    length = len(data); a = b = c = (0xDEADBEEF + length + initval) & 0xFFFFFFFF; offset = 0
    while length > 12:
        a = (a + struct.unpack_from("<I", data, offset)[0]) & 0xFFFFFFFF
        b = (b + struct.unpack_from("<I", data, offset + 4)[0]) & 0xFFFFFFFF
        c = (c + struct.unpack_from("<I", data, offset + 8)[0]) & 0xFFFFFFFF
        a = (a - c) & 0xFFFFFFFF; a ^= _rot(c, 4);  c = (c + b) & 0xFFFFFFFF
        b = (b - a) & 0xFFFFFFFF; b ^= _rot(a, 6);  a = (a + c) & 0xFFFFFFFF
        c = (c - b) & 0xFFFFFFFF; c ^= _rot(b, 8);  b = (b + a) & 0xFFFFFFFF
        a = (a - c) & 0xFFFFFFFF; a ^= _rot(c, 16); c = (c + b) & 0xFFFFFFFF
        b = (b - a) & 0xFFFFFFFF; b ^= _rot(a, 19); a = (a + c) & 0xFFFFFFFF
        c = (c - b) & 0xFFFFFFFF; c ^= _rot(b, 4);  b = (b + a) & 0xFFFFFFFF
        offset += 12; length -= 12
    remaining = data[offset:]
    if length > 0:
        padded = remaining + b"\x00" * (12 - len(remaining))
        if length >= 1:  a = (a + padded[0]) & 0xFFFFFFFF
        if length >= 2:  a = (a + (padded[1] << 8)) & 0xFFFFFFFF
        if length >= 3:  a = (a + (padded[2] << 16)) & 0xFFFFFFFF
        if length >= 4:  a = (a + (padded[3] << 24)) & 0xFFFFFFFF
        if length >= 5:  b = (b + padded[4]) & 0xFFFFFFFF
        if length >= 6:  b = (b + (padded[5] << 8)) & 0xFFFFFFFF
        if length >= 7:  b = (b + (padded[6] << 16)) & 0xFFFFFFFF
        if length >= 8:  b = (b + (padded[7] << 24)) & 0xFFFFFFFF
        if length >= 9:  c = (c + padded[8]) & 0xFFFFFFFF
        if length >= 10: c = (c + (padded[9] << 8)) & 0xFFFFFFFF
        if length >= 11: c = (c + (padded[10] << 16)) & 0xFFFFFFFF
        if length >= 12: c = (c + (padded[11] << 24)) & 0xFFFFFFFF
        c ^= b; c = (c - _rot(b, 14)) & 0xFFFFFFFF
        a ^= c; a = (a - _rot(c, 11)) & 0xFFFFFFFF
        b ^= a; b = (b - _rot(a, 25)) & 0xFFFFFFFF
        c ^= b; c = (c - _rot(b, 16)) & 0xFFFFFFFF
        a ^= c; a = (a - _rot(c, 4)) & 0xFFFFFFFF
        b ^= a; b = (b - _rot(a, 14)) & 0xFFFFFFFF
        c ^= b; c = (c - _rot(b, 24)) & 0xFFFFFFFF
    return c

# ── Dynamic Path Finder ──────────────────────────────────────────────
def find_papgt_path():
    """Scans the entire game folder to find the exact location of 0.papgt."""
    search_dir = os.path.expanduser("~/Library/Application Support/Steam/steamapps/common/Crimson Desert")
    for root, dirs, files in os.walk(search_dir):
        if "0.papgt" in files and "meta" in root.lower():
            return os.path.join(root, "0.papgt")
    return None

# ── PAMT Parser ──────────────────────────────────────────────────────
def find_inventory_entry(pamt_path, paz_dir):
    with open(pamt_path, 'rb') as f: data = f.read()
    pamt_stem = os.path.splitext(os.path.basename(pamt_path))[0]
    off = 4
    paz_count = struct.unpack_from('<I', data, off)[0]; off += 4
    off += 8
    for i in range(paz_count):
        off += 8
        if i < paz_count - 1: off += 4
    folder_size = struct.unpack_from('<I', data, off)[0]; off += 4
    folder_end = off + folder_size
    folder_prefix = ""
    while off < folder_end:
        parent = struct.unpack_from('<I', data, off)[0]
        slen = data[off + 4]
        name = data[off + 5:off + 5 + slen].decode('utf-8', errors='replace')
        if parent == 0xFFFFFFFF: folder_prefix = name
        off += 5 + slen
    node_size = struct.unpack_from('<I', data, off)[0]; off += 4
    node_start = off
    nodes = {}
    while off < node_start + node_size:
        rel = off - node_start
        parent = struct.unpack_from('<I', data, off)[0]
        slen = data[off + 4]
        name = data[off + 5:off + 5 + slen].decode('utf-8', errors='replace')
        nodes[rel] = (parent, name)
        off += 5 + slen
    def build_path(node_ref):
        parts = []; cur = node_ref
        while cur != 0xFFFFFFFF and len(parts) < 64:
            if cur not in nodes: break
            p, n = nodes[cur]
            parts.append(n)
            cur = p
        return ''.join(reversed(parts))
    folder_count = struct.unpack_from('<I', data, off)[0]; off += 4
    off += 4
    off += folder_count * 16
    while off + 20 <= len(data):
        node_ref, paz_offset, comp_size, orig_size, flags = struct.unpack_from('<IIIII', data, off)
        paz_index = flags & 0xFF
        node_path = build_path(node_ref)
        full_path = f"{folder_prefix}/{node_path}" if folder_prefix else node_path
        if 'inventory.pabgb' in full_path.lower():
            paz_num = int(pamt_stem) + paz_index
            paz_file = os.path.join(paz_dir, f"{paz_num}.paz")
            return (paz_file, paz_offset, comp_size, orig_size, flags, off + 4)
        off += 20
    return None

# ── Integrity Updates ────────────────────────────────────────────────
def update_pamt_comp_size(pamt_path, record_offset, new_comp_size):
    with open(pamt_path, 'rb') as f: data = bytearray(f.read())
    old_comp = struct.unpack_from('<I', data, record_offset + 4)[0]
    struct.pack_into('<I', data, record_offset + 4, new_comp_size)
    pamt_hash = hashlittle(bytes(data[12:]), INTEGRITY_SEED)
    struct.pack_into('<I', data, 0, pamt_hash)
    with open(pamt_path, 'wb') as f: f.write(bytes(data))
    return old_comp

def _find_papgt_entry_count(papgt, entry_start):
    file_size = len(papgt)
    for n in range(1, 100):
        size_pos = entry_start + n * 12
        if size_pos + 4 > file_size: break
        string_size = struct.unpack_from('<I', papgt, size_pos)[0]
        if size_pos + 4 + string_size == file_size: return n
    return 0

def update_papgt(papgt_path, pamt_path, pamt_subdir):
    if not papgt_path or not os.path.exists(papgt_path):
        print("❌ ERROR: Could not find the PAPGT file.")
        return False
        
    print(f"🔍 PAPGT file detected: {papgt_path}")
    
    with open(pamt_path, 'rb') as f: pamt_data = f.read()
    new_pamt_hash = hashlittle(pamt_data[12:], INTEGRITY_SEED)
    
    with open(papgt_path, 'rb') as f: papgt = bytearray(f.read())
    if len(papgt) < 16:
        print("❌ ERROR: The PAPGT file is too small or corrupted.")
        return False
    
    entry_start = 12
    entry_count = _find_papgt_entry_count(papgt, entry_start)
    string_table_start = entry_start + entry_count * 12 + 4
    
    found = False
    for i in range(entry_count):
        pos = entry_start + i * 12
        name_offset = struct.unpack_from('<I', papgt, pos + 4)[0]
        abs_off = string_table_start + name_offset
        if abs_off >= len(papgt): continue
        end = papgt.index(0, abs_off) if 0 in papgt[abs_off:] else len(papgt)
        dir_name = papgt[abs_off:end].decode('ascii', errors='replace')
        if dir_name == pamt_subdir:
            struct.pack_into('<I', papgt, pos + 8, new_pamt_hash)
            found = True; break
            
    if not found:
        print(f"❌ ERROR: Could not find directory info for '{pamt_subdir}' inside PAPGT.")
        return False
        
    papgt_hash = hashlittle(bytes(papgt[12:]), INTEGRITY_SEED)
    struct.pack_into('<I', papgt, 4, papgt_hash)
    with open(papgt_path, 'wb') as f: f.write(bytes(papgt))
    
    print("✅ PAPGT integrity checksum updated successfully!")
    return True

# ── Core Patching Logic ──────────────────────────────────────────────
def apply_patch(papgt_path, info, new_default, new_max):
    data = info['decompressed']
    struct.pack_into('<H', data, info['char_ds_offset'], new_default)
    struct.pack_into('<H', data, info['char_ms_offset'], new_max)

    if info['is_compressed']:
        payload = lz4.block.compress(bytes(data), store_size=False)
        new_comp_size = len(payload)
        print(f"📦 Compressed size changed: {info['comp_size']} -> {new_comp_size} bytes")
        
        if new_comp_size > info['comp_size']:
            print(f"⚠️ Data size increased: Safely appending to the end of the file.")
            paz_size = os.path.getsize(info['paz_path'])
            new_offset = paz_size
            with open(info['paz_path'], 'r+b') as f:
                f.seek(new_offset); f.write(payload)
            
            pamt_path = info['pamt_path']
            with open(pamt_path, 'rb') as f: pamt_data = bytearray(f.read())
            struct.pack_into('<I', pamt_data, info['pamt_record_offset'], new_offset)
            struct.pack_into('<I', pamt_data, info['pamt_record_offset'] + 4, new_comp_size)
            with open(pamt_path, 'wb') as f: f.write(bytes(pamt_data))
        else:
            with open(info['paz_path'], 'r+b') as f:
                f.seek(info['paz_offset']); f.write(payload)
            if new_comp_size != info['comp_size']:
                update_pamt_comp_size(info['pamt_path'], info['pamt_record_offset'], new_comp_size)
    else:
        with open(info['paz_path'], 'r+b') as f:
            f.seek(info['paz_offset']); f.write(bytes(data))

    return update_papgt(papgt_path, info['pamt_path'], PAZ_SUBDIR)

def main():
    print(f"==================================================")
    print(f"  🚀 {VERSION} Inventory Expander Patch (180/999 Safe Mode)")
    print(f"==================================================")

    base_path = os.path.expanduser("~/Library/Application Support/Steam/steamapps/common/Crimson Desert/CrimsonDesert_Steam.app/Contents/Resources/packages")
    paz_dir = os.path.join(base_path, PAZ_SUBDIR)
    pamt_path = os.path.join(paz_dir, PAMT_FILE)
    
    # 🚨 Auto-search for 0.papgt
    papgt_src = find_papgt_path()

    if not os.path.exists(pamt_path):
        print("❌ ERROR: Could not find original data (PAMT).")
        sys.exit(1)

    entry = find_inventory_entry(pamt_path, paz_dir)
    if not entry:
        print("❌ ERROR: Failed to parse inventory data.")
        sys.exit(1)

    paz_f, p_off, c_s, o_s, flg, rec_off = entry
    is_compressed = c_s != o_s and ((flg >> 16) & 0x0F) == 2

    # 📦 Create individual backups
    backup_paz = paz_f + ".inventory_backup"
    backup_pamt = pamt_path + ".inventory_backup"
    
    print(f"📦 Checking original backups...")
    if not os.path.exists(backup_paz):
        shutil.copy2(paz_f, backup_paz)
        print(f"  - PAZ backup complete")
    if not os.path.exists(backup_pamt):
        shutil.copy2(pamt_path, backup_pamt)
        print(f"  - PAMT backup complete")
        
    if papgt_src:
        backup_papgt = papgt_src + ".inventory_backup"
        if not os.path.exists(backup_papgt):
            shutil.copy2(papgt_src, backup_papgt)
            print(f"  - PAPGT backup complete")

    with open(paz_f, 'rb') as f:
        f.seek(p_off); raw = f.read(c_s)

    try:
        decompressed = lz4.block.decompress(raw, uncompressed_size=o_s) if is_compressed else raw
    except:
        print("❌ ERROR: Failed to decompress data.")
        sys.exit(1)
    
    idx = decompressed.find(CHAR_SIG)
    if idx < 0:
        print("❌ ERROR: Could not find Character signature.")
        sys.exit(1)

    base = idx + len(CHAR_SIG); ds_off = ms_off = None
    for off in range(0, 30):
        d = struct.unpack_from('<H', decompressed, base + off)[0]
        m = struct.unpack_from('<H', decompressed, base + off + 2)[0]
        if d == VANILLA_DEFAULT and m == VANILLA_MAX:
            ds_off = base + off; ms_off = ds_off + 2; break

    if ds_off is None:
        marker = bytes([0x00, 0x28, 0x80, 0x02])
        for off in range(4, 40):
            if decompressed[base + off:base + off + 4] == marker:
                ds_off = base + off - 4; ms_off = ds_off + 2; break

    if ds_off is None:
        print("❌ ERROR: Failed to find slot data offset.")
        sys.exit(1)

    info = {
        'paz_path': paz_f, 'pamt_path': pamt_path, 'paz_offset': p_off,
        'comp_size': c_s, 'orig_size': o_s, 'is_compressed': is_compressed,
        'pamt_record_offset': rec_off, 'decompressed': bytearray(decompressed),
        'char_ds_offset': ds_off, 'char_ms_offset': ms_off
    }

    if apply_patch(papgt_src, info, NEW_DEFAULT, NEW_MAX):
        # macOS quarantine removal
        app_path = os.path.expanduser("~/Library/Application Support/Steam/steamapps/common/Crimson Desert/CrimsonDesert_Steam.app")
        os.system(f'sudo xattr -rd com.apple.quarantine "{app_path}"')
        os.system(f'sudo xattr -cr "{app_path}"')
        print(f"\n🎉 Patch and security bypass completed! (180 / 999)")
        print("You can now launch the game!")
    else:
        print("\n❌ An error occurred while applying the patch.")
        sys.exit(1)

if __name__ == '__main__':
    main()