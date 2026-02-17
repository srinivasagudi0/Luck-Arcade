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
    """Run a best-of-3 rock-paper-scissors match."""
    print("Rock, Paper, Scissors.")
    print()
    print("Best of 3. First to 2 wins. Ties do not count.")

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
                print("Leaving Rock, Paper, Scissors.")
                return

            user_choice = normalize_rps_choice(user_input)
            if user_choice is None:
                print("Pick rock, paper, or scissors.")
                continue

            comp_choice = rd.choice(CHOICES)
            result = rps_round_result(user_choice, comp_choice)
            print()
            print(f"You chose: {user_choice}")
            print(f"Computer chose: {comp_choice}")

            if result == "tie":
                print("Tie round.")
            elif result == "win":
                user_wins += 1
                print("You take this round.")
            else:
                comp_wins += 1
                print("Computer takes this round.")

            print(f"Score — You: {user_wins} | Computer: {comp_wins}")
            print()

        if user_wins > comp_wins:
            print("You won the match.")
        else:
            print("Computer won the match.")

        again = prompt_yes_no("Play another best-of-3 match? (y/n): ", allow_quit=True)
        if again is True:
            print()
            continue
        print("Done with Rock, Paper, Scissors.")
        return

# rock_paper_scissors.py
