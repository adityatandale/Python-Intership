"""
Guess the Number Game - Streamlit App
Task 2

The program picks a random number in a range, the user guesses, and gets
"higher"/"lower" hints until they find it. Tracks number of attempts.

Run with:
    pip install streamlit
    streamlit run guess_number.py
"""

import streamlit as st
import random

st.set_page_config(page_title="Guess the Number", page_icon="🎯", layout="centered")

DIFFICULTIES = {
    "Easy (1-50)": (1, 50),
    "Medium (1-100)": (1, 100),
    "Hard (1-500)": (1, 500),
}

# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------

def start_new_game(low: int, high: int):
    st.session_state.low = low
    st.session_state.high = high
    st.session_state.target = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.won = False
    st.session_state.game_started = True


if "game_started" not in st.session_state:
    st.session_state.game_started = False

# ---------------------------------------------------------------------------
# Title + instructions
# ---------------------------------------------------------------------------

st.title("🎯 Guess the Number")
st.write(
    "I'm thinking of a number. Guess it, and I'll tell you if you need to "
    "go higher or lower. Try to find it in as few attempts as possible."
)

# ---------------------------------------------------------------------------
# Setup screen
# ---------------------------------------------------------------------------

if not st.session_state.game_started:
    st.subheader("Choose a difficulty")
    difficulty = st.radio("Range", list(DIFFICULTIES.keys()), index=1)
    if st.button("▶️ Start Game", type="primary"):
        low, high = DIFFICULTIES[difficulty]
        start_new_game(low, high)
        st.rerun()

# ---------------------------------------------------------------------------
# Active game screen
# ---------------------------------------------------------------------------

else:
    low, high = st.session_state.low, st.session_state.high
    st.info(f"Guess a number between **{low}** and **{high}**.")

    if not st.session_state.won:
        with st.form("guess_form", clear_on_submit=True):
            guess_input = st.text_input("Your guess")
            submitted = st.form_submit_button("Guess")

        if submitted:
            # Input validation
            if not guess_input.strip():
                st.warning("Enter a number before guessing.")
            else:
                try:
                    guess = int(guess_input)
                except ValueError:
                    st.error(f"'{guess_input}' isn't a whole number. Try again.")
                else:
                    if guess < low or guess > high:
                        st.warning(f"Stay within the range {low}-{high}.")
                    else:
                        st.session_state.attempts += 1

                        if guess == st.session_state.target:
                            st.session_state.won = True
                            st.session_state.history.append((guess, "Correct! 🎉"))
                        elif guess < st.session_state.target:
                            st.session_state.history.append((guess, "Higher ⬆️"))
                        else:
                            st.session_state.history.append((guess, "Lower ⬇️"))

        st.metric("Attempts so far", st.session_state.attempts)

    else:
        st.success(
            f"🎉 Correct! The number was **{st.session_state.target}**. "
            f"You got it in **{st.session_state.attempts}** attempt"
            f"{'s' if st.session_state.attempts != 1 else ''}."
        )

    # Guess history
    if st.session_state.history:
        st.subheader("Guess history")
        for i, (g, result) in enumerate(st.session_state.history, start=1):
            st.write(f"{i}. Guessed **{g}** → {result}")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Play again (same range)"):
            start_new_game(low, high)
            st.rerun()
    with col2:
        if st.button("⚙️ Change difficulty"):
            st.session_state.game_started = False
            st.rerun()
