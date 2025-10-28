# excel_insights/nodes/nodes.py
from agents import function_tool
from excel_insights.nodes.schemas import (
    PlannerInput, PlannerOutput, PlotPlan, PlotCode, EditInput, EditResponse
)

# Planner Tool
# ---- Planner ----
@function_tool()
def plan_plots(payload: PlannerInput) -> PlannerOutput:
    """
    Create structured plot plans from a user objective and parsed tables.
    """
    return PlannerOutput(plans=[])


# ---- Code Generator ----
@function_tool()
def generate_code(plan: PlotPlan) -> PlotCode:
    """
    Generate Python plotting code for a given PlotPlan.

    Notes
    -----
    - The function must use st.session_state["tables"] to fetch actual data.
    - Output code should build a figure object assigned to variable `fig`.
    - Acceptable backends: matplotlib or plotly.
    """
    return PlotCode(plot_id=plan.plot_id, code="fig = None")

# ---- Editor ----
@function_tool()
def edit_code(payload: EditInput) -> EditResponse:
    """
    Edit existing plot code or trigger replan/regenerate.

    Notes
    -----
    - Must only generate edits relevant to the parsed data in
      st.session_state["tables"].
    - Out-of-scope requests should be refused.

    """
    return EditResponse(action="replan", code="", reason="Not implemented yet")