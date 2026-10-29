import unittest
from types import SimpleNamespace

from auto_caption import group_words, make_srt, srt_time


class AutoCaptionTests(unittest.TestCase):
    def test_timestamp_rounding(self):
        self.assertEqual(srt_time(61.234), "00:01:01,234")

    def test_short_phrase_segmentation(self):
        words = [SimpleNamespace(start=i * .4, end=i * .4 + .3, word=w)
                 for i, w in enumerate("coming days we are going to face a lot of water problems".split())]
        groups = group_words(words, max_words=4)
        self.assertEqual(len(groups), 3)
        self.assertEqual(groups[0][2], "coming days we are")
        self.assertLessEqual(max(len(g[2].split()) for g in groups), 4)

    def test_pause_splits_caption(self):
        words = [SimpleNamespace(start=0, end=.3, word="hello"),
                 SimpleNamespace(start=1.4, end=1.9, word="world")]
        self.assertEqual(len(group_words(words)), 2)

    def test_invalid_words_skipped(self):
        words = [SimpleNamespace(start=1, end=1, word="oops"),
                 SimpleNamespace(start=1, end=2, word="తెలుగు")]
        self.assertEqual(group_words(words)[0][2], "తెలుగు")

    def test_srt(self):
        self.assertIn("00:00:01,000 --> 00:00:02,000", make_srt([(1, 2, "hello")]))


if __name__ == "__main__":
    unittest.main()
