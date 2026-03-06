# Luck Arcade

Small arcade project with a CLI and a Flask UI.
It has Dice Roll, Coin Flip, Rock Paper Scissors, plus two space mini-games.

## Requirements
- Python 3.10+

## Games
- Dice Roll: pick a number from 1-6 and try to hit it.
- Coin Flip: call heads/tails and see if it lands your way.
- Rock Paper Scissors: one round against the computer in the web UI, best-of-3 in CLI.
- Meteor Dodge (UI): choose a lane and avoid a meteor.
- Planet Guess (UI): guess the orbit from 1 to 8.
- Number Guess: find the hidden number in 3 tries.

## Run (Flask UI)
```bash
pip install -r requirements.txt
# or: pip install -e .[ui]
python3 app.py
```

Then open `http://127.0.0.1:8000`.

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
- Flask session state keeps browser-local attempts, game history, the activity feed, and active Number Guess rounds.

## How to Use Quick Command
In the web UI, use the Quick Command panel in the left sidebar.
Supported commands are:
- `help`
- `stats`
- `reset`

`menu` and `quit` are intentionally ignored in the browser because navigation is handled by the game menu.

## Files
- `app.py`: Flask UI for all games.
- `templates/index.html`: main Flask template.
- `static/styles.css`: UI styling.
- `main.py`: CLI menu and game selection.
- `dice_roll.py`, `coin_flip.py`, `rock_paper_scissors.py`: game logic.
- `cli_utils.py`: shared CLI input helpers.
- `stats.py`: persistent stats load/save helpers.
- `README.md`: this documentation file.

## Updates

### For CLI version
- Added support for `help`, `stats`, `menu`, and `quit` commands for smoother flow.
- Updated CLI files to use shared command handling from `cli_utils.py`.
- Added `stats.py` for persistent win/loss tracking across sessions.
- Added a new game: **Number Guess**.
- Reworked `main.py`.
- Added and updated tests for CLI helpers and stats behavior.

### For Flask version
- Replaced the Streamlit UI with a Flask app while keeping the same games and persistent stats.
- Preserved session reset behavior, activity feed, quick commands, and per-game history.
- Kept Number Guess as a multi-step session round with 3 tries and reset support.
- Moved UI structure into `templates/` and `static/` for maintainability.

## License
MIT (see `LICENSE`).
