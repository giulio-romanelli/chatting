from Utils import *

##-------------------------------------------------------------------------------------##
## Print page
##-------------------------------------------------------------------------------------##
def Print() -> None:
    
    st.markdown("# Print your book of stories...")
    with st.spinner('\n Preparing your book of stories... \n'):
        printStories(True)
    displayPDF("myStories.pdf")

    return
   
#st.set_page_config(layout="wide", page_title="Print", page_icon="book")
st.set_page_config(layout="centered", page_title="Print", page_icon="book")
Print()

