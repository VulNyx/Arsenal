# **RSAcrack**

### Overview

If you have a **private key (id_rsa)** protected by a **passphrase** and you want to obtain the **password**, `RSAcrack` will attempt to obtain the **public key** with the [ssh-keygen](https://manpages.ubuntu.com/manpages/noble/man1/ssh-keygen.1.html) binary, performing a **brute force** attack until a successful collision occurs.

![](/RSAcrack/img/screenshot.png)

### Download

```sh
wget --no-check-certificate -q "https://raw.githubusercontent.com/VulNyx/Arsenal/refs/heads/main/RSAcrack/RSAcrack" && chmod +x RSAcrack
```

### Download & Install (PATH)

```cmd
wget --no-check-certificate -q "https://raw.githubusercontent.com/VulNyx/Arsenal/refs/heads/main/RSAcrack/RSAcrack" -O /usr/bin/RSAcrack && chmod +x /usr/bin/RSAcrack
```

### Usage

```sh
RSAcrack -k <KEY> -w <WORDLIST>
```

> [!WARNING]
> The cracking speed can vary depending on which tool the key is generated with.

| Key Generated | Cracking Speed     |
|---------------|--------------------|
| OpenSSL       | :heavy_check_mark: |
| ssh-keygen    | :x:                |
| PuTTYgen      | :heavy_check_mark: |
| 8gwifi        | :heavy_check_mark: |
