"""Reusable modules for the Streamlit app"""

from datetime import date

import streamlit as st

def get_sidebar():
    """Additional sidebar image and description."""
    today = date(2024, 11, 27)
    today_format = today.strftime('%B %-d, %Y')
    
    with st.sidebar:
        st.image('assets/img/TheTorturedPoetsDepartment.jpg')
        st.markdown(f"""
        <h3 style="text-align: center;">Taylor Swift - Song Discography</h3>

        <p style="text-align: center;">This is an ongoing, open-source project. Follow along on <a href='https://github.com/madelinerclark/taylor-swift-discography'>Github</a>!</p>

        <p style="text-align: center;">Data was last updated on <b>{today_format}</b>.</p>
        
        """, unsafe_allow_html=True)

def increase_width():
    """Increases width of main section of app."""
    st.markdown(
        """
        <style>
            section.main > div {max-width:65rem}
        </style>
        """,
        unsafe_allow_html=True
    )