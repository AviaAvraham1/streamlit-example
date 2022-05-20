from collections import namedtuple
import os
from time import sleep
import altair as alt
import math
import pandas as pd
import streamlit as st
#from gtts import gTTS
import base64
#from script.py import foo 
from transformers import DetrFeatureExtractor, DetrForObjectDetection, pipeline
from PIL import Image
import requests
from pyzbar import pyzbar
import cv2
import numpy as np
from bidi.algorithm import get_display
from io import BytesIO
import gzip
import xml.etree.ElementTree as ET

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


#myobj = gTTS(text="Bak Bouk", lang='en', slow=True)
#myobj.save("welcome.mp3")

#audio_file = open('welcome.mp3', 'rb')
#audio_bytes = audio_file.read()

##st.audio(audio_bytes, format='audio/mp3')

#mymidia_placeholder = st.empty()

#mymidia_str = "data:audio/ogg;base64,%s"%(base64.b64encode(audio_bytes).decode())
#mymidia_html = """
#                <audio autoplay class="stAudio">
#                <source src="%s" type="audio/ogg">
#                Your browser does not support the audio element.
#                </audio>
#            """%mymidia_str

#mymidia_placeholder.empty()
#sleep(1)
#mymidia_placeholder.markdown(mymidia_html, unsafe_allow_html=True)

def read_barcodes(frame):
    if st.session_state.barcode == -1 :    
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            st.session_state.barcode = barcode.data.decode('utf-8')        



if 'barcode' not in st.session_state :
    st.session_state.barcode = -1
    

picture = st.camera_input("Take a picture")
#test = null;

if picture:
    st.image(picture)
    img = Image.open(picture)
    cv2_img = cv2.imdecode(np.frombuffer(picture.getbuffer(), np.uint8), cv2.IMREAD_COLOR)
    read_barcodes(cv2_img)
    if st.session_state.barcode == -1:
        model = pipeline("image-classification")
        arr = model(img)
        st.title(arr[0]['label'])
    else:
        r = requests.get('http://prices.shufersal.co.il/FileObject/UpdateCategory?catID=2&storeId=19')
        page = r.text
        startIdx = page.rfind('<a href')
        endIdx = page.find('"',startIdx+9)
        fileLink = page[startIdx+9:endIdx]
        fileLink= fileLink.replace('amp;','')
        # open file
        r2 = requests.get(fileLink)
        with gzip.open(BytesIO(r2.content)) as prices:
            tree = ET.parse(prices)
        # work on full price report XML
        root = tree.getroot()
        for item in root.find('Items'):
            if item.find('ItemCode').text == st.session_state.barcode:
                st.title(item.find('ItemName').text)
                st.title('מחיר ' + item.find('ItemPrice').text)
                st.title(item.find('Quantity').text + ' ' + item.find('UnitQty').text)

