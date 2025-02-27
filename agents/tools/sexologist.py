
from langchain_community.chat_models import ChatOpenAI
    
def tool_sexologist(llm: ChatOpenAI, query: str) -> str:
    """ you are a sexologist """
    prompt = f"{query}"
    result = llm.invoke(prompt)

    return {
        "output": result.content,
        "agent": "sexologist",
    }
