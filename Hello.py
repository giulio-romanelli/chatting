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
#import pyaudio
import base64
import wave
#from pygame import mixer
from openai import OpenAI
from gtts import gTTS
import streamlit as st
from streamlit.logger import get_logger
import time
import os
#from array import array
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
#from docx import Document
#from audio_recorder_streamlit import audio_recorder
import math
#import datetime
from streamlit_mic_recorder import mic_recorder

##-------------------------------------------------------------------------------------##
## OpenAI
##-------------------------------------------------------------------------------------## 
#os.environ['OPENAI_API_KEY'] = 'xxx'

##-------------------------------------------------------------------------------------##
## chatBot
##-------------------------------------------------------------------------------------##
def chatBot(input):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "Sei un assistente virtuale. Rispondi al massimo con 50 parole"},
        #{"role": "system", "content": "You are the best children story author in the world. Write a story about this topic"},
        {"role": "user", "content": input}
        ]
    )
    return(completion.choices[0].message.content)

##-------------------------------------------------------------------------------------##
## summarizeBot
##-------------------------------------------------------------------------------------##
def summarizeBot(input):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "Riassumi il testo fornito"},
        {"role": "user", "content": input}
        ]
    )
    return(completion.choices[0].message.content)

##-------------------------------------------------------------------------------------##
## sentimentAnalysis
##-------------------------------------------------------------------------------------##
def sentimentAnalysis(transcript):
    content = f"What emotion is the following text expressing?\n{transcript}"
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful assistant. Answer with one word choosing between Positive, Neutral, Negative"},
        {"role": "user", "content": content}
        ]
    )
    return(completion.choices[0].message.content)

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
## playAudioEmbedded
##-------------------------------------------------------------------------------------##   
# TODO Change playbackRate
def playAudioEmbedded(filename, background=False):

    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        # <audio controls autoplay="true"> in case you want to show controls
        md = f"""
            <audio id="audio" autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

##-------------------------------------------------------------------------------------##
## stopAudio
##-------------------------------------------------------------------------------------##   
def stopAudio( ):
    # if mixer.get_init():
    #     mixer.music.stop()
    #     mixer.quit()
    return

# ##-------------------------------------------------------------------------------------##
# ## recordAudio
# ##-------------------------------------------------------------------------------------##     
# def recordAudio(outputFile, NOISE=100, SILENCE=2):
#     # Defining audio variables
#     CHUNK = 1024
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1
#     RATE = 44100
      
#     # Calling pyadio module and starting recording 
#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT,
#                 channels=CHANNELS, 
#                 rate=RATE, 
#                 input=True,
#                 frames_per_buffer=CHUNK)
 
#     stream.start_stream()
 
#     # Recording data until under threshold
#     frames=[]
#     isilent = 0
#     isilentmax = int(RATE / CHUNK * SILENCE)
#     while True:
#         data=stream.read(CHUNK)
#         data_chunk = array('h',data)
#         volume = max(data_chunk)
#         frames.append(data)
#         if volume < NOISE:
#             isilent = isilent + 1
#         else:
#             isilent = 0
#         if isilent > isilentmax: 
#             break
#     done = 1
#     if ( len(frames)-1 == isilentmax ): done = -1
            
#     # Stopping recording   
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
    
#     # Saving file with wave module    
#     wf = wave.open(outputFile, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
#     wf.close()
#     return done

##-------------------------------------------------------------------------------------##
## speechToTextGoogle
##-------------------------------------------------------------------------------------##
def speechToTextGoogle(filename, language="en"):
    # TODO
    return

##-------------------------------------------------------------------------------------##
## speechToTextOpenAI
##-------------------------------------------------------------------------------------##
def speechToTextOpenAI(filename, language="en"):
    client = OpenAI()
    audio_file= open(filename, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        language=language,
        file=audio_file,
        response_format="text"
    )
    
    # Controls
    if transcript.find("Amara.org") > 0: transcript = " "
    if transcript.find("prossimo episodio") > 0: transcript = " "

    return transcript

#-------------------------------------------------------------------------------------##
# textToSpeechGoogle
#-------------------------------------------------------------------------------------##
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

##-------------------------------------------------------------------------------------##
## textToSpeechOpenAI
##-------------------------------------------------------------------------------------##
def textToSpeechOpenAI(text, filename, language="alloy"):
    
    # Check audio file is not open
    while True:
        try:
            myfile = open(filename, "wb")
            break                             
        except IOError:
            stopAudio( )   
    
    speech_file_path = Path(__file__).parent / filename
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice=language, # alloy, onyx, fable
        input=text
    )
    response.stream_to_file(speech_file_path)

##-------------------------------------------------------------------------------------##
## createReport
##-------------------------------------------------------------------------------------##
def createReport():
 
    # Read 
    with open('Questions.txt', 'r') as f:
        Questions=f.read()
    n = 0
    Sentiments = [ int(0) ]*1000
    with open('Sentiments.txt', 'r') as f:
        for line in f:
            Sentiments[n] = int(line)
            n += 1
    Sentiments = Sentiments[0:n]

    # Post processing
    Experience = [ int(0) ]*n
    xAxis = [ int(0) ]*n
    Colors = [ 'white' ]*n
    Experience[0] = 0 #Sentiments[0]
    for k in range(1, n):
        Experience[k] = Experience[k-1] + Sentiments[k-1]
        xAxis[k] = k
        if ( Sentiments[k]>0 ): Colors[k] = "green"
        if ( Sentiments[k]==0 ): Colors[k] = "yellow"
        if ( Sentiments[k]<0 ): Colors[k] = "red"

    # Creating the bar plot
    fig = plt.figure()
    yticks = range(math.floor(min(Experience)-1), math.ceil(max(Experience)+1))
    plt.yticks(yticks)
    plt.grid(visible=True, axis='y', linestyle='--')
    #plt.ylim(-1.1, 1.1)
    plt.bar(xAxis, Sentiments, bottom = Experience, color = Colors)
    plt.xlabel("Interactions")
    plt.ylabel("Sentiment evolution")
    plt.savefig('Experience.png')

    # Summarize
    summary = summarizeBot(Questions)
    # document = Document()
    # document.add_heading("Sintesi discussione voicebot " + str(datetime.date.today()), level=1)
    # p = document.add_paragraph(summary)
    # p = document.add_picture('Experience.png')
    # document.save('Summary.docx')

    return summary

##-------------------------------------------------------------------------------------##
## run
##-------------------------------------------------------------------------------------##
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
        fq = open('Questions.txt', 'w'); fq.close()
        fs = open('Sentiments.txt', 'w'); fs.close()
    inputFile = "input.wav" 
    outputFile = "output.mp3"

    # Initialize session
    st.title("Chat")
    withAudio = st.sidebar.toggle('Audio')
    withMic = st.sidebar.toggle('Mic')
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # audio = mic_recorder(start_prompt="Start recording...", stop_prompt="Stop recording...", key='recorder_test', just_once=True, use_container_width=True)
    # if audio:       
    #     st.audio(audio['bytes'])    
    # exit(-1)

    # Chat prompt
    prompt = ""
    prompt = st.chat_input("Write here...")

    # Audio prompt
    volume = -1
    question = ""
    if ( ( not prompt ) and withMic ): 
        # Version with prompt (valid for clent - server) audio_recorder
        #audio_bytes = audio_recorder("", icon_name="microphone", icon_size="2x")
        # if ( audio_bytes ): volume = len(audio_bytes)
        # if ( volume > 0 ):
        #     with open(inputFile, mode='wb') as f:
        #         f.write(audio_bytes)
        #     question=speechToTextOpenAI(inputFile, "IT")
        # FYI There is a bug in the library as audio_bytes is always restored
        
        audio = mic_recorder(start_prompt="Start recording...", stop_prompt="Stop recording...", key='recorder', just_once=True, use_container_width=True)
        if audio: 
            audio_bytes = audio['bytes']
            st.audio(audio_bytes)
            volume = len(audio_bytes)
            st.write(volume)
        if ( volume > 0 ):
            with open(inputFile, mode='wb') as f:
                f.write(audio_bytes)
            question=speechToTextOpenAI(inputFile, "IT")
            
        # Version listening in the background (valid locally)     
        #with st.spinner('\n Speak up \n'):
            #volume = recordAudio(inputFile)
            #if ( volume > 0 ): question=speechToTextOpenAI(inputFile, "IT")
    if ( len(question) > 0 ): prompt = question 

    if prompt:

        # Chat message question
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
        # Commands
        question = prompt
        answer = ""
        if ( question == "/summary" ):
            answer = createReport()
            answer = "Di seguito la sintesi dei punti chiave toccati durante la conversazione \n \n \n" + answer
        elif ( question == "/sentiment" ):
            answer = "Di seguito la sintesi della evoluzione del sentiment della conversazione"
            createReport()
        else:
            # Chatbot
            if ( len(question) > 0 ): answer=chatBot(question)
        
        # Chat message answer
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
        if ( question == "/sentiment" ): st.image('Experience.png')
        
        # Play audio
        if ( withAudio and len(answer) > 0 ): textToSpeechGoogle(answer, outputFile, "it")
        #if ( withAudio and len(answer) > 0 ): textToSpeechOpenAI(answer, outputFile, "onyx")
        #if ( withAudio and len(answer) > 0 ): playAudio(outputFile)
        if ( withAudio and len(answer) > 0 ): playAudioEmbedded(outputFile)

        # Sentiment analysis
        sentiment = ""
        #sentiment = sentimentAnalysis(question)
        sentimentId = 0; 
        if sentiment == "Positive": sentimentId = 1
        if sentiment == "Negative": sentimentId = -1

        # Store results
        if ( 'k' in st.session_state ):
            fq = open('Questions.txt', 'a'); fq.write(question + '\n'); fq.close()
            fs = open('Sentiments.txt', 'a'); fs.write(str(sentimentId) + '\n'); fs.close()
            st.session_state['k'] = str(int(st.session_state['k']) + 1)

        if withMic: st.rerun()
    if withMic: st.rerun()

##-------------------------------------------------------------------------------------##
## Main
##-------------------------------------------------------------------------------------##
if __name__ == "__main__":
    run()
