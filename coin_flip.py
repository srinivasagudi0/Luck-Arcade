import random as rd

from cli_utils import prompt_nonempty, prompt_yes_no, run_global_command
from stats import update_and_persist_stats


def _normalize_choice(text: str) -> str | None:
    if not text:
        return None
    first = text.strip()[0].lower()
    if first == "h":
        return "Heads"
    if first == "t":
        return "Tails"
    return None


def continuous_game_coin_flip():
    """Coin flip loop with simple session tracking."""
    attempts = 0
    streak = 0

    print("Coin Flip time.")
    print()
    print("Call it: Heads or Tails.")
    print("Commands: help, stats, menu, quit")

    while True:
        user_input = prompt_nonempty(
            'Enter your prediction (Heads/Tails) or "quit" to exit: ',
            allow_quit=True,
            empty_message="Please enter Heads or Tails.",
        )
        if user_input is None:
            print("Leaving coin flip. See you later.")
            return

        signal = run_global_command(
            user_input,
            context="game",
            on_help=lambda: print("Type heads/tails (or h/t). Use menu to return."),
            on_stats=lambda: print(f"Attempts: {attempts} | Streak: {streak}"),
        )
        if signal == "quit":
            print("Leaving coin flip. See you later.")
            return
        if signal == "menu":
            print("Returning to main menu.")
            return
        if signal == "handled":
            continue

        user_choice = _normalize_choice(user_input)
        if user_choice is None:
            print("Hmm, that was not heads or tails.")
            continue

        attempts += 1
        coin_result = rd.choice(["Heads", "Tails"])
        print()
        print("Coin says:", coin_result)

        if coin_result == user_choice:
            streak += 1
            update_and_persist_stats("coin", "win")
            print("Nice call, you got it.")
        else:
            streak = 0
            update_and_persist_stats("coin", "loss")
            print("Nope, not this one.")

        print(f"Attempts this session: {attempts}")
        print(f"Current winning streak: {streak}")

        again = prompt_yes_no("Flip again? (y/n): ", allow_quit=True)
        if again is True:
            print()
            continue
        print("Done with coin flip for now.")
        return


# coin_flip.py
