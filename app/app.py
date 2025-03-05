import dash_bootstrap_components as dbc
import dash
from app.app_layout import layout
from app.app_callback import register_callbacks
from flask import Flask

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
server = Flask(__name__)
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css],
    server=server,
)
app.layout = layout
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
