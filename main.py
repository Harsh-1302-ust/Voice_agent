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

        save_message("user", user_text)

        web_context = search_web(user_text)
        history = get_recent_history()

        ai_response = ask_llm(history, web_context)
        print("AI Response:", ai_response)

        save_message("assistant", ai_response)
        speak(ai_response)


if __name__ == "__main__":
    main()
