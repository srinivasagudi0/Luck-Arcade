import random as rd

from cli_utils import prompt_nonempty, run_global_command
from stats import update_and_persist_stats

greet = """
Dice Roll game.
Pick a number between 1 and 6.
    """


def continuous_game_dice_roll():
    """Keep rolling until your guessed number shows up."""
    print(greet)
    print("Commands: help, stats, menu, quit")
    while True:
        user_prediction = prompt_nonempty(
            'Enter your prediction (1-6) or "quit" to exit: ',
            allow_quit=True,
            empty_message="Please enter a number between 1 and 6.",
        )
        if user_prediction is None:
            print("Dice game closed.")
            return

        signal = run_global_command(
            user_prediction,
            context="game",
            on_help=lambda: print("Type a number 1-6. Use menu to return."),
            on_stats=lambda: print("Stats: shown after a completed round."),
        )
        if signal == "quit":
            print("Dice game closed.")
            return
        if signal == "menu":
            print("Returning to main menu.")
            return
        if signal == "handled":
            continue
        try:
            up = int(user_prediction)
        except ValueError:
            print("That was not a number from 1 to 6.")
            continue
        if not 1 <= up <= 6:
            print("Use a number from 1 to 6.")
            continue

        attempts = 0
        while True:
            attempts += 1
            dice_roll = rd.randint(1, 6)
            print()
            print(f"You rolled a {dice_roll}.")
            if dice_roll == up:
                update_and_persist_stats("dice", "win")
                print("Nice, you guessed it.")
                print(f'It took {attempts} attempt{"s" if attempts != 1 else ""} to get it right.')
                print("Good run.")
                break
            else:
                print("Not yet. Rolling again...")

        print()
        return


def game_dice_roll():
    """One prediction, one roll, then done."""
    print(greet)
    print("Commands: help, stats, menu, quit")
    while True:
        user_prediction = prompt_nonempty(
            'Enter your prediction (1-6) or "quit" to exit: ',
            allow_quit=True,
            empty_message="Please enter a number between 1 and 6.",
        )
        if user_prediction is None:
            print("Dice game closed.")
            return

        signal = run_global_command(
            user_prediction,
            context="game",
            on_help=lambda: print("Type a number 1-6. Use menu to return."),
            on_stats=lambda: print("Stats: not tracked yet for single-roll mode."),
        )
        if signal == "quit":
            print("Dice game closed.")
            return
        if signal == "menu":
            print("Returning to main menu.")
            return
        if signal == "handled":
            continue
        try:
            up = int(user_prediction)
        except ValueError:
            print("That was not a number from 1 to 6.")
            continue
        if not 1 <= up <= 6:
            print("Use a number from 1 to 6.")
            continue

        dice_roll = rd.randint(1, 6)
        print()
        print(f"You rolled a {dice_roll}.")
        if dice_roll == up:
            update_and_persist_stats("dice", "win")
            print("Nice, you guessed it.")
        else:
            update_and_persist_stats("dice", "loss")
            print("No match this time.")
        print("Good run.")
        return

# dice_roll.py wokring on this also 