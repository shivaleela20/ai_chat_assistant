import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="Ai Chat Assistant",layout="wide")

def init():
    api_key = st.sidebar.text_input("Enter your OpenAI API Key",type="password")
    if not api_key:
        st.stop()
    os.environ["OPENAI_API_KEY"]=api_key
    if "client" not in st.session_state:
        st.session_state.client = OpenAI(api_key=api_key)

def main():
    st.title("AI Chat Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages=[]
        system_prompt="You are a helpful AI assistant detailed knowledge answering questions about various topics"

        st.session_state.messages.append({"role":"system","content":system_prompt})

    user_input = st.text_area("Enter your question:")
    if not os.getenv("OPENAI_API_KEY"):
        st.warning("Please enter your API key to start chatting!")
    elif user_input:
         temperature = st.sidebar.slider("Creativity",0.1,1.0,0.7)
         try:
            if not st.session_state.messages or st.session_state.messages[-1]["role"] !="user"or st.session_state.messages[-1]["content"]!=user_input:
                st.session_state.messages.append({"role":"user","content":user_input})
            with st.spinner("AI Assistant is thinking..."):
                response = st.session_state.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    temperature=temperature,
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )

                assistant_response = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            st.subheader("Chat History")

            for message in reversed(st.session_state.messages):
                if message["role"] == "user":
                    st.chat_message("user").markdown(message["content"])
                elif message["role"] == "assistant":
                    st.chat_message("assistant").markdown(message["content"])
         except Exception as e:
            st.error(f"Error: {str(e)}")

# Main function entry point
if __name__ == "__main__":
    init()
    main()








