import os
import pathlib
import subprocess
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).resolve().parent / "ZIPcrack"


class DependencyTests(unittest.TestCase):
    def test_missing_7z_stops_without_installing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            for name, body in (("which", "exit 1"), ("apt", 'echo invoked > "$APT_MARKER"')):
                command = root / name
                command.write_text("#!/bin/bash\n" + body + "\n")
                command.chmod(0o755)
            marker = root / "apt-called"
            env = dict(os.environ, PATH=directory, APT_MARKER=str(marker))
            result = subprocess.run(
                ["/bin/bash", str(SCRIPT), "-f", "archive.zip", "-w", "words"],
                cwd=root, env=env, capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("7z", result.stderr.lower())
            self.assertFalse(marker.exists())
            self.assertNotIn("Password not found", result.stdout)


if __name__ == "__main__":
    unittest.main()
