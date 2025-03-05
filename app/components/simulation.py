from dash import html
from app.components import (
    student_input,
    enemy_input,
    skill_input,
)
import plotly.express as px
from dash import Input, Output, State
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
    damage_simulation,
)
from dash import dcc

layout = html.Div(
    [
        html.H2("ダメージシミュレーション"),
        html.Label("スキルを撃つ回数"),
        dcc.Input(id="skill_num", type="number", min=1, value=1, step=1),
        html.Label("目標ダメージ"),
        dcc.Input(id="target_damage", type="number", min=0, value=10000),
        # ボタン
        html.Button("シミュレーション開始", id="calc_button", n_clicks=0),
        # ダメージ計算結果ヒストグラム
        dcc.Graph(id="damage_histogram", figure={}),
        html.Div(id="max_damage"),
        html.Div(id="min_damage"),
        html.Div(id="average_damage"),
        html.Div(id="prob_over_target"),
    ]
)


def register_simulation_callback(app):
    @app.callback(
        Output("damage_histogram", "figure"),
        Output("max_damage", "children"),
        Output("min_damage", "children"),
        Output("average_damage", "children"),
        Output("prob_over_target", "children"),
        Input("calc_button", "n_clicks"),
        student_input.student_state,
        enemy_input.enemy_state,
        skill_input.skill_state,
        State("buff_table", "data"),
        State("debuff_table", "data"),
        State("skill_num", "value"),
        State("target_damage", "value"),
        prevent_initial_call=True,
    )
    def simulate_damage(n_clicks, *args):
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
        damage_list = damage_simulation(
            student, enemy, skill, args[31], 100_000 // (args[31] * skill_args[1])
        )
        max_damage = max(damage_list)
        min_damage = min(damage_list)
        target_damage = args[32]
        fig = px.histogram(
            damage_list,
            range_x=(
                min(min_damage - 1000, target_damage - 1000),
                max(max_damage + 1000, target_damage + 1000),
            ),
            labels={"value": "ダメージ"},
            nbins=500,
            title="ダメージ分布",
        )
        # add a vertical line at target_damage
        fig.add_vline(x=target_damage, line_dash="dash", line_color="red")
        fig.update_layout(showlegend=False)
        fig.update_yaxes(visible=False)
        average_damage = sum(damage_list) / len(damage_list)
        prob_over_target = (
            sum(damage >= args[32] for damage in damage_list) / len(damage_list) * 100
        )
        return (
            fig,
            f"最大ダメージ: {max_damage}",
            f"最小ダメージ: {min_damage}",
            f"平均ダメージ: {average_damage:.0f}",
            f"目標ダメージを超える確率: {prob_over_target:.5g}%",
        )
