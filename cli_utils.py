from __future__ import annotations

QUIT_COMMANDS = ("quit", "exit", "q", "stop", "end")
HELP_COMMANDS = ("help", "h", "?", "info", "instructions")
MENU_COMMANDS = ("menu", "m", "main menu", "home", "back")
STATS_COMMANDS = ("stats", "stat", "score", "scores")


def is_quit(text: str) -> bool:
    return text.strip().lower() in QUIT_COMMANDS


def _safe_input(prompt: str) -> str | None:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def handle_global_command(text: str, context: str) -> str | None:
    value = text.strip().lower()
    if not value:
        return None
    if value in QUIT_COMMANDS:
        return "quit"
    if value in HELP_COMMANDS:
        return "help"
    if value in STATS_COMMANDS:
        return "stats"
    if value in MENU_COMMANDS and context != "main_menu":
        return "menu"
    return None


def run_global_command(
    text: str,
    *,
    context: str,
    on_help=None,
    on_stats=None,
) -> str | None:
    cmd = handle_global_command(text, context)
    if cmd == "quit":
        return "quit"
    if cmd == "menu":
        return "menu"
    if cmd == "help":
        if on_help:
            on_help()
        else:
            print("Commands: help, stats, menu, quit")
        return "handled"
    if cmd == "stats":
        if on_stats:
            on_stats()
        else:
            print("Stats are not available on this screen yet.")
        return "handled"
    return None


def prompt_nonempty(
    prompt: str,
    *,
    allow_quit: bool = False,
    empty_message: str = "Please enter a value.",
) -> str | None:
    while True:
        raw = _safe_input(prompt)
        if raw is None:
            return None
        value = raw.strip()
        if not value:
            print(empty_message)
            continue
        if allow_quit and is_quit(value):
            return None
        return value


def prompt_yes_no(prompt: str, *, allow_quit: bool = False) -> bool | None:
    while True:
        raw = _safe_input(prompt)
        if raw is None:
            return None
        value = raw.strip()
        if not value:
            print("Please type yes or no.")
            continue
        if allow_quit and is_quit(value):
            return None
        if value.lower().startswith("y"):
            return True
        if value.lower().startswith("n"):
            return False
        print("Please type yes or no.")
