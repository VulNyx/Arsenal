# **RSAcrack**

#### Get the `passphrase` of a private key (`id_rsa`).

![](/RSAcrack/img/screenshot.png)

---

## Download

```sh
wget --no-check-certificate -q "https://raw.githubusercontent.com/VulNyx/Arsenal/refs/heads/main/RSAcrack/RSAcrack" && chmod +x RSAcrack
```

## Download & Install (PATH)

```cmd
wget --no-check-certificate -q "https://raw.githubusercontent.com/VulNyx/Arsenal/refs/heads/main/RSAcrack/RSAcrack" -O /usr/bin/RSAcrack && chmod +x /usr/bin/RSAcrack
```

## Usage

```sh
RSAcrack -k <KEY> -w <WORDLIST>
```

---

> [!WARNING]
> The cracking speed can vary depending on which tool the key is generated with.

| Key Generated | Cracking Speed     |
|---------------|--------------------|
| OpenSSL       | :heavy_check_mark: |
| ssh-keygen    | :x:                |
| PuTTYgen      | :heavy_check_mark: |
| 8gwifi        | :heavy_check_mark: |

---
