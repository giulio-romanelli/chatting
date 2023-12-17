from Utils import *

##-------------------------------------------------------------------------------------##
## Read page
##-------------------------------------------------------------------------------------##
def Gallery() -> None:

    st.markdown("# Browse through your drawings...")
    images = os.listdir("./images")
    N = len(images)
    cols = st.columns(2)
    k = 0
    addRows = True
    while addRows:
        for j in range(0, len(cols)):
            if ( k < N ):
                with cols[j]:
                    st.image("./images/" + images[k], images[k][:-8])
                    k = k + 1
            else:
                addRows = False
                break

    return
   
#st.set_page_config(layout="wide", page_title="Gallery", page_icon="book")
st.set_page_config(layout="centered", page_title="Gallery", page_icon="book")
Gallery()
