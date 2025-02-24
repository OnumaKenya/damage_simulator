from enum import Enum

HAT = {"攻撃力(%)": 50, "会心ダメージ(固定値)": 2000}
GLOVE = {"攻撃力(%)": 50, "会心値(固定値)": 500, "命中値(固定値)": 220}
SHOE = {"攻撃力(%)": 46}

BAG = {}
BADGE = {}
HAIRPIN = {"会心値(固定値)": 150}

AMULATE = {"会心値(固定値)": 250}
WATCH = {"会心値(固定値)": 440, "会心ダメージ(固定値)": 2500}
NECKLACE = {"攻撃力(%)": 14}


class Equip1(Enum):
    帽子 = HAT
    グローブ = GLOVE
    靴 = SHOE


class Equip2(Enum):
    鞄 = BAG
    バッジ = BADGE
    ヘアピン = HAIRPIN


class Equip3(Enum):
    お守り = AMULATE
    時計 = WATCH
    ネックレス = NECKLACE
