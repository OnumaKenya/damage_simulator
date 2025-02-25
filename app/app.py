import pandas as pd
import streamlit as st
from damage_simulator.calc_damage import (
    calc_critical_ratio,
    calc_hit_ratio,
    calc_total_damage,
    calc_total_damage_expected,
    damage_simulation,
)
from damage_simulator.enemy import Enemy
from damage_simulator.skill import Skill
from damage_simulator.students import Student
import matplotlib.pyplot as plt
from damage_simulator.ui.df_input import buff_df_input, debuff_df_input
from damage_simulator.ui.student_input import student_input, enemy_input


def main():
    st.title("ブルアカ簡易ダメージ計算")
    st.header("生徒ステータス")
    student_input()
    raw_student = st.session_state.raw_student
    st.header("スキル情報入力")
    col1, col2 = st.columns(2)
    with col1:
        skill_ratio = st.number_input("スキル倍率(%)", min_value=0.0, value=100.0)
        hit_num = st.number_input("ヒット数", min_value=1, value=1)
    with col2:
        with st.expander("分割率入力", expanded=False):
            ser = pd.Series(
                [round(100.0 / hit_num, 2)] * hit_num,
                name="分割率(%)",
                index=range(1, hit_num + 1),
            )
            edited_ser = st.data_editor(ser)
            if edited_ser.isna().any():
                st.warning("空欄を埋めてください。")
            hit_ratio = list(edited_ser.values)
    st.header("バフ入力")
    buff_df_input()
    buff_list_df = st.session_state.buff_list_df
    buff_list = list(zip(buff_list_df["バフ種"], buff_list_df["バフ量"]))

    st.header("敵情報入力")
    enemy_input()
    enemy = st.session_state.raw_enemy
    st.header("デバフ入力")
    debuff_df_input()
    debuff_list_df = st.session_state.debuff
    debuff_list = list(zip(debuff_list_df["デバフ種"], debuff_list_df["デバフ量"]))

    student = Student.from_raw_student(raw_student, buff_list)
    skill = Skill(skill_ratio=skill_ratio, hit_ratio=hit_ratio)
    enemy = Enemy.from_raw_enemy(enemy, debuff_list)
    with st.sidebar:
        st.header("ダメージ計算")
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
            index=["会心", "非会心"],
        )
        st.write(damage_df)
        # 命中率
        hit_ratio = calc_hit_ratio(student, enemy)
        st.write(f"命中率: {hit_ratio:.2f}%")
        # 会心発生率
        critical_ratio = calc_critical_ratio(student, enemy)
        st.write(f"会心発生率: {critical_ratio:.2f}%")
        # ダメージ期待値
        expected_damage = calc_total_damage_expected(student, enemy, skill)
        st.write(f"ダメージ期待値: {expected_damage}")

    st.header("ダメージシミュレーション")

    total_number = st.number_input("EXを撃つ回数・巻き込む敵の数", min_value=1, value=1)
    target_damage = st.number_input("目標ダメージ", min_value=0, value=0)
    # シミュレーション機能
    if st.button("シミュレーション"):
        st.session_state.student = raw_student
        st.session_state.enemy = enemy
        damage_list = damage_simulation(
            student, enemy, skill, total_number, 1_000_000 // total_number
        )
        # ダメージ分布
        fig, ax = plt.subplots()
        ax.hist(damage_list, bins=50, range=(min(damage_list), max(damage_list)))
        # y軸の目盛りを表示しない
        ax.yaxis.set_visible(False)
        # 目標ダメージの描画
        ax.axvline(target_damage, color="red")
        st.pyplot(fig)
        st.write(f"最大ダメージ: {max(damage_list)}")
        st.write(f"最小ダメージ: {min(damage_list)}")
        st.write(f"平均ダメージ: {sum(damage_list) / len(damage_list)}")
        st.write(
            f"目標ダメージを超える確率: {sum([1 for x in damage_list if x >= target_damage]) / len(damage_list) * 100}%"
        )


main()
