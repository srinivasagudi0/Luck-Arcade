import os
import random as rd
from flask import Flask, redirect, render_template, request, session, url_for

from cli_utils import handle_global_command
from stats import load_stats, update_and_persist_stats

GAMES = {
    "Dice Roll": "dice",
    "Coin Flip": "coin",
    "Rock Paper Scissors": "rps",
    "Meteor Dodge": "meteor",
    "Planet Guess": "planet",
    "Number Guess": "guess",
}

GAME_LABELS = {value: key for key, value in GAMES.items()}
GAME_META = {
    "Dice Roll": {"icon": "🎲", "subtitle": "Pick a number and see if the die agrees with you."},
    "Coin Flip": {"icon": "🪙", "subtitle": "Call heads or tails and ride your luck."},
    "Rock Paper Scissors": {"icon": "✊", "subtitle": "One clean round against the computer."},
    "Meteor Dodge": {"icon": "☄️", "subtitle": "Choose your lane and avoid impact."},
    "Planet Guess": {"icon": "🪐", "subtitle": "Scan the right orbit to lock onto the target."},
    "Number Guess": {"icon": "🔢", "subtitle": "Find the hidden number in three tries."},
}
GAME_PLAYBOOK = {
    "Dice Roll": (
        "Set your target number from 1 to 6.",
        "Press Roll once to launch the round.",
        "Match the roll to score a win.",
    ),
    "Coin Flip": (
        "Choose Heads or Tails.",
        "Flip once to resolve instantly.",
        "Matching side scores a win.",
    ),
    "Rock Paper Scissors": (
        "Choose Rock, Paper, or Scissors.",
        "Play one round against computer choice.",
        "Ties are neutral and not logged.",
    ),
    "Meteor Dodge": (
        "Pick your lane: Left, Center, or Right.",
        "Engage thrusters to reveal meteor lane.",
        "Avoid the meteor lane to win.",
    ),
    "Planet Guess": (
        "Scan an orbit from 1 to 8.",
        "Ping to compare your orbit with target.",
        "Exact orbit lock is a win.",
    ),
    "Number Guess": (
        "Pick a number from 1 to 10.",
        "Use higher/lower hints across 3 tries.",
        "Find the target before tries run out.",
    ),
}
SESSION_DEFAULTS = {
    "dice_attempts": 0,
    "coin_attempts": 0,
    "rps_attempts": 0,
    "meteor_attempts": 0,
    "planet_attempts": 0,
    "guess_attempts": 0,
    "dice_history": [],
    "coin_history": [],
    "rps_history": [],
    "meteor_history": [],
    "planet_history": [],
    "guess_history": [],
    "activity_feed": [],
    "guess_tries_left": 3,
}

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "luck-arcade-dev-secret")


def _ensure_session_state() -> None:
    for key, value in SESSION_DEFAULTS.items():
        session.setdefault(key, value.copy() if isinstance(value, list) else value)
    session.setdefault("guess_target", rd.randint(1, 10))


def _reset_session_state() -> None:
    for key in list(SESSION_DEFAULTS.keys()) + ["guess_target"]:
        session.pop(key, None)
    _ensure_session_state()


def _stats() -> dict:
    return load_stats()


def _wins(stats: dict, game: str) -> int:
    return stats[f"stats_{game}_win"]


def _losses(stats: dict, game: str) -> int:
    return stats[f"stats_{game}_loss"]


def _plays(stats: dict, game: str) -> int:
    return _wins(stats, game) + _losses(stats, game)


def _win_rate_number(stats: dict, game: str) -> int:
    plays = _plays(stats, game)
    return 0 if plays == 0 else round((_wins(stats, game) / plays) * 100)


def _win_rate(stats: dict, game: str) -> str:
    return f"{_win_rate_number(stats, game)}%"


def _total_wins(stats: dict) -> int:
    return sum(_wins(stats, game) for game in GAMES.values())


def _luck_index_number(stats: dict) -> int:
    total = stats["stats_total"]
    return 0 if total == 0 else round((_total_wins(stats) / total) * 100)


def _luck_index(stats: dict) -> str:
    return f"{_luck_index_number(stats)}%"


def _best_game_summary(stats: dict) -> str:
    played = [
        (label, _win_rate_number(stats, game), _plays(stats, game))
        for label, game in GAMES.items()
        if _plays(stats, game) > 0
    ]
    if not played:
        return "No leading sector yet"
    label, rate, rounds = max(played, key=lambda item: (item[1], item[2]))
    return f"Top sector: {label} ({rate}% over {rounds} rounds)"


def _record_result(game: str, outcome: str, detail: str) -> None:
    persisted = update_and_persist_stats(game, outcome)
    history_key = f"{game}_history"
    history = list(session.get(history_key, []))
    history.insert(0, detail)
    session[history_key] = history[:25]
    game_label = GAME_LABELS[game]
    icon = GAME_META[game_label]["icon"]
    result_tag = "WIN" if outcome == "win" else "LOSS"
    feed = list(session.get("activity_feed", []))
    feed.insert(0, f"{icon} {game_label}: {detail} [{result_tag}]")
    session["activity_feed"] = feed[:30]
    session["last_persisted_stats"] = persisted


