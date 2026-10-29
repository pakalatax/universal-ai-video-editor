"""Offline smoke tests for original video-editing commands."""
import json
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

if __name__ == "__main__":
    unittest.main()
