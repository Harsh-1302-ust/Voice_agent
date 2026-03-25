import ssl
import urllib3

# -------- SSL / Proxy Patch --------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

try:
    import httpx

    class PatchedClient(httpx.Client):
        def __init__(self, *args, **kwargs):
            kwargs["verify"] = False
            super().__init__(*args, **kwargs)

    class PatchedAsyncClient(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            kwargs["verify"] = False
            super().__init__(*args, **kwargs)

    httpx.Client = PatchedClient
    httpx.AsyncClient = PatchedAsyncClient
except Exception:
    pass

try:
    import requests
    original_request = requests.Session.request

    def patched_request(self, *args, **kwargs):
        kwargs["verify"] = False
        return original_request(self, *args, **kwargs)

    requests.Session.request = patched_request
except Exception:
    pass
# -----------------------------------

from speech import listen
from tts import speak
from mongodb import save_message, get_recent_history
from tavily_search import search_web
from llm import ask_llm
from backend.intent import detect_intent
from tools import handle_tool


def main():
    while True:
        try:
            user_text = listen()
            print("You said:", user_text)
        except Exception:
            print("Could not understand audio")
            continue

        if user_text.lower().strip() in ["stop", "exit"]:
            print("Stopping execution.")
            break

        # Save user input
        save_message("user", user_text)

        # 🔥 Step 1: Detect Intent
        intent = detect_intent(user_text)
        print("Detected intent:", intent)

        # 🔥 Step 2: Handle Tool (if applicable)
        tool_response = handle_tool(intent, user_text)
        if tool_response:
            print("Tool Response:", tool_response)
            save_message("assistant", tool_response)
            speak(tool_response)
            continue

        # 🔥 Step 3: Smart Search (only if needed)
        web_context = ""
        if intent == "search":
            web_context = search_web(user_text)

        # 🔥 Step 4: Get Memory
        history = get_recent_history()

        # 🔥 Step 5: LLM Response
        ai_response = ask_llm(history, web_context)
        print("AI Response:", ai_response)

        # Save + Speak
        save_message("assistant", ai_response)
        speak(ai_response)


if __name__ == "__main__":
    main()