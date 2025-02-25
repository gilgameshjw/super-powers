
import os
from datetime import datetime
import streamlit as st
from openai import OpenAI
import asyncio

from tools.researcher import run_researcher
# from agents.agent import create_agent, generate_response_agent


# Function to simulate a spinner while waiting for run_researcher
def run_with_spinner(prompt, report_type, config):
    with st.spinner("Generating research report... Please wait."):
        return run_researcher(prompt, report_type, config.mock)


def generate_response_agent_w_spinner(agent, user_input, chat_history=[]):
    """Generate the response from the agent"""
    with st.spinner("Generating response... Please wait."):
        data = {
            "chat_history": chat_history, 
            "input": user_input
        }
        output = agent.invoke(data)
        print("output:", output)
    return output["output"]

async def stream_response(message, delta_t=0.1):
    for line in str(message).splitlines():
        yield line + "\n"  # Ensures that each line is correctly formatted
        await asyncio.sleep(delta_t)  # Simulate processing time


# chat_history = []

# Function to handle streaming in Streamlit
async def stream_to_streamlit(response):
    placeholder = st.empty()  # Create a placeholder for the streaming content
    buffer = ""  # Buffer to accumulate streamed lines

    # Iterate over the asynchronous generator
    async for line in stream_response(response):
        buffer += line  # Append the new line to the buffer
        placeholder.markdown(buffer)  # Update the placeholder with the accumulated content

def handle_file_upload():
    uploaded_file = st.file_uploader("Upload a file (any format)", type=None)  # Allow any file type
    if uploaded_file:
        # Save the file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            file_path = tmp_file.name

        # Add a message indicating the file was uploaded
        file_message = f"Uploaded file: {uploaded_file.name}"
        st.session_state.messages.append({"role": "user", "content": file_message})
        with st.chat_message("user"):
            st.markdown(file_message)

        # Process the file (example: just acknowledge it for now)
        agent_response = f"Received file: {uploaded_file.name}"
        st.session_state.messages.append({"role": "assistant", "content": agent_response})
        with st.chat_message("assistant"):
            st.markdown(agent_response)


def run_agent_answer(config, prompt):
    """Generate the response from the agent"""
    # Generate assistant response
    # response = None
    with st.chat_message("assistant", avatar="resources/images/scientist_0.png"):
        response = generate_response_agent_w_spinner(
            config.agent,
            prompt,
            chat_history=st.session_state.messages
        )
        # Stream the response
        #st.write("Streaming response:")
        asyncio.run(stream_to_streamlit(response))  # Stream the response asynchronously
    return response



# Chat
def chat(config):
    # Set up the title and chat history
    st.title("JAJA PAS GPT")
    if "messages" not in st.session_state:
        st.session_state.messages = []
        response = run_agent_answer(config, "Introduce yourself and what your tools are.")
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    

    # Chat input
    #with st.chat_message("user", avatar="resources/images/user_0.png"):
    #        st.markdown(prompt)
    prompt = st.chat_input("Your text here:") #config.translations["placeholder"])
    # File Upload
    handle_file_upload()

    if prompt:
        # Add user message to the chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="resources/images/user_0.png"):
            st.markdown(prompt)

        # run_agent_answer()
        response = run_agent_answer(config, prompt)

        # Add assistant message to the chat history
        st.session_state.messages.append({"role": "assistant", "content": response})