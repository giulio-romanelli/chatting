from Utils import *

##-------------------------------------------------------------------------------------##
## Read page
##-------------------------------------------------------------------------------------##
def Read() -> None:

    st.markdown("# Read/listen to your story...")
    #st.write("Get ready to read and/or listen to one of the stories you have created")
    
    stories = os.listdir("./stories")
    option = st.selectbox('Which story do you want to read?', stories)
    fid = open("./stories/" + str(option), 'r', encoding='latin-1')
    text = fid.read()
    tmp = text.split("\n",3)
    date = tmp[0]
    words = tmp[1]
    language = tmp[2]
    body = tmp[3]
    st.text_input('Language:', language, disabled=True)
    st.text_input('Length:', words + " words, approx. " + str(math.ceil(60.0*int(words)/120.0/60.0)) + " minutes", disabled=True)
    voice = st.selectbox('Who should read the story?', ("chatbot", "alloy", "onyx", "fable"))
    st.write("\n")
    click = st.button("Read to me...", use_container_width=True)

    if click:
        outputFile = "temp.mp3"
        if ( ( voice == "alloy" or voice == "onyx" or voice == "fable" ) and ( len(body) < 4096 ) ):
            textToSpeechOpenAI(body, outputFile, language=voice)
        else:
            language_code = "en"
            if language == "Italian": language_code = "it"
            textToSpeechGoogle(body, outputFile, language_code)
        st.balloons()
        playAudioEmbedded(outputFile)

    st.divider()
    output_words = len(body.split())
    txt = st.text_area( "Here it is your story...", body, height = int(output_words/10.0*30) )

    return
   
#st.set_page_config(layout="wide", page_title="Read", page_icon="book")
st.set_page_config(layout="centered", page_title="Read", page_icon="book")
Read()

