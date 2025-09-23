import polars as pl
from typing import Optional

def parse_excel_sheet(
    path,
    sheet_name: str,
    name_row: Optional[int] = None,
    header_row: int = 1,
    unit_row: Optional[int] = None,
    data_start_row: int = 1,
    engine: str = "calamine"
):
    """
    Parse an Excel sheet into structured parts using Polars.
    Row indices are 1-based (Excel-style, consistent with your Streamlit UI).
    """

    # Load all rows with no header so we can slice manually
    raw = pl.read_excel(
        source=path,
        sheet_name=sheet_name,
        engine=engine,
        has_header=False,
    )

    # Convert to a list of lists (rows)
    rows = raw.to_numpy().tolist()

    # Table name row
    table_name = str(rows[name_row - 1][0]) if name_row else None

    # Headers
    headers = [str(x) if x is not None else f"col{i}" for i, x in enumerate(rows[header_row - 1])]

    # Units
    units = rows[unit_row - 1] if unit_row else ["Unitless"] * len(headers)

    # Data rows
    start = data_start_row - 1 if data_start_row else (
        unit_row if unit_row else header_row
    )
    data_rows = rows[start:]

    # Build Polars DataFrame
    df = pl.DataFrame(data_rows, schema=headers, orient="row")

    return {
        "table_name": table_name,
        "headers": headers,
        "units": units,
        "data": df,   # Polars DataFrame
    }