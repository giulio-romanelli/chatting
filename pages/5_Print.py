from Utils import *
#import docx2pdf
#import pythoncom

##-------------------------------------------------------------------------------------##
## Print page
##-------------------------------------------------------------------------------------##
def Print() -> None:
    
    # Create a book
    st.markdown("# Create your book of stories...")
    
    with st.spinner('\n Preparing your book of stories... \n'):
        printStoriesWord()

    # PDF only works locally with docx2pdf
    #pythoncom.CoInitialize()
    #docx2pdf.convert("myStories.docx")
    #displayPDF("myStories.pdf")

    with open('./myStories.docx', 'rb') as f:
        clicked = st.download_button('Download your book of bedtime stories (.docx)...', f, file_name='myStories.docx', use_container_width=True)       

    return
   
st.set_page_config(layout="centered", page_title="Print", page_icon="book")
Print()

