

import os
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents import Tool
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.agents import create_openai_functions_agent

from tools.researcher import run_researcher


prompt_agent_personality = """
    You are a friendly conversational, smart agent.
"""


def set_up_agent(config):
    
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", 
        temperature=0, 
        api_key=config.llm["api_key"])    

    # Tools
    @tool
    def run_researcher(query: str) -> str:
        """ docstring """
        research_report, research_costs, research_time = run_researcher(prompt, report_type, config.mock)
        response = "find research below" #research_report[:1000]

        print(response)
        print(f"costs: {research_costs}")
        print(f"time: {research_time}")
        
        # Save the full report to a temporary file
        report_file_path = "tmp/report.md"
        os.makedirs(os.path.dirname(report_file_path), exist_ok=True)  # Ensure the directory exists
        with open(report_file_path, "w", encoding="utf-8") as f:
            f.write(research_report)
        
        # write research costs and time to chat in dictionary format:
        d_research = {
                    "status": "completed",
                    "costs": research_costs,
                    "time": research_time
        }

        return {
            "research_metadata": d_research,
            "response": response,
            "agent": "researcher",
            "file_data": "report_file_path"     
        }

    @tool
    def run_coder (query: str) -> str:
        """ docstring """
        prompt = f"{query}"
        result = llm.invoke(prompt)
        return result.content


    # Set up tools
    run_researcher.__doc__ = config.d_personalities["researcher"]
    run_coder.__doc__ = config.d_personalities["coder"]

    tools = [
        run_researcher,
        run_coder
    ]
    
    # create agent
    agent = create_agent(tools, llm, plan="default")

    agent = AgentExecutor(agent=agent, tools=tools)

    return agent


def generate_response_agent(agent, user_input, chat_history=[]):
    """
    Generate the response from the agent
    """
    data = {"chat_history": chat_history, "input": user_input}
    output = agent.invoke(data)
    chat_history.append(user_input)
    chat_history.append(output["output"])
    return output["output"]
