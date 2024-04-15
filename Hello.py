##-------------------------------------------------------------------------------------##
## Import
##-------------------------------------------------------------------------------------##
from Utils import *

##-------------------------------------------------------------------------------------##
## Main
##-------------------------------------------------------------------------------------##
# TODO Split text so at max 4096 characters for text to speech
# TODO Fix Audio with mic issues
# TODO Move to default user folder and login
LOGGER = get_logger(__name__)
def run():

    st.set_page_config(layout="wide", page_title="Home", page_icon="book")
    st.write("# Welcome to your bedtime stories!")
    st.write("Get creative and shape your own bedtime stories and pictures. Have fun writing, drawing, reading and listening. Below you can find a summary of your activity")
    st.write("\n")
    
    # Populate database
    os.system("mkdir stories")
    os.system("mkdir images")
    stories = os.listdir("./stories")
    N = len(stories)
    Ddates = [ " " ]*N
    Llanguages = [ " " ]*N
    Wwords = [ int(0) ]*N
    Ttitles = [ " " ]*N
    Sstories = [ int(1) ]*N
    maxTime = 0.0
    for k in range(0, N):
        filepath = "./stories/" + str(stories[k])
        fid = open(filepath, 'r', encoding='latin-1')
        text = fid.read()
        fid.close()
        temp = text.split("\n",4)
        creation_time = os.path.getctime(filepath)
        #creation_datetime = time.strftime("%d %b %Y", time.gmtime(creation_time))
        #Ddates[k] = creation_datetime
        Ddates[k] = temp[0]
        maxTime = max( creation_time, maxTime )
        Wwords[k] = temp[1]
        Llanguages[k] = temp[2]
        Ttitles[k] = temp[3]
        if (len(text) < 1 or len(temp[3]) < 1 or len(temp[4]) < 1 ): 
            os.remove("./stories/" + str(stories[k]))
            st.rerun()

    # Summary over the last Ndays days
    Npast = 30
    uniqueLanguages = np.unique(Llanguages)
    Nlanguages = len(uniqueLanguages)
    today = time.time()
    pastDdays = [ i for i in range(-Npast+1, 1) ]
    pastTtimes = [ today ]*Npast
    pastDdates = [ "" ]*Npast
    pastWwords = [ [ int(0) ]*Npast for i in range(0, Nlanguages+4) ]
    pastSstories = [ [ int(0) ]*Npast for i in range(0, Nlanguages+4) ]
    # total, short (<300), medium (300-600), long (600+), for each language
    for i in range(0, Npast): 
        pastTtimes[i] = float(today)-float(i)*24.0*60.0*60.0
        pastDdates[i] = time.strftime("%d %b %Y", time.gmtime(pastTtimes[i]))
        for k in range(0, N):
            if ( Ddates[k] == pastDdates[i] ):
                WordsK = int(Wwords[k])
                LanguageK = Llanguages[k]
                pastWwords[0][i] += WordsK
                if ( WordsK < 300 ): pastWwords[1][i] += WordsK
                if ( WordsK >= 300 and WordsK < 600 ): pastWwords[2][i] += WordsK
                if ( WordsK >= 600 ): pastWwords[3][i] += WordsK
                for j in range(0, Nlanguages):
                    if ( LanguageK == uniqueLanguages[j] ): pastWwords[4+j][i] += WordsK
                pastSstories[0][i] += 1
                if ( WordsK < 300 ): pastSstories[1][i] += 1
                if ( WordsK >= 300 and WordsK < 600 ): pastSstories[2][i] += 1
                if ( WordsK >= 600 ): pastSstories[3][i] += 1
                for j in range(0, Nlanguages):
                    if ( LanguageK == uniqueLanguages[j] ): pastSstories[4+j][i] += 1
    
    # Totals                
    totalSstories = [ int(0) for i in range(0, Nlanguages+4) ]
    totalWwords = [ int(0) for i in range(0, Nlanguages+4) ] 
    for k in range(0, N):
        WordsK = int(Wwords[k])
        LanguageK = Llanguages[k]
        totalSstories[0] += 1
        totalWwords[0] += WordsK
        if ( WordsK < 300 ): totalSstories[1] += 1; totalWwords[1] += WordsK
        if ( WordsK >= 300 and WordsK < 600 ): totalSstories[2] += 1; totalWwords[2] += WordsK
        if ( WordsK >= 600 ): totalSstories[3] += 1; totalWwords[3] += WordsK
        for j in range(0, Nlanguages):
            if ( LanguageK == uniqueLanguages[j] ): totalSstories[4+j] += 1; totalWwords[4+j] += WordsK
    deltaSstories = [ int(0) for i in range(0, Nlanguages+4) ]
    deltaWwords = [ int(0) for i in range(0, Nlanguages+4) ] 
    for j in range(0, Nlanguages+4):
        deltaSstories[j] = totalSstories[j] - sum(pastSstories[j][:])
        deltaWwords[j] = totalWwords[j] - sum(pastWwords[j][:])      

    # Cumulated
    cumulatedWwords = [ [ int(0) ]*Npast for i in range(0, Nlanguages+4) ]
    cumulatedSstories = [ [ int(0) ]*Npast for i in range(0, Nlanguages+4) ]  
    for j in range(0, Nlanguages+4):
        #cumulatedWwords[j][Npast-1] = pastWwords[j][Npast-1] 
        #cumulatedSstories[j][Npast-1] = pastSstories[j][Npast-1]
        cumulatedWwords[j][Npast-1] = pastWwords[j][Npast-1] + deltaWwords[j] # Sum delta outside the time window for reporting
        cumulatedSstories[j][Npast-1] = pastSstories[j][Npast-1] + deltaSstories[j] # Sum delta outside the time window for reporting
    for i in range(0, Npast-1):
        for j in range(0, Nlanguages+4):
            cumulatedWwords[j][Npast-1-i-1] = cumulatedWwords[j][Npast-1-i] + pastWwords[j][Npast-1-i-1]
            cumulatedSstories[j][Npast-1-i-1] = cumulatedSstories[j][Npast-1-i] + pastSstories[j][Npast-1-i-1]

    # Metrics 
    col1, col2 = st.columns(2)
    with col1: 
        st.metric(label="Total stories", value=cumulatedSstories[0][0], delta=pastSstories[0][0])
    with col2: 
        st.metric(label="Total words", value=cumulatedWwords[0][0], delta=pastWwords[0][0])
    # with col3: 
    #     st.metric(label="Languages", value=Nlanguages)
    st.divider()

   # Data frame
    dfpast = pd.DataFrame(
    {
        "Date": pastDdates,        
        "Total words": cumulatedWwords[0],
        "Short": cumulatedWwords[1],
        "Medium": cumulatedWwords[2],
        "Long": cumulatedWwords[3],
        "Total stories": cumulatedSstories[0],
        "English": cumulatedSstories[4],
        "Italian": cumulatedSstories[5],
    }    
    )
    dfpast['Date'] = pd.to_datetime(dfpast['Date'])
    dfpast['Date'] = dfpast['Date'].dt.strftime('%b %d')
    dfpast = dfpast.sort_values(by='Date')

    with col1:
        st.write("**Total stories by language**")
        st.line_chart(dfpast, x="Date", y=["Total stories", "English", "Italian"], width=10)
    with col2:
        st.write("**Total words by story type**")
        st.line_chart(dfpast, x="Date", y=["Total words", "Short", "Medium", "Long"], width=10)

    # Data frame
    df = pd.DataFrame(
    {
        "Created on": Ddates,        
        "Title": Ttitles,
        "Language": Llanguages,
        "No. of words": Wwords,
    }    
    )
    
    st.write("**List of your bedtime stories**")
    result = st.data_editor(df, hide_index=True, use_container_width=True, disabled=True)
    #st.table(df, hide_index=True)

if __name__ == "__main__":
    run()
