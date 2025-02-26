

import os
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents import Tool
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.agents import create_openai_functions_agent

from tools.researcher import run_researcher



class FlexibleOutputAgentExecutor(AgentExecutor):
    """
        Ensure a given format for the agent
    """
    def _call(self, inputs: dict) -> dict:
        # Call the original AgentExecutor
        raw_output = super()._call(inputs)
        
        # Check if the output is already a dictionary
        if isinstance(raw_output, dict):
            if "avatar" in raw_output:
                print("DBG: raw_output is a dictionary")
                return raw_output  # Return as-is if it's a dictionary
            else:
                print("DBG2: raw_output has no avatar")
                return {
                    "response": raw_output["output"],
                    "avatar": "resources/images/giraffe_0.png"
                }
        
        # If the output is a string, wrap it in a dictionary with the "response" key
        elif isinstance(raw_output, str):
            return {
                "response": raw_output,
                "avatar": "resources/images/giraffe_0.png"
            }
        
        # Fallback for unexpected output types
        else:
            return {
                "response": "Unexpected output format.",
                "avatar": "resources/images/giraffe_0.png"
            }


def set_up_agent(config):
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-0125", 
        temperature=0, 
        api_key=config.llm["api_key"]
    )  

    # Tools
    @tool
    def tool_researcher(query: str) -> str:
        """ docstring """
        report_type = "research_report"

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
            "avatar": "resources/images/scientist_0.png",
            "file_data": report_file_path     
        }

    @tool
    def tool_coder (query: str) -> str:
        """ docstring """
        prompt = f"{query}"
        result = llm.invoke(prompt)

        return {
            "response": result.content,
            "agent": "coder",
            "avatar": "resources/images/coder_0.png",
        }
    
    @tool
    def tool_psychologist(query: str) -> str:
        """ docstring """
        prompt = f"{query}"
        result = llm.invoke(prompt)

        return {
            "response": result.content,
            "agent": "psychologist",
            "avatar": "resources/images/psychologist_0.png",
        }

    @tool
    def tool_sexologist(query: str) -> str:
        """ docstring """
        prompt = f"{query}"
        result = llm.invoke(prompt)

        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("Sexologist response:")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        return {
            "response": result.content,
            "agent": "sexologist",
            "avatar": "resources/images/sexologist_0.png",
        }


    # Set up tools
    tool_researcher.__doc__ = config.d_personalities["researcher"]
    tool_coder.__doc__ = config.d_personalities["coder"]
    tool_psychologist.__doc__ = config.d_personalities["psychologist"]
    tool_sexologist.__doc__ = config.d_personalities["sexologist"]

    main_agent_personality = config.d_personalities["main_agent"]
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", main_agent_personality),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    tools = [
        tool_researcher,
        tool_coder,
        tool_psychologist,
        tool_sexologist
    ]
    
    # create agent
    agent = create_openai_functions_agent(llm, tools, prompt)

    agent = FlexibleOutputAgentExecutor(agent=agent, tools=tools)

    return agent
