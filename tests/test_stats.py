import tempfile
import unittest
from pathlib import Path

from stats import default_stats, format_stats_summary, load_stats, update_and_persist_stats


class TestStats(unittest.TestCase):
    def test_load_stats_returns_defaults_when_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "stats.json"
            self.assertEqual(load_stats(str(path)), default_stats())

    def test_update_and_persist_stats(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "stats.json"
            update_and_persist_stats("coin", "win", storage_path=str(path))
            update_and_persist_stats("coin", "loss", storage_path=str(path))
            data = load_stats(str(path))
            self.assertEqual(data["stats_total"], 2)
            self.assertEqual(data["stats_coin_win"], 1)
            self.assertEqual(data["stats_coin_loss"], 1)

    def test_format_stats_summary(self):
        data = default_stats()
        data["stats_total"] = 3
        data["stats_dice_win"] = 2
        summary = format_stats_summary(data)
        self.assertIn("Total plays: 3", summary)
        self.assertIn("dice: 2W/0L", summary)
