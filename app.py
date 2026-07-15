import pathlib

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Race: Haiti Bus vs World",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit's default chrome so the game canvas gets the full viewport.
st.markdown(
    """
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
        iframe {height: 100vh !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

HTML_PATH = pathlib.Path(__file__).parent / "game.html"
game_html = HTML_PATH.read_text(encoding="utf-8")

components.html(game_html, height=900, scrolling=False)
