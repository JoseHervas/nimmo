import sys, os
from langchain.tools import tool
# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from modules.news import NewsAPI

class SearchInput(BaseModel):
    category: str = Field(description="should be a category in english", default="science")

@tool("search_news", return_direct=False, args_schema=SearchInput)
def search_news(category: str) -> str:
    """Searches the News for the given category."""
    available_categories = ['science', 'technology', 'business', 'entertainment', 'general', 'health', 'sports']
    if category not in available_categories:
        return f"ERROR: {category} is not a valid category. Try again with one of {available_categories}"
    return NewsAPI().get_top_headlines(category)
