"""QC summary page."""
import dash
from dash import dash_table, html
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path="/qc", name="QC")

layout = dbc.Container([
    html.H2("QC Summary"),
    html.P("Subject-level quality control metrics."),
    dash_table.DataTable(
        id="qc-table",
        columns=[],  # populated at runtime
        data=[],
        filter_action="native",
        sort_action="native",
        page_size=20,
        style_table={"overflowX": "auto"},
    ),
], fluid=True)
