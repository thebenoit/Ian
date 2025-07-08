from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from tools.searchFacebook import SearchFacebook
from langgraph.prebuilt import ToolNode
from langchain.tools import Tool
from langchain.tools import StructuredTool
import os
import json
from langchain_core.messages import ToolMessage
from IPython.display import Image, display
from tools.base_tool import BaseTool
from langgraph.checkpoint.memory import MemorySaver
import time
from pydantic import BaseModel, Field
from typing import Any
from tools.coordinatesInput import CoordinatesInput
from tools.getCooridinates import GetCoordinates

load_dotenv()

print("running...")

memory = MemorySaver()

#initiate the state of the agent
class State(TypedDict):
    """State of the agent"""
    messages: Annotated[list, add_messages]
    #default values for the agent
    city: str = None
    location_near: dict = None
    radius: str = None
    minBudget: float = None
    maxBudget: float = None
    minBedrooms: int = None
    maxBedrooms: int = None
    coordinates: dict = None




#input schema for the web scraper tool
class WebScraperInput(BaseModel):
    lat: float = Field(description="The latitude of the location to search for")
    lon: float = Field(description="The longitude of the location to search for")
    minBudget: float = Field(description="The minimum budget for the rental")
    maxBudget: float = Field(description="The maximum budget for the rental")
    minBedrooms: int = Field(
        description="The minimum number of bedrooms for the rental"
    )
    maxBedrooms: int = Field(
        description="The maximum number of bedrooms for the rental"
    )
    


print("state initialized...")



# instantiate the tools
scraper = SearchFacebook()
coordinates_finder = GetCoordinates()

config = {"configurable": {"thread_id": "1"}}

# search facebook Marketplace according to the provided parameters
search_tool = StructuredTool.from_function(
    func=scraper.execute,
    name=scraper.name,
    description=scraper.description,
    args_schema=WebScraperInput,
)

# find coordinates of locations based on OpenStreetMap tags (schools, parks, restaurants, etc.)
coordinates_tool = StructuredTool.from_function(
    func=coordinates_finder.execute,
    name=coordinates_finder.name,
    description=coordinates_finder.description,
    args_schema=CoordinatesInput,
)
#put the tools in a list
tools = [search_tool, coordinates_tool]


print("tools initialized...")

graphBuilder = StateGraph(State)

print("graphBuilder initialized...")

# init the llm
moveout = init_chat_model("gpt-4o-mini", model_provider="openai")

#connect the tools to the llm
moveout = moveout.bind_tools(tools)

print("moveout llm initialized and binded to tools...")


def chatbot(state: State):
    # get the last message
    return {"messages": [moveout.invoke(state["messages"])]}

def validate_preferences(state: State):
    value = interrupt(
        "validate_preferences",
        "Please validate your preferences",
        state,
    )
    return {"preferences": value}

def route_tools(
    state: State,
):
    """use conditional_edge to route to the tool node if the last message contains
    a tool call otherwise route to the end"""

    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tool"
    return END


graphBuilder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graphBuilder.add_node("tool_node", tool_node)

graphBuilder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tool": "tool_node", END: END},
)


graphBuilder.add_edge("tool_node", "chatbot")
graphBuilder.add_edge(START, "chatbot")
# graphBuilder.add_edge("chatbot", END)
graph = graphBuilder.compile(checkpointer=memory)

#stream the graph updates(display the messages)
def stream_graph_updates(user_input: str):
    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config,
    ):
        for value in event.values():
            message = value["messages"][-1]
            if isinstance(message, ToolMessage):
                print(f"TOOL RESULT: {message.content}")
            print("moveout3.0:", message.pretty_print())


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
