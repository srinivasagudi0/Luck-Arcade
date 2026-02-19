# Luck Arcade

Small arcade project with a CLI and a Streamlit UI.
It has Dice Roll, Coin Flip, Rock Paper Scissors, Number Guess, plus two space mini-games.

## Requirements
- Python 3.10+

## Games
- Dice Roll: pick a number from 1-6 and try to hit it.
- Coin Flip: call heads/tails and see if it lands your way.
- Rock Paper Scissors: best of 3 against the computer.
- Number Guess: find the number from 1 to 10 in 3 tries.
- Meteor Dodge (UI): choose a lane and avoid a meteor.
- Planet Guess (UI): guess the orbit from 1 to 8.

## Run (Streamlit UI)
```bash
pip install -r requirements.txt
# or: pip install -e .[ui]
streamlit run app.py
```

## Run (CLI)
```bash
python3 main.py
```
Choose 1-4 to play.

Global commands work across the CLI:
- `help` / `h` / `?` for a quick reminder
- `stats` / `stat` / `score` / `scores` to view saved totals
- `menu` / `m` / `back` to return to the main menu (inside games)
- `quit` / `exit` / `q` to leave

### Optional: install as a CLI command
```bash
pip install -e .
luck-arcade
```

## Notes
- Very small dependency list.
- Inputs are case-insensitive in the CLI.
- Invalid input is handled with simple retry prompts.
- Win/loss totals are saved in `stats.json`, so progress carries across restarts.

## How to Use Quick Command
In the CLI, type commands directly at any input prompt.
If you are inside a game, `menu` takes you back to game selection.
Use `stats` any time to see your saved totals.

In Streamlit, open the sidebar and use the **Quick Command** box.
Supported commands are `help`, `stats`, and `reset`.

## Files
- `app.py`: Streamlit UI for all games.
- `main.py`: CLI menu and game selection.
- `dice_roll.py`, `coin_flip.py`, `rock_paper_scissors.py`, `number_guess.py`: game logic.
- `app.py` includes space-themed UI styling and extra UI-only games.
- `cli_utils.py`: shared CLI input helpers.
- `stats.py`: persistent stats load/save helpers.
- `README.md`: This documentation file.

## License
MIT (see `LICENSE`).

---
Have fun and good luck.
