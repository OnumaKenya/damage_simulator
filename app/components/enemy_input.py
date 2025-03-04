import dash
from dash import dcc, html, Input, Output, State
import pickle
from damage_simulator.constants import ENEMY_DIR
from damage_simulator.enemy import Armor, RawEnemy

raw_default_enemy = RawEnemy()
status_1_layout = html.Div(
    [
        html.Div(
            [
                html.Label("敵レベル"),
                dcc.Input(
                    id="enemy_level", type="number", value=raw_default_enemy.level
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "margin-right": "10px",
            },
        ),
        html.Div(
            [
                html.Label("装甲"),
                dcc.Dropdown(
                    id="enemy_armor",
                    options=[
                        {"label": armor.name, "value": armor.name} for armor in Armor
                    ],
                    value=raw_default_enemy.armor.name,
                    style={"width": "200px"},
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "margin-right": "10px",
            },
        ),
        html.Div(
            [
                html.Label("防御力"),
                dcc.Input(
                    id="enemy_defence", type="number", value=raw_default_enemy.defence
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
            },
        ),
    ],
    style={"display": "flex"},
)
status_2_layout = html.Div(
    [
        html.Div(
            [
                html.Label("回避値"),
                dcc.Input(
                    id="enemy_dodge", type="number", value=raw_default_enemy.dodge
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "margin-right": "10px",
            },
        ),
        html.Div(
            [
                html.Label("会心発生抵抗値"),
                dcc.Input(
                    id="enemy_critical_resist",
                    type="number",
                    value=raw_default_enemy.critical_resist,
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "margin-right": "10px",
            },
        ),
        html.Div(
            [
                html.Label("会心ダメージ抵抗(%)"),
                dcc.Input(
                    id="enemy_critical_damage_resist",
                    type="number",
                    value=raw_default_enemy.critical_damage_resist,
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "margin-right": "10px",
            },
        ),
    ],
    style={"display": "flex"},
)
status_3_layout = html.Div(
    [
        html.Label("被ダメージ抵抗(%)"),
        dcc.Input(
            id="enemy_damage_resist",
            type="number",
            value=raw_default_enemy.damage_resist,
            style={"width": "200px"},
        ),
    ],
    style={
        "display": "flex",
        "flex-direction": "column",
        "margin-right": "10px",
    },
)

layout = html.Div(
    [
        html.H2("敵情報入力"),
        html.H4("敵プリセット読み込み"),
        dcc.Dropdown(
            id="enemy_preset_dropdown",
            options=[
                {"label": f.stem, "value": f.stem} for f in ENEMY_DIR.glob("*.pkl")
            ],
            placeholder="敵プリセット名",
        ),
        html.Button("敵読み込み", id="load_enemy_btn", n_clicks=0),
        html.H4("ステータス"),
        status_1_layout,
        status_2_layout,
        status_3_layout,
        html.Div(id="enemy_error_message", style={"color": "red"}),
        html.H4("敵プリセット保存"),
        dcc.Input(
            id="enemy_preset_name",
            type="text",
            placeholder="敵プリセット名",
            style={
                "width": "95%",
                "height": "25px",
                "fontSize": "16px",
                "padding": "5px",
            },
        ),
        html.Button("敵保存", id="save_enemy_btn", n_clicks=0),
        html.Div(id="enemy_save_status_message", style={"color": "green"}),
    ],
    style={
        "width": "50%",
        "margin-left": "10px",
    },
)

enemy_id = [
    "enemy_level",
    "enemy_armor",
    "enemy_defence",
    "enemy_dodge",
    "enemy_critical_resist",
    "enemy_critical_damage_resist",
    "enemy_damage_resist",
]
enemy_input = [Input(i, "value") for i in enemy_id]
enemy_output = [Output(i, "value", allow_duplicate=True) for i in enemy_id]
enemy_state = [State(i, "value") for i in enemy_id]


def register_enemy_callback(app):
    @app.callback(
        enemy_output,
        Input("load_enemy_btn", "n_clicks"),
        State("enemy_preset_dropdown", "value"),
        prevent_initial_call=True,
    )
    def load_enemy(n_clicks, preset_name):
        if preset_name:
            with open(ENEMY_DIR / f"{preset_name}.pkl", "rb") as f:
                enemy = pickle.load(f)
            return (
                enemy.level,
                enemy.armor.name,
                enemy.defence,
                enemy.dodge,
                enemy.critical_resist,
                enemy.critical_damage_resist,
                enemy.damage_resist,
            )
        return dash.no_update

    @app.callback(
        Output("enemy_save_status_message", "children"),
        Output("enemy_preset_dropdown", "options"),
        Input("save_enemy_btn", "n_clicks"),
        State("enemy_preset_name", "value"),
        enemy_state,
        prevent_initial_call=True,
    )
    def save_enemy_preset(n_clicks, preset_name, *args):
        enemy = RawEnemy(
            level=args[0],
            armor=Armor[args[1]],
            defence=args[2],
            dodge=args[3],
            critical_resist=args[4],
            critical_damage_resist=args[5],
            damage_resist=args[6],
        )
        enemy_path = ENEMY_DIR / f"{preset_name}.pkl"
        if enemy_path.exists():
            with open(enemy_path, "wb") as f:
                pickle.dump(enemy, f)
            return "同名の敵プリセットを上書きしました。", dash.no_update
        with open(enemy_path, "wb") as f:
            pickle.dump(enemy, f)
        options = [{"label": f.stem, "value": f.stem} for f in ENEMY_DIR.glob("*.pkl")]
        return f"{preset_name}を保存しました。", options


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
    register_enemy_callback(app)
    app.run_server(debug=True)
