import os
from typing import List, Annotated, Sequence
from langchain_community.tools import WikipediaQueryRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryInput
from langchain_huggingface.embeddings import huggingface
from typing_extensions import TypedDict

from langgraph.prebuilt import create_react_agent
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


from langgraph.graph import StateGraph, START, END
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from langchain_core.document_loaders import Document

from langchain_community.document_loaders import WebBaseLoader # take url and convert it into the document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.graph.message import add_messages


urls = ["https://www.ibm.com/think/topics/agentic-ai-vs-generative-ai#7281538", "https://docs.databricks.com/aws/en/generative-ai/agent-bricks/key-info-extraction"]

# storing the data of url in the form of document

loaders = [WebBaseLoader(url) for url in urls] # the webBaseLoader 
docs = []

for loader in loaders :
    docs.extend(loader.load())


# len(docs) = 2 , first elements contains the full data of that particular url
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

chunks = splitter.split_documents(docs)

Embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

vectore_store = FAISS.from_documents(chunks, Embeddings)
retriever = vectore_store.as_retriever()

# retriever.invoke() 

def retriever_tool_funtion(query : str) -> str :
    """  Use this tools to fetch the relevant knowledge base info """

    docs = retriever.invoke(query)
    return "\n".join(doc.page_content for doc in docs)


retriever_tool = tool(retriever_tool_funtion)
wikitool = WikipediaQueryRun(api_wrapper = WikipediaAPIWrapper())

tools = [retriever_tool, wikitool]



# Initialise the llm and bind the tools with the llm
load_dotenv() # load the environment variable
api_key= os.getenv("claudeAPI")

claude = ChatAnthropic(
    model = "claude-haiku-4-5-20251001",
    temperature = 0.7,
    api_key= api_key
)


agent = create_react_agent(claude, tools) # Agent Bind the tools automatically with the LLM



# Agent State

class AgentState(TypedDict) :
    # Annotated provides the metadata
    # BaseMessage is the base class for all messages types in LangChain, it defines the common structure for messages in a conversation
    messages : Annotated[Sequence[BaseMessage], add_messages]

builder = StateGraph(AgentState)
builder.add_node('react_agent', agent) 
builder.set_entry_point("react_agent")
builder.add_edge("react_agent", END)
graph= builder.compile()



user_query  = "what is the difference b/w agentic AI and GenAI"
state = {'messages' : [HumanMessage(content = user_query)]}
result = graph.invoke(state)
print(result['messages'][-1].content)


















