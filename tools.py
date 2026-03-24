from mongodb import save_message, get_recent_history

def handle_tool(intent, user_text):
    if intent == "save_note":
        save_message("note", user_text)
        return "Got it. I've saved your note."

    if intent == "recall":
        history = get_recent_history(5)
        texts = [msg["content"] for msg in history if msg["role"] == "user"]
        return "Here are your recent inputs: " + " | ".join(texts)

    return None