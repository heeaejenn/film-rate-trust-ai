import streamlit as st
from st_clickable_images import clickable_images

clicked = clickable_images(
    [
        "https://github.com/heeaejenn/film-rate-trust-ai/blob/heeae_streamlit/data/movie_poster/blank_space.png"
    ],
    titles=['blankspace'],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "5px", "height": "200px"},
)

#st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")
if st.button(clicked):
    st.switch_page("pages/notebook.py")