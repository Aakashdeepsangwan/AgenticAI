from fastapi import FastAPI, HTTPException
import uvicorn
from schemas import PostCreate
from DB import Post, create_db_and_tables, get_async_session
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app : FastAPI) :
    await create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan)
text_post =  {
    1: {"title": "New Post", "content": "cool post"},
    2: {"title": "Getting Started", "content": "A beginner's guide to the basics."},
    3: {"title": "Deep Dive", "content": "Exploring advanced concepts and patterns."},
    4: {"title": "Tips & Tricks", "content": "Useful shortcuts and best practices."},
    5: {"title": "Common Mistakes", "content": "What to avoid and how to fix it."},
    6: {"title": "Quick Tutorial", "content": "Step-by-step walkthrough in 5 minutes."},
    7: {"title": "Behind the Scenes", "content": "How it works under the hood."},
    8: {"title": "FAQ", "content": "Frequently asked questions answered."},
    9: {"title": "Resources", "content": "Links and references for further learning."},
    10: {"title": "Wrap Up", "content": "Summary and next steps."}
}


## query parameters - comes after the ? marks in the url


### FastAPI : It automatically validates all data going into and coming out of the function


@app.get("/posts")
def get_all_posts(limit : int = None) :
    if limit :
        return list(text_post.values())[:limit]

    return text_post


@app.get("/posts/{id}")
def get_post(id : int ):
    if id not in text_post :
        raise HTTPException(status_code = 404, detail= "Post don't found")
    return text_post[id]



@app.get("/hello-world") # decorator in the fastapi
def hello_world() :
    return {"message" : "Hello World"} # Json



## We send the data using path parameter and query parameter, but data can also be sent using request Body Parameter
# PostCreate is the request body

@app.post("/posts") 
def create_post(post : PostCreate) -> PostCreate:
    new_post = {"title" : post.title, "content" : post.content}
    text_post[max(text_post.keys())+1] = new_post
    return new_post












