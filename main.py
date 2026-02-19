from dice_roll import continuous_game_dice_roll as dr
from coin_flip import continuous_game_coin_flip as cf
from rock_paper_scissors import game_rock_paper_scissors as rps
from cli_utils import prompt_nonempty, prompt_yes_no, run_global_command
from stats import format_stats_summary, load_stats
from number_guess import game_number_guess as ng

def run_cli():
    print("Welcome to Luck Arcade!")
    print("Nothing fancy here, just quick luck-based games.")

    while True:
        print("\nPick a game:")
        print("  1. Dice Roll (Nightmare)")
        print("  2. Coin Flip (Medium)")
        print("  3. Rock Paper Scissors (Hard)")
        print("  4. Number Guess (Medium)")

        raw = prompt_nonempty(
            '\nEnter a game number (1-4) or "quit"/"exit"/"q" to exit: ',
            allow_quit=True,
            empty_message="Please enter a choice.",
        )
        if raw is None:
            print("Goodbye!")
            return

        signal = run_global_command(
            raw,
            context="main_menu",
            on_help=lambda: (
                print("\nType 1, 2, 3, or 4 to play."),
                print("Commands: help, stats, quit."),
            ),
            on_stats=lambda: print(f"\n{format_stats_summary(load_stats())}"),
        )
        if signal == "quit":
            print("Goodbye!")
            return
        if signal == "handled":
            continue

        try:
            choice = int(raw)
        except ValueError:
            print("That is not a number. Try again with 1, 2, 3, or 4.")
            continue

        if choice == 1:
            print("\nDice Roll: guess a number and keep rolling until it matches.")
            dr()
        elif choice == 2:
            print("\nCoin Flip: call heads or tails and test your luck.")
            cf()
        elif choice == 3:
            print("\nRock Paper Scissors: beat the computer in a best-of-3.")
            rps()
        elif choice == 4:
            print("\nNumber Guess: guess a number from 1 to 10 in 3 tries.")
            ng()
        else:
            print("Only 1, 2, 3, or 4 works here.")
            continue

        again = prompt_yes_no('\nReturn to main menu? (y/n): ', allow_quit=True)
        if again is True:
            continue
        print("Thanks for playing! Goodbye.")
        return


if __name__ == "__main__":
    run_cli()
