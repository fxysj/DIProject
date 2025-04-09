from typing import Callable, Dict
from langchain_core.tools import Tool

registry: Dict[str, Callable[[], Tool]] = {
    "calculate_bmi": lambda: __import__('mcp_tools.calculate_bmi', fromlist=['build']).build(),
}