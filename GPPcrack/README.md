# GPPcrack

### Overview

Tool to decrypt passwords (**`cpassword`**) from [Group Policy Preferences (GPP)](https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/information-group-policy-preferences-events) taking advantage of [Microsoft](https://microsoft.com) release of the [AES key](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be).

### Download

```sh
wget --no-check-certificate -q "https://raw.githubusercontent.com/VulNyx/Arsenal/refs/heads/main/GPPcrack/GPPcrack.py" && chmod +x GPPcrack.py
```

### Usage

```cmd
python3 GPPcrack.py <cpassword>
```

Invalid Base64 or ciphertext lengths produce an error instead of a traceback.
To test these cases, run `python3 GPPcrack/test_invalid_input.py` from the
repository root with the tool's Python dependency installed.
