import asyncio
from typing import TypedDict, Annotated, List

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

from utils.model_loader import get_llm
from prompt_library.trip_planner_prompt import TRIP_PLANNER_SYSTEM_PROMPT
from logger.logging import logger

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "add_messages"]


async def create_trip_planner_graph():
    llm = get_llm()

    # Correct way: Create client WITHOUT async with at module level
    client = MultiServerMCPClient({
        "trip_mcp": {
            "transport": "stdio",
            "command": "uv",
            "args": ["run", "python", "-m", "trip_mcp.mcp_server"],
        }
    })

    # Get tools (this starts the connection)
    mcp_tools = await client.get_tools()

    logger.info(f"✅ Successfully loaded {len(mcp_tools)} MCP tools")

    # Build the graph
    def agent_node(state: AgentState):
        messages = state["messages"]
        system_msg = [{"role": "system", "content": TRIP_PLANNER_SYSTEM_PROMPT}]
        response = llm.bind_tools(mcp_tools).invoke(system_msg + messages)
        return {"messages": [response]}

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(mcp_tools))

    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        tools_condition,
        {"tools": "tools", END: END}
    )
    workflow.add_edge("tools", "agent")

    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    return app


# Create the graph at module level (this will now work)
graph = asyncio.run(create_trip_planner_graph())