import streamlit as st

from components.tabs.about import about
from components.tabs.sources import sources
from components.tabs.settings import settings


def sidebar():

    with st.sidebar:
        with st.container(border=True):
            sources()


        settings()
