from Utils import *
#import docx2pdf
#import pythoncom

##-------------------------------------------------------------------------------------##
## Print page
##-------------------------------------------------------------------------------------##
def Print() -> None:
    
    st.markdown("# Print your book of stories...")
    
    withPDF = False # Only works locally with docx2pdf
    with st.spinner('\n Preparing your book of stories... \n'):
        printStories()
    
    if withPDF:
        #pythoncom.CoInitialize()
        #docx2pdf.convert("myStories.docx")
        displayPDF("myStories.pdf")
    else:
        with open('./myStories.docx', 'rb') as f:
            clicked = st.download_button('Download all your bedtime stories', f, file_name='myStories.docx', use_container_width=True) 

    return
   
#st.set_page_config(layout="wide", page_title="Print", page_icon="book")
st.set_page_config(layout="centered", page_title="Print", page_icon="book")
Print()

