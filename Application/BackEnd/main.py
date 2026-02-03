"""  FastAPI applications with EndPoints   """

import sys
from pathlib import Path

# Allow importing AgenticRAG from parent (Application/) when running from BackEnd/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from pydantic import BaseModel, Field
from pydantic_core import CoreConfig
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import AgenticRAG
from langchain_core.messages import  HumanMessage


app = FastAPI(title = "writing backend code for RAG System")

# CORS : Allow the React FrontEnd to call your API
app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:5173", "*"],

        
    allow_headers = ["*"],  
    allow_methods = ["*"],  # allow all HTTP methods
    allow_credentials = True # allow cookies    
)


class ChatRequest(BaseModel) :
    message : str


# chat Route
@app.post("/chat")
def chat_check(request: ChatRequest):
    # 1. Build state: graph expects {"messages": [HumanMessage(...)]}
    state = {"messages": [HumanMessage(content=request.message)]}

    # 2. Invoke the RAG graph (from AgenticRAG.py)
    result = AgenticRAG.graph.invoke(state)

    # 3. Extract the last message (the AI's response)
    last_message = result["messages"][-1]
    response_text = last_message.content

    return {"response": response_text}


@app.get("/")
def api_call() :
    return {"message" : "I will going to write the BackEnd code with API"}

# Health message
@app.get("/health")
def health():
    return {"Status" : "ok"}

