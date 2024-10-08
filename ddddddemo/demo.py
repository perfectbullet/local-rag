import streamlit as st


uploaded_file = st.file_uploader("选择文集那", help='helphelphelphelphelphelp')
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)
