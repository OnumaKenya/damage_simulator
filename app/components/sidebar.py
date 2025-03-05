from dash import html
from app.components import (
    student_input,
    enemy_input,
    skill_input,
)
import pandas as pd
from dash import Input, Output, dash_table
from damage_simulator.students import (
    RawStudent,
    Student,
    Equip1,
    Equip2,
    Equip3,
    Chikei,
    Element,
)
from damage_simulator.enemy import RawEnemy, Enemy, Armor
from damage_simulator.skill import Skill
from damage_simulator.calc_damage import (
    calc_critical_ratio,
    calc_hit_ratio,
    calc_total_damage,
    calc_total_damage_expected,
)

layout = html.Div(
    [
        html.H2("ダメージ計算結果"),
        dash_table.DataTable(
            id="damage_table",
            editable=False,
            row_deletable=False,
            style_table={"margin-top": "10px"},
        ),
        # 会心率と命中率の表示
        html.Div(id="critical_ratio", style={"margin-top": "10px"}),
        html.Div(id="hit_ratio", style={"margin-top": "10px"}),
        html.Div(id="expected_damage", style={"margin-top": "10px"}),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "15%",
        "padding": "20px",
        "background-color": "#f8f9fa",
    },
)


def register_sidebar_callback(app):
    @app.callback(
        Output("damage_table", "data"),
        Output("critical_ratio", "children"),
        Output("hit_ratio", "children"),
        Output("expected_damage", "children"),
        student_input.student_input,
        enemy_input.enemy_input,
        skill_input.skill_input,
        Input("buff_table", "data"),
        Input("debuff_table", "data"),
    )
    def calc_damage(*args):
        student_args = args[:19]
        enemy_args = args[19:26]
        skill_args = args[26:29]
        buff_list = [(dic["バフ種"], float(dic["バフ量"])) for dic in args[29]]
        debuff_list = [(dic["デバフ種"], float(dic["デバフ量"])) for dic in args[30]]
        raw_student = RawStudent(
            rarity=student_args[0],
            is_wb="is_wb" in student_args[2],
            level=student_args[1],
            attack=student_args[3],
            critical=student_args[4],
            critical_damage=student_args[5],
            ignore_defence=student_args[6],
            ignore_defence_ratio=student_args[7],
            stable=student_args[8],
            hit=student_args[9],
            weapon_attack=student_args[10],
            kizuna_bonus=student_args[11],
            support_attack=student_args[12],
            equip1=Equip1[student_args[13]],
            equip2=Equip2[student_args[14]],
            equip3=Equip3[student_args[15]],
            chikei=Chikei[student_args[16]],
            element=Element[student_args[17]],
            is_all_critical="is_all_critical" in student_args[18],
            is_no_critical="is_no_critical" in student_args[18],
            is_ignore_stable="is_ignore_stable" in student_args[18],
        )
        raw_enemy = RawEnemy(
            level=enemy_args[0],
            armor=Armor[enemy_args[1]],
            defence=enemy_args[2],
            dodge=enemy_args[3],
            critical_resist=enemy_args[4],
            critical_damage_resist=enemy_args[5],
            damage_resist=enemy_args[6],
        )
        skill = Skill(
            skill_ratio=skill_args[0],
            hit_ratio=[float(dic["hit_ratio"]) for dic in skill_args[2]],
        )
        student = Student.from_raw_student(raw_student, buff_list)
        enemy = Enemy.from_raw_enemy(raw_enemy, debuff_list)
        # 会心最大ダメージ
        critical_damage_max = calc_total_damage(student, enemy, skill, 1.0, True)
        # 会心最小ダメージ
        critical_damage_min = calc_total_damage(student, enemy, skill, 0.0, True)
        # 非会心最大ダメージ
        damage_max = calc_total_damage(student, enemy, skill, 1.0, False)
        # 非会心最小ダメージ
        damage_min = calc_total_damage(student, enemy, skill, 0.0, False)
        damage_df = pd.DataFrame(
            [[critical_damage_max, critical_damage_min], [damage_max, damage_min]],
            columns=["最大ダメージ", "最小ダメージ"],
            index=pd.Index(["会心", "非会心"], name=""),
        )
        # 命中率
        hit_ratio = calc_hit_ratio(student, enemy)
        # 会心発生率
        critical_ratio = calc_critical_ratio(student, enemy)
        # 期待値
        expected_damage = calc_total_damage_expected(student, enemy, skill)
        return (
            damage_df.reset_index().to_dict("records"),
            f"会心率: {critical_ratio:.2f}%",
            f"命中率: {hit_ratio:.2f}%",
            f"ダメージ期待値: {expected_damage:.2f}",
        )
