#!/usr/bin/python3

from Cryptodome.Cipher import AES
import base64
import sys

if len(sys.argv) != 2:
    print(f"\n[+] Usage: {sys.argv[0]} <cpassword>")
    sys.exit(1)

cpassword = sys.argv[1].strip()

KEY = bytes.fromhex(
    "4e9906e8fcb66cc9faf49310620ffee8"
    "f496e806cc057990209b09a433b66c1b"
)

IV = b"\x00" * 16

padding = (4 - len(cpassword) % 4) % 4
cpassword_padded = cpassword + ("=" * padding)

try:
    encrypted = base64.b64decode(cpassword_padded)
except Exception:
    print("[!] Error: cpassword is not valid Base64")
    sys.exit(1)

cipher = AES.new(KEY, AES.MODE_CBC, IV)
decrypted = cipher.decrypt(encrypted)

pad_len = decrypted[-1]
if pad_len < 1 or pad_len > 16:
    print("[!] Invalid padding")
    sys.exit(1)

decrypted = decrypted[:-pad_len]

try:
    password = decrypted.decode("utf-16le")
except UnicodeDecodeError:
    print("[!] Error decoding UTF-16LE")
    sys.exit(1)

print(password)
