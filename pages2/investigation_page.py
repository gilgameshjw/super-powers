
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
    data = {
        "chat_history": chat_history, 
        "input": user_input
    }
    output = agent.invoke(data)
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


# Investigation and Support page
def investigation_page(config):
    # Set up the title and chat history
    st.title(config.translations["title"])
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    print(st.session_state.messages)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    prompt = st.chat_input(config.translations["placeholder"])
    if prompt:
        # Add user message to the chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="resources/images/user_0.png"):
            st.markdown(prompt)

        # Generate assistant response
        response = None
        with st.chat_message("assistant", avatar="resources/images/scientist_0.png"):
            response = generate_response_agent_w_spinner(
                config.agent,
                prompt,
                chat_history=st.session_state.messages
            )

            # Stream the response
            st.write("Streaming response:")
            asyncio.run(stream_to_streamlit(response))  # Stream the response asynchronously

        # Add assistant message to the chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
