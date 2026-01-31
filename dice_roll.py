import random as rd

from cli_utils import prompt_nonempty

greet = """
Welcome to the Dice Roll Game!
Here, you can test your luck by predicting the outcome of a dice roll.
Predict a number between 1 and 6 (inclusive).
    """


def continuous_game_dice_roll():
    """Keep rolling the die until the user's prediction appears.

    User can type 'quit', 'exit', or 'q' before starting to cancel the game.
    """
    print(greet)
    while True:
        user_prediction = prompt_nonempty(
            'Enter your prediction (1-6) or "quit" to exit: ',
            allow_quit=True,
            empty_message="Please enter a number between 1 and 6.",
        )
        if user_prediction is None:
            print('Thank you for playing the Dice Roll Game!')
            return
        try:
            up = int(user_prediction)
        except ValueError:
            print('Invalid input. Please enter a number between 1 and 6.')
            continue
        if not 1 <= up <= 6:
            print('Please enter a number between 1 and 6.')
            continue

        attempts = 0
        # Roll until the user's prediction matches
        while True:
            attempts += 1
            dice_roll = rd.randint(1, 6)
            print()
            print(f"You rolled a {dice_roll}.")
            if dice_roll == up:
                print("Congratulations! You guessed it right! :)")
                print(f'It took {attempts} attempt{"s" if attempts != 1 else ""} to get it right.')
                print('Thank you for playing the Dice Roll Game!')
                break
            else:
                print("Sorry, you guessed it wrong. Continuing until you get it...")

        print()
        # Return to caller after a successful run
        return


def game_dice_roll():
    """Hardcore version: one prediction, one roll, then done.

    User can type 'quit', 'exit', or 'q' to cancel before the single roll.
    """
    print(greet)
    while True:
        user_prediction = prompt_nonempty(
            'Enter your prediction (1-6) or "quit" to exit: ',
            allow_quit=True,
            empty_message="Please enter a number between 1 and 6.",
        )
        if user_prediction is None:
            print('Thank you for playing the Dice Roll Game!')
            return
        try:
            up = int(user_prediction)
        except ValueError:
            print('Invalid input. Please enter a number between 1 and 6.')
            continue
        if not 1 <= up <= 6:
            print('Please enter a number between 1 and 6.')
            continue

        # Hardcore: a single roll only
        dice_roll = rd.randint(1, 6)
        print()
        print(f"You rolled a {dice_roll}.")
        if dice_roll == up:
            print("Congratulations! You guessed it right! :)")
        else:
            print("Sorry, you guessed it wrong. :(")
        print('Thank you for playing the Dice Roll Game!')
        return

# End of dice_roll.py
