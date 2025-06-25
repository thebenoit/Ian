from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

print("running...")


class State(TypedDict):
    """State of the agent"""

    messages: Annotated[list, add_messages]


graphBuilder = StateGraph(State)

llm = init_chat_model("gpt-3.5-turbo", model_provider="openai")


def chatbot(state: State):
    # get the last message
    return {"messages": [llm.invoke(state["messages"])]}


graphBuilder.add_node("chatbot", chatbot)

graphBuilder.add_edge(START, "chatbot")
graphBuilder.add_edge("chatbot", END)
graph = graphBuilder.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


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
