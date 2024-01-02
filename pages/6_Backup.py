from Utils import *

##-------------------------------------------------------------------------------------##
## Backup page
##-------------------------------------------------------------------------------------##
def Backup() -> None:

    # Bulk download/upload
    st.markdown("# Backup your stories...")

    col1, col2 = st.columns(2)

    with col1:
        zipFolder("./stories", "stories.zip")
        with open('./stories.zip', 'rb') as f:
            clickedDownloadStories = st.download_button('Download your stories...', f, file_name='stories.zip', use_container_width=True) 

    with col2:
        zipFolder("./images", "images.zip")
        with open('./images.zip', 'rb') as f:
            clickedDownloadImages = st.download_button('Download your gallery...', f, file_name='images.zip', use_container_width=True) 

    uploadedFile = st.file_uploader("Upload your stories or gallery...")
    if uploadedFile is not None:
        if uploadedFile.name == "stories.zip":
            with open("./stories.zip","wb") as f:
                f.write(uploadedFile.getbuffer())
            unzipFolder("./stories.zip", ".")
        elif uploadedFile.name == "images.zip":
            with open("./images.zip","wb") as f:
                f.write(uploadedFile.getbuffer())
            unzipFolder("./images.zip", ".")            

    return
   
st.set_page_config(layout="centered", page_title="Backup", page_icon="book")
Backup()