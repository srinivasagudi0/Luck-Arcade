import unittest

from coin_flip import _normalize_choice as normalize_coin_choice
from rock_paper_scissors import normalize_rps_choice, rps_round_result


class TestCoinFlip(unittest.TestCase):
    def test_normalize_choice(self):
        cases = {
            "h": "Heads",
            "Heads": "Heads",
            " heads ": "Heads",
            "t": "Tails",
            "Tails": "Tails",
            " tails ": "Tails",
            "x": None,
            "": None,
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(normalize_coin_choice(text), expected)


class TestRockPaperScissors(unittest.TestCase):
    def test_normalize_rps_choice(self):
        cases = {
            "r": "Rock",
            "rock": "Rock",
            "p": "Paper",
            "paper": "Paper",
            "s": "Scissors",
            "scissors": "Scissors",
            "x": None,
            "": None,
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(normalize_rps_choice(text), expected)

    def test_rps_round_result(self):
        self.assertEqual(rps_round_result("Rock", "Rock"), "tie")
        self.assertEqual(rps_round_result("Rock", "Scissors"), "win")
        self.assertEqual(rps_round_result("Rock", "Paper"), "loss")
        self.assertEqual(rps_round_result("Paper", "Rock"), "win")
        self.assertEqual(rps_round_result("Scissors", "Paper"), "win")

