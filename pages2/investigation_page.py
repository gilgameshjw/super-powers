import streamlit as st
from openai import OpenAI
import asyncio

from tools.researcher import run_researcher


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
        with st.chat_message("user"):
            st.markdown(prompt)

        if "research" in prompt.lower():
            report_type = "research_report"
            # report_type = "subtopic_report"
            research_report, research_costs = run_researcher(prompt, report_type)
            #asyncio.run(get_report(prompt, report_type))
            response = research_report[:100]
            #print(research_report)
            print(f"costs: {research_costs}")


        else:

            with st.chat_message("assistant"):
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
            # timer waiting 2 mins
            #import time
            #time.sleep(120)

        st.session_state.messages.append({"role": "assistant", "content": response})
