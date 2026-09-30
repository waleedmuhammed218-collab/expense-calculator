from langgraph.graph import StateGraph, START
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages


# =========================
# LOAD ENVIRONMENT
# =========================

load_dotenv()


# =========================
# LLM
# =========================

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)


# =========================
# EXPENSE CALCULATOR TOOL
# =========================

@tool
def expense_calculator(
    food: int,
    transport: int,
    Things: int
):
    """Calculate total expenses."""

    total = food + transport + Things

    return total


# =========================
# TOOLS
# =========================

tools = [expense_calculator]

tool_node = ToolNode(tools)

llm_with_tool = llm.bind_tools(tools)


# =========================
# STATE
# =========================

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# =========================
# CHAT NODE
# =========================

def chat_node(state: ChatState):

    messages = state["messages"]

    response = llm_with_tool.invoke(messages)

    return {
        "messages": [response]
    }


# =========================
# GRAPH
# =========================

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)


# =========================
# EDGES
# =========================

graph.add_edge(START, "chat_node")

graph.add_conditional_edges(
    "chat_node",
    tools_condition
)

graph.add_edge("tools", "chat_node")


# =========================
# COMPILE
# =========================

app = graph.compile()