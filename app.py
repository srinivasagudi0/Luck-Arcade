import random as rd
from html import escape

import streamlit as st

st.set_page_config(page_title="Luck Arcade", page_icon="🎰", layout="wide")

GAMES = {
    "Dice Roll": "dice",
    "Coin Flip": "coin",
    "Rock Paper Scissors": "rps",
    "Meteor Dodge": "meteor",
    "Planet Guess": "planet",
}


def _init_state():
    defaults = {
        "stats_total": 0,
        "stats_dice_win": 0,
        "stats_dice_loss": 0,
        "stats_coin_win": 0,
        "stats_coin_loss": 0,
        "stats_rps_win": 0,
        "stats_rps_loss": 0,
        "stats_meteor_win": 0,
        "stats_meteor_loss": 0,
        "stats_planet_win": 0,
        "stats_planet_loss": 0,
        "dice_attempts": 0,
        "coin_attempts": 0,
        "rps_attempts": 0,
        "meteor_attempts": 0,
        "planet_attempts": 0,
        "dice_history": [],
        "coin_history": [],
        "rps_history": [],
        "meteor_history": [],
        "planet_history": [],
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def _reset_state():
    for key in list(st.session_state.keys()):
        if key.startswith("stats_") or key.endswith("_history") or key.endswith("_attempts"):
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


def _total_wins() -> int:
    return sum(_wins(game_key) for game_key in GAMES.values())


def _luck_index() -> str:
    total = st.session_state["stats_total"]
    if total == 0:
        return "0%"
    return f"{round((_total_wins() / total) * 100)}%"


def _apply_theming():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

        :root {
            --arc-ink: #11231d;
            --arc-muted: #35564d;
            --arc-paper: rgba(255, 252, 245, 0.78);
            --arc-edge: rgba(17, 35, 29, 0.14);
            --arc-green: #0b8a67;
            --arc-gold: #c68015;
            --arc-sea: #0f6a89;
            --arc-shadow: 0 18px 40px rgba(17, 35, 29, 0.12);
        }

        html, body, [class*="css"] {
            font-family: "Bricolage Grotesque", sans-serif;
            color: var(--arc-ink);
        }

        .stApp {
            background:
                radial-gradient(circle at 18% 18%, rgba(11, 138, 103, 0.22) 0%, transparent 40%),
                radial-gradient(circle at 86% 8%, rgba(198, 128, 21, 0.24) 0%, transparent 37%),
                linear-gradient(145deg, #f4efe4 0%, #f4f2ea 45%, #e5efe8 100%);
        }

        .arcade-backdrop {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: -2;
            opacity: 0.52;
            background:
                linear-gradient(90deg, rgba(17, 35, 29, 0.06) 1px, transparent 1px),
                linear-gradient(0deg, rgba(17, 35, 29, 0.06) 1px, transparent 1px);
            background-size: 34px 34px;
        }

        .arcade-noise {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: -1;
            opacity: 0.17;
            mix-blend-mode: soft-light;
            background-image: radial-gradient(rgba(0, 0, 0, 0.32) 0.7px, transparent 0.7px);
            background-size: 2px 2px;
        }

        .main .block-container {
            max-width: 1260px;
            padding-top: 1.35rem;
            padding-bottom: 2.2rem;
        }

        .hero {
            position: relative;
            overflow: hidden;
            border-radius: 22px;
            border: 1px solid var(--arc-edge);
            background:
                linear-gradient(120deg, rgba(255, 252, 245, 0.9), rgba(244, 252, 248, 0.84)),
                linear-gradient(210deg, rgba(11, 138, 103, 0.15), rgba(198, 128, 21, 0.14));
            box-shadow: var(--arc-shadow);
            padding: 1.6rem 1.6rem 1.35rem;
            margin-bottom: 1rem;
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: auto -22% -70% auto;
            width: 340px;
            height: 340px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(11, 138, 103, 0.22), transparent 67%);
            animation: arcPulse 9s ease-in-out infinite;
        }

        .hero-kicker {
            margin: 0;
            color: var(--arc-green);
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-weight: 800;
            font-size: 0.79rem;
        }

        .hero-title {
            margin: 0.3rem 0 0.45rem;
            font-size: clamp(2rem, 4vw, 3.2rem);
            line-height: 1.06;
            letter-spacing: -0.02em;
            color: var(--arc-ink);
        }

        .hero-copy {
            margin: 0;
            max-width: 900px;
            color: var(--arc-muted);
            font-size: 1.03rem;
            line-height: 1.4;
        }

        .hero-row {
            margin-top: 0.9rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
        }

        .hero-chip {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            border: 1px solid var(--arc-edge);
            background: rgba(255, 252, 245, 0.9);
            color: #17342c;
            padding: 0.28rem 0.72rem;
            font-size: 0.82rem;
            font-weight: 700;
            box-shadow: 0 4px 14px rgba(17, 35, 29, 0.09);
        }

        .score-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 0.72rem;
            margin: 0.5rem 0 0.95rem;
        }

        .score-card {
            border-radius: 16px;
            border: 1px solid var(--arc-edge);
            padding: 0.88rem 0.95rem 0.9rem;
            background: var(--arc-paper);
            box-shadow: var(--arc-shadow);
        }

        .score-label {
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 0.11em;
            font-size: 0.68rem;
            font-weight: 800;
            color: #3f5b53;
        }

        .score-value {
            margin: 0.34rem 0 0.2rem;
            color: #10251f;
            font-size: 1.3rem;
            font-weight: 800;
            line-height: 1;
        }

        .score-sub {
            margin: 0;
            color: #4b665e;
            font-size: 0.76rem;
            font-weight: 600;
            letter-spacing: 0.03em;
        }

        .game-heading {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 0.9rem;
        }

        .game-icon {
            width: 46px;
            height: 46px;
            border-radius: 13px;
            display: grid;
            place-items: center;
            font-size: 1.42rem;
            background: linear-gradient(140deg, rgba(11, 138, 103, 0.82), rgba(15, 106, 137, 0.74));
            box-shadow: 0 9px 18px rgba(11, 138, 103, 0.22);
        }

        .game-title {
            margin: 0;
            color: #10251f;
            font-size: clamp(1.45rem, 2.6vw, 1.88rem);
            line-height: 1.05;
            letter-spacing: -0.01em;
        }

        .game-subtitle {
            margin: 0.25rem 0 0;
            color: #46635a;
            font-size: 0.95rem;
        }

        .stButton > button {
            border-radius: 999px;
            border: 1px solid rgba(17, 35, 29, 0.2);
            color: #17342c;
            background: linear-gradient(120deg, rgba(11, 138, 103, 0.3), rgba(198, 128, 21, 0.34));
            font-weight: 800;
            letter-spacing: 0.01em;
            box-shadow: 0 8px 18px rgba(17, 35, 29, 0.15);
            transition: transform 150ms ease, box-shadow 180ms ease, filter 180ms ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            filter: saturate(1.1);
            box-shadow: 0 12px 24px rgba(17, 35, 29, 0.18);
        }

        .stButton > button:focus {
            border-color: rgba(11, 138, 103, 0.7);
            box-shadow: 0 0 0 0.22rem rgba(11, 138, 103, 0.24);
        }

        div[data-testid="stMetric"] {
            border-radius: 15px;
            border: 1px solid var(--arc-edge);
            background: var(--arc-paper);
            padding: 0.76rem 0.95rem;
            box-shadow: 0 8px 20px rgba(17, 35, 29, 0.09);
        }

        div[data-testid="stMetricValue"] {
            color: #0f2922;
            font-weight: 800;
        }

        div[data-testid="stMetricLabel"] {
            color: #46635a;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            font-size: 0.69rem;
            font-weight: 700;
        }

        div[data-testid="stSlider"] [role="slider"] {
            background: var(--arc-ink) !important;
            border: 2px solid rgba(255, 255, 255, 0.9);
        }

        div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div:first-child {
            background: linear-gradient(90deg, var(--arc-green), var(--arc-gold));
            height: 0.5rem;
        }

        div[data-testid="stSegmentedControl"] div[role="radiogroup"] {
            gap: 0.4rem;
            background: rgba(255, 252, 245, 0.62);
            border: 1px solid var(--arc-edge);
            border-radius: 999px;
            padding: 0.34rem;
        }

        div[data-testid="stSegmentedControl"] label {
            border-radius: 999px;
            color: #315047;
            font-weight: 700;
            border: 1px solid rgba(17, 35, 29, 0.09);
            transition: background 120ms ease, color 120ms ease, transform 120ms ease;
        }

        div[data-testid="stSegmentedControl"] label:has(input:checked) {
            background: linear-gradient(120deg, rgba(11, 138, 103, 0.27), rgba(198, 128, 21, 0.28));
            color: #17342c;
            transform: translateY(-1px);
        }

        div[data-testid="stRadio"] > div {
            background: rgba(255, 252, 245, 0.62);
            border: 1px solid var(--arc-edge);
            border-radius: 14px;
            padding: 0.5rem 0.56rem;
        }

        div[data-testid="stRadio"] label p {
            color: #204239;
            font-weight: 700;
        }

        .history-card {
            border-radius: 16px;
            border: 1px solid var(--arc-edge);
            background: var(--arc-paper);
            box-shadow: var(--arc-shadow);
            padding: 0.9rem 1rem;
        }

        .history-title {
            margin: 0;
            color: #17342c;
            font-size: 0.89rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .history-card ul {
            margin: 0.54rem 0 0;
            padding-left: 1.08rem;
        }

        .history-card li {
            margin-bottom: 0.28rem;
            color: #2f4d45;
            font-family: "Space Mono", monospace;
            font-size: 0.82rem;
            line-height: 1.35;
        }

        .history-empty {
            border-radius: 14px;
            border: 1px dashed rgba(17, 35, 29, 0.2);
            background: rgba(255, 252, 245, 0.56);
            padding: 0.86rem 0.95rem;
            color: #44655c;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .section-break {
            height: 1px;
            margin: 1rem 0 1.15rem;
            background: linear-gradient(90deg, transparent, rgba(17, 35, 29, 0.25), transparent);
        }

        .rulebook {
            border: 1px solid var(--arc-edge);
            border-radius: 16px;
            background: var(--arc-paper);
            box-shadow: var(--arc-shadow);
            padding: 0.95rem 1rem;
            color: #315047;
            font-size: 0.89rem;
            line-height: 1.45;
        }

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(165deg, rgba(246, 240, 227, 0.95), rgba(232, 242, 236, 0.92)),
                linear-gradient(190deg, rgba(11, 138, 103, 0.14), rgba(198, 128, 21, 0.14));
            border-right: 1px solid rgba(17, 35, 29, 0.12);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p {
            color: #1d3c33;
        }

        .sidebar-note {
            color: #33584f;
            font-size: 0.83rem;
            line-height: 1.35;
            margin-top: 0.15rem;
        }

        @keyframes arcPulse {
            0%, 100% { transform: scale(1); opacity: 0.7; }
            50% { transform: scale(1.12); opacity: 0.96; }
        }

        @media (max-width: 900px) {
            .hero {
                padding: 1.2rem 1.15rem 1.1rem;
            }
            .score-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _record_result(game: str, outcome: str, detail: str):
    st.session_state["stats_total"] += 1
    st.session_state[f"stats_{game}_{outcome}"] += 1
    history_key = f"{game}_history"
    st.session_state[history_key].insert(0, detail)
    st.session_state[history_key] = st.session_state[history_key][:25]


def _header():
    st.markdown('<div class="arcade-backdrop"></div><div class="arcade-noise"></div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <section class="hero">
            <p class="hero-kicker">Luck Arcade Session</p>
            <h1 class="hero-title">Quick Arcade Rounds</h1>
            <p class="hero-copy">
                Roll, flip, duel, dodge, and guess. Stats update live while you play.
            </p>
            <div class="hero-row">
                <span class="hero-chip">Rounds: {st.session_state["stats_total"]}</span>
                <span class="hero-chip">Wins: {_total_wins()}</span>
                <span class="hero-chip">Luck: {_luck_index()}</span>
                <span class="hero-chip">Modes: 5</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _stats_bar():
    cards = [
        ("Total Plays", str(st.session_state["stats_total"]), "All games together"),
        ("Dice Roll", f"{_wins('dice')}W / {_losses('dice')}L", f"{_win_rate('dice')} win rate"),
        ("Coin Flip", f"{_wins('coin')}W / {_losses('coin')}L", f"{_win_rate('coin')} win rate"),
        ("Rock Paper Scissors", f"{_wins('rps')}W / {_losses('rps')}L", f"{_win_rate('rps')} win rate"),
        ("Meteor Dodge", f"{_wins('meteor')}W / {_losses('meteor')}L", f"{_win_rate('meteor')} win rate"),
        ("Planet Guess", f"{_wins('planet')}W / {_losses('planet')}L", f"{_win_rate('planet')} win rate"),
    ]
    cards_html = "".join(
        f"""
        <article class="score-card">
            <p class="score-label">{escape(label)}</p>
            <p class="score-value">{escape(value)}</p>
            <p class="score-sub">{escape(subtext)}</p>
        </article>
        """
        for label, value, subtext in cards
    )
    st.markdown(f'<section class="score-grid">{cards_html}</section>', unsafe_allow_html=True)


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


def _game_heading(icon: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="game-heading">
            <div class="game-icon">{escape(icon)}</div>
            <div>
                <h2 class="game-title">{escape(title)}</h2>
                <p class="game-subtitle">{escape(subtitle)}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _game_dice():
    _game_heading("🎲", "Dice Roll", "Pick a number from 1 to 6 and try to hit it.")
    col1, col2 = st.columns([1.05, 0.95], gap="large")
    with col1:
        st.markdown("Pick your number, then roll once.")
        prediction = st.slider("Your prediction", 1, 6, 3)
        if st.button("Roll the die", key="dice-roll"):
            st.session_state["dice_attempts"] += 1
            roll = rd.randint(1, 6)
            outcome = "win" if roll == prediction else "loss"
            _record_result("dice", outcome, f"Predicted {prediction}, rolled {roll}")
            st.success(f"Rolled {roll}. {'You got it.' if outcome == 'win' else 'Miss this round.'}")

    with col2:
        st.metric("Total attempts", st.session_state["dice_attempts"])
        _render_history("Dice Roll", "dice_history")


def _game_coin():
    _game_heading("🪙", "Coin Flip", "Call heads or tails and see what happens.")
    col1, col2 = st.columns([1.05, 0.95], gap="large")
    with col1:
        st.markdown("Pick a side, then flip.")
        choice = st.segmented_control(
            "Your call",
            options=["Heads", "Tails"],
            default="Heads",
        )
        if st.button("Flip coin", key="coin-flip"):
            st.session_state["coin_attempts"] += 1
            result = rd.choice(["Heads", "Tails"])
            outcome = "win" if result == choice else "loss"
            _record_result("coin", outcome, f"Called {choice}, got {result}")
            st.info(f"Coin: {result}. {'Nice call.' if outcome == 'win' else 'No luck this one.'}")

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
    _game_heading("✊", "Rock Paper Scissors", "Pick your move and face the computer.")
    choices = ["Rock", "Paper", "Scissors"]
    col1, col2 = st.columns([1.05, 0.95], gap="large")
    with col1:
        st.markdown("Choose your move, then play one round.")
        user_choice = st.segmented_control(
            "Your choice",
            options=choices,
            default="Rock",
        )
        if st.button("Play", key="rps-play"):
            st.session_state["rps_attempts"] += 1
            comp_choice = rd.choice(choices)
            result = _rps_winner(user_choice, comp_choice)
            detail = f"You: {user_choice} | Computer: {comp_choice}"
            if result == "tie":
                st.warning(f"Tie round. {detail}")
            elif result == "win":
                st.success(f"You win this round. {detail}")
            else:
                st.info(f"Computer wins this round. {detail}")
            if result != "tie":
                _record_result("rps", result, detail)

    with col2:
        st.metric("Total attempts", st.session_state["rps_attempts"])
        _render_history("Rock Paper Scissors", "rps_history")


def _game_meteor():
    _game_heading("☄️", "Meteor Dodge", "Pick a lane and hope the meteor misses.")
    col1, col2 = st.columns([1.05, 0.95], gap="large")
    with col1:
        st.markdown("Pick a lane, then fire thrusters.")
        lane = st.segmented_control("Your lane", options=["Left", "Center", "Right"], default="Center")
        if st.button("Engage thrusters", key="meteor-play"):
            st.session_state["meteor_attempts"] += 1
            incoming = rd.choice(["Left", "Center", "Right"])
            outcome = "loss" if incoming == lane else "win"
            detail = f"Lane: {lane} | Meteor: {incoming}"
            if outcome == "win":
                st.success(f"Safe. Meteor came through {incoming}.")
            else:
                st.warning(f"Hit. Meteor came through {incoming}.")
            _record_result("meteor", outcome, detail)

    with col2:
        st.metric("Total attempts", st.session_state["meteor_attempts"])
        _render_history("Meteor Dodge", "meteor_history")


def _game_planet():
    _game_heading("🪐", "Planet Guess", "Guess the hidden planet from orbit 1 to 8.")
    col1, col2 = st.columns([1.05, 0.95], gap="large")
    with col1:
        st.markdown("Set your orbit guess, then ping.")
        guess = st.slider("Your scan orbit", 1, 8, 4)
        if st.button("Ping the planet", key="planet-play"):
            st.session_state["planet_attempts"] += 1
            target = rd.randint(1, 8)
            outcome = "win" if target == guess else "loss"
            detail = f"Guessed {guess}, target was {target}"
            if outcome == "win":
                st.balloons()
                st.success("You found it.")
            else:
                hint = "higher" if target > guess else "lower"
                st.info(f"Not orbit {guess}. Hint: try {hint}.")
            _record_result("planet", outcome, detail)

    with col2:
        st.metric("Total attempts", st.session_state["planet_attempts"])
        _render_history("Planet Guess", "planet_history")


def _sidebar():
    with st.sidebar:
        st.header("Game Menu")
        game = st.radio(
            "Pick a challenge",
            list(GAMES.keys()),
            index=0,
        )
        st.markdown("---")
        st.header("Session Controls")
        st.button("Reset session", on_click=_reset_state, use_container_width=True)
        st.markdown(
            '<p class="sidebar-note">Clears attempts, history, and all current session stats.</p>',
            unsafe_allow_html=True,
        )
    return game


def main():
    _apply_theming()
    _init_state()
    game = _sidebar()
    _header()
    _stats_bar()
    st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

    if game == "Dice Roll":
        _game_dice()
    elif game == "Coin Flip":
        _game_coin()
    elif game == "Meteor Dodge":
        _game_meteor()
    elif game == "Planet Guess":
        _game_planet()
    else:
        _game_rps()

    st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="rulebook">
            <strong>Rulebook:</strong>
            Dice Roll: win if your number matches the roll.
            Coin Flip: win if the coin matches your call.
            Rock Paper Scissors: ties are neutral and not logged as wins/losses.
            Meteor Dodge: win if your lane is different from the meteor lane.
            Planet Guess: win only on an exact orbit match.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
