# obfuscate_license.py
import os
import sys
import base64
import zlib

def obfuscate_file(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    start_marker = "# <<<LIC-START>>>"
    end_marker = "# <<<LIC-END>>>"

    if start_marker not in src or end_marker not in src:
        print("ERROR: markers not found. Make sure your file has the markers:")
        print(start_marker, end_marker)
        return

    before, rest = src.split(start_marker, 1)
    lic_and_after = rest.split(end_marker, 1)
    license_block = lic_and_after[0]
    after = lic_and_after[1]

    # Compress & base64 the license text
    compressed = zlib.compress(license_block.encode("utf-8"), level=9)
    b64 = base64.b64encode(compressed).decode("ascii")

    # Build loader that will decode, decompress and exec the license at runtime
    # We keep the loader compact to reduce visibility of the license content.
    loader = (
        f"# --- LICENSE BLOCK (obfuscated) ---\n"
        f"import base64, zlib\n"
        f"_b = {repr(b64)}\n"
        f"_s = zlib.decompress(base64.b64decode(_b)).decode('utf-8')\n"
        f"exec(compile(_s, '<license>', 'exec'), globals())\n"
        f"# --- END LICENSE LOADER ---\n"
    )

    new_src = before + loader + after

    # Save backup and overwrite original
    # backup = path + ".backup"
    # if not os.path.exists(backup):
    #     with open(backup, "w", encoding="utf-8") as f:
    #         f.write(src)
    #     print(f"Backup written to: {backup}")
    # else:
    #     print(f"Backup already exists: {backup} (original preserved)")

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_src)

    print(f"File obfuscated and written to: {path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python obfuscate_license.py <path-to-your-python-file>")
        sys.exit(1)
    target = sys.argv[1]
    if not os.path.exists(target):
        print("File not found:", target)
        sys.exit(1)
    obfuscate_file(target)
