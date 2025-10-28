import streamlit as st
from pathlib import Path
import json
from excel_insights.nodes.guardrail import guardrail_check
from excel_insights.nodes.create_agent import agent
from excel_insights.nodes.schemas import PlannerInput, Grid, TableItem

DEFAULT_PAYLOAD_FILE = Path(".insight_payload.json")

def save_payload(payload: dict, file: Path = DEFAULT_PAYLOAD_FILE):
    """Save the current LLM payload to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        st.success(f"Payload saved to {file}")
    except Exception as e:
        st.error(f"Failed to save payload: {e}")

def load_payload(file: Path = DEFAULT_PAYLOAD_FILE) -> dict:
    """Load the LLM payload from a JSON file, if it exists."""
    try:
        if file.exists():
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            st.warning(f"No payload file found at {file}")
            return {}
    except Exception as e:
        st.error(f"Failed to load payload: {e}")
        return {}
    
def specify_objective():
    st.markdown("### Dashboard Layout")
    col1, col2 = st.columns(2)
    with col1:
        rows = st.number_input("Number of rows", min_value=1, max_value=5, value=2, step=1)
    with col2:
        cols = st.number_input("Number of columns", min_value=1, max_value=5, value=2, step=1)
        
    st.write(f"Dashboard grid: {rows} x {cols}")

    st.markdown("### Define Your Objective")
    user_objective = st.text_area(
        "What would you like to learn or visualize from the data?",
        placeholder="e.g. Derive insights from the data, compare categories, plot time series..."
    )

    if st.button("Confirm Objective & Layout"):
        table_context = []
        for key, tbl in st.session_state["tables"].items():
            # Keep it light: only show first 5 rows
            sample = tbl["data"].head(5).to_pandas().to_dict(orient="records")

            table_context.append(
                TableItem(
                    key=key,
                    table_name=tbl.get("table_name"),
                    headers=tbl.get("headers"),
                    units=tbl.get("units"),
                    sample_rows=sample,
                )
            )
        
        grid = Grid(rows=rows, columns=cols)

        st.session_state["insight_spec"] = PlannerInput(
            objective=user_objective.strip() if user_objective else "Derive insights from the data",
            grid=grid,
            tables=table_context,
        )
        st.success("✅ Saved insight specification")

def show_objective():
    # Show what is saved (if any)
    if "insight_spec" in st.session_state:
        st.markdown("#### Current specification")
        st.json(st.session_state["insight_spec"])

    return st.session_state.get("insight_spec", None)

def objective_dashboard():
    st.header("Objective")
    if "tables" not in st.session_state or not st.session_state["tables"]:
        st.info("Please parse some tables first in the 📂 File Uploads tab.")
    else:
        specify_objective()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Save Objective"):
                save_payload(st.session_state["insight_spec"])
        with col2:
            if st.button("📂 Import Objective"):
                st.session_state["insight_spec"] = load_payload()
        with col3:
            if st.session_state["insight_spec"]:
                st.download_button(
                    label="⬇️ Download Payload",
                    data=json.dumps(st.session_state["insight_spec"], indent=2),
                    file_name="insight_payload.json",
                    mime="application/json",
                )
        show_objective()
        with col4:
            if st.button("Generate Insights"):
                if st.session_state["insight_spec"]:
                    if not guardrail_check(st.session_state["insight_spec"]["objective"]):
                        st.error("❌ Objective fails guardrail checks")
                    else:
                        with st.spinner("Generating insights..."):
                            result = agent.run(st.session_state["insight_spec"])
                            plans = result.output
                            st.session_state["plans"] = plans
                            st.success("✅ Insights generated")