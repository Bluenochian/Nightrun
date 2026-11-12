"""A few offline checks for things that actually broke in 2.0.

These tests don't need Forge, a GPU, or any of the user's images.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import requests

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT if (ROOT / "modules").is_dir() else ROOT / "nightrun_2.3"
sys.path.insert(0, str(PACKAGE / "modules"))

import nightrun_runtime as run


class Nightrun22Tests(unittest.TestCase):
    def setUp(self):
        run.RUN_LOG = None

    def tearDown(self):
        run.RUN_LOG = None

    def test_health_endpoint_rejects_http_errors(self):
        response = mock.Mock()
        response.raise_for_status.side_effect = requests.HTTPError("503")
        with mock.patch.object(run.requests, "get", return_value=response):
            self.assertFalse(run.api_alive())

        response.raise_for_status.side_effect = None
        with mock.patch.object(run.requests, "get", return_value=response):
            self.assertTrue(run.api_alive())

    def test_bad_api_request_does_not_restart_forge(self):
        response = mock.Mock(content=b"bad request")
        response.raise_for_status.side_effect = requests.HTTPError(
            "400 Bad Request", response=mock.Mock(status_code=400)
        )
        with mock.patch.object(run.requests, "post", return_value=response):
            with mock.patch.object(run, "ensure_forge") as restart:
                with self.assertRaisesRegex(RuntimeError, "Forge rejected"):
                    run.post_api("/sdapi/v1/txt2img", {}, timeout=5, repo=Path("."), retries=2)
                restart.assert_not_called()

    def test_corrupt_pattern_is_no_longer_one_giant_word(self):
        self.assertIsNotNone(run.BLOCKED_POSITIVE_PATTERN.search("fart"))
        self.assertIsNotNone(run.BLOCKED_POSITIVE_PATTERN.search("shit"))
        self.assertIsNone(run.BLOCKED_POSITIVE_PATTERN.search("drumstick"))

    def test_ambiguous_lora_names_are_not_guessed(self):
        index = {"darkknightv1": "DarkKnight_v1", "darkknightv2": "DarkKnight_v2"}
        settings = {"lora_scan": {"skip_missing_when_folder_found": True}}
        self.assertIsNone(run.resolve_lora_name("darkknight", True, index, settings))
        self.assertIsNone(run.resolve_lora_name("dk", True, index, settings))
        self.assertEqual(run.resolve_lora_name("darkknightv1", True, index, settings), "DarkKnight_v1")

    def test_cooling_honors_stop_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            stop = Path(tmp) / "STOP_AFTER_CURRENT_IMAGE.txt"
            stop.write_text("stop")
            with mock.patch.object(run, "get_gpu_temp", return_value=90):
                with mock.patch.object(run.time, "sleep") as sleeper:
                    self.assertFalse(run.wait_for_temperature(
                        {"temperature": {"pause_above_c": 70, "resume_below_c": 55}}, stop
                    ))
                    sleeper.assert_not_called()

    def test_pillow_missing_does_not_install_anything(self):
        data = b"test bytes"
        with mock.patch.object(run, "Image", None):
            self.assertEqual(run._stamp_png_metadata(data), data)

    def test_zero_and_negative_counts_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(run, "resolve_config_path", return_value=Path(tmp) / "config.json"):
                with mock.patch.object(run, "load_json", return_value={"count": 2}):
                    with mock.patch.object(run, "resolve_repo", return_value=Path(tmp)):
                        for invalid in ("0", "-2"):
                            with self.subTest(invalid=invalid):
                                with mock.patch.object(sys, "argv", ["nightrun.py", "--count", invalid]):
                                    with self.assertRaises(SystemExit) as err:
                                        run.main()
                                    self.assertEqual(err.exception.code, 2)

    def test_failed_generation_is_not_reported_as_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "renders"
            output.mkdir()
            config = {
                "count": 1, "checkpoint": "dummy", "run_folder_prefix": "nightrun",
                "base": {"width": 512, "height": 512, "steps": 20, "steps_min": 20, "steps_max": 20},
                "upscale": {"enabled": False, "width": 1024, "height": 1024},
                "long_run_chill": {"enabled": False},
                "empty_run_cleanup": {"enabled": False},
                "sleep_between_images_seconds": 0,
            }
            stub = lambda *a, **k: None
            with mock.patch.object(sys, "argv", ["nightrun.py", "--mode", "base", "--count", "1"]):
                with mock.patch.object(run, "resolve_config_path", return_value=root / "config.json"):
                    with mock.patch.object(run, "load_json", return_value=config):
                        with mock.patch.object(run, "resolve_repo", return_value=root):
                            with mock.patch.object(run, "resolve_output_root", return_value=output):
                                with mock.patch.object(run, "cleanup_empty_run_folders", return_value=[]):
                                    with mock.patch.object(run, "ensure_forge", side_effect=stub):
                                        with mock.patch.object(run, "set_options", side_effect=stub):
                                            with mock.patch.object(run, "compose_prompt", return_value=(
                                                "test prompt", "negative", {}, [], []
                                            )):
                                                with mock.patch.object(run, "get_gpu_stats", return_value={}):
                                                    with mock.patch.object(run, "generate_base", side_effect=RuntimeError("fake GPU failure")):
                                                        with mock.patch.object(run, "make_contact_sheet", side_effect=stub):
                                                            run.main()
            summaries = list(output.glob("nightrun-*/summary.json"))
            self.assertEqual(len(summaries), 1)
            result = json.loads(summaries[0].read_text())
            self.assertEqual(result["status"], "FAILED")
            self.assertEqual(result["count_completed"], 0)
            self.assertEqual(result["count_failed"], 1)
            self.assertEqual(result["count_attempted"], 1)


if __name__ == "__main__":
    unittest.main()
