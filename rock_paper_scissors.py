import random as rd

from cli_utils import prompt_nonempty, prompt_yes_no

CHOICES = ("Rock", "Paper", "Scissors")
_BEATS = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}


def normalize_rps_choice(text: str) -> str | None:
    if not text:
        return None
    first = text.strip()[0].lower()
    if first == "r":
        return "Rock"
    if first == "p":
        return "Paper"
    if first == "s":
        return "Scissors"
    return None


def rps_round_result(user_choice: str, comp_choice: str) -> str:
    if user_choice == comp_choice:
        return "tie"
    return "win" if _BEATS[user_choice] == comp_choice else "loss"


def game_rock_paper_scissors():
    """Play a best-of-3 rock-paper-scissors match against the computer."""
    print("Rock, Paper, Scissors Game!")
    print()
    print("Best of 3: first to 2 wins (ties don't count).")

    while True:
        user_wins = 0
        comp_wins = 0

        while user_wins < 2 and comp_wins < 2:
            user_input = prompt_nonempty(
                'Enter your choice (Rock/Paper/Scissors) or "quit" to exit: ',
                allow_quit=True,
                empty_message="Please enter Rock, Paper, or Scissors.",
            )
            if user_input is None:
                print("Thanks for playing Rock, Paper, Scissors!")
                return

            user_choice = normalize_rps_choice(user_input)
            if user_choice is None:
                print("Invalid input. Please enter Rock, Paper, or Scissors.")
                continue

            comp_choice = rd.choice(CHOICES)
            result = rps_round_result(user_choice, comp_choice)
            print()
            print(f"You chose: {user_choice}")
            print(f"Computer chose: {comp_choice}")

            if result == "tie":
                print("It's a tie!")
            elif result == "win":
                user_wins += 1
                print("You win this round! Congratulations!")
            else:
                comp_wins += 1
                print("You lose this round. Better luck next time!")

            print(f"Score — You: {user_wins} | Computer: {comp_wins}")
            print()

        if user_wins > comp_wins:
            print("You are the overall winner of the best of 3!")
        else:
            print("The computer wins the best of 3.")

        again = prompt_yes_no("Play another best-of-3 match? (y/n): ", allow_quit=True)
        if again is True:
            print()
            continue
        print("Thank you for playing Rock, Paper, Scissors!")
        return

# end of rock_paper_scissors.py
