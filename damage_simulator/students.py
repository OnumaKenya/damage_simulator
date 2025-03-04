from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

from damage_simulator.constants import RARITY_ATTACK_RATIO
from damage_simulator.equip import Equip1, Equip2, Equip3


class Element(Enum):
    爆発: int = 0
    貫通: int = 1
    神秘: int = 2
    振動: int = 3


class Chikei(Enum):
    SS: float = 1.3
    S: float = 1.2
    A: float = 1.1
    B: float = 1.0
    C: float = 0.9
    D: float = 0.8


@dataclass(frozen=True)
class RawStudent:
    rarity: int = 3  # 星
    is_wb: bool = True  # 能力解放有無
    level: int = 90  # レベル
    attack: int = 3846  # 攻撃力
    kizuna_bonus: int = 591  # 絆ボーナス
    support_attack: int = 1090  # 攻撃力支援値
    hit: int = 101  # 命中値
    critical: int = 203  # 会心値
    critical_damage: int = 200  # 会心ダメージ
    stable: int = 1372  # 安定値
    ignore_defence_ratio: int = 0  # 防御無視
    ignore_defence: int = 0  # 防御貫通
    equip1: Equip1 = Equip1.グローブ  # 装備1
    equip2: Equip2 = Equip2.バッジ  # 装備2
    equip3: Equip3 = Equip3.時計  # 装備3
    chikei: Chikei = Chikei.SS  # 地形適正
    weapon_attack: int = 831  # 固有武器
    element: Element = Element.爆発  # 攻撃属性
    is_all_critical: bool = False  # 全会心
    is_no_critical: bool = False  # 会心なし
    is_ignore_stable: bool = False  # 安定値無視


@dataclass(frozen=True)
class Student:
    level: int  # レベル
    attack: int  # 攻撃力
    hit: int  # 命中値
    critical: int  # 会心値
    critical_damage: int  # 会心ダメージ
    stable: int  # 安定値
    stable_ratio: float  # 安定率
    ignore_defence_ratio: int  # 防御無視
    ignore_defence: int  # 防御貫通
    chikei: Chikei  # 地形適正
    element: Element  # 攻撃属性
    weak_ratio: float  # 弱点属性倍率
    damage_ratio: float  # 与ダメージ倍率
    is_all_critical: bool  # 全会心
    is_no_critical: bool  # 会心なし
    is_ignore_stable: bool  # 安定値無視

    @staticmethod
    def from_raw_student(
        raw_student: RawStudent, buffs: None | list[tuple[str, float]] = None
    ) -> Student:
        buff_dict = defaultdict(float)
        for equip in [raw_student.equip1, raw_student.equip2, raw_student.equip3]:
            for key, value in equip.value.items():
                buff_dict[key] += value
        buff_dict["攻撃力(固定値)"] += (
            raw_student.kizuna_bonus
            + raw_student.weapon_attack
            + raw_student.support_attack
        )
        if buffs:
            for key, value in buffs:
                buff_dict[key] += value
        attack = round(
            raw_student.attack
            / RARITY_ATTACK_RATIO[raw_student.rarity]
            * RARITY_ATTACK_RATIO[5]
        )
        if raw_student.is_wb:
            attack += round(
                raw_student.attack
                / RARITY_ATTACK_RATIO[raw_student.rarity]
                * RARITY_ATTACK_RATIO[1]
                * 0.05
            )

        attack = round(
            (attack + buff_dict["攻撃力(固定値)"])
            * (1.0 + buff_dict["攻撃力(%)"] / 100)
        )
        critical = raw_student.critical
        critical = round(
            (critical + buff_dict["会心値(固定値)"])
            * (1.0 + buff_dict["会心値(%)"] / 100)
        )
        critical_damage = raw_student.critical_damage
        critical_damage = round(
            (critical_damage + buff_dict["会心ダメージ(固定値)"] / 100)
            * (1.0 + buff_dict["会心ダメージ(%)"] / 100)
        )
        weak_ratio = 2.0 + buff_dict["属性特効"] / 100
        damage_ratio = 1.0 + buff_dict["与ダメージ増加(%)"] / 100
        stable_ratio = 0.2 * (1 - buff_dict["安定率減少"] / 100)
        if raw_student.is_all_critical and raw_student.is_no_critical:
            raise ValueError("全会心と会心なしは同時に選択できません。")
        data = {
            "level": raw_student.level,
            "stable": raw_student.stable,
            "stable_ratio": stable_ratio,
            "ignore_defence_ratio": raw_student.ignore_defence_ratio,
            "ignore_defence": raw_student.ignore_defence,
            "chikei": raw_student.chikei,
            "element": raw_student.element,
            "attack": attack,
            "hit": raw_student.hit,
            "critical": critical,
            "critical_damage": critical_damage,
            "weak_ratio": weak_ratio,
            "damage_ratio": damage_ratio,
            "is_all_critical": raw_student.is_all_critical,
            "is_no_critical": raw_student.is_no_critical,
            "is_ignore_stable": raw_student.is_ignore_stable,
        }
        return Student(**data)
