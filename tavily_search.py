from tavily import TavilyClient
from config import TAVILY_API_KEY

tavily = TavilyClient(api_key=TAVILY_API_KEY)

def search_web(query):
    results = tavily.search(query=query, max_results=3)
    context = ""

    for item in results.get("results", []):
        context += item.get("content", "") + "\n"

    return context
