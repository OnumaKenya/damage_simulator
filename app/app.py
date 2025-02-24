import pandas as pd
import streamlit as st
from streamlit.column_config import NumberColumn, SelectboxColumn, TextColumn
import pickle
from damage_simulator.buffs import Buff, Debuff
from damage_simulator.calc_damage import (
    calc_critical_ratio,
    calc_hit_ratio,
    calc_total_damage,
    calc_total_damage_expected,
    damage_simulation,
)
from damage_simulator.constants import BUFF_DIR, DEBUFF_DIR, STUDENT_DIR, ENEMY_DIR
from damage_simulator.enemy import Armor, Enemy, RawEnemy
from damage_simulator.equip import Equip1, Equip2, Equip3
from damage_simulator.skill import Skill
from damage_simulator.students import Chikei, Element, RawStudent, Student
import matplotlib.pyplot as plt


def main():
    # init session state
    if "buff" not in st.session_state:
        data = {
            "バフ種": [],
            "バフ量": [],
            "備考": [],
        }
        st.session_state.buff = pd.DataFrame(data).astype(
            {"バフ種": "str", "バフ量": "float", "備考": "str"}
        )
    else:
        st.session_state.buff = st.session_state.buff.astype(
            {"バフ種": "str", "バフ量": "float", "備考": "str"}
        )
    if "debuff" not in st.session_state:
        data = {
            "デバフ種": [],
            "デバフ量": [],
            "備考": [],
        }
        st.session_state.debuff = pd.DataFrame(data).astype(
            {"デバフ種": "str", "デバフ量": "float", "備考": "str"}
        )
    else:
        st.session_state.debuff = st.session_state.debuff.astype(
            {"デバフ種": "str", "デバフ量": "float", "備考": "str"}
        )
    if "student" not in st.session_state:
        st.session_state.student = RawStudent()
    if "enemy" not in st.session_state:
        st.session_state.enemy = RawEnemy()

    st.title("ブルアカ簡易ダメージ計算")
    st.header("生徒ステータス")

    with st.expander("生徒プリセット保存・読み込み", expanded=False):
        student_preset_name = st.text_input("生徒プリセット名")
        if st.button("生徒保存"):
            if (STUDENT_DIR / f"{student_preset_name}.pkl").exists():
                # ファイルが存在する場合は上書き確認
                if st.checkbox("同名の生徒プリセットが存在します。上書きしますか？"):
                    with open(STUDENT_DIR / f"{student_preset_name}.pkl", "wb") as f:
                        pickle.dump(st.session_state.student, f)
            else:
                with open(STUDENT_DIR / f"{student_preset_name}.pkl", "wb") as f:
                    pickle.dump(st.session_state.student, f)
        student_preset_read_name = st.selectbox(
            "生徒プリセット名", [f.stem for f in STUDENT_DIR.glob("*.pkl")]
        )
        if st.button("生徒読み込み"):
            with open(STUDENT_DIR / f"{student_preset_read_name}.pkl", "rb") as f:
                st.session_state.student = pickle.load(f)
    with st.expander("生徒ステータス入力", expanded=True):
        student_default = st.session_state.student
        # レアリティと攻撃能力解放
        col1, col2, col3 = st.columns(3)
        with col1:
            rarity = st.number_input(
                "★", min_value=1, max_value=5, value=student_default.rarity
            )
        with col2:
            is_wb = st.checkbox("攻撃WB有", value=student_default.is_wb)
        with col3:
            student_level = st.number_input(
                "レベル", min_value=1, value=student_default.level
            )
        # 戦闘ステータス
        st.subheader("ステータス")
        col1, col2, col3 = st.columns(3)
        with col1:
            attack = st.number_input(
                "攻撃力", min_value=0, value=student_default.attack
            )
            critical = st.number_input(
                "会心値", min_value=0, value=student_default.critical
            )
            ignore_defence = st.number_input(
                "防御貫通", min_value=0, value=student_default.ignore_defence
            )
            support_attack = st.number_input(
                "支援値", min_value=0, value=student_default.support_attack
            )
        with col2:
            hit = st.number_input("命中値", min_value=0, value=student_default.hit)
            critical_damage = st.number_input(
                "会心ダメージ(%)", min_value=0, value=student_default.critical_damage
            )
            ignore_defence_ratio = st.number_input(
                "防御無視(%)", min_value=0, value=student_default.ignore_defence_ratio
            )
        with col3:
            stable = st.number_input(
                "安定値", min_value=0, value=student_default.stable
            )
            weapon_attack = st.number_input(
                "固有武器攻撃力", min_value=0, value=student_default.weapon_attack
            )
            kizuna_bonus = st.number_input(
                "攻撃力絆ボーナス", min_value=0, value=student_default.kizuna_bonus
            )
        col1, col2, col3 = st.columns(3)
        with col1:
            is_all_critical = st.checkbox(
                "全会心", value=student_default.is_all_critical
            )
        with col2:
            is_no_critical = st.checkbox(
                "会心なし", value=student_default.is_no_critical
            )
        with col3:
            is_ignore_stable = st.checkbox(
                "安定値無視", value=student_default.is_ignore_stable
            )
        # 装備選択
        st.subheader("装備")
        col1, col2, col3 = st.columns(3)
        with col1:
            equip1 = st.selectbox(
                "装備1",
                ["帽子", "グローブ", "靴"],
                index=["帽子", "グローブ", "靴"].index(student_default.equip1.name),
            )
        with col2:
            equip2 = st.selectbox(
                "装備2",
                ["鞄", "バッジ", "ヘアピン"],
                index=["鞄", "バッジ", "ヘアピン"].index(student_default.equip2.name),
            )
        with col3:
            equip3 = st.selectbox(
                "装備3",
                ["お守り", "時計", "ネックレス"],
                index=["お守り", "時計", "ネックレス"].index(
                    student_default.equip3.name
                ),
            )

        # 地形適正
        st.subheader("地形適正・攻撃属性")
        col1, col2 = st.columns(2)
        with col1:
            chikei = st.selectbox(
                "地形適正",
                ["SS", "S", "A", "B", "C", "D"],
                index=["SS", "S", "A", "B", "C", "D"].index(
                    student_default.chikei.name
                ),
            )
        with col2:
            element = st.selectbox(
                "攻撃属性",
                ["爆発", "貫通", "神秘", "振動"],
                index=["爆発", "貫通", "神秘", "振動"].index(
                    student_default.element.name
                ),
            )

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

    with st.expander("バフプリセット保存・読み込み", expanded=False):
        buff_preset_name = st.text_input("バフプリセット名")
        if st.button("バフ保存"):
            if (BUFF_DIR / f"{buff_preset_name}.csv").exists():
                # ファイルが存在する場合は上書き確認
                if st.checkbox("同名のバフプリセットが存在します。上書きしますか？"):
                    st.session_state.buff.to_csv(
                        BUFF_DIR / f"{buff_preset_name}.csv", index=False
                    )
            else:
                st.session_state.buff.to_csv(
                    BUFF_DIR / f"{buff_preset_name}.csv", index=False
                )
        buff_preset_read_name = st.selectbox(
            "バフプリセット名", [f.stem for f in BUFF_DIR.glob("*.csv")]
        )
        if st.button("バフ読み込み"):
            st.session_state.buff = pd.read_csv(
                BUFF_DIR / f"{buff_preset_read_name}.csv"
            )
    with st.expander("バフ入力", expanded=True):
        column_config = {
            "バフ種": SelectboxColumn(
                options=list(map(lambda x: x.value, Buff.__members__.values())),
                width=200,
                required=True,
            ),
            "バフ量": NumberColumn(required=True),
            "備考": TextColumn(width=200),
        }
        # st.session_state.buffを編集可能なDataFrameとして表示
        buff_list_df = st.data_editor(
            st.session_state.buff, column_config=column_config, num_rows="dynamic"
        )
        buff_list_df = buff_list_df[["バフ種", "バフ量", "備考"]].reset_index(drop=True)
        if not buff_list_df.equals(st.session_state.buff):
            st.session_state.buff = buff_list_df
        buff_list = list(zip(buff_list_df["バフ種"], buff_list_df["バフ量"]))
    st.header("敵情報入力")

    with st.expander("敵プリセット保存・読み込み", expanded=False):
        enemy_preset_name = st.text_input("敵プリセット名")
        if st.button("敵保存"):
            if (ENEMY_DIR / f"{enemy_preset_name}.pkl").exists():
                # ファイルが存在する場合は上書き確認
                if st.checkbox("同名の敵プリセットが存在します。上書きしますか？"):
                    with open(ENEMY_DIR / f"{enemy_preset_name}.pkl", "wb") as f:
                        pickle.dump(st.session_state.enemy, f)
            else:
                with open(ENEMY_DIR / f"{enemy_preset_name}.pkl", "wb") as f:
                    pickle.dump(st.session_state.enemy, f)
        enemy_preset_read_name = st.selectbox(
            "敵プリセット名", [f.stem for f in ENEMY_DIR.glob("*.pkl")]
        )
        if st.button("敵読み込み"):
            with open(ENEMY_DIR / f"{enemy_preset_read_name}.pkl", "rb") as f:
                st.session_state.enemy = pickle.load(f)

    with st.expander("敵情報入力", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            enemy_level = st.number_input(
                "敵レベル", min_value=1, value=st.session_state.enemy.level
            )
            critical_resist = st.number_input(
                "会心発生抵抗値",
                min_value=0,
                value=st.session_state.enemy.critical_resist,
            )
            damage_resist = st.number_input(
                "被ダメージ抵抗(%)",
                min_value=0,
                value=st.session_state.enemy.damage_resist,
            )
        with col2:
            armor = st.selectbox("装甲", ["軽装備", "重装甲", "特殊装甲", "弾力装甲"])
            dodge = st.number_input(
                "回避値", min_value=0, value=st.session_state.enemy.dodge
            )
        with col3:
            defence = st.number_input(
                "防御力", min_value=0, value=st.session_state.enemy.defence
            )
            critical_damage_resist = st.number_input(
                "会心ダメージ抵抗(%)",
                min_value=0,
                value=st.session_state.enemy.critical_damage_resist,
            )
    st.header("デバフ入力")
    with st.expander("デバフプリセット保存・読み込み", expanded=False):
        debuff_preset_name = st.text_input("デバフプリセット名")
        if st.button("デバフ保存"):
            if (DEBUFF_DIR / f"{debuff_preset_name}.csv").exists():
                # ファイルが存在する場合は上書き確認
                if st.checkbox("同名のデバフプリセットが存在します。上書きしますか？"):
                    st.session_state.debuff.to_csv(
                        DEBUFF_DIR / f"{debuff_preset_name}.csv", index=False
                    )
            else:
                st.session_state.debuff.to_csv(
                    DEBUFF_DIR / f"{debuff_preset_name}.csv", index=False
                )
        debuff_preset_read_name = st.selectbox(
            "デバフプリセット名", [f.stem for f in DEBUFF_DIR.glob("*.csv")]
        )
        if st.button("デバフ読み込み"):
            st.session_state.debuff = pd.read_csv(
                DEBUFF_DIR / f"{debuff_preset_read_name}.csv"
            )
    with st.expander("デバフ入力", expanded=True):
        column_config_debuff = {
            "デバフ種": SelectboxColumn(
                options=list(map(lambda x: x.value, Debuff.__members__.values())),
                width=200,
                required=True,
            ),
            "デバフ量": NumberColumn(required=True),
            "備考": TextColumn(width=200),
        }
        # st.session_state.debuffを編集可能なDataFrameとして表示
        debuff_list_df = st.data_editor(
            st.session_state.debuff,
            column_config=column_config_debuff,
            num_rows="dynamic",
        )
        debuff_list_df = debuff_list_df[["デバフ種", "デバフ量", "備考"]].reset_index(
            drop=True
        )
        st.session_state.debuff = debuff_list_df
        debuff_list = list(zip(debuff_list_df["デバフ種"], debuff_list_df["デバフ量"]))
    raw_student = RawStudent(
        rarity=rarity,
        is_wb=is_wb,
        level=student_level,
        attack=attack,
        hit=hit,
        critical=critical,
        critical_damage=critical_damage,
        stable=stable,
        ignore_defence_ratio=ignore_defence_ratio,
        ignore_defence=ignore_defence,
        weapon_attack=weapon_attack,
        kizuna_bonus=kizuna_bonus,
        support_attack=support_attack,
        equip1=Equip1[equip1],
        equip2=Equip2[equip2],
        equip3=Equip3[equip3],
        chikei=Chikei[chikei],
        element=Element[element],
        is_all_critical=is_all_critical,
        is_no_critical=is_no_critical,
        is_ignore_stable=is_ignore_stable,
    )
    st.session_state.student = raw_student
    student = Student.from_raw_student(raw_student, buff_list)
    skill = Skill(skill_ratio=skill_ratio, hit_ratio=hit_ratio)
    enemy = RawEnemy(
        level=enemy_level,
        armor=Armor[armor],
        defence=defence,
        dodge=dodge,
        critical_resist=critical_resist,
        critical_damage_resist=critical_damage_resist,
        damage_resist=damage_resist,
    )
    enemy = Enemy.from_raw_enemy(enemy, debuff_list)
    with st.sidebar:
        st.header("ダメージ計算")
        # 会心最大ダメージ
        critical_damage_max = calc_total_damage(student, enemy, skill, 1.0, True)
        st.write(f"会心最大ダメージ: {critical_damage_max}")
        # 会心最小ダメージ
        critical_damage_min = calc_total_damage(student, enemy, skill, 0.0, True)
        st.write(f"会心最小ダメージ: {critical_damage_min}")
        # 非会心最大ダメージ
        damage_max = calc_total_damage(student, enemy, skill, 1.0, False)
        st.write(f"非会心最大ダメージ: {damage_max}")
        # 非会心最小ダメージ
        damage_min = calc_total_damage(student, enemy, skill, 0.0, False)
        st.write(f"非会心最小ダメージ: {damage_min}")
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
        st.write(f"平均ダメージ: {sum(damage_list) / len(damage_list)}")
        st.write(
            f"目標ダメージを超える確率: {sum([1 for x in damage_list if x >= target_damage]) / len(damage_list) * 100}%"
        )


main()
