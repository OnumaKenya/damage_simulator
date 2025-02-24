from damage_simulator.constants import WEAK_RATIO, DAMAGE_FUNC
from damage_simulator.enemy import Enemy
from damage_simulator.skill import Skill
from damage_simulator.students import Student

import random


def round_down_4(num: float) -> float:
    return int(num * 10000) / 10000


def calc_raw_damage(
    student: Student,
    enemy: Enemy,
    skill: Skill,
    random_num: float,
    is_critical: bool,
    hit_num: int,
) -> int:
    damage = 1
    # バフ込み攻撃力
    damage = int(damage * student.attack)
    # スキル倍率
    damage = int(damage * skill.skill_ratio / 100)
    # 乱数
    if not student.is_ignore_stable:
        rand_lb = min(
            1.0, student.stable / (student.stable + 1000) + student.stable_ratio
        )
        rand_ub = 1.0
        damage = int(damage * (rand_lb + (rand_ub - rand_lb) * random_num))

    # 補正倍率
    # レベル差補正
    level_diff = max(0, min(30, enemy.level - student.level))
    level_mul = 1 - 0.02 * level_diff
    # 装甲倍率
    if student.element.value == enemy.armor.value:
        armor_mul = student.weak_ratio
    else:
        armor_mul = WEAK_RATIO[student.element.value][enemy.armor.value]
    # 地形適正
    chikei_mul = student.chikei.value
    adjust_ratio = round_down_4(round_down_4(level_mul * armor_mul) * chikei_mul)
    damage = int(damage * adjust_ratio)
    # 防御倍率
    defence_true = max(
        0,
        enemy.defence * (1 - student.ignore_defence_ratio / 100)
        - student.ignore_defence,
    )
    defence_ratio = round_down_4((1666.66 + defence_true) / 1666.66)
    damage = int(damage * (1.0 / defence_ratio))
    # 会心倍率
    if is_critical:
        damage = int(
            damage * (student.critical_damage - enemy.critical_damage_resist) / 100
        )
    # 分割率
    damage = int(damage * skill.hit_ratio[hit_num] / 100)
    # 敵被ダメージ倍率
    damage = int(damage * enemy.damage_ratio)
    # 与ダメージ増加
    damage = int(damage * student.damage_ratio)
    return damage


def decrease_damage(damage: int) -> int:
    for (x_min, x_max), (a, b) in DAMAGE_FUNC:
        if x_min <= damage < x_max:
            return int(a * damage + b)


def calc_damage(
    student: Student,
    enemy: Enemy,
    skill: Skill,
    random_num: float,
    is_critical: bool,
    hit_num: int,
) -> int:
    damage = calc_raw_damage(student, enemy, skill, random_num, is_critical, hit_num)
    damage = decrease_damage(damage)
    return damage


def calc_total_raw_damage(
    student: Student, enemy: Enemy, skill: Skill, random_num: float, is_critical: bool
) -> int:
    total_damage = 0
    for hit_num in range(len(skill.hit_ratio)):
        total_damage += calc_raw_damage(
            student, enemy, skill, random_num, is_critical, hit_num
        )
    return total_damage


def calc_total_damage(
    student: Student, enemy: Enemy, skill: Skill, random_num: float, is_critical: bool
) -> int:
    total_damage = 0
    for hit_num in range(len(skill.hit_ratio)):
        total_damage += calc_damage(
            student, enemy, skill, random_num, is_critical, hit_num
        )
    return total_damage


def calc_hit_ratio(student: Student, enemy: Enemy) -> float:
    if student.hit > enemy.dodge:
        return 100
    else:
        return round_down_4(666.666 / (666.666 + enemy.dodge - student.hit)) * 100


def calc_critical_ratio(student: Student, enemy: Enemy) -> float:
    if student.is_all_critical:
        return 100.0
    elif student.is_no_critical:
        return 0.0
    else:
        return (
            round_down_4(
                (student.critical - enemy.critical_resist)
                / (student.critical - enemy.critical_resist + 666.66)
            )
            * 100
        )


def calc_damage_expected(damage_min: int, damage_max: int) -> float:
    res = 0.0
    for (x_min, x_max), (a, b) in DAMAGE_FUNC:
        x_min_interval = max(x_min, damage_min)
        x_max_interval = min(x_max, damage_max)
        if x_min_interval < x_max_interval:
            res += (
                (a * (x_min_interval + x_max_interval) / 2 + b)
                * (x_max_interval - x_min_interval)
                / (damage_max - damage_min)
            )
    return res


def calc_total_damage_expected(student: Student, enemy: Enemy, skill: Skill) -> float:
    damage_expected = 0.0
    for hit_num in range(len(skill.hit_ratio)):
        critical_damage_max = calc_raw_damage(student, enemy, skill, 1.0, True, hit_num)
        critical_damage_min = calc_raw_damage(student, enemy, skill, 0.0, True, hit_num)
        normal_damage_max = calc_raw_damage(student, enemy, skill, 1.0, False, hit_num)
        normal_damage_min = calc_raw_damage(student, enemy, skill, 0.0, False, hit_num)
        hit_ratio = calc_hit_ratio(student, enemy) / 100
        critical_ratio = calc_critical_ratio(student, enemy) / 100
        damage_expected += (
            critical_ratio
            * calc_damage_expected(critical_damage_min, critical_damage_max)
            + (1 - critical_ratio)
            * calc_damage_expected(normal_damage_min, normal_damage_max)
        ) * hit_ratio
    return round_down_4(damage_expected)


def damage_simulation(
    student: Student,
    enemy: Enemy,
    skill: Skill,
    total_number: int,
    trial: int,
) -> list[int]:
    damage_list = []
    hit_ratio = calc_hit_ratio(student, enemy)
    critical_ratio = calc_critical_ratio(student, enemy)
    for _ in range(trial):
        total_damage = 0
        for _enemy in range(total_number):
            for hit_num in range(len(skill.hit_ratio)):
                is_hit = random.random() * 100 < hit_ratio
                is_critical = random.random() * 100 < critical_ratio
                if not is_hit:
                    continue
                total_damage += calc_damage(
                    student, enemy, skill, random.random(), is_critical, hit_num
                )
        damage_list.append(total_damage)
    return damage_list
