# graph.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any

# Define the global state
class AppState(TypedDict, total=False):
    objective: str
    grid: str
    tables: Dict[str, Any]
    plans: List[Dict[str, Any]]
    codes: List[str]
    plots: List[Any]
    history: Dict[str, List[str]]  # for Editor undo functionality

def build_graph():
    workflow = StateGraph(AppState)

    workflow.add_node("guardrail", guardrail_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("codegen", codegen_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("editor", editor_node)

    # Edges
    workflow.set_entry_point("guardrail")
    workflow.add_edge("guardrail", "planner")
    workflow.add_edge("planner", "codegen")
    workflow.add_edge("codegen", "executor")
    workflow.add_edge("executor", "editor")
    workflow.add_edge("editor", END)