import streamlit as st
import pandas as pd
from pathlib import Path
from excel_insights.parser import parse_excel_sheet
from excel_insights.ui_components.config_manager import apply_configs_to_state, save_configs, load_configs
from excel_insights.ui_components.objective import objective_dashboard
from excel_insights.ui_components.insight import specify_insight
import json


st.set_page_config(page_title="Excel Insights", layout="wide")

if "tables" not in st.session_state:
    st.session_state["tables"] = {}

if "insight_spec" not in st.session_state:
    st.session_state["insight_spec"] = {}

st.title("📊 Excel Insights App")

tabs = st.tabs(["📂 File Uploads", "📝 Objective", "💡 Insights"])
with tabs[0]:
    
    st.header("Config Management")

    uploaded_cfg = st.file_uploader("Upload config JSON (optional)", type=["json"], key="config_upload")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Save Configs"):
            save_configs(st.session_state.get("configs", {}))
            st.success("Configs saved to .excel_configs.json")

    with col2:
        if st.button("📂 Import Configs"):
            if uploaded_cfg is not None:
                st.session_state["configs"] = json.load(uploaded_cfg)
                apply_configs_to_state(st.session_state["configs"], st.session_state)
                st.success("Configs imported from uploaded file")
            else:
                st.session_state["configs"] = load_configs()
                apply_configs_to_state(st.session_state["configs"], st.session_state)
                st.success("Configs imported from .excel_configs.json")

    with col3:
        st.download_button(
            "⬇️ Download Current Configs",
            data=json.dumps(st.session_state.get("configs", {}), indent=2),
            file_name="excel_configs.json",
            mime="application/json"
        )

    uploaded_files = st.file_uploader(
        "Upload one or more Excel files",
        type=["xlsx", "xls"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uf in uploaded_files:
            path = Path(uf.name)
            xls = pd.ExcelFile(uf)
            st.subheader(f"File: {path.name}")
            if st.button(f"Parse All Sheets in {path.name}", key=f"parseall_{uf.name}"):
                for sheet in xls.sheet_names:
                    cfg_key = f"{uf.name}_{sheet}"   # consistent with config keys
                    cfg = st.session_state["configs"].get(cfg_key, {})
                    parsed = parse_excel_sheet(
                        uf,
                        sheet,
                        name_row=cfg.get("name"),
                        header_row=cfg.get("header"),
                        unit_row=cfg.get("unit"),
                        data_start_row=cfg.get("data"),
                    )
                    st.session_state["tables"][cfg_key] = parsed
                st.success(f"All sheets in {path.name} parsed successfully")

            for sheet in xls.sheet_names:
                st.markdown(f"**Sheet: {sheet}**")
                toggle_cols = st.columns(2)
                with toggle_cols[0]:
                    use_name_row = st.checkbox("Use Table Name Row", value=st.session_state.get(f"use_name_{uf.name}_{sheet}", True), key=f"use_name_{uf.name}_{sheet}")
                with toggle_cols[1]:
                    use_unit_row = st.checkbox("Use Unit Row", value=st.session_state.get(f"use_unit_{uf.name}_{sheet}", True), key=f"use_unit_{uf.name}_{sheet}")
                
                cols = st.columns(4)
                with cols[0]:
                    name_row = st.number_input(
                            "Table Name Row",
                            min_value=1,
                            value=1,
                            step=1,
                            key=f"name_{uf.name}_{sheet}",
                            disabled=not use_name_row
                        )
                    if not use_name_row:
                        name_row = None
                with cols[1]:
                    header_row = st.number_input("Header Row", min_value=1, value=2, step=1, key=f"header_{uf.name}_{sheet}")
                with cols[2]:
                    unit_row = st.number_input("Unit Row", min_value=1, value=3, step=1, key=f"unit_{uf.name}_{sheet}", disabled=not use_unit_row)
                    if not use_unit_row:
                        unit_row = None
                with cols[3]:
                    data_row = st.number_input("First Data Row", min_value=1, value=4, step=1, key=f"data_{uf.name}_{sheet}")

                cfg_key = f"{uf.name}_{sheet}"
                st.session_state.setdefault("configs", {})
                st.session_state["configs"][cfg_key] = {
                    "name": name_row,
                    "header": header_row,
                    "unit": unit_row,
                    "data": data_row
                }
                if st.button(f"Parse {sheet}", key=f"parse_{uf.name}_{sheet}"):
                    parsed = parse_excel_sheet(
                        uf, sheet,
                        name_row=name_row,
                        header_row=header_row,
                        unit_row=unit_row,
                        data_start_row=data_row
                    )
                    st.session_state["tables"][f"{uf.name}:{sheet}"] = parsed
                    st.success(f"Parsed {sheet} successfully")
    if uploaded_files and st.button("🌐 Parse All Files"):
        for uf in uploaded_files:
            xls = pd.ExcelFile(uf)
            for sheet in xls.sheet_names:
                cfg_key = f"{uf.name}_{sheet}"
                cfg = st.session_state["configs"].get(cfg_key, {})
                parsed = parse_excel_sheet(
                    uf,
                    sheet,
                    name_row=cfg.get("name"),
                    header_row=cfg.get("header"),
                    unit_row=cfg.get("unit"),
                    data_start_row=cfg.get("data"),
                )
                st.session_state["tables"][cfg_key] = parsed
        st.success("All files parsed successfully")

    if st.session_state["tables"]:
        st.header("Parsed Tables")
        for key, tbl in st.session_state["tables"].items():
            st.subheader(key)
            if tbl["table_name"]:
                st.write(f"**Table Name**: {tbl['table_name']}")
            st.write("**Headers:**", tbl["headers"])
            if tbl["units"] is not None:
                st.write("**Units:**", tbl["units"])
            st.dataframe(tbl["data"].head())

with tabs[1]:
    objective_dashboard()

with tabs[2]:
    st.header("Insights")
    specify_insight()