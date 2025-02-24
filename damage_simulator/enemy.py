from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum


class Armor(Enum):
    軽装備: int = 0
    重装甲: int = 1
    特殊装甲: int = 2
    弾力装甲: int = 3


@dataclass(frozen=True)
class RawEnemy:
    level: int = 90
    armor: Armor = Armor.軽装備
    defence: int = 100
    dodge: int = 0
    critical_resist: int = 100
    critical_damage_resist: int = 50
    damage_resist: int = 0


@dataclass(frozen=True)
class Enemy:
    level: int
    armor: Armor
    defence: int
    dodge: int
    critical_resist: int
    critical_damage_resist: int
    damage_resist: int
    damage_ratio: float

    @staticmethod
    def from_raw_enemy(
        raw_enemy: RawEnemy, debuff_list: None | list[tuple[str, float]] = None
    ) -> Enemy:
        debuff_dict = defaultdict(float)
        if debuff_list:
            for debuff, value in debuff_list:
                if debuff != "被ダメージ増加":
                    debuff_dict[debuff] = min(80.0, value + debuff_dict[debuff])
                else:
                    debuff_dict[debuff] += value
        defense = round(raw_enemy.defence * (1 - debuff_dict["防御力"] / 100))
        dodge = round(raw_enemy.dodge * (1 - debuff_dict["回避値"] / 100))
        critical_resist = round(
            raw_enemy.critical_resist * (1 - debuff_dict["会心抵抗値"] / 100)
        )
        critical_damage_resist = round(
            raw_enemy.critical_damage_resist
            * (1 - debuff_dict["会心ダメージ抵抗"] / 100)
        )
        damage_ratio = 1.0 + debuff_dict["被ダメージ増加"] / 100
        return Enemy(
            level=raw_enemy.level,
            armor=raw_enemy.armor,
            defence=defense,
            dodge=dodge,
            critical_resist=critical_resist,
            critical_damage_resist=critical_damage_resist,
            damage_resist=raw_enemy.damage_resist,
            damage_ratio=damage_ratio,
        )
