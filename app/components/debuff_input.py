import dash
from dash import dcc, html, dash_table
import pandas as pd
from damage_simulator.buffs import Debuff
from damage_simulator.constants import DEBUFF_DIR
from dash import Input, Output, State
import os

# 初期データ
initial_df = pd.DataFrame({"デバフ種": [], "デバフ量": [], "備考": []}).astype(
    {"デバフ種": "str", "デバフ量": "float", "備考": "str"}
)


def get_debuff_presets():
    return [f.stem for f in DEBUFF_DIR.glob("*.csv")]


debuff_options = [
    {"label": b.value, "value": b.value} for b in Debuff.__members__.values()
]

layout = html.Div(
    [
        html.H3("デバフ管理"),
        dcc.Dropdown(
            id="debuff_preset_dropdown",
            options=[{"label": name, "value": name} for name in get_debuff_presets()],
            placeholder="デバフプリセット名",
        ),
        html.Button("デバフ読み込み", id="load_debuff", n_clicks=0),
        dash_table.DataTable(
            id="debuff_table",
            columns=[
                {
                    "name": "デバフ種",
                    "id": "デバフ種",
                    "presentation": "dropdown",
                },
                {
                    "name": "デバフ量",
                    "id": "デバフ量",
                    "type": "numeric",
                },
                {"name": "備考", "id": "備考", "type": "text"},
            ],
            data=initial_df.to_dict("records"),
            editable=True,
            row_deletable=True,
            dropdown={"デバフ種": {"options": debuff_options}},
            style_data={
                "whiteSpace": "normal",
                "height": "auto",
            },
            style_cell_conditional=[
                {"if": {"column_id": "デバフ種"}, "width": "35%"},
                {"if": {"column_id": "デバフ量"}, "width": "15%"},
                {"if": {"column_id": "備考"}, "width": "50%"},
            ],
        ),
        html.Button("行追加", id="add_debuff_row", n_clicks=0),
        html.Br(),
        dcc.Input(
            id="preset_name_read_debuff",
            type="text",
            placeholder="デバフプリセット名",
            style={
                "width": "95%",
                "height": "25px",
                "fontSize": "16px",
                "padding": "5px",
            },
        ),
        html.Button("デバフ保存", id="save_debuff", n_clicks=0),
        html.Div(id="debuff_save_status_message"),
    ],
    style={
        "width": "100%",
        "display": "inline-block",
        "vertical-align": "top",
        "margin-left": "10px",
    },
)


def register_debuff_callback(app):
    @app.callback(
        Output("debuff_table", "data"),
        Input("load_debuff", "n_clicks"),
        State("debuff_preset_dropdown", "value"),
        prevent_initial_call=True,
    )
    def load_debuff_preset(n_clicks, preset_name):
        if preset_name and os.path.exists(DEBUFF_DIR / f"{preset_name}.csv"):
            return pd.read_csv(DEBUFF_DIR / f"{preset_name}.csv").to_dict("records")
        return dash.no_update

    @app.callback(
        Output("debuff_table", "data", allow_duplicate=True),
        Input("add_debuff_row", "n_clicks"),
        State("debuff_table", "data"),
        prevent_initial_call=True,
    )
    def add_debuff_row(n_clicks, rows):
        rows.append({"デバフ種": "", "デバフ量": 0, "備考": ""})
        return rows

    @app.callback(
        Output("debuff_save_status_message", "children"),
        Output("debuff_preset_dropdown", "options"),
        Input("save_debuff", "n_clicks"),
        State("preset_name_read_debuff", "value"),
        State("debuff_table", "data"),
        State("debuff_preset_dropdown", "options"),
        prevent_initial_call=True,
    )
    def save_debuff_preset(n_clicks, preset_name, data, options):
        if preset_name:
            df = pd.DataFrame(data)
            df.to_csv(DEBUFF_DIR / f"{preset_name}.csv", index=False)
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
        "Debuff Input",
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css],
    )
    app.layout = layout
    register_debuff_callback(app)
    app.run_server(debug=True)
