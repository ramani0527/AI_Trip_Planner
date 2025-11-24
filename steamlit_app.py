import streamlit as st
import datetime
import requests
import sys

BASE_URL = "https://localhost:8000"

st.set_page_config(
    page_icon= "TPAA",
    page_title="Travel planner Agentic Application",
    layout= "centered",
    initial_sidebar_state="expanded"
)

st.title("Travel planner Agentic Application")
#Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
st.header("need to plan a trip, Let me help ")
with st.form(key= "query_form", clear_on_submit= True):
     user_input = st.text_input("User Input", placeholder="e.g. Plan a trip to Assam in 5 days")
     submit_button = st.form_submit_button("Send")   

if submit_button and user_input.strip():
    try:
        with st.spinner("bot is thinking..."):
           payload = { "question ": user_input}
           response = requests.post(f"{BASE_URL}/query",json=payload)
        if response.status_code == 200:
            answer = response.json().get("answer","No answer returned")
            marksown_content = f"""# AI Travel Plan
        
        
           {answer}   
           
           
           """
            st.markdown(marksown_content)
        else:
            st.error("Bot failed to respond:" + response.text)
        
    except Exception as e:
        raise f"The response failed due to {e}"
                
           
           