import fastapi
import os
from fastapi import FastAPI
import uvicorn
from copilotkit import LangGraphAGUIAgent 
from ag_ui_langgraph import add_langgraph_fastapi_endpoint 
from agents.ian import graph

app = FastAPI()

add_langgraph_fastapi_endpoint(
    app=app,
    agent=LangGraphAGUIAgent(
        name="ian",
        description="A chatbot that can help you find appartments all over the world",
        graph=graph
    ),
    path="/chat",
)

# add new route for health check
@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}
 
def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "server:app", # the path to your FastAPI file, replace this if its different
        host="0.0.0.0",
        port=port,
        reload=True,
    )