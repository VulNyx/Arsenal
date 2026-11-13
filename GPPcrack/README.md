# GPPcrack

### Overview

Tool to decrypt passwords (**`cpassword`**) from [Group Policy Preferences (GPP)](https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/information-group-policy-preferences-events) taking advantage of [Microsoft](https://microsoft.com) release of the [AES key](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be).

### Download

```sh
wget --no-check-certificate -q "https://raw.githubusercontent.com/VulNyx/Arsenal/refs/heads/main/GPPcrack/GPPcrack.py" && chmod +x GPPcrack.py
```

### Setup

Both `GPPcrack.py` and the companion `GPPencrypt.py` require Python 3 and
`pycryptodomex`. Create a virtual environment and install the dependency:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install pycryptodomex
```

On Windows, activate it with `.venv\Scripts\activate` instead. If you downloaded
only `GPPcrack.py`, download `GPPencrypt.py` separately to use the companion.

### Usage

```cmd
python3 GPPcrack.py <cpassword>
```

To create a cpassword from a password:

```sh
python3 GPPencrypt.py "example password"
```

### Test

From the repository root with the virtual environment active, run
`python3 GPPcrack/test_gpp.py`. The tests check first-run messages and an
encryption/decryption round trip.
