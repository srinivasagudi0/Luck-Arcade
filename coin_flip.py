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
    """Coin flip loop with simple session tracking."""
    attempts = 0
    streak = 0

    print("Coin Flip time.")
    print()
    print("Call it: Heads or Tails.")

    while True:
        user_input = prompt_nonempty(
            'Enter your prediction (Heads/Tails) or "quit" to exit: ',
            allow_quit=True,
            empty_message="Please enter Heads or Tails.",
        )
        if user_input is None:
            print("Leaving coin flip. See you later.")
            return

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
            print("Nice call, you got it.")
        else:
            streak = 0
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
