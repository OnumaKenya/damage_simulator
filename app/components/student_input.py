import dash
from dash import dcc, html, Input, Output, State
import pickle
from damage_simulator.constants import STUDENT_DIR, SKILL_DIR
from damage_simulator.equip import Equip1, Equip2, Equip3
from damage_simulator.students import Chikei, Element, RawStudent
from components import skill_input
from damage_simulator.skill import Skill

raw_default_student = RawStudent()
status_1_layout = html.Div(
    [
        html.Div(
            [
                html.Label("★"),
                dcc.Input(
                    id="rarity",
                    type="number",
                    min=1,
                    max=5,
                    value=raw_default_student.rarity,
                    style={"width": "50px"},
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
                html.Label("レベル"),
                dcc.Input(
                    id="student_level",
                    type="number",
                    min=1,
                    value=raw_default_student.level,
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "margin-right": "10px",
            },
        ),
        dcc.Checklist(
            value=[],
            id="is_wb",
            options=[{"label": "攻撃WB有", "value": "is_wb"}],
            style={"margin-top": "10px"},
        ),
    ],
    style={
        "display": "flex",
    },
)
status_2_layout = html.Div(
    [
        html.Div(
            [
                html.Label("攻撃力"),
                dcc.Input(
                    id="attack", type="number", min=0, value=raw_default_student.attack
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
                html.Label("会心値"),
                dcc.Input(
                    id="critical",
                    type="number",
                    min=0,
                    value=raw_default_student.critical,
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
                html.Label("会心ダメージ(%)"),
                dcc.Input(
                    id="critical_damage",
                    type="number",
                    min=0,
                    value=raw_default_student.critical_damage,
                ),
            ],
            style={"display": "flex", "flex-direction": "column"},
        ),
    ],
    style={
        "display": "flex",
    },
)
status_3_layout = html.Div(
    [
        html.Div(
            [
                html.Label("防御貫通"),
                dcc.Input(
                    id="ignore_defence",
                    type="number",
                    min=0,
                    value=raw_default_student.ignore_defence,
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
                html.Label("防御無視(%)"),
                dcc.Input(
                    id="ignore_defence_ratio",
                    type="number",
                    min=0,
                    max=100,
                    value=raw_default_student.ignore_defence_ratio,
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
                html.Label("安定値"),
                dcc.Input(
                    id="stable", type="number", min=0, value=raw_default_student.stable
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "margin-right": "10px",
            },
        ),
    ],
    style={
        "display": "flex",
    },
)
status_4_layout = html.Div(
    [
        html.Div(
            [
                html.Label("命中値"),
                dcc.Input(
                    id="hit",
                    type="number",
                    min=0,
                    value=raw_default_student.hit,
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
                html.Label("固有武器攻撃力"),
                dcc.Input(
                    id="weapon_attack",
                    type="number",
                    min=0,
                    value=raw_default_student.weapon_attack,
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
                html.Label("攻撃力絆ボーナス"),
                dcc.Input(
                    id="kizuna_bonus",
                    type="number",
                    min=0,
                    value=raw_default_student.kizuna_bonus,
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "margin-right": "10px",
            },
        ),
    ],
    style={
        "display": "flex",
    },
)
status_5_layout = html.Div(
    [
        html.Div(
            [
                html.Label("支援値"),
                dcc.Input(
                    id="support_attack",
                    type="number",
                    min=0,
                    value=raw_default_student.support_attack,
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
            },
        ),
        html.Div(
            [
                html.Label("地形適正"),
                dcc.Dropdown(
                    id="chikei",
                    options=[
                        {"label": x, "value": x} for x in Chikei.__members__.keys()
                    ],
                    placeholder="地形適正",
                    value=raw_default_student.chikei.name,
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
                html.Label("攻撃属性"),
                dcc.Dropdown(
                    id="element",
                    options=[
                        {"label": x, "value": x} for x in Element.__members__.keys()
                    ],
                    value=raw_default_student.element.name,
                    placeholder="攻撃属性",
                    style={"width": "200px"},
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "margin-right": "10px",
            },
        ),
    ],
    style={
        "display": "flex",
    },
)
status_6_layout = dcc.Checklist(
    value=[],
    id="is_critical_stable",
    options=[
        {"label": "全会心", "value": "is_all_critical"},
        {"label": "会心なし", "value": "is_no_critical"},
        {"label": "安定値無視", "value": "is_ignore_stable"},
    ],
    style={
        "margin-top": "10px",
        "display": "flex",
        # 少しだけ間隔をあける
        "gap": "10px",
    },
)
equip_layout = html.Div(
    [
        dcc.Dropdown(
            id="equip1",
            options=[{"label": x, "value": x} for x in Equip1.__members__.keys()],
            placeholder="装備1",
            value=raw_default_student.equip1.name,
            style={"width": "200px"},
        ),
        dcc.Dropdown(
            id="equip2",
            options=[{"label": x, "value": x} for x in Equip2.__members__.keys()],
            placeholder="装備2",
            value=raw_default_student.equip2.name,
            style={
                "width": "200px",
            },
        ),
        dcc.Dropdown(
            id="equip3",
            options=[{"label": x, "value": x} for x in Equip3.__members__.keys()],
            placeholder="装備3",
            value=raw_default_student.equip3.name,
            style={
                "width": "200px",
            },
        ),
    ],
    style={
        "display": "flex",
    },
)
layout = html.Div(
    [
        html.H2("生徒情報入力"),
        html.H4("生徒プリセット読み込み"),
        dcc.Dropdown(
            id="student_preset_dropdown",
            options=[
                {"label": f.stem, "value": f.stem} for f in STUDENT_DIR.glob("*.pkl")
            ],
            placeholder="生徒プリセット名",
        ),
        html.Button("生徒読み込み", id="load_student_btn", n_clicks=0),
        html.H4("ステータス"),
        status_1_layout,
        status_2_layout,
        status_3_layout,
        status_4_layout,
        status_5_layout,
        status_6_layout,
        html.Div(id="student_error_message", style={"color": "red"}),
        html.H4("装備"),
        equip_layout,
        html.H4("生徒プリセット保存"),
        dcc.Input(
            id="student_preset_name",
            type="text",
            placeholder="生徒プリセット名",
            style={
                "width": "95%",
                "height": "25px",
                "fontSize": "16px",
                "padding": "5px",
            },
        ),
        html.Button("生徒保存", id="save_student_btn", n_clicks=0),
        html.Div(id="student_save_status_message", style={"color": "green"}),
    ],
)

student_id = [
    "rarity",
    "student_level",
    "is_wb",
    "attack",
    "critical",
    "critical_damage",
    "ignore_defence",
    "ignore_defence_ratio",
    "stable",
    "hit",
    "weapon_attack",
    "kizuna_bonus",
    "support_attack",
    "equip1",
    "equip2",
    "equip3",
    "chikei",
    "element",
    "is_critical_stable",
]
student_input = [Input(i, "value") for i in student_id]
student_output = [Output(i, "value", allow_duplicate=True) for i in student_id]
student_state = [State(i, "value") for i in student_id]


def register_student_callback(app):
    @app.callback(
        student_output,
        skill_input.skill_output,
        Input("load_student_btn", "n_clicks"),
        State("student_preset_dropdown", "value"),
        prevent_initial_call=True,
    )
    def load_student_preset(n_clicks, preset_name):
        student_path = STUDENT_DIR / f"{preset_name}.pkl"
        skill_path = SKILL_DIR / f"{preset_name}.pkl"
        if student_path.exists():
            with open(student_path, "rb") as f:
                student = pickle.load(f)
            if skill_path.exists():
                with open(skill_path, "rb") as f:
                    skill = pickle.load(f)
            else:
                skill = Skill(skill_ratio=100.0, hit_ratio=[100.0])
            return (
                student.rarity,
                student.level,
                ["is_wb"] if student.is_wb else [],
                student.attack,
                student.critical,
                student.critical_damage,
                student.ignore_defence,
                student.ignore_defence_ratio,
                student.stable,
                student.hit,
                student.weapon_attack,
                student.kizuna_bonus,
                student.support_attack,
                student.equip1.name,
                student.equip2.name,
                student.equip3.name,
                student.chikei.name,
                student.element.name,
                [
                    "is_all_critical" if student.is_all_critical else "",
                    "is_no_critical" if student.is_no_critical else "",
                    "is_ignore_stable" if student.is_ignore_stable else "",
                ],
                skill.skill_ratio,
                len(skill.hit_ratio),
                [{"hit_ratio": h} for h in skill.hit_ratio],
            )

        return dash.no_update

    @app.callback(
        Output("student_save_status_message", "children"),
        Output("student_preset_dropdown", "options"),
        Input("save_student_btn", "n_clicks"),
        State("student_preset_name", "value"),
        student_state,
        skill_input.skill_state,
        prevent_initial_call=True,
    )
    def save_student_preset(n_clicks, preset_name, *args):
        student = RawStudent(
            rarity=args[0],
            is_wb="is_wb" in args[2],
            level=args[1],
            attack=args[3],
            critical=args[4],
            critical_damage=args[5],
            ignore_defence=args[6],
            ignore_defence_ratio=args[7],
            stable=args[8],
            hit=args[9],
            weapon_attack=args[10],
            kizuna_bonus=args[11],
            support_attack=args[12],
            equip1=Equip1[args[13]],
            equip2=Equip2[args[14]],
            equip3=Equip3[args[15]],
            chikei=Chikei[args[16]],
            element=Element[args[17]],
            is_all_critical="is_all_critical" in args[18],
            is_no_critical="is_no_critical" in args[18],
            is_ignore_stable="is_ignore_stable" in args[18],
        )
        skill = Skill(
            skill_ratio=args[19],
            hit_ratio=[d["hit_ratio"] for d in args[21]],
        )
        student_path = STUDENT_DIR / f"{preset_name}.pkl"
        skill_path = SKILL_DIR / f"{preset_name}.pkl"
        if student_path.exists():
            with open(student_path, "wb") as f:
                pickle.dump(student, f)
            with open(skill_path, "wb") as f:
                pickle.dump(skill, f)
            return "同名の生徒プリセットを上書きしました。", dash.no_update
        with open(student_path, "wb") as f:
            pickle.dump(student, f)
        with open(skill_path, "wb") as f:
            pickle.dump(skill, f)
        options = [
            {"label": f.stem, "value": f.stem} for f in STUDENT_DIR.glob("*.pkl")
        ]
        return "生徒プリセットを保存しました。", options

    @app.callback(
        Output("student_error_message", "children"),
        Output("is_critical_stable", "value", allow_duplicate=True),
        Input("is_critical_stable", "value"),
        prevent_initial_call=True,
    )
    def check_critical_stable(values):
        if "is_all_critical" in values and "is_no_critical" in values:
            new_values = [
                v for v in values if v != "is_no_critical" and v != "is_all_critical"
            ]
            return "全会心と会心なしは同時に選択できません。", new_values
        return "", dash.no_update


if __name__ == "__main__":
    import dash_bootstrap_components as dbc

    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )

    app = dash.Dash(
        "Student Input",
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css],
    )
    app.layout = html.Div([layout], style={"width": "45%"})
    register_student_callback(app)
    app.run_server(debug=True)
