### GPPcrack

![GitHub stars](https://img.shields.io/github/stars/d4t4s3c/RSAcrack?logoColor=yellow) ![GitHub forks](https://img.shields.io/github/forks/d4t4s3c/RSAcrack?logoColor=purple) ![GitHub watchers](https://img.shields.io/github/watchers/d4t4s3c/RSAcrack?logoColor=green)</br>
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/d4t4s3c/RSAcrack) ![GitHub contributors](https://img.shields.io/github/contributors/d4t4s3c/RSAcrack)

### Overview

Tool to decrypt passwords (**`cpassword`**) from [Group Policy Preferences (GPP)](https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/information-group-policy-preferences-events) taking advantage of [Microsoft](https://microsoft.com) release of the [AES key](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be).

![](/img/img.png)

### Download

```sh
wget --no-check-certificate -q "https:/" && chmod +x GPPcrack
```

### Usage

```cmd
python3 GPPcrack <cpassword>
```
