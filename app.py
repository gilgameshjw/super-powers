import os
import streamlit as st

from src.config import Config  # Import the Config class
from pages2.investigation_page import investigation_page  # Import the Investigation page logic
from pages2.support_page import support_page  # Import the Support page logic
from pages2.support_page_2 import support_page_2  # Import the Support page logic
from src.utils import reset_page_language



# Initialize configuration
config = Config("config.yaml")

# set attributes
config.set_attributes()

# set browser
config.set_browser_search("tavily")

# Sidebar radio for LLM provider selection
llm_providers = ["openai", "claude", "deepseek"]
st.sidebar.title("LLM Provider")
selected_provider = st.sidebar.radio("Select LLM Provider", options=llm_providers, index=0)
if "provider" not in st.session_state or selected_provider != st.session_state["provider"]:
    config.set_llm_provider(selected_provider)
    st.session_state["provider"] = selected_provider


if "language" not in st.session_state:
    config.set_pages_translations("en")
    st.session_state["language"] = "en"


st.sidebar.title("Language")
language = st.sidebar.text_input(
    "Enter your language code (e.g., 'en', 'cn', 'ar', 'ru', 'cn', 'fr', 'kz',...): ", 
    value="en"
).strip()


# if language changed, update config
if language != st.session_state["language"]:
    reset_page_language(config, language)

# set search agent
if "search_agent" not in st.session_state:
    config.set_researcher()
    st.session_state["search_agent"] = "config.researcher"
    os.environ['OPENAI_API_KEY'] = config.researcher["openai_api_key"] 
    os.environ['TAVILY_API_KEY'] = config.researcher["tavily_api_key"]

if "agent" not in st.session_state:
    # set agent
    config.set_up_agent()
    st.session_state["agent"] = "config.agent"

# Top navigation bar
pages = ["Investigation", "Support us", "Donate"]
selected_page = st.selectbox("Pages", pages, index=0)

# Load the selected page
if selected_page == "Investigation":
    investigation_page(config)  # Call the Investigation page logic
    
elif selected_page == "Support us":
    support_page(config)  # Call the Support page logic

elif selected_page == "Donate":
    support_page_2(config)  # Call the Support page logic