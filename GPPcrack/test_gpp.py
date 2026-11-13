import importlib.util
import pathlib
import subprocess
import sys
import unittest


DIRECTORY = pathlib.Path(__file__).resolve().parent


def run_without_packages(script, *args):
    return subprocess.run(
        [sys.executable, "-S", str(DIRECTORY / script), *args],
        capture_output=True,
        text=True,
    )


class FirstRunTests(unittest.TestCase):
    def test_crack_shows_usage_without_dependencies(self):
        result = run_without_packages("GPPcrack.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_crack_explains_missing_dependency(self):
        result = run_without_packages("GPPcrack.py", "example")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("python3 -m pip install pycryptodomex", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


    def test_encrypt_shows_usage_without_dependencies(self):
        result = run_without_packages("GPPencrypt.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_encrypt_explains_missing_dependency(self):
        result = run_without_packages("GPPencrypt.py", "example")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("python3 -m pip install pycryptodomex", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


class CryptoTests(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("Cryptodome"), "pycryptodomex is not installed")
    def test_encrypt_decrypt_round_trip(self):
        password = "Example password"
        encrypted = subprocess.run(
            [sys.executable, str(DIRECTORY / "GPPencrypt.py"), password],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        decrypted = subprocess.run(
            [sys.executable, str(DIRECTORY / "GPPcrack.py"), encrypted],
            capture_output=True, text=True, check=True,
        ).stdout.rstrip("\n")
        self.assertEqual(decrypted, password)


if __name__ == "__main__":
    unittest.main()
