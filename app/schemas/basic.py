from typing import Optional

from pydantic import HttpUrl

from .base import BaseModelORJson
from .common import MCAssets, NiceBuffScript, NiceTrait
from .enums import (
    FuncApplyTarget,
    NiceBuffType,
    NiceEventType,
    NiceFuncTargetType,
    NiceFuncType,
    NiceSvtFlag,
    NiceSvtType,
    SvtClass,
)


class BasicBuff(BaseModelORJson):
    id: int
    name: str
    icon: HttpUrl
    type: NiceBuffType
    script: NiceBuffScript
    vals: list[NiceTrait]
    tvals: list[NiceTrait]
    ckSelfIndv: list[NiceTrait]
    ckOpIndv: list[NiceTrait]


class BasicFunction(BaseModelORJson):
    funcId: int
    funcType: NiceFuncType
    funcTargetType: NiceFuncTargetType
    funcTargetTeam: FuncApplyTarget
    functvals: list[NiceTrait]
    funcquestTvals: list[NiceTrait]
    traitVals: list[NiceTrait] = []
    buffs: list[BasicBuff]


class BasicSkill(BaseModelORJson):
    id: int
    name: str
    ruby: str
    icon: Optional[HttpUrl] = None


class BasicTd(BaseModelORJson):
    id: int
    name: str
    ruby: str


class BasicServant(BaseModelORJson):
    id: int
    collectionNo: int
    name: str
    type: NiceSvtType
    flag: NiceSvtFlag
    className: SvtClass
    rarity: int
    atkMax: int
    hpMax: int
    face: HttpUrl


class BasicEquip(BaseModelORJson):
    id: int
    collectionNo: int
    name: str
    type: NiceSvtType
    flag: NiceSvtFlag
    rarity: int
    atkMax: int
    hpMax: int
    face: HttpUrl
    bondEquipOwner: Optional[int]
    valentineEquipOwner: Optional[int]


class BasicMysticCode(BaseModelORJson):
    id: int
    name: str
    item: MCAssets


class BasicCommandCode(BaseModelORJson):
    id: int
    collectionNo: int
    name: str
    rarity: int
    face: HttpUrl


class BasicReversedSkillTd(BaseModelORJson):
    servant: list[BasicServant] = []
    MC: list[BasicMysticCode] = []
    CC: list[BasicCommandCode] = []


class BasicReversedSkillTdType(BaseModelORJson):
    basic: Optional[BasicReversedSkillTd] = None


class BasicSkillReverse(BasicSkill):
    reverse: Optional[BasicReversedSkillTdType] = None


class BasicTdReverse(BasicTd):
    reverse: Optional[BasicReversedSkillTdType] = None


class BasicReversedFunction(BaseModelORJson):
    skill: list[BasicSkillReverse] = []
    NP: list[BasicTdReverse] = []


class BasicReversedFunctionType(BaseModelORJson):
    basic: Optional[BasicReversedFunction] = None


class BasicFunctionReverse(BasicFunction):
    reverse: Optional[BasicReversedFunctionType] = None


class BasicReversedBuff(BaseModelORJson):
    function: list[BasicFunctionReverse] = []


class BasicReversedBuffType(BaseModelORJson):
    basic: Optional[BasicReversedBuff] = None


class BasicBuffReverse(BasicBuff):
    reverse: Optional[BasicReversedBuffType] = None


class BasicEvent(BaseModelORJson):
    id: int
    type: NiceEventType
    name: str
    noticeAt: int
    startedAt: int
    endedAt: int
    finishedAt: int
    materialOpenedAt: int
    warIds: list[int]


class BasicWar(BaseModelORJson):
    id: int
    coordinates: list[list[int]]
    age: str
    name: str
    longName: str
    eventId: int
