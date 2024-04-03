import google.generativeai as genai
import PyPDF2
import streamlit as st

#AI setup
genai.configure(api_key="AIzaSyADxArDsnTX2y5ydo1FKqf3tSLzYAhXnws")

# Set up the model
generation_config = {
  "temperature": 0.1,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 500,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

#convo = model.start_chat(history=[],prompt=startmessage+text_content)
convo = model.start_chat(history=[])

startmessage="Hello.\nBelow I will provide you a text.\nAfter that I will ask you some questions about it. Reply with\n \"Everything OK\" if you understood the text and are ready to answer my questions.\n\n"

def read_pdf(content):
  text=""
  for page in PyPDF2.PdfReader(content).pages:
    text+=page.extract_text()
  return text

file_submitted=False
st.title('PDF-analizotron')
with st.form('my_form'):
  if file_submitted:
    msg=st.text_area("Enter question:")
    submitted=st.form_submit_button('AAA')
    if submitted:
        convo.send_message(msg)
        st.info(convo.last.text)
  else:
    pdffile=st.file_uploader("Upload PDF",type=["pdf"])
    submitted=st.form_submit_button('Upload')
    if submitted:
      text_content=read_pdf(pdffile)
      if len(text_content)>30000*5:
        #token is about 4 letters or 0.75 words in English, we count it as 5 to count spaces also(roughly)
        st.info("Due to Gemini 1.0 limitations, texts longer than 30 000 tokens cannot be proceeded.")
      else:
        convo.send_message(startmessage+text_content)
        file_submitted=True