def _set_flash(kind: str, title: str, detail: str, icon: str) -> None:
    session["flash_banner"] = {
        "kind": kind if kind in {"win", "loss", "neutral"} else "neutral",
        "title": title,
        "detail": detail,
        "icon": icon,
    }


def _consume_flash() -> dict | None:
    return session.pop("flash_banner", None)


def _quick_command(text: str) -> None:
    value = text.strip()
    if not value:
        _set_flash("neutral", "Quick Command", "Enter a command to run.", "⌨️")
        return
    if value.lower() in ("reset", "clear"):
        _reset_session_state()
        _set_flash("neutral", "Session reset", "Saved totals are still available.", "⌨️")
        return
    action = handle_global_command(value, context="main_menu")
    if action == "help":
        _set_flash("neutral", "Quick Command", "Try: help, stats, reset", "⌨️")
    elif action == "stats":
        stats = _stats()
        _set_flash(
            "neutral",
            "Saved totals",
            f"Total plays: {stats['stats_total']} | Wins: {_total_wins(stats)} | Luck index: {_luck_index(stats)}",
            "⌨️",
        )
    elif action in ("menu", "quit"):
        _set_flash("loss", "Quick Command", f"'{value}' is not used here. Use the game menu.", "⌨️")
    else:
        _set_flash("loss", "Quick Command", f"Unknown command: '{value}'. Try 'help'.", "⌨️")


def _rps_winner(user: str, comp: str) -> str:
    if user == comp:
        return "tie"
    wins = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
    return "win" if wins[user] == comp else "loss"


def _handle_game_action(game_label: str, form: dict) -> None:
    game = GAMES[game_label]

    if game == "dice":
        prediction = int(form.get("prediction", 3))
        session["dice_attempts"] = session.get("dice_attempts", 0) + 1
        roll = rd.randint(1, 6)
        outcome = "win" if roll == prediction else "loss"
        _record_result("dice", outcome, f"Predicted {prediction}, rolled {roll}")
        if outcome == "win":
            _set_flash("win", f"Rolled {roll}", "Perfect call. You matched the die.", "🎲")
        else:
            _set_flash("loss", f"Rolled {roll}", f"You predicted {prediction}. Queue up another round.", "🎲")
        return

    if game == "coin":
        choice = form.get("choice", "Heads")
        session["coin_attempts"] = session.get("coin_attempts", 0) + 1
        result = rd.choice(["Heads", "Tails"])
        outcome = "win" if result == choice else "loss"
        _record_result("coin", outcome, f"Called {choice}, got {result}")
        if outcome == "win":
            _set_flash("win", f"Coin landed {result}", "Clean read on the flip.", "🪙")
        else:
            _set_flash("loss", f"Coin landed {result}", f"You called {choice}. Try a quick rematch.", "🪙")
        return

    if game == "rps":
        user_choice = form.get("user_choice", "Rock")
        session["rps_attempts"] = session.get("rps_attempts", 0) + 1
        comp_choice = rd.choice(["Rock", "Paper", "Scissors"])
        result = _rps_winner(user_choice, comp_choice)
        detail = f"You: {user_choice} | Computer: {comp_choice}"
        if result == "tie":
            _set_flash("neutral", "Tie round", detail, "✊")
        else:
            _record_result("rps", result, detail)
            title = "You won the round" if result == "win" else "Computer won the round"
            _set_flash(result, title, detail, "✊")
        return

    if game == "meteor":
        lane = form.get("lane", "Center")
        session["meteor_attempts"] = session.get("meteor_attempts", 0) + 1
        incoming = rd.choice(["Left", "Center", "Right"])
        outcome = "loss" if incoming == lane else "win"
        detail = f"Lane: {lane} | Meteor: {incoming}"
        _record_result("meteor", outcome, detail)
        if outcome == "win":
            _set_flash("win", "Safe passage", f"Meteor crossed {incoming}. You chose {lane}.", "☄️")
        else:
            _set_flash("loss", "Direct hit", f"Meteor crossed {incoming}. You chose {lane}.", "☄️")
        return

    if game == "planet":
        guess = int(form.get("guess", 4))
        session["planet_attempts"] = session.get("planet_attempts", 0) + 1
        target = rd.randint(1, 8)
        outcome = "win" if target == guess else "loss"
        _record_result("planet", outcome, f"Guessed {guess}, target was {target}")
        if outcome == "win":
            _set_flash("win", "Target located", f"Orbit {guess} was the correct scan.", "🪐")
        else:
            hint = "higher" if target > guess else "lower"
            _set_flash("neutral", f"Not orbit {guess}", f"Hint from scan: go {hint}.", "🪐")
        return

    if game == "guess":
        if form.get("action") == "reset_round":
            session["guess_target"] = rd.randint(1, 10)
            session["guess_tries_left"] = 3
            _set_flash("neutral", "Round reset", "Started a fresh number puzzle.", "🔢")
            return

        guess = int(form.get("guess", 5))
        session["guess_attempts"] = session.get("guess_attempts", 0) + 1
        target = session["guess_target"]
        tries_left = session["guess_tries_left"]
        if guess == target:
            used = 4 - tries_left
            suffix = "s" if used != 1 else ""
            _record_result("guess", "win", f"Guessed {guess} correctly in {used} attempt{suffix}")
            _set_flash("win", "Correct guess", f"It was {target}. Solved in {used} attempt{suffix}.", "🔢")
            session["guess_target"] = rd.randint(1, 10)
            session["guess_tries_left"] = 3
            return

        tries_left -= 1
        session["guess_tries_left"] = tries_left
        if tries_left <= 0:
            _record_result("guess", "loss", f"Missed 3 tries, target was {target}")
            _set_flash("loss", "Out of tries", f"The number was {target}. Fresh round loaded.", "🔢")
            session["guess_target"] = rd.randint(1, 10)
            session["guess_tries_left"] = 3
        else:
            hint = "higher" if target > guess else "lower"
            _set_flash("neutral", "Keep scanning", f"Try {hint}. Tries left: {tries_left}.", "🔢")


