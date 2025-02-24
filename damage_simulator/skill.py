from dataclasses import dataclass


@dataclass(frozen=True)
class Skill:
    skill_ratio: float
    hit_ratio: list[float]
