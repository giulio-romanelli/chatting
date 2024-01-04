from Utils import *

##-------------------------------------------------------------------------------------##
## Chat page
##-------------------------------------------------------------------------------------##
def Chat() -> None:

    st.markdown("# Talk to me...")
    verticalSpaceSideBar()
    language = st.sidebar.selectbox('Language', ("en", "it"))
    chatVoiceBot( language )

    return
   
#st.set_page_config(layout="wide", page_title="Chat", page_icon="book")
st.set_page_config(layout="centered", page_title="Chat", page_icon="book")
Chat()

