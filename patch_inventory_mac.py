"""
Crimson Desert - Inventory Expander v2.0.1 (Mac Edition)
Patches the game's PAZ archive to increase inventory slot count.
"""

import struct
import shutil
import os
import sys

VERSION = "2.0.1 (Mac)"

PAZ_SUBDIR = "0008"
PAZ_FILE = "0.paz"
PAMT_FILE = "0.pamt"

VANILLA_DEFAULT = 50
VANILLA_MAX = 240
SAFE_MAX_CEILING = 999

# Signature in decompressed data
CHAR_SIG = struct.pack('<I', 9) + b'Character\x00\x01'
INTEGRITY_SEED = 0xC5EDE

# ── Bob Jenkins hashlittle ───────────────────────────────────────────
def _rot(v, k):
    return ((v << k) | (v >> (32 - k))) & 0xFFFFFFFF

def hashlittle(data: bytes, initval: int = 0) -> int:
    length = len(data)
    a = b = c = (0xDEADBEEF + length + initval) & 0xFFFFFFFF
    offset = 0

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
        offset += 12
        length -= 12

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

# ── PAMT parser (minimal, self-contained) ────────────────────────────
def find_inventory_entry(pamt_path, paz_dir):
    with open(pamt_path, 'rb') as f:
        data = f.read()

    pamt_stem = os.path.splitext(os.path.basename(pamt_path))[0]
    off = 4
    paz_count = struct.unpack_from('<I', data, off)[0]; off += 4
    off += 8

    for i in range(paz_count):
        off += 8
        if i < paz_count - 1:
            off += 4

    folder_size = struct.unpack_from('<I', data, off)[0]; off += 4
    folder_end = off + folder_size
    folder_prefix = ""
    while off < folder_end:
        parent = struct.unpack_from('<I', data, off)[0]
        slen = data[off + 4]
        name = data[off + 5:off + 5 + slen].decode('utf-8', errors='replace')
        if parent == 0xFFFFFFFF:
            folder_prefix = name
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
        parts = []
        cur = node_ref
        while cur != 0xFFFFFFFF and len(parts) < 64:
            if cur not in nodes:
                break
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

# ── LZ4 decompression/compression ────────────────────────────────────
def lz4_decompress(data, orig_size):
    import lz4.block
    return lz4.block.decompress(data, uncompressed_size=orig_size)

def lz4_compress(data):
    import lz4.block
    return lz4.block.compress(data, store_size=False)

# ── Integrity chain updates ──────────────────────────────────────────
def update_pamt_comp_size(pamt_path, record_offset, new_comp_size):
    with open(pamt_path, 'rb') as f:
        data = bytearray(f.read())
    old_comp = struct.unpack_from('<I', data, record_offset + 4)[0]
    struct.pack_into('<I', data, record_offset + 4, new_comp_size)
    pamt_hash = hashlittle(bytes(data[12:]), INTEGRITY_SEED)
    struct.pack_into('<I', data, 0, pamt_hash)
    with open(pamt_path, 'wb') as f:
        f.write(bytes(data))
    return old_comp

def update_papgt(game_dir, pamt_subdir):
    papgt_path = os.path.join(game_dir, "meta", "0.papgt")
    pamt_path = os.path.join(game_dir, pamt_subdir, PAMT_FILE)
    if not os.path.exists(papgt_path):
        return False
    with open(pamt_path, 'rb') as f:
        pamt_data = f.read()
    new_pamt_hash = hashlittle(pamt_data[12:], INTEGRITY_SEED)
    with open(papgt_path, 'rb') as f:
        papgt = bytearray(f.read())
    if len(papgt) < 16:
        return False

    entry_start = 12
    entry_count = _find_papgt_entry_count(papgt, entry_start)
    string_table_size_pos = entry_start + entry_count * 12
    string_table_start = string_table_size_pos + 4

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
            found = True
            break

    if not found: return False
    papgt_hash = hashlittle(bytes(papgt[12:]), INTEGRITY_SEED)
    struct.pack_into('<I', papgt, 4, papgt_hash)
    with open(papgt_path, 'wb') as f:
        f.write(bytes(papgt))
    return True

def _find_papgt_entry_count(papgt, entry_start):
    file_size = len(papgt)
    for n in range(1, 100):
        size_pos = entry_start + n * 12
        if size_pos + 4 > file_size: break
        string_size = struct.unpack_from('<I', papgt, size_pos)[0]
        if size_pos + 4 + string_size == file_size: return n
    return 0

