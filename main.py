import asyncio
import sys

from agent.agentic_workflow import graph
from logger.logging import logger
from langchain_core.messages import HumanMessage, AIMessage


async def main():

    if len(sys.argv) < 2:
        print(
            'Usage: uv run python main.py "Plan a 7-day family trip to Tokyo in June with moderate budget"'
        )
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    logger.info(f"Starting trip planning for: {query}")

    config = {"configurable": {"thread_id": "cli_trip"}}

    inputs = {"messages": [HumanMessage(content=query)]}

    print("\n🌍 Agentic Trip Planner\n")

    final_answer = None

    async for event in graph.astream(inputs, config=config, stream_mode="values"):

        last_message = event["messages"][-1]

        if isinstance(last_message, AIMessage):

            # Show tool usage
            if last_message.tool_calls:
                for tool in last_message.tool_calls:
                    print(f"🔧 Using tool: {tool['name']}")

            # Capture final response
            if last_message.content:
                final_answer = last_message.content

    print("\n================ Final Travel Plan ================\n")

    if final_answer:
        print(final_answer)

    print("\n==================================================\n")


if __name__ == "__main__":
    asyncio.run(main())