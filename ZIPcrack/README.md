# **ZIPcrack**

#### Get the password of a compressed `ZIP` file.

![](/ZIPcrack/img/screenshot.png)

---

## Download

```sh
wget --no-check-certificate -q "https://raw.githubusercontent.com/VulNyx/Arsenal/refs/heads/main/ZIPcrack/ZIPcrack" && chmod +x ZIPcrack
```

## Download & Install (PATH)

```cmd
wget --no-check-certificate -q "https://raw.githubusercontent.com/VulNyx/Arsenal/refs/heads/main/ZIPcrack/ZIPcrack" -O /usr/bin/ZIPcrack && chmod +x /usr/bin/ZIPcrack
```

## Usage

Install 7-Zip and ensure the `7z` command is available on your `PATH` before
running ZIPcrack. The script reports a missing dependency without installing it.

```sh
ZIPcrack -f <FILE> -w <WORDLIST>
```

To check missing-dependency handling, run `python3 ZIPcrack/test_dependency.py`
from the repository root.

---
