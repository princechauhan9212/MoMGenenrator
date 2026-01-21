import os 
import google.generativeai as genai
import streamlit as st
from Pdfextractor import text_extractor
from wordextractor import doc_text_extract
from image2text import extract_text_image


# Lets configure genai model 
gemini_key = os.getenv('Google_API_Key2')
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite',
                               generation_config={'temperature':0.9})

# Lets create the sidebar 

st.sidebar.title('UPLOAD Your NOTES :')
st.sidebar.subheader('Only Upload image, PDF, DOCX')
user_file = st.sidebar.file_uploader('upload Here :',
                                     type=['pdf','docx','png','jpeg','jpg','jfif'])

if user_file:
    st.sidebar.success('File Uploaded Successfully')
    if user_file.type == 'application/pdf':
        user_text = text_extractor(user_file)

    elif user_file.type in ['image/png','image/jpeg','image/jpg,','image/jfif']:
        user_text = extract_text_image(user_file)

    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = doc_text_extract(user_file)

# Lets create main page 

st.title(':orange[MoM Generator:-] :green[AI Assisted Minutes of Meeting Generator]')
st.subheader(':blue[THis application creates generalized minutes of meeting]')
st.write(''' 
Follow the steps :
1. Upload the notres in PDF.DOCX or Image Format In sidebar.
3. Click "Generate" to generate MoM.''')

if st.button('Generate'):
    with st.spinner('please wait...'):
        prompt = f''' 
        <Role> Your are an expert in waiting and formating minutes of meetings.
        <Goal> Create minutes of meetings from the notes that user has provided.
        <Context> The user has provided  some. rough notes as text. Here are the notes{user_text} 
        <Format> The Output must follow the below format 
        * Title: assume title of the meeting 
        * Agenda : assume agenda of the meeting
        * Attendees : Name of the attendes(if name of the attendees is not there keep it N/A)
        * Date And Place : date and the place of the meeting (if not provided keep it only )
        * Body : The body should follow the following sequence of points
            * Key Points discused
            * Highlight any decision that has been taken
            * Mention Actionable Items.
            * Mention any deadline if discused.
            * Mention next meeting date if discused.
            * Add a 2-3 line of summary .
            
        <Instructions>
        * Use Bullet points and highlight the importance keywords by making them bold .
        * Generate the output in docx format'''

        response = model.generate_content(prompt)
        st.write(response.text)


    if st.download_button(label='DOWNLOAD',
                         data=response.text,
                         file_name='mom_generated.text',
                         mime='text/plain'):
        st.success('Your file is downloaded')
        