from dice_roll import continuous_game_dice_roll as dr
from coin_flip import continuous_game_coin_flip as cf
from rock_paper_scissors import game_rock_paper_scissors as rps
from cli_utils import prompt_nonempty, prompt_yes_no



def greeting_message():
    print('Thanks for using Luck Arcade!')
    greeting = (
        "Welcome to Luck Arcade!\n"
        "Here, you can try your luck with various games and win exciting prizes.\n"
        "Choose a game to get started, and may the odds be in your favor!\n"
    )

    menu = (
        "Please select a game:\n"
        "  1. Dice Roll (Nightmare)\n"
        "  2. Coin Flip (Medium)\n"
        "  3. Rock Paper Scissors (Hard)"
    )



    print(greeting)
    print(menu)


def instructions(choice):
    if choice == 1:
        print('You predict a dice roll. Roll a die and try to match your number!')
    elif choice == 2:
        print('You predict a coin flip. Flip a coin and try to match the side!')
    elif choice == 3:
        print('You predict Rock, Paper, or Scissors. Play against the computer and try to win!')
    else:
        print('Invalid choice. Please select a valid game number.')


def run_cli():
    greeting_message()
    while True:
        selection = prompt_nonempty(
            '\nEnter a game number (1-3) or "quit"/"exit"/"q" to exit: ',
            allow_quit=True,
            empty_message="Please enter a choice.",
        )
        if selection is None:
            print("Goodbye!")
            return
        if selection.lower() in ('help', 'h', '?'):
            help = """
            To play a game, enter the corresponding number (1-3).
            To exit the program at any time, type 'quit', 'exit', or 'q'.
            Enjoy your time at Luck Arcade!
            """
            print(help)
            continue

        try:
            choice = int(selection)
        except ValueError:
            print('Invalid input. Enter a number between 1 and 3, or "quit" to exit.')
            continue
        if choice not in (1, 2, 3):
            print('Please select a valid game number (1-3).')
            continue

        instructions(choice)
        if choice == 1:
            dr()
        elif choice == 2:
            cf()
        elif choice == 3:
            rps()

        again = prompt_yes_no('\nReturn to main menu? (y/n): ', allow_quit=True)
        if again is True:
            continue
        print('Thanks for playing! Goodbye.')
        return


if __name__ == '__main__':
    run_cli()

#end of main.py
# Did most of the updates in main.py to integate the games together.
