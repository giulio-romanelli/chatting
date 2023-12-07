# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
from pygame import mixer
from openai import OpenAI
import streamlit as st
from streamlit.logger import get_logger
import time
import os

##-------------------------------------------------------------------------------------##
## playAudio
##-------------------------------------------------------------------------------------##   
def playAudio(filename, background=False):

    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()
    while not background:
        if mixer.music.get_busy() == False:
            #mixer.quit()
            break

##-------------------------------------------------------------------------------------##
## stopAudio
##-------------------------------------------------------------------------------------##   
def stopAudio( ):
    if mixer.get_init():
        mixer.music.stop()
        mixer.quit()

##-------------------------------------------------------------------------------------##
## textToSpeechGoogle
##-------------------------------------------------------------------------------------##
def textToSpeechGoogle(text, filename, language="en"):

    # Check audio file is not open
    while True:
        try:
            myfile = open(filename, "wb")
            break                             
        except IOError:
            stopAudio( )

    speech = gTTS(text, lang=language)
    speech.save(filename)




LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Chatting",
        page_icon="👋",
    )

    st.markdown("""
      <style>
      div.stSpinner > div {
        text-align:center;
        align-items: center;
        justify-content: center;
      }
      </style>""", unsafe_allow_html=True)

    # Initiatlize environment
    if 'k' not in st.session_state:
        st.session_state['k'] = str(0)

    # Initialize session
    st.title("Chat")
    withAudio = st.sidebar.toggle('Audio')
    withMic = st.sidebar.toggle('Mic')
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat prompt
    prompt = ""
    prompt = st.chat_input("Write here...")

    if prompt:

        # Chat message question
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
        # Commands
        question = prompt
        answer = "Great to interact with you!"
        
        # Chat message answer
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
        if ( question == "/sentiment" ): st.image('Experience.png')
        
        # Store results
        if ( 'k' in st.session_state ):
            st.session_state['k'] = str(int(st.session_state['k']) + 1)


if __name__ == "__main__":
    run()
