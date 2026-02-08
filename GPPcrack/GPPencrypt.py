#!/usr/bin/python3

from Cryptodome.Cipher import AES
import base64
import sys

if len(sys.argv) != 2:
    print(f"\n[+] Usage: {sys.argv[0]} <password>")
    sys.exit(1)

password = sys.argv[1]

KEY = bytes.fromhex(
    "4e9906e8fcb66cc9faf49310620ffee8"
    "f496e806cc057990209b09a433b66c1b"
)

IV = b"\x00" * 16

data = password.encode("utf-16le")

pad_len = 16 - (len(data) % 16)
data += bytes([pad_len]) * pad_len

cipher = AES.new(KEY, AES.MODE_CBC, IV)
encrypted = cipher.encrypt(data)

cpassword = base64.b64encode(encrypted).decode("ascii").rstrip("=")

print(cpassword)
