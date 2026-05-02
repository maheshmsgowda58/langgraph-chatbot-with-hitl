from langgraph.graph import StateGraph, START
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langgraph.types import interrupt
from dotenv import load_dotenv
import requests

load_dotenv()

# -------------------
# 1. LLM (Groq)
# -------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",   # stable model
    temperature=0
)

# -------------------
# 2. PORTFOLIO (STATE)
# -------------------
# Simple in-memory portfolio
PORTFOLIO = {}

# -------------------
# 3. TOOLS
# -------------------

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch the latest stock price for a given stock symbol.
    
    Args:
        symbol: Stock symbol (e.g., AAPL, TSLA)

    Returns:
        JSON response with stock price details
    """
    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    )
    r = requests.get(url, timeout=10)
    return r.json()


# -------------------
# BUY STOCK (HITL)
# -------------------
@tool
def purchase_stock(symbol: str, quantity: int) -> dict:
    """Buy a stock after human approval."""
    decision = interrupt(f"Approve BUY {quantity} shares of {symbol}?")

    if isinstance(decision, str) and decision.lower() == "yes":
        PORTFOLIO[symbol] = PORTFOLIO.get(symbol, 0) + quantity

        return {
            "status": "success",
            "message": f"✅ Bought {quantity} shares of {symbol}",
            "portfolio": PORTFOLIO
        }

    return {
        "status": "cancelled",
        "message": "❌ Purchase cancelled"
    }


# -------------------
# SELL STOCK (HITL + VALIDATION)
# -------------------
@tool
def sell_stock(symbol: str, quantity: int) -> dict:
    """Sell a stock after validation and human approval."""

    owned = PORTFOLIO.get(symbol, 0)

    # ❌ NOT OWNED
    if owned == 0:
        return {
            "status": "error",
            "message": f"❌ You do not own any shares of {symbol}"
        }

    # ❌ NOT ENOUGH
    if quantity > owned:
        return {
            "status": "error",
            "message": f"❌ You only have {owned} shares of {symbol}, cannot sell {quantity}"
        }

    # HITL approval
    decision = interrupt(f"Approve SELL {quantity} shares of {symbol}?")

    if isinstance(decision, str) and decision.lower() == "yes":
        PORTFOLIO[symbol] -= quantity

        # clean zero
        if PORTFOLIO[symbol] == 0:
            del PORTFOLIO[symbol]

        return {
            "status": "success",
            "message": f"✅ Sold {quantity} shares of {symbol}",
            "portfolio": PORTFOLIO
        }

    return {
        "status": "cancelled",
        "message": "❌ Sell cancelled"
    }


# -------------------
# VIEW PORTFOLIO
# -------------------
@tool
def view_portfolio() -> dict:
    """View current stock holdings."""
    return {
        "portfolio": PORTFOLIO
    }


# -------------------
# TOOL LIST
# -------------------
tools = [get_stock_price, purchase_stock, sell_stock, view_portfolio]

llm_with_tools = llm.bind_tools(tools)

# -------------------
# 4. STATE
# -------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# -------------------
# 5. NODE
# -------------------
def chat_node(state: ChatState):

    from langchain_core.messages import SystemMessage

    system = SystemMessage(content="""
You are a helpful stock assistant.

Rules:
- Normal chatbot for general questions
- Use tools only when needed

Stock rules:
- Use get_stock_price → for price
- Use purchase_stock → for buying
- Use sell_stock → for selling
- Use view_portfolio → when user asks holdings

Always respond clearly.
""")

    messages = [system] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}

tool_node = ToolNode(tools)

# -------------------
# 6. MEMORY
# -------------------
memory = MemorySaver()

# -------------------
# 7. GRAPH
# -------------------
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

chatbot = graph.compile(checkpointer=memory)