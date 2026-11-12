"""Linux Native packaging, XDG installation and actual dry-run checks."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "linux-native/build.py"


class NativePackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="nightrun-linux-native-tests-")
        cls.output = Path(cls.temp.name) / "output"
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--output", str(cls.output)],
            capture_output=True, text=True, timeout=90,
        )
        if result.returncode:
            raise RuntimeError(result.stdout + "\n" + result.stderr)
        cls.package = cls.output / "nightrun-linux"

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def native_env(self, home):
        return {
            **os.environ,
            "HOME": str(home),
            "XDG_DATA_HOME": str(home / "data with spaces"),
            "XDG_CONFIG_HOME": str(home / "config with spaces"),
            "XDG_STATE_HOME": str(home / "state with spaces"),
            "NIGHTRUN_PYTHON": sys.executable,
        }

    def test_package_is_linux_only(self):
        files = [f for f in self.package.rglob("*") if f.is_file()]
        self.assertGreater(len(files), 55)
        self.assertFalse([f for f in files if f.suffix.lower() in (".bat", ".ico", ".exe")])
        for name in ("nightrun", "install.sh", "uninstall.sh", "modules/nightrun_runtime.py",
                     "pools/genre.txt", "assets/icons/nightrun.png"):
            self.assertTrue((self.package / name).exists(), name)
        for script in ("nightrun", "install.sh", "uninstall.sh"):
            p = subprocess.run(["bash", "-n", str(self.package / script)], capture_output=True)
            self.assertEqual(p.returncode, 0, (script, p.stderr.decode()))

    def test_archives_are_valid_and_match_hashes(self):
        recorded = {}
        for line in (self.output / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ")
            recorded[name] = digest
        self.assertEqual(set(recorded), {"nightrun-linux-native.zip", "nightrun-linux-native.tar.gz"})
        for name, digest in recorded.items():
            self.assertEqual(hashlib.sha256((self.output / name).read_bytes()).hexdigest(), digest)
        with zipfile.ZipFile(self.output / "nightrun-linux-native.zip") as archive:
            self.assertIsNone(archive.testzip())
            self.assertIn("nightrun-linux/nightrun.py", archive.namelist())

    def test_cli_setup_keeps_config_in_xdg_and_dry_run_works(self):
        with tempfile.TemporaryDirectory(prefix="native cli paths ") as folder:
            home = Path(folder) / "my home"
            home.mkdir()
            forge = Path(folder) / "Forge with spaces"
            (forge / "models/Stable-diffusion").mkdir(parents=True)
            (forge / "launch.py").write_text("# fake Forge for offline tests\n")
            (forge / "models/Stable-diffusion/demo.safetensors").write_bytes(b"")
            env = self.native_env(home)
            result = subprocess.run([
                "bash", str(self.package / "nightrun"), "setup",
                "--repo", str(forge), "--non-interactive", "--checkpoint", "demo.safetensors"
            ], env=env, capture_output=True, text=True, timeout=40)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            config = Path(env["XDG_CONFIG_HOME"]) / "nightrun-linux/config.local.json"
            self.assertTrue(config.exists())
            saved = json.loads(config.read_text())
            self.assertEqual(saved["paths"]["repo"], str(forge.resolve()))
            self.assertFalse((self.package / "config.local.json").exists())
            self.assertTrue((Path(env["XDG_STATE_HOME"]) / "nightrun-linux/setup_report.json").exists())

            run = subprocess.run(
                ["bash", str(self.package / "nightrun"), "dry-run", "--count", "1"],
                env=env, capture_output=True, text=True, timeout=40,
            )
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            summaries = list((forge / "test-renders").glob("nightrun-*/summary.json"))
            self.assertEqual(len(summaries), 1)
            result = json.loads(summaries[0].read_text())
            self.assertEqual(result["status"], "OK")
            self.assertEqual(result["count_attempted"], 1)
            self.assertEqual(result["count_completed"], 1)
            stop = subprocess.run(
                ["bash", str(self.package / "nightrun"), "stop"],
                env=env, capture_output=True, text=True,
            )
            self.assertEqual(stop.returncode, 0)
            self.assertTrue((Path(env["XDG_STATE_HOME"]) / "nightrun-linux/STOP_AFTER_CURRENT_IMAGE.txt").exists())

    def test_user_install_symlink_and_desktop_entries_work_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix="native install ") as folder:
            home = Path(folder) / "user name"
            home.mkdir()
            env = self.native_env(home)
            run = subprocess.run(
                ["bash", str(self.package / "install.sh"), "--no-deps"],
                env=env, capture_output=True, text=True, timeout=40,
            )
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            link = home / ".local/bin/nightrun-linux"
            self.assertTrue(link.is_symlink())
            result = subprocess.run([str(link), "help"], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Nightrun Linux Native", result.stdout)
            menu = Path(env["XDG_DATA_HOME"]) / "applications/io.bluenochian.Nightrun.desktop"
            self.assertTrue(menu.exists())
            text = menu.read_text()
            self.assertIn('Exec="', text)
            self.assertIn("user name", text)
            self.assertIn("data with spaces", os.readlink(link))
            self.assertIn("Terminal=true", text)
            self.assertIn("Icon=io.bluenochian.nightrun", text)
            icon = Path(env["XDG_DATA_HOME"]) / "icons/hicolor/256x256/apps/io.bluenochian.nightrun.png"
            self.assertTrue(icon.exists())
            config_dir = Path(env["XDG_CONFIG_HOME"]) / "nightrun-linux"
            config_dir.mkdir(parents=True)
            (config_dir / "config.local.json").write_text('{"original":true}')
            again = subprocess.run(
                ["bash", str(self.package / "install.sh"), "--no-deps"],
                env=env, capture_output=True, text=True, timeout=40,
            )
            self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
            self.assertEqual((config_dir / "config.local.json").read_text(), '{"original":true}')
            gone = subprocess.run(
                ["bash", str(self.package / "uninstall.sh")],
                env=env, capture_output=True, text=True, timeout=40,
            )
            self.assertEqual(gone.returncode, 0, gone.stdout + gone.stderr)
            self.assertFalse(link.exists())
            self.assertTrue((config_dir / "config.local.json").exists())

    def test_second_launch_cannot_clear_existing_stop_signal(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder) / "home"
            home.mkdir()
            env = self.native_env(home)
            config = Path(env["XDG_CONFIG_HOME"]) / "nightrun-linux/config.local.json"
            config.parent.mkdir(parents=True)
            config.write_text("{}")
            state = Path(env["XDG_STATE_HOME"]) / "nightrun-linux"
            state.mkdir(parents=True)
            stop = state / "STOP_AFTER_CURRENT_IMAGE.txt"
            stop.touch()
            lock = state / "batch.lock"
            owner = subprocess.Popen(
                ["bash", "-c", 'exec 9>"$1"; flock -x 9; sleep 3', "test", str(lock)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            try:
                time.sleep(0.25)
                another = subprocess.run(
                    ["bash", str(self.package / "nightrun"), "base"],
                    env=env, capture_output=True, text=True, timeout=4,
                )
                self.assertEqual(another.returncode, 3, another.stderr)
                self.assertTrue(stop.exists())
            finally:
                owner.terminate()
                owner.wait(timeout=4)


if __name__ == "__main__":
    unittest.main()
