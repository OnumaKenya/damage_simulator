import dash
from dash import dcc, html, Output, Input, State, dash_table

basic_input_layout = html.Div(
    [
        html.Label("スキル倍率(%)"),
        html.Br(),
        dcc.Input(
            id="skill_ratio",
            type="number",
            min=0,
            value=100,
            style={"width": "100%"},
        ),
        html.Br(),
        html.Label("ヒット数"),
        html.Br(),
        dcc.Input(
            id="hit_num",
            type="number",
            min=1,
            value=1,
            step=1,
            style={"width": "100%"},
        ),
        html.Div(id="warning", style={"color": "red", "margin-top": "10px"}),
    ],
    style={"width": "40%", "margin-right": "10px"},
)

hit_ratio_layout = html.Div(
    dash_table.DataTable(
        id="hit_ratio_table",
        columns=[{"name": "分割率(%)", "id": "hit_ratio"}],
        # 初期値: 100%の1ヒット
        data=[{"hit_ratio": 100.0}],
        editable=True,
        row_deletable=False,
        style_table={"margin-top": "10px"},
    ),
)
layout_main = html.Div(
    [
        basic_input_layout,
        hit_ratio_layout,
    ],
    style={"display": "flex"},
)

layout = html.Div(
    [
        html.H2("スキル情報"),
        layout_main,
    ],
    style={"display": "flex", "flex-direction": "column"},
)
skill_id = ["skill_ratio", "hit_num", "hit_ratio_table"]
skill_input = [
    Input("skill_ratio", "value"),
    Input("hit_num", "value"),
    Input("hit_ratio_table", "data"),
]
skill_output = [
    Output("skill_ratio", "value", allow_duplicate=True),
    Output("hit_num", "value", allow_duplicate=True),
    Output("hit_ratio_table", "data", allow_duplicate=True),
]
skill_state = [
    State("skill_ratio", "value"),
    State("hit_num", "value"),
    State("hit_ratio_table", "data"),
]


def register_skill_callback(app):
    @app.callback(
        Output("hit_ratio_table", "data"),
        Output("warning", "children"),
        Input("hit_num", "value"),
        State("hit_ratio_table", "data"),
    )
    def update_table(hit_num, data):
        if not hit_num or hit_num < 1:
            return dash.no_update, "ヒット数を1以上にしてください。"
        # hit_ratio_tableの長さがhit_numと等しい場合、何もしない
        if len(data) == hit_num:
            return dash.no_update, ""
        initial_values = [round(100.0 / hit_num, 2)] * hit_num
        data = [{"hit_ratio": value} for value in initial_values]

        return data, ""


if __name__ == "__main__":
    import dash_bootstrap_components as dbc

    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )

    app = dash.Dash(
        "Enemy Input",
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css],
    )
    app.layout = html.Div([layout], style={"width": "45%"})
    register_skill_callback(app)
    app.run_server(debug=True)
