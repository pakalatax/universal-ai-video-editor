"""Offline smoke tests for original video-editing commands."""
import json
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

def cmd(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)

class EditorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="uve-test-")
        cls.directory = Path(cls.temp.name)
        cls.input = cls.directory / "input.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=320x240:rate=10", "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=44100", "-t", "1.2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-y", str(cls.input)], check=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_probe(self):
        r = cmd(HERE / "video_editor.py", "probe", "--input", self.input)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("streams", json.loads(r.stdout))

    def test_trim_and_no_overwrite(self):
        output = self.directory / "trim.mp4"
        command = (HERE / "video_editor.py", "trim", "--input", self.input, "--output", output, "--start", "0.1", "--duration", "0.6")
        r = cmd(*command)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(output.is_file())
        self.assertNotEqual(cmd(*command).returncode, 0)

    def test_advanced_dry_run(self):
        r = cmd(HERE / "advanced_editor.py", "speed", "--input", self.input, "--output", self.directory / "fast.mp4", "--factor", "1.2", "--dry-run")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(json.loads(r.stdout)["dry_run"])

    def test_thumbnail(self):
        path = self.directory / "thumb.jpg"
        r = cmd(HERE / "advanced_editor.py", "thumbnail", "--input", self.input, "--output", path, "--time", "0.5")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(path.is_file())

    def test_join(self):
        path = self.directory / "joined.mp4"
        r = cmd(HERE / "advanced_editor.py", "join", "--input", self.input, "--second", self.input, "--output", path)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(path.is_file())

    def test_invalid_speed(self):
        r = cmd(HERE / "advanced_editor.py", "speed", "--input", self.input, "--output", self.directory / "invalid.mp4", "--factor", "4")
        self.assertNotEqual(r.returncode, 0)

    def test_easy_plan(self):
        r = cmd(HERE / "easy_editor.py", "plan", "--input", self.input, "--output", self.directory / "planned.mp4", "--preset", "short")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["preset"], "short")

    def test_easy_render(self):
        output = self.directory / "simple.mp4"
        r = cmd(HERE / "easy_editor.py", "render", "--input", self.input, "--output", output, "--preset", "youtube", "--quality", "draft")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(output.is_file())

    def test_easy_refuses_existing_file(self):
        r = cmd(HERE / "easy_editor.py", "render", "--input", self.input, "--output", self.input)
        self.assertNotEqual(r.returncode, 0)

    def test_speech_keep_ranges(self):
        spec = importlib.util.spec_from_file_location("speech_editor", HERE / "speech_editor.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.keep_ranges(3.0, [(0.5, 1.7)], 0.8, 0.3), [(0.0, 0.65), (1.55, 3.0)])
        self.assertEqual(module.intervals("silence_start: 0.5\nsilence_end: 1.7 | silence_duration: 1.2", 3.0), [(0.5, 1.7)])

    def test_speech_dry_run(self):
        r = cmd(HERE / "speech_editor.py", "render", "--input", self.input, "--output", self.directory / "speech.mp4")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('"dry_run": true', r.stdout)

    def test_provider_adapters_no_network(self):
        spec = importlib.util.spec_from_file_location("provider_gateway", HERE / "provider_gateway.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        previous = {key: os.environ.get(key) for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY")}
        try:
            for key in previous:
                os.environ[key] = "test-placeholder-not-real"
            for provider in ("openai", "anthropic", "gemini", "ollama"):
                url, headers, payload = module.request_for(provider, "test-model", "Hello")
                self.assertIn("model", url if provider == "gemini" else str(payload))
                self.assertTrue(headers["Content-Type"] == "application/json")
            self.assertEqual(module.parse_response("ollama", {"message": {"content": "ok"}}), "ok")
        finally:
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

if __name__ == "__main__":
    unittest.main()
