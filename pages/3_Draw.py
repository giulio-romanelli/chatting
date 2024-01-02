from Utils import *

##-------------------------------------------------------------------------------------##
## Read page
##-------------------------------------------------------------------------------------##
def Draw() -> None:

    st.markdown("# Create a drawing for your story...")
     
    stories = os.listdir("./stories")
    option = st.selectbox('Which story do you want to create a drawing for?', stories)
    fid = open("./stories/" + str(option), 'r', encoding='latin-1')
    text = fid.read()
    tmp = text.split("\n",3)
    date = tmp[0]
    words = tmp[1]
    language = tmp[2]
    body = tmp[3]
    st.write("\n")
    click = st.button("Create a new drawing...", use_container_width=True)
    st.divider()

    if click:

        # Summary
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "Sumarize the given text in 50 words"},
            {"role": "user", "content": body}
            ]
        )
        summary = completion.choices[0].message.content
        summary_words = len(summary.split())
        #txt = st.text_area( "Short summary...", summary, height = int(summary_words/10.0*25) )
        st.markdown( summary )

        # Drawing
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt="Create a drawing on the following story: " + summary,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url     
        st.balloons()  
        st.image(image_url)

        img_data = requests.get(image_url).content
        #with open("./images/" + str(datetime.date.today()) + " " + option +".png", 'wb') as handler:
        #    handler.write(img_data)        
        with open("./images/" + option +".png", 'wb') as handler:
            handler.write(img_data)               

    return
   
#st.set_page_config(layout="wide", page_title="Draw", page_icon="book")
st.set_page_config(layout="centered", page_title="Draw", page_icon="book")
Draw()

# Gallery function