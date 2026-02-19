import random as rd
from html import escape

import streamlit as st

from cli_utils import handle_global_command
from stats import load_stats, update_and_persist_stats

st.set_page_config(page_title="Luck Arcade", page_icon="🎰", layout="wide")

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
    "Dice Roll": {
        "icon": "🎲",
        "subtitle": "Pick a number and see if the die agrees with you.",
    },
    "Coin Flip": {
        "icon": "🪙",
        "subtitle": "Call heads or tails and ride your luck.",
    },
    "Rock Paper Scissors": {
        "icon": "✊",
        "subtitle": "One clean round against the computer.",
    },
    "Meteor Dodge": {
        "icon": "☄️",
        "subtitle": "Choose your lane and avoid impact.",
    },
    "Planet Guess": {
        "icon": "🪐",
        "subtitle": "Scan the right orbit to lock onto the target.",
    },
    "Number Guess": {
        "icon": "🔢",
        "subtitle": "Find the hidden number in three tries.",
    },
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


def _init_state():
    persisted = load_stats()
    defaults = {
        "stats_total": persisted["stats_total"],
        "stats_dice_win": persisted["stats_dice_win"],
        "stats_dice_loss": persisted["stats_dice_loss"],
        "stats_coin_win": persisted["stats_coin_win"],
        "stats_coin_loss": persisted["stats_coin_loss"],
        "stats_rps_win": persisted["stats_rps_win"],
        "stats_rps_loss": persisted["stats_rps_loss"],
        "stats_meteor_win": persisted["stats_meteor_win"],
        "stats_meteor_loss": persisted["stats_meteor_loss"],
        "stats_planet_win": persisted["stats_planet_win"],
        "stats_planet_loss": persisted["stats_planet_loss"],
        "stats_guess_win": persisted["stats_guess_win"],
        "stats_guess_loss": persisted["stats_guess_loss"],
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
        "guess_target": rd.randint(1, 10),
        "guess_tries_left": 3,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def _reset_state():
    for key in list(st.session_state.keys()):
        if (
            key.startswith("stats_")
            or key.endswith("_history")
            or key.endswith("_attempts")
            or key in ("activity_feed", "guess_target", "guess_tries_left")
        ):
            del st.session_state[key]
    _init_state()


def _wins(game: str) -> int:
    return st.session_state[f"stats_{game}_win"]


def _losses(game: str) -> int:
    return st.session_state[f"stats_{game}_loss"]


def _plays(game: str) -> int:
    return _wins(game) + _losses(game)


def _win_rate(game: str) -> str:
    plays = _plays(game)
    if plays == 0:
        return "0%"
    return f"{round((_wins(game) / plays) * 100)}%"


def _win_rate_number(game: str) -> int:
    plays = _plays(game)
    if plays == 0:
        return 0
    return round((_wins(game) / plays) * 100)


def _total_wins() -> int:
    return sum(_wins(game_key) for game_key in GAMES.values())


def _luck_index() -> str:
    total = st.session_state["stats_total"]
    if total == 0:
        return "0%"
    return f"{round((_total_wins() / total) * 100)}%"


def _luck_index_number() -> int:
    total = st.session_state["stats_total"]
    if total == 0:
        return 0
    return round((_total_wins() / total) * 100)


def _apply_theming():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

        :root {
            --bg: #0f172a;
            --panel: #111b30;
            --panel-2: #0d1526;
            --text: #e6ecf5;
            --muted: #9fb3d1;
            --accent: #4f9cff;
            --accent-2: #22c55e;
            --edge: rgba(255,255,255,0.06);
            --shadow: 0 16px 30px rgba(0,0,0,0.35);
        }

        html, body, [class*="css"] {
            font-family: "Poppins", sans-serif;
            color: var(--text);
        }

        .stApp {
            background: radial-gradient(circle at 12% 20%, rgba(79,156,255,0.12), transparent 26%),
                        radial-gradient(circle at 82% 12%, rgba(34,197,94,0.10), transparent 26%),
                        linear-gradient(140deg, #0b1222 0%, #0f172a 40%, #0b1222 100%);
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 0.8rem;
            padding-bottom: 1.6rem;
        }

        .hero {
            border-radius: 18px;
            border: 1px solid var(--edge);
            background: var(--panel);
            box-shadow: var(--shadow);
            padding: 1.1rem 1.2rem 1rem;
            margin-bottom: 0.75rem;
        }

        .hero-kicker {
            margin: 0;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-weight: 700;
            font-size: 0.72rem;
        }

        .hero-title {
            margin: 0.2rem 0 0.35rem;
            color: var(--text);
            font-size: clamp(1.6rem, 3vw, 2.3rem);
            line-height: 1.05;
            letter-spacing: -0.01em;
        }

        .hero-copy {
            margin: 0;
            color: var(--muted);
            font-size: 0.98rem;
            line-height: 1.36;
        }

        .hero-row {
            margin-top: 0.65rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
        }

        .hero-chip {
            display: inline-flex;
            align-items: center;
            border-radius: 12px;
            border: 1px solid var(--edge);
            background: var(--panel-2);
            color: var(--text);
            padding: 0.28rem 0.65rem;
            font-size: 0.78rem;
            font-weight: 700;
        }

        .panel {
            border-radius: 14px;
            border: 1px solid var(--edge);
            background: var(--panel);
            box-shadow: var(--shadow);
            padding: 0.9rem 1rem;
        }

        .section-break {
            height: 1px;
            margin: 0.9rem 0 1rem;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
        }

        div[data-testid="stMetric"] {
            border-radius: 12px;
            border: 1px solid var(--edge);
            background: var(--panel-2);
            padding: 0.7rem 0.8rem;
            box-shadow: var(--shadow);
        }

        div[data-testid="stMetricValue"] {
            color: var(--text);
            font-weight: 800;
        }

        div[data-testid="stMetricLabel"] {
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.68rem;
            font-weight: 700;
        }

        div[data-testid="stSlider"] [role="slider"] {
            background: var(--accent) !important;
            border: 2px solid rgba(255,255,255,0.8);
        }

        div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div:first-child {
            background: var(--accent);
            height: 0.48rem;
        }

        div[data-testid="stSegmentedControl"] div[role="radiogroup"] {
            gap: 0.3rem;
            background: var(--panel-2);
            border: 1px solid var(--edge);
            border-radius: 12px;
            padding: 0.32rem;
        }

        div[data-testid="stSegmentedControl"] label {
            border-radius: 10px;
            color: var(--text);
            font-weight: 600;
            border: 1px solid var(--edge);
        }

        div[data-testid="stSegmentedControl"] label:has(input:checked) {
            background: var(--accent);
            color: #0b1222;
            border-color: var(--accent);
        }

        div[data-testid="stRadio"] > div {
            background: var(--panel-2);
            border: 1px solid var(--edge);
            border-radius: 12px;
            padding: 0.45rem 0.55rem;
        }

        div[data-testid="stRadio"] label p {
            color: var(--text);
            font-weight: 600;
        }

        div[data-baseweb="input"] > div {
            border-radius: 10px;
            border-color: var(--edge);
            background: var(--panel-2);
        }

        div[data-baseweb="input"] input {
            color: var(--text) !important;
        }

        div[data-baseweb="input"] input::placeholder {
            color: var(--muted) !important;
        }

        .result-banner {
            border-radius: 12px;
            border: 1px solid var(--edge);
            padding: 0.6rem 0.7rem;
            margin-top: 0.35rem;
            box-shadow: var(--shadow);
            background: var(--panel-2);
        }

        .result-top {
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.42rem;
            font-weight: 800;
            font-size: 0.9rem;
        }

        .result-text {
            margin: 0.18rem 0 0;
            color: var(--muted);
            font-size: 0.82rem;
            line-height: 1.32;
            font-weight: 600;
        }

        .result-win { border-color: rgba(34,197,94,0.5); }
        .result-loss { border-color: rgba(239,68,68,0.5); }
        .result-neutral { border-color: rgba(255,255,255,0.12); }

        .history-card, .feed-card, .rulebook {
            border-radius: 12px;
            border: 1px solid var(--edge);
            background: var(--panel);
            box-shadow: var(--shadow);
            padding: 0.8rem 0.9rem;
        }

        .history-title, .feed-title, .rulebook-title {
            margin: 0;
            color: var(--text);
            font-size: 0.9rem;
            font-weight: 800;
            letter-spacing: 0.02em;
        }

        .history-card li,
        .feed-item,
        .rulebook-copy,
        .rulebook-list li {
            color: var(--muted);
            font-size: 0.84rem;
            line-height: 1.32;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(160deg, #0c1324 0%, #0a1020 100%);
            border-right: 1px solid var(--edge);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p {
            color: var(--text);
        }

        .sidebar-note {
            color: var(--muted);
            font-size: 0.82rem;
        }

        @media (max-width: 900px) {
            .hero { padding: 0.9rem 1rem; }
            .main .block-container { padding-top: 0.6rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _record_result(game: str, outcome: str, detail: str):
    persisted = update_and_persist_stats(game, outcome)
    st.session_state["stats_total"] = persisted["stats_total"]
    st.session_state[f"stats_{game}_win"] = persisted[f"stats_{game}_win"]
    st.session_state[f"stats_{game}_loss"] = persisted[f"stats_{game}_loss"]
    history_key = f"{game}_history"
    st.session_state[history_key].insert(0, detail)
    st.session_state[history_key] = st.session_state[history_key][:25]
    game_label = GAME_LABELS[game]
    icon = GAME_META[game_label]["icon"]
    result_tag = "WIN" if outcome == "win" else "LOSS"
    st.session_state["activity_feed"].insert(0, f"{icon} {game_label}: {detail} [{result_tag}]")
    st.session_state["activity_feed"] = st.session_state["activity_feed"][:30]


def _result_banner(kind: str, title: str, detail: str, icon: str):
    safe_kind = kind if kind in {"win", "loss", "neutral"} else "neutral"
    st.markdown(
        f"""
        <div class="result-banner result-{safe_kind}">
            <p class="result-top">{escape(icon)} {escape(title)}</p>
            <p class="result-text">{escape(detail)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _best_game_summary() -> str:
    played = [
        (label, _win_rate_number(game), _plays(game))
        for label, game in GAMES.items()
        if _plays(game) > 0
    ]
    if not played:
        return "No leading sector yet"

    label, rate, rounds = max(played, key=lambda item: (item[1], item[2]))
    return f"Top sector: {label} ({rate}% over {rounds} rounds)"


def _sidebar_game_cards(active_game: str):
    cards = []
    for label, game in GAMES.items():
        meta = GAME_META[label]
        cards.append(
            {
                "label": label,
                "icon": meta["icon"],
                "subtitle": meta["subtitle"],
                "rate": _win_rate(game),
                "active": label == active_game,
            }
        )

    rows = st.container()
    for card in cards:
        rows.markdown(
            f"""
            <article class="selector-card{' active' if card['active'] else ''}">
                <div class="selector-row">
                    <p class="selector-title">{escape(card['icon'])} {escape(card['label'])}</p>
                    <span class="selector-rate">Win {escape(card['rate'])}</span>
                </div>
                <p class="selector-sub">{escape(card['subtitle'])}</p>
            </article>
            """,
            unsafe_allow_html=True,
        )


def _activity_feed_panel():
    feed = st.session_state["activity_feed"][:8]
    if not feed:
        st.markdown(
            """
            <section class="feed-card">
                <p class="feed-title">Flight Log</p>
                <p class="feed-empty">No rounds recorded yet. Play any sector to start the log.</p>
            </section>
            """,
            unsafe_allow_html=True,
        )
        return

    items_html = "".join(f'<div class="feed-item">{escape(item)}</div>' for item in feed)
    st.markdown(
        f"""
        <section class="feed-card">
            <p class="feed-title">Flight Log</p>
            <div class="feed-list">{items_html}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _mission_brief(active_game: str):
    steps = GAME_PLAYBOOK[active_game]
    active_meta = GAME_META[active_game]
    items_html = "".join(f"<li>{escape(step)}</li>" for step in steps)
    st.markdown(
        f"""
        <section class="brief-card">
            <p class="brief-kicker">How to play</p>
            <p class="brief-title">{escape(active_meta['icon'])} {escape(active_game)}</p>
            <ol class="brief-list">{items_html}</ol>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _header(active_game: str):
    active_icon = GAME_META[active_game]["icon"]
    active_subtitle = GAME_META[active_game]["subtitle"]
    st.markdown(
        f"""
        <section class="hero">
            <p class="hero-kicker">Luck Arcade</p>
            <h1 class="hero-title">Arcade Hub</h1>
            <p class="hero-copy">
                Quick mini-games with instant results. Active game: <strong>{escape(active_icon)} {escape(active_game)}</strong> — {escape(active_subtitle)}
            </p>
            <div class="hero-row">
                <span class="hero-chip">Rounds: {st.session_state["stats_total"]}</span>
                <span class="hero-chip">Wins: {_total_wins()}</span>
                <span class="hero-chip">Win rate: {_luck_index()}</span>
                <span class="hero-chip">Games: {len(GAMES)}</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _stats_bar():
    cards = [
        ("Total rounds", st.session_state["stats_total"], "Across all games"),
        ("Total wins", _total_wins(), "Across all games"),
        ("Win rate", _luck_index(), "Across all games"),
        ("Dice Roll", f"{_wins('dice')}W / {_losses('dice')}L", f"{_win_rate('dice')} WR"),
        ("Coin Flip", f"{_wins('coin')}W / {_losses('coin')}L", f"{_win_rate('coin')} WR"),
        ("RPS", f"{_wins('rps')}W / {_losses('rps')}L", f"{_win_rate('rps')} WR"),
        ("Meteor", f"{_wins('meteor')}W / {_losses('meteor')}L", f"{_win_rate('meteor')} WR"),
        ("Planet", f"{_wins('planet')}W / {_losses('planet')}L", f"{_win_rate('planet')} WR"),
        ("Number Guess", f"{_wins('guess')}W / {_losses('guess')}L", f"{_win_rate('guess')} WR"),
    ]
    for start in range(0, len(cards), 3):
        row = cards[start : start + 3]
        cols = st.columns(len(row))
        for col, (label, value, subtext) in zip(cols, row):
            col.metric(label, value, subtext)


def _render_history(title: str, history_key: str):
    history = st.session_state[history_key]
    if not history:
        st.markdown(
            '<div class="history-empty">No rounds yet. Play once and this fills up.</div>',
            unsafe_allow_html=True,
        )
        return

    items_html = "".join(f"<li>{escape(item)}</li>" for item in history[:8])
    st.markdown(
        f"""
        <div class="history-card">
            <p class="history-title">Recent Rounds: {escape(title)}</p>
            <ul>{items_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _game_heading(icon: str, title: str, subtitle: str, tip: str):
    st.markdown(
        f"""
        <section class="game-shell">
        <div class="game-heading">
            <div class="game-icon">{escape(icon)}</div>
            <div>
                <h2 class="game-title">{escape(title)}</h2>
                <p class="game-subtitle">{escape(subtitle)}</p>
            </div>
        </div>
        <div class="game-tip">{escape(tip)}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _game_dice():
    _game_heading(
        "🎲",
        "Dice Roll",
        "Pick a number from 1 to 6 and try to hit it.",
        "One tap, one roll. Clean and quick.",
    )
    col1, col2 = st.columns([1.05, 0.95], gap="large")
    with col1:
        prediction = st.slider("Your prediction", 1, 6, 3)
        if st.button("Roll the die", key="dice-roll"):
            st.session_state["dice_attempts"] += 1
            roll = rd.randint(1, 6)
            outcome = "win" if roll == prediction else "loss"
            _record_result("dice", outcome, f"Predicted {prediction}, rolled {roll}")
            if outcome == "win":
                _result_banner("win", f"Rolled {roll}", "Perfect call. You matched the die.", "🎲")
            else:
                _result_banner(
                    "loss",
                    f"Rolled {roll}",
                    f"You predicted {prediction}. Queue up another round.",
                    "🎲",
                )

    with col2:
        st.metric("Total attempts", st.session_state["dice_attempts"])
        _render_history("Dice Roll", "dice_history")


def _game_coin():
    _game_heading(
        "🪙",
        "Coin Flip",
        "Call heads or tails and see what happens.",
        "Short rounds with instant result tracking.",
    )
    col1, col2 = st.columns([1.05, 0.95], gap="large")
    with col1:
        choice = st.segmented_control("Your call", options=["Heads", "Tails"], default="Heads")
        if st.button("Flip coin", key="coin-flip"):
            st.session_state["coin_attempts"] += 1
            result = rd.choice(["Heads", "Tails"])
            outcome = "win" if result == choice else "loss"
            _record_result("coin", outcome, f"Called {choice}, got {result}")
            if outcome == "win":
                _result_banner("win", f"Coin landed {result}", "Clean read on the flip.", "🪙")
            else:
                _result_banner(
                    "loss",
                    f"Coin landed {result}",
                    f"You called {choice}. Try a quick rematch.",
                    "🪙",
                )

    with col2:
        st.metric("Total attempts", st.session_state["coin_attempts"])
        _render_history("Coin Flip", "coin_history")


def _rps_winner(user: str, comp: str) -> str:
    if user == comp:
        return "tie"
    wins = {
        "Rock": "Scissors",
        "Paper": "Rock",
        "Scissors": "Paper",
    }
    return "win" if wins[user] == comp else "loss"


def _game_rps():
    _game_heading(
        "✊",
        "Rock Paper Scissors",
        "Pick your move and face the computer.",
        "Ties are neutral and do not affect win/loss stats.",
    )
    choices = ["Rock", "Paper", "Scissors"]
    col1, col2 = st.columns([1.05, 0.95], gap="large")
    with col1:
        user_choice = st.segmented_control("Your choice", options=choices, default="Rock")
        if st.button("Play", key="rps-play"):
            st.session_state["rps_attempts"] += 1
            comp_choice = rd.choice(choices)
            result = _rps_winner(user_choice, comp_choice)
            detail = f"You: {user_choice} | Computer: {comp_choice}"
            if result == "tie":
                _result_banner("neutral", "Tie round", detail, "✊")
            elif result == "win":
                _record_result("rps", result, detail)
                _result_banner("win", "You won the round", detail, "✊")
            else:
                _record_result("rps", result, detail)
                _result_banner("loss", "Computer won the round", detail, "✊")

    with col2:
        st.metric("Total attempts", st.session_state["rps_attempts"])
        _render_history("Rock Paper Scissors", "rps_history")


def _game_meteor():
    _game_heading(
        "☄️",
        "Meteor Dodge",
        "Pick a lane and hope the meteor misses.",
        "If the meteor lands in your lane, it is a loss.",
    )
    col1, col2 = st.columns([1.05, 0.95], gap="large")
    with col1:
        lane = st.segmented_control("Your lane", options=["Left", "Center", "Right"], default="Center")
        if st.button("Engage thrusters", key="meteor-play"):
            st.session_state["meteor_attempts"] += 1
            incoming = rd.choice(["Left", "Center", "Right"])
            outcome = "loss" if incoming == lane else "win"
            detail = f"Lane: {lane} | Meteor: {incoming}"
            if outcome == "win":
                _result_banner("win", "Safe passage", f"Meteor crossed {incoming}. You chose {lane}.", "☄️")
            else:
                _result_banner("loss", "Direct hit", f"Meteor crossed {incoming}. You chose {lane}.", "☄️")
            _record_result("meteor", outcome, detail)

    with col2:
        st.metric("Total attempts", st.session_state["meteor_attempts"])
        _render_history("Meteor Dodge", "meteor_history")


def _game_planet():
    _game_heading(
        "🪐",
        "Planet Guess",
        "Guess the hidden planet from orbit 1 to 8.",
        "Exact match wins. You get a higher/lower hint on misses.",
    )
    col1, col2 = st.columns([1.05, 0.95], gap="large")
    with col1:
        guess = st.slider("Your scan orbit", 1, 8, 4)
        if st.button("Ping the planet", key="planet-play"):
            st.session_state["planet_attempts"] += 1
            target = rd.randint(1, 8)
            outcome = "win" if target == guess else "loss"
            detail = f"Guessed {guess}, target was {target}"
            if outcome == "win":
                st.balloons()
                _result_banner("win", "Target located", f"Orbit {guess} was the correct scan.", "🪐")
            else:
                hint = "higher" if target > guess else "lower"
                _result_banner(
                    "neutral",
                    f"Not orbit {guess}",
                    f"Hint from scan: go {hint}.",
                    "🪐",
                )
            _record_result("planet", outcome, detail)

    with col2:
        st.metric("Total attempts", st.session_state["planet_attempts"])
        _render_history("Planet Guess", "planet_history")


def _game_number_guess():
    _game_heading(
        "🔢",
        "Number Guess",
        "You get 3 tries to find a number from 1 to 10.",
        "Misses give you a higher/lower hint before the next try.",
    )
    col1, col2 = st.columns([1.05, 0.95], gap="large")

    with col1:
        st.caption(f"Tries left in current round: {st.session_state['guess_tries_left']}")
        guess = st.slider("Your guess", 1, 10, 5)

        if st.button("Submit guess", key="guess-play"):
            st.session_state["guess_attempts"] += 1
            target = st.session_state["guess_target"]

            if guess == target:
                used = 4 - st.session_state["guess_tries_left"]
                detail = f"Guessed {guess} correctly in {used} attempt{'s' if used != 1 else ''}"
                _record_result("guess", "win", detail)
                _result_banner("win", "Correct guess", f"It was {target}. Solved in {used} attempt{'s' if used != 1 else ''}.", "🔢")
                st.balloons()
                st.session_state["guess_target"] = rd.randint(1, 10)
                st.session_state["guess_tries_left"] = 3
            else:
                st.session_state["guess_tries_left"] -= 1
                if st.session_state["guess_tries_left"] <= 0:
                    detail = f"Missed 3 tries, target was {target}"
                    _record_result("guess", "loss", detail)
                    _result_banner("loss", "Out of tries", f"The number was {target}. Fresh round loaded.", "🔢")
                    st.session_state["guess_target"] = rd.randint(1, 10)
                    st.session_state["guess_tries_left"] = 3
                else:
                    hint = "higher" if target > guess else "lower"
                    _result_banner(
                        "neutral",
                        "Keep scanning",
                        f"Try {hint}. Tries left: {st.session_state['guess_tries_left']}.",
                        "🔢",
                    )

        if st.button("Reset number round", key="guess-reset"):
            st.session_state["guess_target"] = rd.randint(1, 10)
            st.session_state["guess_tries_left"] = 3
            _result_banner("neutral", "Round reset", "Started a fresh number puzzle.", "🔢")

    with col2:
        st.metric("Total attempts", st.session_state["guess_attempts"])
        st.metric("Tries left", st.session_state["guess_tries_left"])
        _render_history("Number Guess", "guess_history")


def _quick_command_panel():
    st.markdown("---")
    st.subheader("Quick Command")
    st.markdown(
        '<p class="quick-hint">Use a shortcut button or type a command. Best for fast, low-friction control.</p>',
        unsafe_allow_html=True,
    )
    short1, short2, short3 = st.columns(3, gap="small")
    if short1.button("Help", key="quick-help", use_container_width=True):
        st.info("Try: help, stats, reset")
    if short2.button("Stats", key="quick-stats", use_container_width=True):
        st.markdown(
            f"**Total plays:** {st.session_state['stats_total']}  \n"
            f"**Wins:** {_total_wins()}  \n"
            f"**Luck index:** {_luck_index()}"
        )
    if short3.button("Reset", key="quick-reset", use_container_width=True):
        _reset_state()
        st.success("Session reset. Saved totals are still available.")

    with st.form("quick-command-form", clear_on_submit=True):
        raw = st.text_input("Type a command", placeholder="help, stats, reset")
        submitted = st.form_submit_button("Run command", use_container_width=True)

    if not submitted:
        return

    text = raw.strip()
    if not text:
        st.info("Enter a command to run.")
        return

    if text.lower() in ("reset", "clear"):
        _reset_state()
        st.success("Session reset. Saved totals are still available.")
        return

    action = handle_global_command(text, context="main_menu")

    if action == "help":
        st.info("Try: help, stats, reset")
    elif action == "stats":
        st.markdown(
            f"**Total plays:** {st.session_state['stats_total']}  \n"
            f"**Wins:** {_total_wins()}  \n"
            f"**Luck index:** {_luck_index()}"
        )
    elif action in ("menu", "quit"):
        st.warning(f"'{text}' is not used in Streamlit. Use the game picker above.")
    else:
        st.error(f"Unknown command: '{text}'. Try 'help'.")


def _sidebar() -> str:
    with st.sidebar:
        st.header("Game Menu")
        game = st.radio("Pick a challenge", list(GAMES.keys()), index=0, label_visibility="collapsed")
        st.caption(
            f"Rounds {st.session_state['stats_total']} | "
            f"Wins {_total_wins()} | Win rate {_luck_index()}"
        )

        st.markdown("---")
        st.header("Session Controls")
        st.button("Reset session", on_click=_reset_state, use_container_width=True)
        st.markdown(
            '<p class="sidebar-note">Clears local attempts and round history while preserving saved totals.</p>',
            unsafe_allow_html=True,
        )

        _quick_command_panel()

    return game


def _render_rulebook():
    st.markdown(
        """
        <div class="rulebook">
            <p class="rulebook-title">Starboard Rules</p>
            <p class="rulebook-copy">
                Every mission logs to your stats and flight log.
                Keep this nearby when switching sectors.
            </p>
            <ul class="rulebook-list">
                <li>Dice Roll: win if your number matches the roll.</li>
                <li>Coin Flip: win if the coin matches your call.</li>
                <li>Rock Paper Scissors: ties are neutral and not logged as wins/losses.</li>
                <li>Meteor Dodge: win if your lane is different from the meteor lane.</li>
                <li>Planet Guess: win only on an exact orbit match.</li>
                <li>Number Guess: win by finding the number in 3 tries.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    _apply_theming()
    _init_state()
    game = _sidebar()
    _header(game)
    _stats_bar()
    st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)
    _mission_brief(game)

    if game == "Dice Roll":
        _game_dice()
    elif game == "Coin Flip":
        _game_coin()
    elif game == "Rock Paper Scissors":
        _game_rps()
    elif game == "Meteor Dodge":
        _game_meteor()
    elif game == "Planet Guess":
        _game_planet()
    else:
        _game_number_guess()

    st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.08, 0.92], gap="large")
    with col1:
        _activity_feed_panel()
    with col2:
        _render_rulebook()


if __name__ == "__main__":
    main()
