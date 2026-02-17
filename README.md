# Luck Arcade

Small arcade project with a CLI and a Streamlit UI.
It has Dice Roll, Coin Flip, Rock Paper Scissors, plus two space mini-games.

## Requirements
- Python 3.10+

## Games
- Dice Roll: pick a number from 1-6 and try to hit it.
- Coin Flip: call heads/tails and see if it lands your way.
- Rock Paper Scissors: best of 3 against the computer.
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
Choose 1-3, or type `quit` / `exit` / `q` to leave.

### Optional: install as a CLI command
```bash
pip install -e .
luck-arcade
```

## Notes
- Very small dependency list.
- Inputs are case-insensitive in the CLI.
- Invalid input is handled with simple retry prompts.

## Files
- `app.py`: Streamlit UI for all games.
- `main.py`: CLI menu and game selection.
- `dice_roll.py`, `coin_flip.py`, `rock_paper_scissors.py`: game logic.
- `app.py` includes space-themed UI styling and extra UI-only games.
- `cli_utils.py`: shared CLI input helpers.
- `README.md`: This documentation file.

## License
MIT (see `LICENSE`).

---
Have fun and good luck.
