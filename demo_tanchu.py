import streamlit as st
from streamlit_modal import Modal

# 定义modal
modal = Modal(
    "Demo Modal",
    key="demo-modal",

    # Optional
    padding=20,  # default value
    max_width=744  # default value
)

open_modal = st.button("Open")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        st.write("Text goes here")

        st.write("Some fancy text")
        value = st.checkbox("Check me")
        st.write(f"Checkbox checked: {value}")