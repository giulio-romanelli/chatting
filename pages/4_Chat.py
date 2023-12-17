from Utils import *

##-------------------------------------------------------------------------------------##
## Read page
##-------------------------------------------------------------------------------------##
def Chat() -> None:

    st.markdown("# Talk to me...")
    language = st.sidebar.selectbox('Language', ("en", "it"))
    chatVoiceBot( language )

    return
   
#st.set_page_config(layout="wide", page_title="Chat", page_icon="book")
st.set_page_config(layout="centered", page_title="Chat", page_icon="book")
Chat()

