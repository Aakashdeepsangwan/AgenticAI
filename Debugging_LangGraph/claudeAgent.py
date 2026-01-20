# Workflow of ChatBot


from email import message
from typing import Annotated
from typing_extensions import TypedDict
from langchain_anthropic import ChatAnthropic
from langgraph import START, END
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages

from langchain_core.messages import BaseMessage
import os
from dotenv import load_dotenv



claudeAPI =  os.getenv("claudeAPI")
langsmithAPI = os.getenv("langsmithAPI")



call_claude = ChatAnthropic(
    model  = "",
    temperature= 0.7,
    api_key= claudeAPI
)



# State for the Graph

class State(TypedDict) :
    messages: Annotated[list[BaseMessage], add_messages]


def make_default_graph() :
    graph_workflow  = StateGraph(State)

    def call_model(state) :
        return {"messages" : [call_claude.invoke(state["messages"])]}

    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_edge("agent", END)
    graph_workflow.add_edge(START, "agent")

    agent = graph_workflow.compile()
    return agent


agent = make_default_graph()



# Now we can run this code in LangGraph Studio

