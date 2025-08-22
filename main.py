import streamlit as st
import random
import json
import os
from PIL import Image

from image_to_base64_converter import convert_image_to_base64

icon = Image.open("images/logo.png")

st.set_page_config(
    page_title="Bonn Cricket Club",
    page_icon=icon,
    layout='wide',
)

image_base64 = convert_image_to_base64()

left_co, cent_co, right_co = st.columns([1, 2, 1])
with cent_co:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{image_base64}" width="120">
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    "<h1 style='text-align: center;'>BMC Match Draw</h1>",
    unsafe_allow_html=True
)


FILE = "cards_state.json"

# Load or create state
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        state = json.load(f)
        numbers = state["numbers"]
        revealed = state["revealed"]
        team_names = state.get("team_names", [""] * len(numbers))
else:
    numbers = random.sample(range(1, 9), 8)   # 8 unique numbers
    revealed = [False] * 8
    team_names = [""] * 8
    with open(FILE, "w") as f:
        json.dump({"numbers": numbers, "revealed": revealed, "team_names": team_names}, f)

# CSS for proper flip card
st.markdown("""
<style>
.card-container {
    perspective: 1000px;
    display: inline-block;
    margin: 10px;
}
.card {
    width: 140px;
    height: 180px;
    border-radius: 15px;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 0.6s;
    cursor: pointer;
}
.card.revealed {
    transform: rotateY(180deg);
}
.card-face {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 22px;
    font-weight: bold;
    backface-visibility: hidden;
    text-align: center;
    padding: 10px;
}
.card-front {
    background-color: #4B0082; /* Dark Purple */
    color: white;
}
.card-back {
    background-color: #d3f8d3;
    color: black;
    transform: rotateY(180deg);
}
</style>
""", unsafe_allow_html=True)

# Save card info after team name is entered
def save_card(i, team_name):
    revealed[i] = True
    team_names[i] = team_name
    with open(FILE, "w") as f:
        json.dump({"numbers": numbers, "revealed": revealed, "team_names": team_names}, f)
    st.rerun()

# Display cards in 2 rows of 4
for row in range(2):
    cols = st.columns(4)
    for col in range(4):
        i = row * 4 + col
        if i >= 8:
            continue
        with cols[col]:
            with st.form(key=f"form_{i}"):
                # Always show input + button
                team_name = st.text_input("Enter team name", value=team_names[i], key=f"name_{i}")
                tap = st.form_submit_button("Tap here")
                if tap and team_name.strip():
                    save_card(i, team_name.strip())

                # Show card (revealed/unrevealed)
                flipped_class = "card revealed" if revealed[i] else "card"
                card_content = f"{numbers[i]}<br><small>{team_names[i]}</small>" if revealed[i] else ""

                # Front: show logo, Back: show number + team name
                st.markdown(f"""
                <div class="card-container">
                    <div class="{flipped_class}">
                        <div class="card-face card-front">
                            <img src="data:image/png;base64,{image_base64}" width="60">
                        </div>
                        <div class="card-face card-back">{card_content}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
