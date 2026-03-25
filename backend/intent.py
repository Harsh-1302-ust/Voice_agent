def detect_intent(user_text: str):
    user_text = user_text.lower()

    if any(word in user_text for word in ["search", "latest", "news", "current"]):
        return "search"

    if any(word in user_text for word in ["save", "note", "remember this"]):
        return "save_note"

    if any(word in user_text for word in ["recall", "what did i say", "history"]):
        return "recall"

    return "chat"