from typing import TypedDict, Annotated
import operator

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from src import config
from src.tools import TOOLS

llm = ChatOpenAI(
    model=config.CHAT_MODEL,
    temperature=0,
    api_key=config.OPENAI_API_KEY,
).bind_tools(TOOLS)

SYSTEM_PROMPT = SystemMessage(
    content=(
        "You are an assistant that can control a browser to complete tasks "
        "for the user - opening websites, searching Google, playing YouTube "
        "videos, sending WhatsApp messages, and filling out forms. "
        "Look at the user's message and figure out which tool(s) to call to "
        "get it done. If a task needs more info from the user (like a "
        "message to send, or a URL), ask for it instead of guessing. "
        "After using a tool, tell the user clearly what you did."
    )
)


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]


def call_model(state: AgentState) -> AgentState:
    messages = [SYSTEM_PROMPT] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(TOOLS))

    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile()