# ── Core patching logic ──────────────────────────────────────────────
def find_and_read_inventory(game_path):
    paz_path = os.path.join(game_path, PAZ_SUBDIR, PAZ_FILE)
    pamt_path = os.path.join(game_path, PAZ_SUBDIR, PAMT_FILE)

    if not os.path.exists(pamt_path): return None
    paz_dir = os.path.join(game_path, PAZ_SUBDIR)
    entry = find_inventory_entry(pamt_path, paz_dir)
    if entry is None: return None

    paz_file, paz_offset, comp_size, orig_size, flags, pamt_rec_off = entry
    is_compressed = comp_size != orig_size and ((flags >> 16) & 0x0F) == 2

    with open(paz_file, 'rb') as f:
        f.seek(paz_offset)
        raw = f.read(comp_size)

    if is_compressed:
        decompressed = lz4_decompress(raw, orig_size)
    else:
        decompressed = raw

    idx = decompressed.find(CHAR_SIG)
    if idx < 0: return None

    ds_off = idx + len(CHAR_SIG)
    ms_off = ds_off + 2
    cur_default = struct.unpack_from('<H', decompressed, ds_off)[0]
    cur_max = struct.unpack_from('<H', decompressed, ms_off)[0]

    return {
        'paz_path': paz_file, 'pamt_path': pamt_path, 'paz_offset': paz_offset,
        'comp_size': comp_size, 'orig_size': orig_size, 'is_compressed': is_compressed,
        'pamt_record_offset': pamt_rec_off, 'decompressed': bytearray(decompressed),
        'char_ds_offset': ds_off, 'char_ms_offset': ms_off,
        'cur_default': cur_default, 'cur_max': cur_max,
    }

def apply_patch(game_path, info, new_default, new_max):
    data = info['decompressed']
    struct.pack_into('<H', data, info['char_ds_offset'], new_default)
    struct.pack_into('<H', data, info['char_ms_offset'], new_max)

    if info['is_compressed']:
        payload = lz4_compress(bytes(data))
        new_comp_size = len(payload)
        
        if new_comp_size > info['comp_size']:
            paz_size = os.path.getsize(info['paz_path'])
            new_offset = paz_size
            with open(info['paz_path'], 'r+b') as f:
                f.seek(new_offset)
                f.write(payload)
            pamt_path = info['pamt_path']
            with open(pamt_path, 'rb') as f:
                pamt_data = bytearray(f.read())
            struct.pack_into('<I', pamt_data, info['pamt_record_offset'], new_offset)
            struct.pack_into('<I', pamt_data, info['pamt_record_offset'] + 4, new_comp_size)
            with open(pamt_path, 'wb') as f:
                f.write(bytes(pamt_data))
        else:
            with open(info['paz_path'], 'r+b') as f:
                f.seek(info['paz_offset'])
                f.write(payload)
            if new_comp_size != info['comp_size']:
                update_pamt_comp_size(info['pamt_path'], info['pamt_record_offset'], new_comp_size)
    else:
        with open(info['paz_path'], 'r+b') as f:
            f.seek(info['paz_offset'])
            f.write(bytes(data))

    update_papgt(game_path, PAZ_SUBDIR)
    return True

# ── Game path finder (Modified for Mac) ──────────────────────────────
def find_game_path():
    """Search default Mac Steam path."""
    mac_path = os.path.expanduser("~/Library/Application Support/Steam/steamapps/common/Crimson Desert/CrimsonDesert_Steam.app/Contents/Resources/packages")
    if os.path.exists(os.path.join(mac_path, PAZ_SUBDIR, PAZ_FILE)):
        return mac_path
    return None

# ── Main ─────────────────────────────────────────────────────────────
def main():
    game_path = find_game_path()
    
    if not game_path:
        print("❌ Cannot find Crimson Desert (packages folder) in the default Mac Steam path.")
        sys.exit(1)

    paz_path = os.path.join(game_path, PAZ_SUBDIR, PAZ_FILE)
    pamt_path = os.path.join(game_path, PAZ_SUBDIR, PAMT_FILE)
    backup_paz = paz_path + ".inventory_backup"
    backup_pamt = pamt_path + ".inventory_backup"
    backup_papgt = os.path.join(game_path, "meta", "0.papgt.inventory_backup")

    info = find_and_read_inventory(game_path)
    if info is None:
        print("❌ Cannot find inventory data or the file is corrupted.")
        sys.exit(1)

    new_default = 180
    new_max = 999

    if not os.path.exists(backup_paz):
        shutil.copy2(paz_path, backup_paz)
    if not os.path.exists(backup_pamt) and os.path.exists(pamt_path):
        shutil.copy2(pamt_path, backup_pamt)
    papgt_src = os.path.join(game_path, "meta", "0.papgt")
    if not os.path.exists(backup_papgt) and os.path.exists(papgt_src):
        shutil.copy2(papgt_src, backup_papgt)

    success = apply_patch(game_path, info, new_default, new_max)
    if not success:
        print("❌ Patch failed. Attempting to restore original files...")
        sys.exit(1)

    print(f"✅ Patch successfully applied! (Starting: {new_default} slots / Max: {new_max} slots)")

if __name__ == '__main__':
    main()