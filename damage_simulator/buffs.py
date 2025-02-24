from enum import Enum

class Buff(Enum):
    attack: str = "攻撃力(固定値)"
    attack_ratio: str = "攻撃力(%)"
    critical: str = "会心値(固定値)"
    critical_ratio: str = "会心値(%)"
    critical_damage: str = "会心ダメージ(固定値)"
    critical_damage_ratio: str = "会心ダメージ(%)"
    weak_ratio: str = "属性特効"
    damage_ratio: str = "与ダメージ増加(%)"
    stable_debuff: str = "安定率減少"

class Debuff(Enum):
    defence: str = "防御力"
    dodge: str = "回避値"
    critical_resist: str = "会心抵抗値"
    critical_damage_resist: str = "会心ダメージ抵抗"
    damage_resist: str = "被ダメージ増加"