@app.route("/", methods=["GET"])
def index():
    _ensure_session_state()
    game = request.args.get("game", "Dice Roll")
    if game not in GAMES:
        game = "Dice Roll"
    stats = _stats()
    flash = _consume_flash()
    history_key = f"{GAMES[game]}_history"
    game_cards = [
        {
            "label": label,
            "icon": GAME_META[label]["icon"],
            "subtitle": GAME_META[label]["subtitle"],
            "rate": _win_rate(stats, key),
            "active": label == game,
        }
        for label, key in GAMES.items()
    ]
    stat_cards = [
        ("Total rounds", stats["stats_total"], "Across all games"),
        ("Total wins", _total_wins(stats), "Across all games"),
        ("Win rate", _luck_index(stats), "Across all games"),
        ("Dice Roll", f"{_wins(stats, 'dice')}W / {_losses(stats, 'dice')}L", f"{_win_rate(stats, 'dice')} WR"),
        ("Coin Flip", f"{_wins(stats, 'coin')}W / {_losses(stats, 'coin')}L", f"{_win_rate(stats, 'coin')} WR"),
        ("RPS", f"{_wins(stats, 'rps')}W / {_losses(stats, 'rps')}L", f"{_win_rate(stats, 'rps')} WR"),
        ("Meteor", f"{_wins(stats, 'meteor')}W / {_losses(stats, 'meteor')}L", f"{_win_rate(stats, 'meteor')} WR"),
        ("Planet", f"{_wins(stats, 'planet')}W / {_losses(stats, 'planet')}L", f"{_win_rate(stats, 'planet')} WR"),
        ("Number Guess", f"{_wins(stats, 'guess')}W / {_losses(stats, 'guess')}L", f"{_win_rate(stats, 'guess')} WR"),
    ]
    return render_template(
        "index.html",
        active_game=game,
        active_key=GAMES[game],
        active_meta=GAME_META[game],
        game_cards=game_cards,
        stats=stats,
        total_wins=_total_wins(stats),
        luck_index=_luck_index(stats),
        best_game_summary=_best_game_summary(stats),
        stat_cards=stat_cards,
        playbook=GAME_PLAYBOOK[game],
        flash=flash,
        history=session.get(history_key, [])[:8],
        activity_feed=session.get("activity_feed", [])[:8],
        attempts={
            "dice": session.get("dice_attempts", 0),
            "coin": session.get("coin_attempts", 0),
            "rps": session.get("rps_attempts", 0),
            "meteor": session.get("meteor_attempts", 0),
            "planet": session.get("planet_attempts", 0),
            "guess": session.get("guess_attempts", 0),
        },
        guess_tries_left=session.get("guess_tries_left", 3),
        rulebook=[
            "Dice Roll: win if your number matches the roll.",
            "Coin Flip: win if the coin matches your call.",
            "Rock Paper Scissors: ties are neutral and not logged as wins/losses.",
            "Meteor Dodge: win if your lane is different from the meteor lane.",
            "Planet Guess: win only on an exact orbit match.",
            "Number Guess: win by finding the number in 3 tries.",
        ],
    )


@app.route("/action", methods=["POST"])
def action():
    _ensure_session_state()
    game = request.form.get("game", "Dice Roll")
    if game not in GAMES:
        game = "Dice Roll"

    action_name = request.form.get("ui_action")
    if action_name == "reset_session":
        _reset_session_state()
        _set_flash("neutral", "Session reset", "Saved totals are still available.", "⌨️")
    elif action_name == "quick_command":
        _quick_command(request.form.get("command", ""))
    else:
        _handle_game_action(game, request.form)

    return redirect(url_for("index", game=game))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(debug=True, port=port)
