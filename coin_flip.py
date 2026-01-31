import random as rd

from cli_utils import prompt_nonempty, prompt_yes_no


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
    """Coin-flip game with session stats (attempts + winning streak)."""
    attempts = 0
    streak = 0

    print("Welcome to the Coin Flip Game!")
    print()
    print("Predict the outcome of a coin flip: Heads or Tails.")

    while True:
        user_input = prompt_nonempty(
            'Enter your prediction (Heads/Tails) or "quit" to exit: ',
            allow_quit=True,
            empty_message="Please enter Heads or Tails.",
        )
        if user_input is None:
            print("See you next time!")
            return

        user_choice = _normalize_choice(user_input)
        if user_choice is None:
            print("Invalid input. Please enter Heads or Tails.")
            continue

        attempts += 1
        coin_flip = rd.choice(["Heads", "Tails"])
        print()
        print("The coin landed on:", coin_flip)

        if coin_flip == user_choice:
            streak += 1
            print("You won! Congratulations! :)")
        else:
            streak = 0
            print("It was not your luck this time. :(")

        print(f"Attempts this session: {attempts}")
        print(f"Current winning streak: {streak}")

        again = prompt_yes_no("Play again? (y/n): ", allow_quit=True)
        if again is True:
            print()
            continue
        print("Thank you for playing the Coin Flip Game!")
        return


# End of coin_flip.py
