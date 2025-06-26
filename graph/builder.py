from langgraph.graph import StateGraph
from services.broken_link_checker import LinkChecker
from services.content_analyzer import ContentAnalyzer

# Node functions
def run_readability(state):
    text = state["input"]
    result = LinkChecker(text).analyze()
    return {"readability": result}

def run_grammar(state):
    text = state["input"]
    result = ContentAnalyzer(text).analyze()
    return {"grammar": result}


# Graph builder
def build_graph():
    builder = StateGraph()

    # Add nodes
    builder.add_node("readability", run_readability)
    builder.add_node("grammar", run_grammar)


    # Set entry points (run in parallel)
    builder.set_entry_point(["readability", "grammar"])

    # After all 3 complete, coordinator runs
    builder.add_edge("readability", "coordinator")
    builder.add_edge("grammar", "coordinator")

    # Final node
    builder.set_finish_point("coordinator")

    return builder.compile()