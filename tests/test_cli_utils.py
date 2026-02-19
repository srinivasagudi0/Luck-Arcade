import unittest
from unittest.mock import patch

from cli_utils import handle_global_command, is_quit, prompt_nonempty, prompt_yes_no, run_global_command


class TestIsQuit(unittest.TestCase):
    def test_is_quit_true(self):
        for text in ("q", "quit", "exit", " Q ", "Quit", "EXIT"):  # mixed casing/spaces
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


class TestGlobalCommands(unittest.TestCase):
    def test_handle_global_command(self):
        samples = {
            "quit": "quit",
            "Q": "quit",
            "help": "help",
            "?": "help",
            "stats": "stats",
            "scores": "stats",
            "menu": "menu",
            "back": "menu",
            "abc": None,
            "": None,
        }
        for text, expected in samples.items():
            with self.subTest(text=text):
                self.assertEqual(handle_global_command(text, "game"), expected)

    def test_handle_global_command_suppresses_menu_inside_main_menu(self):
        self.assertIsNone(handle_global_command("menu", "main_menu"))

    def test_run_global_command(self):
        self.assertEqual(run_global_command("quit", context="game"), "quit")
        self.assertEqual(run_global_command("menu", context="game"), "menu")
        self.assertEqual(run_global_command("x", context="game"), None)

    def test_run_global_command_help_and_stats(self):
        seen = []
        self.assertEqual(
            run_global_command("help", context="game", on_help=lambda: seen.append("help")),
            "handled",
        )
        self.assertEqual(
            run_global_command("stats", context="game", on_stats=lambda: seen.append("stats")),
            "handled",
        )
        self.assertEqual(seen, ["help", "stats"])
