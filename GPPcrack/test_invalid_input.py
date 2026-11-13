import pathlib
import subprocess
import sys
import unittest


SCRIPT = pathlib.Path(__file__).resolve().parent / "GPPcrack.py"


class InvalidInputTests(unittest.TestCase):
    def test_invalid_base64_is_reported_without_traceback(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "@@@"], capture_output=True, text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not valid Base64", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_invalid_ciphertext_length_is_reported_without_traceback(self):
        for value in ("", "AA"):
            with self.subTest(value=value):
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), value], capture_output=True, text=True
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("invalid ciphertext length", (result.stdout + result.stderr).lower())
                self.assertNotIn("Traceback", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
