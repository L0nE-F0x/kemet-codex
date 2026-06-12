"""Generate Kemet Codex PWA icons (gold pyramid on midnight navy).

Pure-stdlib PNG writer — no Pillow required. Run from the project root:
    python tools/gen_icons.py
"""
import os
import struct
import zlib

NAVY = (11, 19, 43)        # #0B132B
GOLD = (201, 168, 108)     # #C9A86C
GOLD_DARK = (169, 133, 75) # #a9854b


def chunk(tag, data):
    raw = tag + data
    return struct.pack(">I", len(data)) + raw + struct.pack(">I", zlib.crc32(raw) & 0xFFFFFFFF)


def write_png(path, size):
    # Triangle geometry (with margin so maskable icons survive cropping)
    apex_y = size * 0.18
    base_y = size * 0.84
    half_w = size * 0.36
    cx = size / 2

    rows = bytearray()
    for y in range(size):
        rows.append(0)  # filter: none
        if apex_y <= y <= base_y:
            t = (y - apex_y) / (base_y - apex_y)
            hw = t * half_w
            x0, x1 = cx - hw, cx + hw
        else:
            x0, x1 = 1, 0  # empty
        for x in range(size):
            if x0 <= x <= x1:
                # subtle vertical shading on the pyramid face
                t = (y - apex_y) / (base_y - apex_y)
                r = int(GOLD[0] + (GOLD_DARK[0] - GOLD[0]) * t)
                g = int(GOLD[1] + (GOLD_DARK[1] - GOLD[1]) * t)
                b = int(GOLD[2] + (GOLD_DARK[2] - GOLD[2]) * t)
                rows += bytes((r, g, b, 255))
            else:
                rows += bytes((*NAVY, 255))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(rows), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    print(f"wrote {path} ({size}x{size}, {os.path.getsize(path)} bytes)")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "icons")
    os.makedirs(out, exist_ok=True)
    write_png(os.path.join(out, "icon-192.png"), 192)
    write_png(os.path.join(out, "icon-512.png"), 512)
