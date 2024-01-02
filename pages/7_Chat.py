from Utils import *

##-------------------------------------------------------------------------------------##
## Chat page
##-------------------------------------------------------------------------------------##
def Chat() -> None:

    st.markdown("# Talk to me...")
    language = st.sidebar.selectbox('Language', ("en", "it"))
    chatVoiceBot( language )

    # Extend vertical spacing of sidebar
    st.sidebar.markdown("""
        <style>
        [data-testid='stSidebarNav'] > ul {
            min-height: 40vh;
        } 
        </style>
        """, unsafe_allow_html=True)

    return
   
#st.set_page_config(layout="wide", page_title="Chat", page_icon="book")
st.set_page_config(layout="centered", page_title="Chat", page_icon="book")
Chat()

