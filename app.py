import random as rd
import streamlit as st

st.set_page_config(page_title="Luck Arcade", page_icon="🪐", layout="wide")


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


def _apply_theming():
    st.markdown(
        """
        <style>
        :root {
            --astro-primary: #8ef5ff;
            --astro-secondary: #ff8fd2;
            --astro-panel: rgba(13, 17, 34, 0.7);
            --astro-border: rgba(255,255,255,0.25);
            --astro-glow: 0 0 25px rgba(142,245,255,0.35);
        }

        main {
            background: radial-gradient(circle at 20% 20%, rgba(142,245,255,0.18), transparent 35%),
                        radial-gradient(circle at 80% 10%, rgba(255,143,210,0.08), transparent 30%),
                        linear-gradient(180deg, #020617 0%, #050b1c 45%, #070d25 100%);
            color: #f0f6ff;
        }

        body {
            background-color: #01030b;
        }

        section[data-testid="stSidebar"] {
            background: rgba(2, 6, 20, 0.9);
            border-right: 1px solid rgba(255,255,255,0.08);
            animation: glow 12s ease-in-out infinite alternate;
        }

        .arcade-card {
            padding: 1.25rem 1.5rem;
            border-radius: 18px;
            background: var(--astro-panel);
            border: 1px solid var(--astro-border);
            box-shadow: 0 20px 40px rgba(3, 6, 20, 0.5);
            position: relative;
            overflow: hidden;
        }

        .arcade-card::before {
            content: "";
            position: absolute;
            inset: -40% -40%;
            background: conic-gradient(
                from 180deg,
                rgba(142,245,255,0.04),
                rgba(255,143,210,0.08),
                rgba(142,245,255,0.04)
            );
            animation: spin 18s linear infinite;
        }
        .arcade-card > * { position: relative; z-index: 1; }

        .starfield {
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.7), transparent),
                radial-gradient(1px 1px at 80% 30%, rgba(255,255,255,0.6), transparent),
                radial-gradient(1px 1px at 50% 80%, rgba(255,255,255,0.5), transparent),
                radial-gradient(1px 1px at 30% 60%, rgba(255,255,255,0.5), transparent);
            animation: drift 40s linear infinite;
            opacity: 0.45;
        }

        .sparkline {
            position: relative;
            width: 100%;
        }

        .sparkline::after {
            content: "";
            position: absolute;
            inset: 0;
            background: url('data:image/svg+xml;utf8,<svg width="80" height="80" xmlns="http://www.w3.org/2000/svg"><circle cx="40" cy="40" r="1" fill="rgba(255,255,255,0.3)" /><circle cx="20" cy="60" r="1" fill="rgba(255,255,255,0.25)" /><circle cx="60" cy="20" r="1" fill="rgba(255,255,255,0.2)" /></svg>');
            mix-blend-mode: lighten;
            opacity: 0.5;
            pointer-events: none;
        }

        .stButton>button {
            border-radius: 999px;
            border: 1px solid rgba(142, 245, 255, 0.5);
            background: linear-gradient(120deg, rgba(142,245,255,0.16), rgba(255,143,210,0.16));
            color: #f8fbff;
            box-shadow: var(--astro-glow);
        }

        h1, h2, h3, h4 {
            color: #f8fbff;
        }

        .astro-chip {
            display: inline-flex;
            align-items: center;
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(142, 245, 255, 0.12);
            gap: 0.35rem;
            font-size: 0.85rem;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        @keyframes drift {
            to { transform: translate3d(-10%, -10%, 0); }
        }
        @keyframes glow {
            from { box-shadow: 0 0 18px rgba(142,245,255,0.15); }
            to   { box-shadow: 0 0 28px rgba(255,143,210,0.2); }
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
    st.markdown('<div class="starfield"></div>', unsafe_allow_html=True)
    st.title("Luck Arcade 🌌")
    st.markdown(
        """
        Command the Nebula Arcade, pick a cosmic challenge, and see if the stars align.
        """
    )


def _stats_bar():
    total = st.session_state["stats_total"]
    metrics = [
        ("Total Plays", total),
        ("Dice", f"{st.session_state['stats_dice_win']} / {st.session_state['stats_dice_loss']}"),
        ("Coin Flip", f"{st.session_state['stats_coin_win']} / {st.session_state['stats_coin_loss']}"),
        ("Rock Paper Scissors", f"{st.session_state['stats_rps_win']} / {st.session_state['stats_rps_loss']}"),
        ("Meteor Dodge", f"{st.session_state['stats_meteor_win']} / {st.session_state['stats_meteor_loss']}"),
        ("Planet Guess", f"{st.session_state['stats_planet_win']} / {st.session_state['stats_planet_loss']}"),
    ]
    cols = st.columns(len(metrics), gap="small")
    for col, (label, value) in zip(cols, metrics):
        col.metric(label, value)


def _render_history(title: str, history_key: str):
    history = st.session_state[history_key]
    if not history:
        st.info("No rounds played yet. Try a game!")
        return
    st.markdown(f"**Recent rounds — {title}:**")
    for item in history:
        st.markdown(f"- {item}")


def _game_dice():
    st.subheader("Dice Roll")
    with st.container():
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("Predict a number between 1 and 6. Roll and see if you nail it.")
            prediction = st.slider("Your prediction", 1, 6, 3)
            if st.button("Roll the die", key="dice-roll"):
                st.session_state["dice_attempts"] += 1
                roll = rd.randint(1, 6)
                outcome = "win" if roll == prediction else "loss"
                _record_result("dice", outcome, f"Predicted {prediction}, rolled {roll}")
                st.success(f"You rolled a {roll} — {'Win!' if outcome == 'win' else 'Not this time.'}")
        with col2:
            st.markdown("Attempts")
            st.metric("Total attempts", st.session_state["dice_attempts"])
            _render_history("Dice", "dice_history")


def _game_coin():
    st.subheader("Coin Flip")
    with st.container():
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("Pick Heads or Tails, then flip the coin.")
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
                st.info(f"Coin shows {result} — {'Win!' if outcome == 'win' else 'Try again.'}")
        with col2:
            st.markdown("Attempts")
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
    st.subheader("Rock Paper Scissors")
    choices = ["Rock", "Paper", "Scissors"]
    with st.container():
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("Choose your weapon and battle the computer.")
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
                    st.warning(f"It's a tie! {detail}")
                elif result == "win":
                    st.success(f"You win! {detail}")
                else:
                    st.info(f"You lose. {detail}")
                if result != "tie":
                    _record_result("rps", result, detail)
        with col2:
            st.markdown("Attempts")
            st.metric("Total attempts", st.session_state["rps_attempts"])
            _render_history("Rock Paper Scissors", "rps_history")


def _game_meteor():
    st.subheader("Meteor Dodge")
    with st.container():
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("Pick a lane and hope the meteor shower misses you.")
            lane = st.segmented_control("Your lane", options=["Left", "Center", "Right"], default="Center")
            if st.button("Engage thrusters", key="meteor-play"):
                st.session_state["meteor_attempts"] += 1
                incoming = rd.choice(["Left", "Center", "Right"])
                outcome = "loss" if incoming == lane else "win"
                detail = f"Lane: {lane} | Meteor: {incoming}"
                if outcome == "win":
                    st.success(f"Safe! The meteor streaked through {incoming}.")
                else:
                    st.warning(f"Direct hit in {incoming}! Hull integrity compromised.")
                _record_result("meteor", outcome, detail)
        with col2:
            st.markdown("Attempts")
            st.metric("Total attempts", st.session_state["meteor_attempts"])
            _render_history("Meteor Dodge", "meteor_history")


def _game_planet():
    st.subheader("Planet Guess")
    with st.container():
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("Scan the system and guess which orbit hides the target planet (1–8).")
            guess = st.slider("Your scan orbit", 1, 8, 4)
            if st.button("Ping the planet", key="planet-play"):
                st.session_state["planet_attempts"] += 1
                target = rd.randint(1, 8)
                outcome = "win" if target == guess else "loss"
                detail = f"Guessed {guess}, target was {target}"
                if outcome == "win":
                    st.balloons()
                    st.success("Direct lock! Planet found.")
                else:
                    hint = "higher" if target > guess else "lower"
                    st.info(f"No signal on orbit {guess}. Try {hint}.")
                _record_result("planet", outcome, detail)
        with col2:
            st.markdown("Attempts")
            st.metric("Total attempts", st.session_state["planet_attempts"])
            _render_history("Planet Guess", "planet_history")


def _sidebar():
    with st.sidebar:
        st.header("Mission Control")
        game = st.radio(
            "Pick a cosmic challenge",
            ["Dice Roll", "Coin Flip", "Rock Paper Scissors", "Meteor Dodge", "Planet Guess"],
            index=0,
        )
        st.markdown("---")
        st.header("Session")
        st.button("Reset session", on_click=_reset_state, use_container_width=True)
        st.caption("Clears attempts, history, and gives the arcade a fresh orbit.")
    return game


def main():
    _apply_theming()
    _init_state()
    game = _sidebar()
    _header()
    _stats_bar()
    st.markdown("---")

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

    st.markdown("---")
    st.markdown(
        "Need rules? Dice: match your number on a six-sided die. Coin Flip: pick Heads or Tails. Rock Paper Scissors: Rock beats Scissors, Scissors beats Paper, Paper beats Rock. "
        "Meteor Dodge: choose a lane; dodge the incoming meteor. Planet Guess: pick the orbit (1–8) to find the hidden world."
    )


if __name__ == "__main__":
    main()
