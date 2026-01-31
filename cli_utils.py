QUIT_COMMANDS = ("quit", "exit", "q")


def is_quit(text: str) -> bool:
    return text.strip().lower() in QUIT_COMMANDS


def _safe_input(prompt: str) -> str | None:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
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
            print("Please enter yes or no.")
            continue
        if allow_quit and is_quit(value):
            return None
        if value.lower().startswith("y"):
            return True
        if value.lower().startswith("n"):
            return False
        print("Please enter yes or no.")
