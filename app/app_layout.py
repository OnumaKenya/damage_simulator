from dash import html
from components import (
    buff_input,
    debuff_input,
    student_input,
    enemy_input,
    sidebar,
    skill_input,
    simulation,
)


# 生徒情報と敵情報を横に並べる
layout_student_enemy = html.Div(
    [
        html.Div(student_input.layout, style={"width": "100%", "margin-right": "10px"}),
        html.Div(skill_input.layout, style={"width": "100%", "margin-right": "10px"}),
        html.Div(enemy_input.layout, style={"width": "100%"}),
    ],
    style={"display": "flex", "width": "100%", "align-items": "stretch"},
)

# バフ管理とデバフ管理を横に並べる
layout_buff_debuf = html.Div(
    [
        html.Div(buff_input.layout, style={"width": "100%"}),
        html.Div(debuff_input.layout, style={"width": "100%"}),
    ],
    style={"display": "flex", "width": "100%", "align-items": "stretch"},
)

layout_main = html.Div(
    [
        html.H1("ブルアカダメージ計算ツール"),
        layout_student_enemy,
        # gap
        html.Div(style={"height": "20px"}),
        # line
        html.Hr(),
        layout_buff_debuf,
        # gap
        html.Div(style={"height": "20px"}),
        # line
        html.Hr(),
        simulation.layout,
    ],
    style={
        "display": "flex",
        "flex-direction": "column",
        "margin-left": "18%",
        "padding": "20px",
    },
)

layout = html.Div(
    [
        sidebar.layout,
        layout_main,
    ],
    style={"display": "flex"},
)

if __name__ == "__main__":
    import dash_bootstrap_components as dbc
    import dash

    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )

    app = dash.Dash(
        "Buff Input",
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css],
    )
    app.layout = layout
    buff_input.register_buff_callback(app)
    debuff_input.register_debuff_callback(app)
    app.run_server(debug=True)
