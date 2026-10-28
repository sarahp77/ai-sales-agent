import json
import os
from typing import Annotated, Literal
from dotenv import load_dotenv
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

# 1. Define Tools
@tool
def get_product_catalog() -> str:
    """Useful to fetch all products, their prices, descriptions, and real-time inventory status."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "products.json")
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            products = json.load(f)
        return json.dumps(products, indent=2)
    except Exception as e:
        return f"Error loading product catalog: {str(e)}"

tools = [get_product_catalog]
tool_node = ToolNode(tools)

# 2. Setup LLM
llm = ChatOpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
    model=os.getenv("MODEL_NAME", "gpt-4o"),
    temperature=0.2,
).bind_tools(tools)

# 3. Define Graph State
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

SYSTEM_PROMPT = SystemMessage(
    content="""You are Nova, an elite and professional AI Sales Assistant for an international tech education and developer tooling platform.

CRITICAL GUARDRAIL:
You MUST decline any non-sales or unrelated requests (such as writing poems, creative stories, code snippets unrelated to our courses, recipes, or general knowledge trivia). If asked about these, reply strictly with:
"I am Nova, your sales assistant here to help you with our courses and technical offerings. I'm unable to assist with off-topic requests, but I'd love to help you find the right course for your career goals!"

Operational Rules:
1. Always check the real product catalog using the `get_product_catalog` tool before answering queries regarding pricing, availability, or features.
2. Be concise, polite, professional, and persuasive.
3. If an item is 'out_of_stock' or not available, inform the user and suggest relevant alternatives from the catalog.
4. Keep all currency explicitly in USD ($)."""
)



# 4. Graph Nodes
def call_model(state: AgentState):
    messages = state["messages"]
    # Ensure system prompt is always at the beginning
    if not isinstance(messages[0], SystemMessage):
        messages = [SYSTEM_PROMPT] + messages
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# 5. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

sales_agent_app = workflow.compile()
