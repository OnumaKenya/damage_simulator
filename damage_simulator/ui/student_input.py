from damage_simulator.constants import STUDENT_DIR, ENEMY_DIR
import streamlit as st

from damage_simulator.enemy import Armor, RawEnemy
from damage_simulator.equip import Equip1, Equip2, Equip3
from damage_simulator.students import Chikei, Element, RawStudent

import pickle


def student_input():
    with st.expander("生徒ステータス入力", expanded=True):
        if "student" not in st.session_state:
            student_default = RawStudent()
        else:
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
    # 生徒ステータスの保存・読み込み
    with st.expander("生徒プリセット保存・読み込み", expanded=False):
        student_preset_name = st.text_input("生徒プリセット名")
        if st.button("生徒保存"):
            if (STUDENT_DIR / f"{student_preset_name}.pkl").exists():
                with open(STUDENT_DIR / f"{student_preset_name}.pkl", "wb") as f:
                    pickle.dump(raw_student, f)
                st.warning("同名の生徒プリセットを上書きしました。")
            else:
                # 新規作成
                with open(STUDENT_DIR / f"{student_preset_name}.pkl", "wb") as f:
                    pickle.dump(raw_student, f)
        student_preset_read_name = st.selectbox(
            "生徒プリセット名", [f.stem for f in STUDENT_DIR.glob("*.pkl")]
        )
        if st.button("生徒読み込み"):
            with open(STUDENT_DIR / f"{student_preset_read_name}.pkl", "rb") as f:
                st.session_state.student = pickle.load(f)
                st.rerun()
    st.session_state.raw_student = raw_student


def enemy_input():
    with st.expander("敵情報入力", expanded=True):
        if "enemy" not in st.session_state:
            enemy_default = RawEnemy()
        else:
            enemy_default = st.session_state.enemy
        col1, col2, col3 = st.columns(3)
        with col1:
            enemy_level = st.number_input(
                "敵レベル", min_value=1, value=enemy_default.level
            )
            critical_resist = st.number_input(
                "会心発生抵抗値", min_value=0, value=enemy_default.critical_resist
            )
            damage_resist = st.number_input(
                "被ダメージ抵抗(%)", min_value=0, value=enemy_default.damage_resist
            )
        with col2:
            armor = st.selectbox(
                "装甲",
                ["軽装備", "重装甲", "特殊装甲", "弾力装甲"],
                index=["軽装備", "重装甲", "特殊装甲", "弾力装甲"].index(
                    enemy_default.armor.name
                ),
            )
            dodge = st.number_input("回避値", min_value=0, value=enemy_default.dodge)
        with col3:
            defence = st.number_input(
                "防御力", min_value=0, value=enemy_default.defence
            )
            critical_damage_resist = st.number_input(
                "会心ダメージ抵抗(%)",
                min_value=0,
                value=enemy_default.critical_damage_resist,
            )

    enemy = RawEnemy(
        level=enemy_level,
        armor=Armor[armor],
        defence=defence,
        dodge=dodge,
        critical_resist=critical_resist,
        critical_damage_resist=critical_damage_resist,
        damage_resist=damage_resist,
    )
    # 敵情報の保存・読み込み
    with st.expander("敵プリセット保存・読み込み", expanded=False):
        enemy_preset_name = st.text_input("敵プリセット名")
        if st.button("敵保存"):
            if (ENEMY_DIR / f"{enemy_preset_name}.pkl").exists():
                with open(ENEMY_DIR / f"{enemy_preset_name}.pkl", "wb") as f:
                    pickle.dump(enemy, f)
                st.warning("同名の敵プリセットを上書きしました。")
            else:
                with open(ENEMY_DIR / f"{enemy_preset_name}.pkl", "wb") as f:
                    pickle.dump(enemy, f)
        enemy_preset_read_name = st.selectbox(
            "敵プリセット名", [f.stem for f in ENEMY_DIR.glob("*.pkl")]
        )
        if st.button("敵読み込み"):
            with open(ENEMY_DIR / f"{enemy_preset_read_name}.pkl", "rb") as f:
                st.session_state.enemy = pickle.load(f)
                st.rerun()
    st.session_state.raw_enemy = enemy
