from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state import AppState
from nodes.guardrail import guardrail_node
from nodes.plan import plan_node
from nodes.codegen import codegen_node
from nodes.execute import execute_node
from nodes.edit import edit_node



def build_graph():
    """
    Function to build Langgraph Agent
    """
    # Initialize Graph
    g = StateGraph(AppState)
    
    # Initialize Nodes
    g.add_node("guardrail", guardrail_node)
    g.add_node("plan", plan_node)
    g.add_node("codegen", codegen_node)
    g.add_node("execute", execute_node)
    g.add_node("edit", edit_node)
    g.set_entry_point("guardrail")

    # Initialize Edges
    g.add_conditional_edges(
        "guardrail",
        lambda s: s.get("route"),
        {
            "plan": "plan",
            "edit": "edit",
            "end": END
        }
    )
    g.add_conditional_edges(
        "edit",
        lambda s: s.get("route"),
        {"plan": "plan", "codegen": "codegen", "end": END},
    )
    g.add_edge("plan", "codegen")
    g.add_edge("codegen", "execute")
    g.add_edge("execute", END)

    return g.compile(checkpointer=MemorySaver())