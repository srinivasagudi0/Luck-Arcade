import random as rd

from cli_utils import prompt_nonempty

greet = """
Dice Roll game.
Pick a number between 1 and 6.
    """


def continuous_game_dice_roll():
    """Keep rolling until your guessed number shows up."""
    print(greet)
    while True:
        user_prediction = prompt_nonempty(
            'Enter your prediction (1-6) or "quit" to exit: ',
            allow_quit=True,
            empty_message="Please enter a number between 1 and 6.",
        )
        if user_prediction is None:
            print("Dice game closed.")
            return
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
    while True:
        user_prediction = prompt_nonempty(
            'Enter your prediction (1-6) or "quit" to exit: ',
            allow_quit=True,
            empty_message="Please enter a number between 1 and 6.",
        )
        if user_prediction is None:
            print("Dice game closed.")
            return
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
            print("Nice, you guessed it.")
        else:
            print("No match this time.")
        print("Good run.")
        return

# dice_roll.py
