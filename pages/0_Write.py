from Utils import *

##-------------------------------------------------------------------------------------##
## Create page
##-------------------------------------------------------------------------------------##
def Write() -> None:

    st.markdown("# Write your story...")
    #st.write("Get creative and shape your own story choosing your favourite characters, topic and setting. You can also specify length of the story and its language")
    
    characters = st.text_input("Who are the main characters of this story?")
    setting = st.text_input("Where and where is this story set?")
    topic = st.text_input("What is the topic of this story?")
    language = st.selectbox("Which language do you want to crate this story in?", ('English', 'Italian')) 
    length = st.slider("How many words is this story long?", 0, 1000, 500, 50)
    st.write("\n")
    click = st.button("Create a new story...", use_container_width=True)
    lines = length/10.0
    pages = length/500.0
    timeToRead = 60.0*length/120.0

    output = ""
    if click:
        input = "Write a children story. The characters are " + characters + ". The story is set in " + setting + ". The topic is " + topic
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are the best children story author in the world. Write a story in " + language + "language. It must be precisely" + str(length) + "words long. The phirst phrase should be the title"},
            {"role": "user", "content": input}
            ]
        )
        output = completion.choices[0].message.content
        st.balloons()

    st.divider()
    output.encode("latin-1")
    output_words = len(output.split())
    txt = st.text_area( "Here it is your story...", output, height = int(output_words/10.0*30) )

    title = output.partition('\n')[0]
    title.replace('"','')
    if ( len(title) > 0 ):
        fid = open("./stories/" + str(title) + ".txt", 'w', encoding='latin-1')
        fid.write(datetime.datetime.now().strftime("%d %b %Y")+"\n") 
        fid.write(str(output_words)+"\n")
        fid.write(language+"\n")
        fid.write(output)
        fid.close()

#st.set_page_config(layout="wide", page_title="Create", page_icon="book")
st.set_page_config(layout="centered", page_title="Write", page_icon="book")
Write()

