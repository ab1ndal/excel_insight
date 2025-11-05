from typing import TypedDict, List, Dict, Optional, Any, Literal

class AppState(TypedDict, total=False):
    # User inputs
    objective: str
    grid: Dict[str, Any]            # expects {"rows": int, "columns": int}
    table_sample: List[Dict[str, Any]]    # your parsed tables

    # Planner output
    plans: List[Dict[str, Any]]     # each plan is a dict version of PlotPlan
    slot_map: Dict[str, str]        # plot_id -> "r,c" string to place in grid

    # Codegen output
    codes: Dict[str, Any]           # plot_id -> code string

    # Execution output
    figures: Dict[str, Any]         # plot_id -> render info or image path

    # Edit loop
    edit_request: Optional[str]
    edit_action: Literal["minor", "replan", "noop"]
    history: Dict[str, List[str]]   # plot_id -> list of code versions

    # Control and Errors    
    status: Literal["ok","blocked","planned","coded","executed","edited","failed"]
    route: Literal["plan", "codegen", "execute","edit", "end"]
    error: Optional[str]
    