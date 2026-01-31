import random as rd
import streamlit as st

st.set_page_config(page_title="Luck Arcade", page_icon="🎲", layout="wide")

st.title('Luck Arcade 🎯')

#Once a win a col animation and a buttn that says continue


def _init_state():
    defaults = {
        "stats_total": 0,
        "stats_dice_win": 0,
        "stats_dice_loss": 0,
        "stats_coin_win": 0,
        "stats_coin_loss": 0,
        "stats_rps_win": 0,
        "stats_rps_loss": 0,
        "dice_attempts": 0,
        "coin_attempts": 0,
        "rps_attempts": 0,
        "dice_history": [],
        "coin_history": [],
        "rps_history": [],
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
            --arcade-primary: #7b5cf1;
            --arcade-secondary: #18c29c;
            --arcade-bg: #0f172a;
            --arcade-card: rgba(255,255,255,0.06);
        }
        .main {
            background: radial-gradient(circle at 10% 20%, rgba(123,92,241,0.08), transparent 25%),
                        radial-gradient(circle at 90% 10%, rgba(24,194,156,0.08), transparent 25%),
                        linear-gradient(135deg, #0b1224 0%, #0f172a 50%, #0b1224 100%);
            color: #e2e8f0;
        }
        section[data-testid="stSidebar"] {
            background: #0b1020;
        }
        .arcade-card {
            padding: 1rem 1.25rem;
            border-radius: 14px;
            background: var(--arcade-card);
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        }
        .arcade-chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.1);
            font-size: 0.85rem;
        }
        h1, h2, h3, h4 { color: #e5e7eb; }
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
    st.title("Luck Arcade 🎯")
    st.markdown(
        "Choose a game, make your prediction, and see if luck is on your side."
    )


def _stats_bar():
    total = st.session_state["stats_total"]
    cols = st.columns(4, gap="medium")
    cols[0].metric("Total Plays", total)
    cols[1].metric(
        "Dice",
        f"{st.session_state['stats_dice_win']} win / {st.session_state['stats_dice_loss']} loss",
    )
    cols[2].metric(
        "Coin Flip",
        f"{st.session_state['stats_coin_win']} win / {st.session_state['stats_coin_loss']} loss",
    )
    cols[3].metric(
        "Rock Paper Scissors",
        f"{st.session_state['stats_rps_win']} win / {st.session_state['stats_rps_loss']} loss",
    )


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


def _sidebar():
    with st.sidebar:
        st.header("Games")
        game = st.radio(
            "Choose a game",
            ["Dice Roll", "Coin Flip", "Rock Paper Scissors"],
            index=0,
        )
        st.markdown("---")
        st.header("Session")
        st.button("Reset session", on_click=_reset_state, use_container_width=True)
        st.caption("Reset clears attempts and recent history.")
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
    else:
        _game_rps()

    st.markdown("---")
    st.markdown(
        "Need rules? Dice: match your number on a six-sided die. Coin Flip: pick Heads or Tails. Rock Paper Scissors: Rock beats Scissors, Scissors beats Paper, Paper beats Rock."
    )


if __name__ == "__main__":
    main()


