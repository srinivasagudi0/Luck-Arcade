# Luck Arcade

Command-line and Streamlit UI bundle of mini-games: Dice Roll, Coin Flip, and Rock Paper Scissors.

## Requirements
- Python 3.10+

## Games
- Dice Roll: predict a number 1-6 and roll to match.
- Coin Flip: call Heads or Tails and flip (tracks attempts + win streak).
- Rock Paper Scissors: best of 3 (first to 2 wins; ties don’t count).

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
Choose 1–3 or type `quit`/`exit`/`q` to leave.

### Optional: install as a CLI command
```bash
pip install -e .
luck-arcade
```

## Notes
- Standard library + Streamlit only.
- Input is case-insensitive for menu selections and in-game prompts.
- Basic error handling for invalid inputs.

## Files
- `app.py`: Streamlit UI for all games.
- `main.py`: CLI menu and game selection.
- `dice_roll.py`, `coin_flip.py`, `rock_paper_scissors.py`: game logic.
- `cli_utils.py`: shared CLI input helpers.
- `README.md`: This documentation file.

## License
MIT (see `LICENSE`).

---
Enjoy playing and testing your luck!
Peace! ✌️
