
import os
#from datetime import datetime
import streamlit as st
#from openai import OpenAI
import asyncio

# from src.background import set_static_background



def generate_response_agent_w_spinner(agent, user_input, chat_history=[]):
    """Generate the response from the agent"""
    with st.spinner("Generating response... Please wait."):
        data = {
            "chat_history": chat_history, 
            "input": user_input
        }
        data["chat_history"] = [d for d in data["chat_history"]]
        output = agent.invoke(data)
        print("############################################################")
        print("output:", output)
        print("############################################################")
    return output #["response"]


async def stream_response(message, delta_t=0.1):
    for line in str(message).splitlines():
        yield line + "\n"  # Ensures that each line is correctly formatted
        await asyncio.sleep(delta_t)  # Simulate processing time


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
        st.session_state.messages.append({"role": "user", "content": file_message, "avatar": "./resources/images/user_0.png"})
        with st.chat_message("user"):
            st.markdown(file_message)

        # Process the file (example: just acknowledge it for now)
        agent_response = f"Received file: {uploaded_file.name}"
        st.session_state.messages.append({"role": "assistant", "content": agent_response, "avatar": "./resources/images/scientist_0.png"})
        with st.chat_message("assistant"):
            st.markdown(agent_response)


def run_agent_answer(config, prompt, chat_history):
    """Generate the response from the agent"""
    # Generate assistant response
    # response = None
    response = generate_response_agent_w_spinner(
            config.agent,
            prompt,
            chat_history=chat_history
        )
    with st.chat_message("assistant", avatar=response["avatar"]):
       asyncio.run(stream_to_streamlit(response["output"]))  # Stream the response asynchronously

    return response

"""
EPIC FAIL TO CHANGE AVATAR SHAPE

def display_helper(role: str, text: str, avatar_path: str, width: int=150):
    " " "Display a helper message with an image " " "
    with st.chat_message(role):
        # Display the image larger using st.image
        st.image(avatar_path, width=width)  # Adjust width as needed
        st.markdown(text)


async def display_helper_async(role: str, text: str, avatar_path: str, width: int = 150):
    " " "
    Display a helper message with an image and stream text asynchronously.
    
    Args:
        role (str): The role of the chat message ("user" or "assistant").
        text (str): The text content to display.
        avatar_path (str): Path to the avatar image.
        width (int): Width of the avatar image.
    " " "
    with st.chat_message(role):
        # Display the image larger using st.image
        st.image(avatar_path, width=width)  # Adjust width as needed
        
        # Stream the text asynchronously
        if isinstance(text, str):
            await stream_to_streamlit(text)
        else:
            st.markdown(text)
"""



# Chat
def chat(config):


    # Set the static background image
    # set_static_background("./resources/images/background_space_savannah.png")

    # Set up the title and chat history
    st.title("JairGPT")

    # Display chat history
    if "messages" in st.session_state:
        for message in st.session_state.messages[:config.memory_depth]:
            with st.chat_message(message["role"], avatar=message["avatar"]):
                st.markdown(message["content"])
            #display_helper(message["role"], message["content"], message["avatar"])
    else:
        st.session_state.messages = []
        response = run_agent_answer(config, "Introduce yourself and what your tools are.", [])
        st.session_state.messages.append({"role": "assistant", "content": response["output"], "avatar": response["avatar"]})

    # Chat input
    prompt = st.chat_input("Your text here:")
    # File Upload
    handle_file_upload()

    if prompt:
        # Add user message to the chat history
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "./resources/images/user_0.png"})
        
        with st.chat_message("user", avatar="./resources/images/user_0.png"):
            st.markdown(prompt)
        #display_helper("user", prompt, "./resources/images/user_0.png")

        # run_agent_answer()
        response = run_agent_answer(config, prompt, st.session_state.messages[:config.memory_depth])

        # Add assistant message to the chat history
        st.session_state.messages.append({"role": "assistant", "content": response["output"], "avatar": response["avatar"]})