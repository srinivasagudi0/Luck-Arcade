import unittest
from unittest.mock import patch

from cli_utils import is_quit, prompt_nonempty, prompt_yes_no


class TestIsQuit(unittest.TestCase):
    def test_is_quit_true(self):
        for text in ("q", "quit", "exit", " Q ", "Quit", "EXIT"):
            with self.subTest(text=text):
                self.assertTrue(is_quit(text))

    def test_is_quit_false(self):
        for text in ("", "qq", "quitt", "no", "yes"):
            with self.subTest(text=text):
                self.assertFalse(is_quit(text))


class TestPromptHelpers(unittest.TestCase):
    def test_prompt_nonempty_returns_value(self):
        with patch("builtins.print"), patch("builtins.input", side_effect=["", "  hello  "]):
            value = prompt_nonempty("Prompt: ")
        self.assertEqual(value, "hello")

    def test_prompt_nonempty_allow_quit(self):
        with patch("builtins.input", side_effect=["quit"]):
            value = prompt_nonempty("Prompt: ", allow_quit=True)
        self.assertIsNone(value)

    def test_prompt_nonempty_eof_returns_none(self):
        with patch("builtins.input", side_effect=EOFError):
            value = prompt_nonempty("Prompt: ")
        self.assertIsNone(value)

    def test_prompt_yes_no_yes(self):
        with patch("builtins.print"), patch("builtins.input", side_effect=["", "y"]):
            value = prompt_yes_no("Prompt: ")
        self.assertTrue(value)

    def test_prompt_yes_no_no(self):
        with patch("builtins.input", side_effect=["no"]):
            value = prompt_yes_no("Prompt: ")
        self.assertFalse(value)

    def test_prompt_yes_no_allow_quit(self):
        with patch("builtins.input", side_effect=["q"]):
            value = prompt_yes_no("Prompt: ", allow_quit=True)
        self.assertIsNone(value)
