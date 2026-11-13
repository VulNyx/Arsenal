import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).resolve().parent / "NYXscan"


class DependencyTests(unittest.TestCase):
    def test_missing_nmap_exits_without_attempting_install(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory)
            apt = path / "apt"
            apt.write_text('#!/bin/bash\necho attempted > "$APT_MARKER"\n')
            apt.chmod(0o755)
            marker = path / "apt-invoked"
            env = dict(os.environ, PATH=directory, APT_MARKER=str(marker))
            result = subprocess.run(
                ["/bin/bash", str(SCRIPT), "-t", "test.invalid"],
                cwd=directory, env=env, capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("nmap", result.stderr.lower())
            self.assertFalse(marker.exists(), "must not attempt package installation")
            self.assertNotIn("Saved Log", result.stdout)

    def test_missing_bat_exits_before_scanning_or_installing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory)
            for name, variable in (("apt", "APT_MARKER"), ("nmap", "NMAP_MARKER")):
                command = path / name
                command.write_text(f'#!/bin/bash\necho attempted > "${variable}"\n')
                command.chmod(0o755)
            apt_marker = path / "apt-invoked"
            nmap_marker = path / "nmap-invoked"
            env = dict(os.environ, PATH=directory, APT_MARKER=str(apt_marker), NMAP_MARKER=str(nmap_marker))
            result = subprocess.run(
                ["/bin/bash", str(SCRIPT), "-t", "test.invalid"],
                cwd=directory, env=env, capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("bat", result.stderr.lower())
            self.assertFalse(apt_marker.exists())
            self.assertFalse(nmap_marker.exists())

    def test_either_bat_command_can_display_results(self):
        for command_name in ("bat", "batcat"):
            with self.subTest(command=command_name), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                bin_dir = root / "bin"
                bin_dir.mkdir()
                for name in ("grep", "cut", "xargs", "tr", "echo"):
                    (bin_dir / name).symlink_to(shutil.which(name))
                timeout = bin_dir / "timeout"
                timeout.write_text("#!/bin/bash\nexit 1\n")
                timeout.chmod(0o755)
                nmap = bin_dir / "nmap"
                nmap.write_text('#!/bin/bash\nfor last do :; done\nprintf "PORT STATE SERVICE\\n80/tcp open http\\n" > "$last"\n')
                nmap.chmod(0o755)
                bat = bin_dir / command_name
                bat.write_text('#!/bin/bash\necho used > "$BAT_MARKER"\n/bin/cat\n')
                bat.chmod(0o755)
                marker = root / "bat-invoked"
                target = "nyxscan-test-" + root.name
                temporary_scan = pathlib.Path("/tmp") / f"{target}.tmp"
                self.addCleanup(temporary_scan.unlink, missing_ok=True)
                env = dict(os.environ, PATH=str(bin_dir), BAT_MARKER=str(marker))
                result = subprocess.run(
                    ["/bin/bash", str(SCRIPT), "-t", target],
                    cwd=root, env=env, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(marker.exists(), result.stderr)


if __name__ == "__main__":
    unittest.main()
