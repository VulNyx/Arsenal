import os
import pathlib
import subprocess
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).resolve().parent / "NYXscan"


class ScanResultTests(unittest.TestCase):
    def run_scan(self, mode):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            for name, body in {
                "which": "exit 0",
                "timeout": "exit 1",
                "nmap": (
                    'echo "$*" >> "$NMAP_CALLS"\n'
                    'if [[ $NMAP_MODE == fail ]]; then exit 1; fi\n'
                    'if [[ $NMAP_MODE == deepfail && " $* " == *" -sVC "* ]]; then exit 1; fi\n'
                    'for last do :; done\n'
                    'if [[ $NMAP_MODE == closed ]]; then state=closed; else state=open; fi\n'
                    'printf "PORT STATE SERVICE\\n80/tcp %s http\\n81/tcp closed http\\n443/tcp %s https\\n" "$state" "$state" > "$last"'
                ),
            }.items():
                command = bin_dir / name
                command.write_text("#!/bin/bash\n" + body + "\n")
                command.chmod(0o755)
            calls = root / "calls"
            target = "nyxscan-results-" + root.name
            temporary_scan = pathlib.Path("/tmp") / f"{target}.tmp"
            self.addCleanup(temporary_scan.unlink, missing_ok=True)
            env = dict(os.environ, PATH=f"{bin_dir}:{os.defpath}", NMAP_MODE=mode, NMAP_CALLS=str(calls))
            result = subprocess.run(
                ["/bin/bash", str(SCRIPT), "-t", target],
                cwd=root, env=env, capture_output=True, text=True,
            )
            return result, calls.read_text().splitlines() if calls.exists() else []

    def test_initial_nmap_failure_stops_the_scan(self):
        result, calls = self.run_scan("fail")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("nmap", result.stderr.lower())
        self.assertIn("fail", result.stderr.lower())
        self.assertEqual(len(calls), 1)
        self.assertNotIn("Saved Log", result.stdout)

    def test_no_open_ports_skips_deep_scan(self):
        result, calls = self.run_scan("closed")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no open tcp ports", result.stdout.lower())
        self.assertEqual(len(calls), 1)
        self.assertNotIn("Saved Log", result.stdout)

    def test_deep_scan_failure_is_reported(self):
        result, calls = self.run_scan("deepfail")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("nmap", result.stderr.lower())
        self.assertIn("fail", result.stderr.lower())
        self.assertEqual(len(calls), 2)
        self.assertIn("-p80,443", calls[1])
        self.assertNotIn("Saved Log", result.stdout)


if __name__ == "__main__":
    unittest.main()
