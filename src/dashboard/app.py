"""
Dashboard application.

Pages:
  /          — cohort overview (biomarker distributions)
  /subject   — subject detail (per-window biomarker traces)
  /qc        — QC summary table
"""
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from pathlib import Path

from ..database.reader import read_cohort_summary
from ..utils.config import load_paths, load_config


def create_app(paths: dict) -> dash.Dash:
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], use_pages=True)

    app.layout = dbc.Container([
        dbc.NavbarSimple(
            brand="EEG Biomarker Platform",
            color="primary",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Cohort", href="/")),
                dbc.NavItem(dbc.NavLink("Subject", href="/subject")),
                dbc.NavItem(dbc.NavLink("QC", href="/qc")),
            ],
        ),
        dash.page_container,
    ], fluid=True)

    return app
