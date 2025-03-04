import dash
from dash import dcc, html, dash_table
import pandas as pd
from damage_simulator.buffs import Buff
from damage_simulator.constants import BUFF_DIR
from dash import Input, Output, State
import os

# 初期データ
initial_df = pd.DataFrame({"バフ種": [], "バフ量": [], "備考": []}).astype(
    {"バフ種": "str", "バフ量": "float", "備考": "str"}
)


def get_buff_presets():
    return [f.stem for f in BUFF_DIR.glob("*.csv")]


buff_options = [{"label": b.value, "value": b.value} for b in Buff.__members__.values()]

layout = html.Div(
    [
        html.H3("バフ管理"),
        dcc.Dropdown(
            id="buff_preset_dropdown",
            options=[{"label": name, "value": name} for name in get_buff_presets()],
            placeholder="バフプリセット名",
        ),
        html.Button("バフ読み込み", id="load_buff", n_clicks=0),
        dash_table.DataTable(
            id="buff_table",
            columns=[
                {
                    "name": "バフ種",
                    "id": "バフ種",
                    "presentation": "dropdown",
                },
                {
                    "name": "バフ量",
                    "id": "バフ量",
                    "type": "numeric",
                },
                {"name": "備考", "id": "備考", "type": "text"},
            ],
            data=initial_df.to_dict("records"),
            editable=True,
            row_deletable=True,
            dropdown={"バフ種": {"options": buff_options}},
            style_data={
                "whiteSpace": "normal",
                "height": "auto",
            },
            style_cell_conditional=[
                {"if": {"column_id": "バフ種"}, "width": "35%"},
                {"if": {"column_id": "バフ量"}, "width": "15%"},
                {"if": {"column_id": "備考"}, "width": "50%"},
            ],
        ),
        html.Button("行追加", id="add_buff_row", n_clicks=0),
        html.Br(),
        dcc.Input(
            id="preset_name",
            type="text",
            placeholder="バフプリセット名",
            style={
                "width": "95%",
                "height": "25px",
                "fontSize": "16px",
                "padding": "5px",
            },
        ),
        html.Button("バフ保存", id="save_buff", n_clicks=0),
        html.Div(id="buff_save_status_message"),
    ],
    style={
        "width": "100%",
        "display": "inline-block",
        "vertical-align": "top",
    },
)


def register_buff_callback(app):
    @app.callback(
        Output("buff_table", "data"),
        Input("load_buff", "n_clicks"),
        State("buff_preset_dropdown", "value"),
        prevent_initial_call=True,
    )
    def load_buff_preset(n_clicks, preset_name):
        if preset_name and os.path.exists(BUFF_DIR / f"{preset_name}.csv"):
            return pd.read_csv(BUFF_DIR / f"{preset_name}.csv").to_dict("records")
        return dash.no_update

    @app.callback(
        Output("buff_table", "data", allow_duplicate=True),
        Input("add_buff_row", "n_clicks"),
        State("buff_table", "data"),
        prevent_initial_call=True,
    )
    def add_buff_row(n_clicks, rows):
        rows.append({"バフ種": "", "バフ量": 0, "備考": ""})
        return rows

    @app.callback(
        Output("buff_save_status_message", "children"),
        Output("buff_preset_dropdown", "options"),
        Input("save_buff", "n_clicks"),
        State("preset_name", "value"),
        State("buff_table", "data"),
        State("buff_preset_dropdown", "options"),
        prevent_initial_call=True,
    )
    def save_buff_preset(n_clicks, preset_name, data, options):
        if preset_name:
            df = pd.DataFrame(data)
            df.to_csv(BUFF_DIR / f"{preset_name}.csv", index=False)
            return f"{preset_name}を保存しました。", options + [
                {"label": preset_name, "value": preset_name}
            ]
        return "プリセット名を入力してください。", options


if __name__ == "__main__":
    import dash_bootstrap_components as dbc

    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )

    app = dash.Dash(
        "Buff Input",
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css],
    )
    app.layout = layout
    register_buff_callback(app)
    app.run_server(debug=True)
