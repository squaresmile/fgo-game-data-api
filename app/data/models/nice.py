from enum import Enum
from typing import List

from pydantic import BaseModel


class Gender(str, Enum):
    Male = "Male"
    Female = "Female"
    Unknown = "Unknown"


class CardType(str, Enum):
    Arts = "Arts"
    Buster = "Buster"
    Quick = "Quick"
    Extra = "Extra"


class NiceServantEntity(BaseModel):
    collectionNo: int
    name: str
    cost: int
    gender: Gender
    attackBaseNp: float
    defenceBaseNp: float
    starAbsorb: int
    starGen: float
    instantDeathChance: float
    atkMax: int
    atkBase: int
    hpMax: int
    hpBase: int
    growthCurve: int
    atkGrowth: List[int]
    hpGrowth: List[int]
    cards: List[CardType]
    busterDistribution: List[int]
    artsDistribution: List[int]
    quickDistribution: List[int]
    extraDistribution: List[int]
    # npDistribution: List[int]
