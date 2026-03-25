from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from mongodb import save_message, get_recent_history
from intent import detect_intent
from tavily_search import search_web
from tools import handle_tool
from llm import ask_llm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(req: ChatRequest):
    user_text = req.message

    # Save user message
    save_message("user", user_text)

    # Intent detection
    intent = detect_intent(user_text)

    # Tool handling
    tool_response = handle_tool(intent, user_text)
    if tool_response:
        save_message("assistant", tool_response)
        return {"response": tool_response}

    # Web search if needed
    web_context = ""
    if intent == "search":
        web_context = search_web(user_text)

    # Memory
    history = get_recent_history()

    # LLM
    ai_response = ask_llm(history, web_context)

    save_message("assistant", ai_response)

    return {"response": ai_response}