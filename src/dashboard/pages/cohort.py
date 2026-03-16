"""Cohort overview page — biomarker distributions across subjects."""
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/", name="Cohort Overview")

BIOMARKER_OPTIONS = ["K_norm_mean", "L_norm_mean", "K_norm_std", "L_norm_std"]

layout = dbc.Container([
    html.H2("Cohort Overview"),
    dbc.Row([
        dbc.Col([
            html.Label("Biomarker"),
            dcc.Dropdown(
                id="cohort-biomarker-dropdown",
                options=[{"label": b, "value": b} for b in BIOMARKER_OPTIONS],
                value=BIOMARKER_OPTIONS[0],
            ),
        ], width=4),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="cohort-histogram"), width=6),
        dbc.Col(dcc.Graph(id="cohort-boxplot"), width=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="cohort-scatter"), width=12),
    ]),
], fluid=True)


@callback(
    Output("cohort-histogram", "figure"),
    Output("cohort-boxplot", "figure"),
    Output("cohort-scatter", "figure"),
    Input("cohort-biomarker-dropdown", "value"),
)
def update_cohort(biomarker):
    # TODO: load real data via read_cohort_summary()
    df = pd.DataFrame({"subject_id": [], biomarker: []})
    hist = px.histogram(df, x=biomarker, title=f"{biomarker} distribution")
    box = px.box(df, y=biomarker, title=f"{biomarker} boxplot")
    scatter = px.scatter(df, x="subject_id", y=biomarker, title=f"{biomarker} per subject")
    return hist, box, scatter
