
from langchain.chat_models import ChatOpenAI

def tool_psychologist(llm: ChatOpenAI, query: str) -> str:
    """ you are a psychologist """
    prompt = f"{query}"
    result = llm.invoke(prompt)

    return {
        "response": result.content,
        "agent": "psychologist",
    }
