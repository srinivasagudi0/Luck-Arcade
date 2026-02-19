import random as rd

from cli_utils import prompt_nonempty, prompt_yes_no, run_global_command
from stats import update_and_persist_stats


def game_number_guess():
    print("Number Guess.")
    print("Guess a number from 1 to 10.")
    print("Commands: help, stats, menu, quit")

    while True:
        target = rd.randint(1, 10)
        tries = 0
        won = False

        while tries < 3:
            raw = prompt_nonempty(
                'Your guess (1-10) or "quit": ',
                allow_quit=True,
                empty_message="Please enter a number.",
            )
            if raw is None:
                print("Leaving Number Guess.")
                return

            signal = run_global_command(
                raw,
                context="game",
                on_help=lambda: print("You get 3 tries. I’ll tell you higher/lower."),
                on_stats=lambda: print("Stats are saved across runs."),
            )
            if signal == "quit":
                print("Leaving Number Guess.")
                return
            if signal == "menu":
                print("Returning to main menu.")
                return
            if signal == "handled":
                continue

            try:
                guess = int(raw)
            except ValueError:
                print("That is not a valid number.")
                continue

            if not 1 <= guess <= 10:
                print("Use a number from 1 to 10.")
                continue

            tries += 1

            if guess == target:
                print(f"Correct. You got it in {tries} try{'ies' if tries > 1 else ''}.")
                update_and_persist_stats("guess", "win")
                won = True
                break

            hint = "higher" if target > guess else "lower"
            left = 3 - tries
            print(f"Not quite. Try {hint}. Attempts left: {left}")

        if not won:
            print(f"Out of tries. The number was {target}.")
            update_and_persist_stats("guess", "loss")

        again = prompt_yes_no("Play Number Guess again? (y/n): ", allow_quit=True)
        if again is True:
            print()
            continue

        print("Done with Number Guess.")
        return

