from typing import TypedDict, Optional, Any

class GraphState(TypedDict, total=False):
    input: str
    readability: dict
    grammar: dict
    sentiment: dict
    insight: str