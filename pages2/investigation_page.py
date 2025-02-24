
import os
from datetime import datetime
import streamlit as st
from openai import OpenAI
import asyncio

from tools.researcher import run_researcher
from agents.agent import create_agent, generate_response_agent


# Function to simulate a spinner while waiting for run_researcher
def run_with_spinner(prompt, report_type, config):
    with st.spinner("Generating research report... Please wait."):
        return run_researcher(prompt, report_type, config.mock)



chat_history = []
user_input = "hello"
#"input": user_input
data = {"chat_history": chat_history, "input": user_input}
output = agent.invoke(data)



def investigation_page(config):
    # Investigation and Support page
    st.title(config.translations["title"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(config.translations["placeholder"])
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="resources/images/user_0.png"):
            st.markdown(prompt)

        response = None
        with st.chat_message("assistant", avatar="resources/images/scientist_0.png"):
            if "research" in prompt.lower():
                report_type = "research_report"
                # report_type = "subtopic_report"
                research_report, research_costs, research_time = run_with_spinner(prompt, report_type, config)
                response = "find research below" #research_report[:1000]

                print(response)
                print(f"costs: {research_costs}")
                print(f"time: {research_time}")
                # write research costs and time to chat in dictionary format:
                d_research = {
                    "status": "completed",
                    "costs": research_costs,
                    "time": research_time
                }
                st.write(d_research)

                st.write(response)


                # Save the full report to a temporary file
                report_file_path = "tmp/report.md"
                os.makedirs(os.path.dirname(report_file_path), exist_ok=True)  # Ensure the directory exists
                with open(report_file_path, "w", encoding="utf-8") as f:
                    f.write(research_report)

                # Display the download button
                download_placeholder = st.empty()  # Placeholder for the download button
                with download_placeholder.container():
                    with open(report_file_path, "rb") as file:
                        download_button = st.download_button(
                            label="Download Report",
                            data=file,
                            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown",
                        )

                # Remove the download button after the file is downloaded
                if download_button:
                    download_placeholder.empty() 

            else:
                client = OpenAI(api_key=config.llm["api_key"])
                stream = client.chat.completions.create(
                    model=config.llm["model_version"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
