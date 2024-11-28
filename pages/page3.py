import streamlit as st
from groq import Groq

import auth
import config

# Configuración de la página
st.set_page_config(
    page_title="Dimex", 
    page_icon="./favicon.ico"  
)

auth.generarLogin()
if 'usuario' in st.session_state:
    #st.header('Página :green[3]')

    with st.sidebar:
        client = Groq(
            api_key=config.APY_KEY,
        )

    client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": config.PROMPT,
            }
        ],
        model="llama3-8b-8192",
    )

    st.title("💬 Chatbot")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        
        #st.info("Please add your API key to continue.")
        #st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        
        st.session_state.messages.append({"role": "assistant", "content": chat_completion.choices[0].message.content})
        st.chat_message("assistant").write(chat_completion.choices[0].message.content)