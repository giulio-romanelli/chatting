from Utils import *

##-------------------------------------------------------------------------------------##
## Edit page
##-------------------------------------------------------------------------------------##
def Edit() -> None:
    
    st.markdown("# Edit your story...")
   
    # Get database
    stories = os.listdir("./stories")
    if len(stories) > 0:     
        option = st.selectbox('Which story do you want to edit?', stories)
        fid = open("./stories/" + str(option), 'r', encoding='latin-1')
        text = fid.read()
        fid.close()
        tmp = text.split("\n",3)
        date = tmp[0]
        words = tmp[1]
        language = tmp[2]
        body = tmp[3]

        # Buttons save and delete
        cols = st.columns(2)
        with cols[0]:
            clickSave = st.button("Save", use_container_width=True)
        with cols[1]:
            clickDelete = st.button("Delete", use_container_width=True)

        # Text
        st.divider()
        output_words = len(body.split())
        output = st.text_area( "Edit your story here...", body, height = int(output_words/10.0*30) )
        output_words = len(output.split())

        # Save changes
        if clickSave:
            fid = open("./stories/" + str(option), 'w', encoding='latin-1')
            fid.write(datetime.datetime.now().strftime("%d %b %Y")+"\n") 
            fid.write(str(output_words)+"\n")
            fid.write(language+"\n")
            fid.write(output)
            fid.close() 

        # Delete story
        if clickDelete:
            os.remove("./stories/" + str(option))
            os.remove("./images/" + str(option) + ".png")
            st.rerun()   

st.set_page_config(layout="centered", page_title="Edit", page_icon="book")
Edit()
