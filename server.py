# server.py
import os
import uvicorn
from agents.ian import graph
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[dict]] = None

# Route de santé (optionnelle, LangGraph a déjà ses endpoints)
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
async def chat(request: ChatRequest):
    # get the user message
    user_message = request.message
    # get the chat history
    chat_history.append(HumanMessage(content=user_message))
    input_data = {"messages": chat_history}
    response = await graph.ainvoke(chat_history=input_data)
    
    return {"response": response.json()}

# def main():
#     print("Starting LangGraph server...")
#     port = int(os.getenv("PORT", "2024"))
#     uvicorn.run(
#         app,
#         host="0.0.0.0", 
#         port=port,
#         reload=True,
#     )

# if __name__ == "__main__":
#     main()