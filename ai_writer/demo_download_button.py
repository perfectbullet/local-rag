import streamlit as st

binary_contents = b"example content"
# Defaults to "application/octet-stream"
st.download_button("Download binary file", binary_contents)