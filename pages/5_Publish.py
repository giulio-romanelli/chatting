from Utils import *
#import docx2pdf
#import pythoncom

##-------------------------------------------------------------------------------------##
## Publish page
##-------------------------------------------------------------------------------------##
def Publish() -> None:
    
    # Create a book
    st.markdown("# Publish your book of stories...")
    
    # Extend vertical spacing of sidebar
    verticalSpaceSideBar()

    #with st.spinner('\n Preparing your book of stories... \n'):
    #    printStoriesWord()
    # PDF only works locally with docx2pdf
    #pythoncom.CoInitialize()
    #docx2pdf.convert("myStories.docx")
    #displayPDF("myStories.pdf")

    # Create word document
    if 'docx' not in st.session_state:
        st.session_state['docx'] = False
    if st.session_state["docx"]:
        with open('./myStories.docx', 'rb') as f:
            clicked = st.download_button('Download your book of stories (.docx)...', f, file_name='myStories.docx', use_container_width=True)  
            st.session_state["docx"] = False
    else:
        clicked = st.button("Create your book of stories (.docx)...", use_container_width=True)
        if clicked:
            st.session_state["docx"] = True
            createStoriesWord()
            time.sleep(1)
            st.rerun()

    # Create mp3 overall
    if 'mp3' not in st.session_state:
        st.session_state['mp3'] = False
    if st.session_state["mp3"]:
        with open('./myStories.mp3', 'rb') as f:
            clicked = st.download_button('Download your book of stories (.mp3)...', f, file_name='myStories.mp3', use_container_width=True)  
            st.session_state["mp3"] = False
    else:
        clicked = st.button("Create your audio-book of stories (.mp3)...", use_container_width=True)
        if clicked:
            st.session_state["mp3"] = True
            createStoriesMp3()
            time.sleep(1)
            st.rerun()

    return
   
st.set_page_config(layout="centered", page_title="Publish", page_icon="book")
Publish()

