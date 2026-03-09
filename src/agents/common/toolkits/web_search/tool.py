"""Web search tools using Tavily API."""

import logging

logger = logging.getLogger(__name__)

# Lazy initialization for TavilySearch
_tavily_search_instance = None


def get_tavily_search():
    """Get TavilySearch instance lazily, only when API key is available.

    Returns:
        TavilySearch instance or None if API key is not configured
    """
    global _tavily_search_instance
    if _tavily_search_instance is None:
        from src import config

        if config.enable_web_search:
            from langchain_tavily import TavilySearch

            _tavily_search_instance = TavilySearch()
            _tavily_search_instance.metadata = {"name": "Tavily 网页搜索"}
    return _tavily_search_instance
