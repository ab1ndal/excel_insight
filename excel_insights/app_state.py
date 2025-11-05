# graph.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any, Optional, Literal

# Define the global state
class AppState(TypedDict, total=False):
    # Insight Specification
    objective: str
    grid: Dict[str, int]
    tables: List[Dict[str, Any]]

    # Planner Output
    plans: List[Dict[str, Any]]
    codes: List[str]
    plots: List[Any]

    # Editor Output
    edit_request: Optional[List[str]] = None
    edit_status: List[Literal["ok", "blocked", "planned", "coded", "edited", "failed"]] = []
    edit_error: Optional[List[str]] = None
    edit_history: Dict[str, List[str]]  # for Editor undo functionality

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