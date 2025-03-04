import dash_bootstrap_components as dbc
import dash
from app_layout import layout
from app_callback import register_callbacks

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(
    "Damage Calculation Tool",
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css],
)
app.layout = layout
register_callbacks(app)
app.run_server()
