"""Linux integration checks that don't require a real GPU or Forge install."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "nightrun_2.3"
sys.path.insert(0, str(PACKAGE / "modules"))
import nightrun_runtime as runtime
spec = importlib.util.spec_from_file_location("setup_linux_port", PACKAGE / "modules" / "setup_pipeline.py")
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


@unittest.skipUnless(sys.platform.startswith("linux"), "Linux-specific")
class LinuxPortTests(unittest.TestCase):
    def test_forge_starts_in_venv_without_windows_cuda_options(self):
        with tempfile.TemporaryDirectory(prefix="forge with spaces ") as folder:
            repo = Path(folder)
            (repo / "launch.py").write_text("pass\n")
            executable = repo / "venv" / "bin" / "python"
            executable.parent.mkdir(parents=True)
            executable.symlink_to(sys.executable)
            proc = mock.Mock()
            proc.poll.return_value = None
            with mock.patch.object(runtime, "api_alive", side_effect=[False, True]):
                with mock.patch.object(runtime.subprocess, "Popen", return_value=proc) as launch:
                    with mock.patch.object(runtime.time, "sleep"):
                        runtime.ensure_forge(repo)
            argv, kw = launch.call_args
            self.assertEqual(argv[0][:3], [str(executable), str(repo / "launch.py"), "--api"])
            self.assertNotIn("--lowvram", argv[0])
            self.assertNotIn("--cuda-malloc", argv[0])
            self.assertNotIn("creationflags", kw)

    def test_forge_early_exit_has_diagnostic(self):
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            (repo / "launch.py").write_text("pass\n")
            executable = repo / "venv" / "bin" / "python"
            executable.parent.mkdir(parents=True)
            executable.symlink_to(sys.executable)
            proc = mock.Mock()
            proc.poll.return_value = 17
            with mock.patch.object(runtime, "api_alive", return_value=False):
                with mock.patch.object(runtime.subprocess, "Popen", return_value=proc):
                    with mock.patch.object(runtime.time, "sleep"):
                        with self.assertRaisesRegex(RuntimeError, "exited with code 17"):
                            runtime.ensure_forge(repo)

    def test_missing_venv_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            (repo / "launch.py").write_text("pass\n")
            with mock.patch.object(runtime, "api_alive", return_value=False):
                with mock.patch.object(runtime.subprocess, "Popen") as launch:
                    with self.assertRaisesRegex(RuntimeError, "Python venv missing"):
                        runtime.ensure_forge(repo)
                    launch.assert_not_called()

    def test_desktop_entry_handles_spaces_and_real_icon(self):
        with tempfile.TemporaryDirectory(prefix="nightrun desktop spaces ") as folder:
            root = Path(folder)
            script = root / "another folder" / "run.sh"
            script.parent.mkdir()
            script.write_text("#!/bin/bash\nexit 0\n")
            icon = PACKAGE / "assets" / "icons" / "nightrun.ico"
            with mock.patch.object(setup, "desktop_dir", return_value=root / "Desktop"):
                with mock.patch.dict(os.environ, {"XDG_CACHE_HOME": str(root / "cache")}):
                    answer = setup._create_linux_shortcut("Nightrun", script, icon, script.parent)
            self.assertTrue(answer["created"], answer)
            desktop = Path(answer["path"]).read_text()
            self.assertIn('Exec=/usr/bin/env bash "', desktop)
            self.assertIn('another folder/run.sh"', desktop)
            self.assertIn("Terminal=true", desktop)
            self.assertTrue(Path(answer["icon"]).exists())

    def test_xdg_desktop_env_expands_home(self):
        with mock.patch.dict(os.environ, {"XDG_DESKTOP_DIR": "$HOME/My Desktop"}):
            self.assertEqual(setup.desktop_dir(), Path.home() / "My Desktop")

    def test_shell_launchers_keep_paths_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix="nightrun launch with spaces ") as folder:
            forge = Path(folder)
            workflow = forge / "workflows" / "nightrun_2.3"
            workflow.mkdir(parents=True)
            for source in PACKAGE.glob("*.sh"):
                shutil.copy(source, workflow / source.name)
            (workflow / "config.json").write_text("{}")
            (workflow / "nightrun.py").write_text(
                'import json,sys,pathlib\npathlib.Path(sys.argv[-1]).write_text(json.dumps(sys.argv[1:-1]))\n'
            )
            args_file = forge / "args with spaces.json"
            env = dict(os.environ, NIGHTRUN_PYTHON=sys.executable, NIGHTRUN_FORGE_REPO=str(forge))
            for mode, script in [
                ("base", "run-nightrun-base-only.sh"),
                ("full", "run-nightrun-full-upscale.sh"),
                ("dry-run", "run-one-dry-test.sh"),
                ("validate", "run-validation-stress-test.sh")
            ]:
                run = subprocess.run(
                    ["bash", str(workflow / script), "--", str(args_file)],
                    capture_output=True, text=True, env=env, timeout=10,
                )
                self.assertEqual(run.returncode, 0, (script, run.stdout, run.stderr))
                self.assertEqual(json.loads(args_file.read_text())[:2], ["--mode", mode])
                self.assertIn(str(workflow / "config.json"), json.loads(args_file.read_text()))

    def test_second_runner_doesnt_clear_running_stop_signal(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("common.sh", "run-nightrun-base-only.sh"):
                shutil.copy(PACKAGE / name, root / name)
            (root / "config.json").write_text("{}")
            (root / "nightrun.py").write_text("pass\n")
            stop = root / "STOP_AFTER_CURRENT_IMAGE.txt"
            stop.touch()
            held = subprocess.Popen(
                ["bash", "-c", 'exec 9>"$1"; flock -x 9; sleep 3', "test", str(root / ".nightrun.lock")],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            try:
                import time
                time.sleep(0.2)
                env = dict(os.environ, NIGHTRUN_PYTHON=sys.executable)
                result = subprocess.run(
                    ["bash", str(root / "run-nightrun-base-only.sh")],
                    env=env, capture_output=True, text=True, timeout=5,
                )
                self.assertEqual(result.returncode, 3, result.stderr)
                self.assertTrue(stop.exists())
            finally:
                held.terminate()
                held.wait(timeout=4)


if __name__ == "__main__":
    unittest.main()
