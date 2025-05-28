import streamlit as st
from groq import Groq

client = Groq(api_key="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")

st.set_page_config(page_title="Real Estate Bot", page_icon="🏡")
st.title("🏡 Real Estate Bot")
st.write("Tell me what kind of property you're looking for, and I'll help match you with options!")

if "messages" not in st.session_state:
    
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are a helpful real estate assistant. Ask clarifying questions if needed, and suggest property types, locations, and options. "
            "Always answer like a real estate agent trying to match the user with a property. If the user asks for options, generate 2-3 realistic property descriptions. "
            "If info is missing (e.g., budget), ask for it politely."
        )}
    ]

user_input = st.chat_input("What type of property are you looking for?")


for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=1000,
            stream=True,
        )

        full_reply = ""
        response_container = st.empty()
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                full_reply += content
                response_container.markdown(full_reply)

        st.session_state.messages.append({"role": "assistant", "content": full_reply})
