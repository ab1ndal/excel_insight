# excel_insights/nodes/schemas.py
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict, Any

# -------- Inputs ---------
class Grid(BaseModel):
    rows: int
    columns: int

class TableItem(BaseModel):
    key: str
    table_name: Optional[str] = None
    headers: Optional[List[str]] = None
    units: Optional[List[str]] = None
    sample_rows: List[List[str]] = Field(default_factory=list)

# -------- Planner --------
class PlannerInput(BaseModel):
    objective: str
    grid: Grid
    tables: List[TableItem]

class PlotPlan(BaseModel):
    plot_id: str
    description: str
    data_sources: List[str]
    transformations: List[str]
    chart_type: Literal["line", "bar", "scatter", "histogram", "box", "heatmap"]
    x_axis: str
    y_axis: str

class PlannerOutput(BaseModel):
    plans: List[PlotPlan]


# -------- Code Generator --------
class PlotCode(BaseModel):
    plot_id: str
    code: str   # Python code string for plotting


# -------- Editor --------
class EditInput(BaseModel):
    current_code: str
    history: List[str]
    edit_request: str

class EditResponse(BaseModel):
    action: Literal["modify_code", "replan", "regenerate"]
    code: Optional[str] = None
    reason: str
