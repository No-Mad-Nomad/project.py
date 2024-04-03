import google.generativeai as genai
import PyPDF2
import streamlit as st

st.title('PDF-analizotron')

text_content = ""
'''
with open("sheckley.pdf", "rb") as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extract text from all pages
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text_content += page.extract_text()

if len(text_content)>30000*5:
    #token is about 4 letters or 0.75 words in English, we count it as 5 to count spaces also(roughly)
    print("Due to Gemini 1.0 limitations, texts longer than 30 000 tokens cannot be proceeded.")
    exit()
'''
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

startmessage="Hello.\nBelow I will provide you a text.\nAfter that I will ask you some questions about it. Reply with\n \"Everything OK\" if you understood the text and are ready to answer my questions.\n\n"

#response = model.start_chat(history=history, prompt="What's your favorite color?")

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

#convo = model.start_chat(history=[],prompt=startmessage+text_content)
convo = model.start_chat(history=[])

#print(convo.last.text)
while True:
  with st.form('my_form'):
    msg=st.text_area("Enter question:")
    submitted=st.form_submit_button('Ask')
    if submitted:
      if msg=="STOP_CONVO": break
      convo.send_message(msg)
      st.info(convo.last.text)
