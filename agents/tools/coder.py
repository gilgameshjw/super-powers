
from langchain_community.chat_models import ChatOpenAI

def tool_coder (llm: ChatOpenAI, query: str) -> str:
    """ you are a coder """
    prompt = f"{query}"
    result = llm.invoke(prompt)

    return {
        "output": result.content,
        "agent": "coder",
    }
