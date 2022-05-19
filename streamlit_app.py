from collections import namedtuple
import os
from time import sleep
import altair as alt
import math
import pandas as pd
import streamlit as st
from gtts import gTTS
import base64
#from script.py import foo 

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


myobj = gTTS(text="Bak Bouk", lang='en', slow=True)
myobj.save("welcome.mp3")

audio_file = open('welcome.mp3', 'rb')
audio_bytes = audio_file.read()

#st.audio(audio_bytes, format='audio/mp3')

mymidia_placeholder = st.empty()

mymidia_str = "data:audio/ogg;base64,%s"%(base64.b64encode(audio_bytes).decode())
mymidia_html = """
                <audio autoplay class="stAudio">
                <source src="%s" type="audio/ogg">
                Your browser does not support the audio element.
                </audio>
            """%mymidia_str

mymidia_placeholder.empty()
sleep(1)
mymidia_placeholder.markdown(mymidia_html, unsafe_allow_html=True)

picture = st.camera_input("Take a picture")

if picture:
     st.image(picture)
