from tavily import TavilyClient
from config import TAVILY_API_KEY

tavily = TavilyClient(api_key=TAVILY_API_KEY)

def search_web(query):
    results = tavily.search(query=query, max_results=3)

    context = ""
    for item in results.get("results", []):
        content = item.get("content", "")
        context += content[:500] + "\n"  # limit size

    return context.strip()