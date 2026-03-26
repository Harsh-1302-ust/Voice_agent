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

# ✅ include session_id
class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.post("/chat")
async def chat(req: ChatRequest):
    user_text = req.message
    session_id = req.session_id

    save_message("user", user_text, session_id=session_id)

    intent = detect_intent(user_text)

    tool_response = handle_tool(intent, user_text)
    if tool_response:
        save_message("assistant", tool_response, session_id=session_id)
        return {"response": tool_response}

    web_context = ""
    if intent == "search":
        web_context = search_web(user_text)

    history = get_recent_history(session_id=session_id)

    ai_response = ask_llm(history, web_context)

    save_message("assistant", ai_response, session_id=session_id)

    return {"response": ai_response}


@app.get("/history/{session_id}")
async def get_history(session_id: str):
    history = get_recent_history(session_id=session_id)

    formatted = []
    for msg in history:
        if msg["role"] in ["user", "assistant"]:
            formatted.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    return {"messages": formatted}