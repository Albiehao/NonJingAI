"""Toolkits for agents."""
# Import tools from individual modules
from src.agents.common.toolkits.calculator import calculator
from src.agents.common.toolkits.human_approval import get_approved_user_goal
from src.agents.common.toolkits.image_gen import text_to_img_demo
from src.agents.common.toolkits.kg_query import query_knowledge_graph
from src.agents.common.toolkits.knowledge_base.tool import get_kb_based_tools
from src.agents.common.toolkits.weather import weather_forecast
from src.agents.common.toolkits.web_search.tool import get_tavily_search
from src.agents.common.toolkits.yolo.tool import yolo
from src.agents.common.toolkits.agrochemicals import get_agrochemical_by_name

__all__ = [
    "calculator",
    "text_to_img_demo",
    "get_approved_user_goal",
    "query_knowledge_graph",
    "weather_forecast",
    "yolo",
    "get_kb_based_tools",
    "get_tavily_search",
    "get_agrochemical_by_name",
]