from datetime import datetime, timezone
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
import re


@tool
def get_current_time() -> dict:
    """Return the current UTC time in ISO‑8601 format.
    Example → {"utc": "2025‑05‑21T06:42:00Z"}"""
    return {"local": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


KEYWORDS = {
    "include": {
        "time", "now", "clock", "current", "tell", "please", "what",
        "время", "времени", "час", "часа", "часов",
        "который", "которое", "сейчас", "текущее",
        "подскажи", "подскажешь", "скажи", "сколько",
    },
    "exclude": {
        "how", "long", "take", "takes", "need", "needs",
        "minutes", "minute", "hours", "hour",
        "start", "begin", "finish", "end", "until", "will", "when",
        "нужно", "нужен", "нужна", "нужны",
        "займет", "занимает", "понадобится", "требуется",
        "тратится", "уходит", "хватит", "хватало",
        "через", "дней", "день", "минут", "минуты", "часов",
        "во"
    },
}


def normalize_message(msg: str) -> set[str]:
    msg = msg.lower()
    msg = re.sub(r"[^\w\s]", "", msg)
    msg = re.sub(r"\s+", " ", msg).strip()
    return set(msg.split())


def manual_check(tool_input):
    msg = tool_input["messages"][-1].content
    words = normalize_message(msg)
    matches_include = words & KEYWORDS["include"]
    matches_exclude = words & KEYWORDS["exclude"]


    if len(matches_include) >= 2 and len(matches_exclude) == 0:
        tool_result = get_current_time.invoke({})
        current_time = tool_result['local']

        return {
            "messages": f"The current time is: {current_time    }",
            "__next__": "END"
        }
    else:
        return {"messages": tool_input["messages"], "__next__": "chat"}



llm = ChatOllama(
    model="mistral",
    tools=[get_current_time],
    system="call function `get_current_time` when you ask something about 'What time is it?'"
)



def chat(state):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": messages + [response]}

builder = StateGraph(MessagesState)
builder.add_node("chat", chat)
builder.add_node("tools", ToolNode([get_current_time]))
builder.add_edge(START, "chat")
builder.add_conditional_edges("chat", {
    "tools": lambda state: state["messages"][-1].tool_calls is not None,
    "END": lambda state: state["messages"][-1].tool_calls is None
})

builder.add_edge("tools", "chat")
builder.set_entry_point("chat")
builder.add_node("manual_check", manual_check)
builder.set_entry_point("manual_check")
builder.add_edge("manual_check", "chat")


app = builder.compile()

