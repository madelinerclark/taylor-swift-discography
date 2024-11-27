import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st

from src import streamlit_mods

streamlit_mods.increase_width()

def main():
    streamlit_mods.get_sidebar()
    content()

def content():
    st.image('assets/img/TTPDLogo.png')
    st.markdown(
        """
    # Welcome!

    This application represents an ongoing project to compile and analyze Taylor Swift's song discography as it exists on [Genius](https://genius.com/). Here you will find several different exploratory data analyses of different aspects of Taylor Swift's songs, including how and when they're released, who she creates her music with, and the traffic for each song on Genius. As Taylor releases more music, this application will grow.

    This project is completely open-source, not for profit, and free for public use; I only ask that you link back here and give credit!

    * Follow along with the project on [Github](https://github.com/madelinerclark/taylor-swift-discography)
    * Add the developer (me) on [LinkedIn](https://www.linkedin.com/in/madelinerclark/), [Bluesky](https://bsky.app/profile/madelinerclark.com), or check out [my personal website](https://madelinerclark.com/)
    """
    )

if __name__ == '__main__':
    main()
