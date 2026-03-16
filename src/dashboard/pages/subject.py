"""Subject detail page — per-window biomarker traces."""
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/subject", name="Subject Detail")

layout = dbc.Container([
    html.H2("Subject Detail"),
    dbc.Row([
        dbc.Col([
            html.Label("Subject ID"),
            dcc.Input(id="subject-id-input", type="text", placeholder="e.g. sub-0001", debounce=True),
        ], width=4),
        dbc.Col([
            html.Label("Biomarker"),
            dcc.Dropdown(
                id="subject-biomarker-dropdown",
                options=[
                    {"label": "K_norm", "value": "K_norm"},
                    {"label": "L_norm", "value": "L_norm"},
                ],
                value="K_norm",
            ),
        ], width=4),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="subject-timeseries"), width=12),
    ]),
], fluid=True)


@callback(
    Output("subject-timeseries", "figure"),
    Input("subject-id-input", "value"),
    Input("subject-biomarker-dropdown", "value"),
)
def update_subject(subject_id, biomarker):
    # TODO: load real window-level data
    df = pd.DataFrame({"window": [], biomarker: []})
    fig = px.line(df, x="window", y=biomarker, title=f"{subject_id} — {biomarker} per window")
    return fig
