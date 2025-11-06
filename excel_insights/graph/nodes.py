# excel_insights/nodes/nodes.py
from excel_insights.nodes.schemas import (
    PlannerInput, PlannerOutput, PlotPlan, PlotCode, EditInput, EditResponse
)
from excel_insights.config import client
from excel_insights.graph.state import AppState

def guardrail_node():
    """
    Guardrail node to check for any potential issues in the user's input
    """
    def _node(state: AppState) -> AppState:
        text = state.get("objective")
        if state.get("edit_request"):
            text += "\n Edit Request: " + state.get("edit_request")
        mod = client.moderations.create(
            model="omni-moderation-latest",
            input=text
        )
        if mod.results[0].flagged:
            state["route"] = "end"
            state["error"] = "Guardrail check failed"
        else:
            if state.get("edit_request"):
                state["route"] = "edit"
            else:
                state["route"] = "plan"
        return state
    return _node

def plan_node():
    """
    Plan node to generate a plan for plots based on the user's input
    """
    def _node(state: AppState) -> AppState:
        
        return state
    return _node
