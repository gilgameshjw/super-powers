
from langchain.chat_models import ChatOpenAI

def tool_coder (llm: ChatOpenAI, query: str) -> str:
    """ you are a coder """
    prompt = f"{query}"
    result = llm.invoke(prompt)

    return {
        "response": result.content,
        "agent": "coder",
    }
