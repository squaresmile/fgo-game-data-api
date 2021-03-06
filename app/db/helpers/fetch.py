from typing import Iterable, Optional, Type, TypeVar, Union

from sqlalchemy import Table
from sqlalchemy.engine import Connection
from sqlalchemy.sql import ColumnElement, select

from app.schemas.base import BaseModelORJson

from ...models.raw import (
    mstBgm,
    mstBgmRelease,
    mstBoxGacha,
    mstBuff,
    mstClosedMessage,
    mstCombineCostume,
    mstCombineLimit,
    mstCombineMaterial,
    mstCombineSkill,
    mstCommandCode,
    mstCommandCodeComment,
    mstCommandCodeSkill,
    mstConstant,
    mstCv,
    mstEquip,
    mstEquipExp,
    mstEquipSkill,
    mstEvent,
    mstEventMission,
    mstEventMissionCondition,
    mstEventMissionConditionDetail,
    mstEventPointBuff,
    mstEventPointGroup,
    mstEventReward,
    mstEventRewardSet,
    mstEventTower,
    mstFriendship,
    mstFunc,
    mstFuncGroup,
    mstGift,
    mstIllustrator,
    mstItem,
    mstMap,
    mstMasterMission,
    mstQuest,
    mstShop,
    mstShopScript,
    mstSpot,
    mstSvt,
    mstSvtCard,
    mstSvtChange,
    mstSvtComment,
    mstSvtCostume,
    mstSvtExp,
    mstSvtExtra,
    mstSvtGroup,
    mstSvtLimit,
    mstSvtLimitAdd,
    mstSvtPassiveSkill,
    mstSvtVoiceRelation,
    mstVoice,
    mstWar,
    mstWarAdd,
)
from ...schemas.raw import (
    MstBgm,
    MstBgmRelease,
    MstBoxGacha,
    MstBuff,
    MstClosedMessage,
    MstCombineCostume,
    MstCombineLimit,
    MstCombineMaterial,
    MstCombineSkill,
    MstCommandCode,
    MstCommandCodeComment,
    MstCommandCodeSkill,
    MstConstant,
    MstCv,
    MstEquip,
    MstEquipExp,
    MstEquipSkill,
    MstEvent,
    MstEventMission,
    MstEventMissionCondition,
    MstEventMissionConditionDetail,
    MstEventPointBuff,
    MstEventPointGroup,
    MstEventReward,
    MstEventRewardSet,
    MstEventTower,
    MstFriendship,
    MstFunc,
    MstFuncGroup,
    MstGift,
    MstIllustrator,
    MstItem,
    MstMap,
    MstMasterMission,
    MstQuest,
    MstShop,
    MstShopScript,
    MstSpot,
    MstSvt,
    MstSvtCard,
    MstSvtChange,
    MstSvtComment,
    MstSvtCostume,
    MstSvtExp,
    MstSvtExtra,
    MstSvtGroup,
    MstSvtLimit,
    MstSvtLimitAdd,
    MstSvtPassiveSkill,
    MstSvtVoiceRelation,
    MstVoice,
    MstWar,
    MstWarAdd,
)


schema_map_fetch_one: dict[  # type:ignore
    Type[BaseModelORJson], tuple[Table, ColumnElement]
] = {
    MstSvt: (mstSvt, mstSvt.c.id),
    MstCv: (mstCv, mstCv.c.id),
    MstIllustrator: (mstIllustrator, mstIllustrator.c.id),
    MstCommandCode: (mstCommandCode, mstCommandCode.c.id),
    MstWar: (mstWar, mstWar.c.id),
    MstEquip: (mstEquip, mstEquip.c.id),
    MstEvent: (mstEvent, mstEvent.c.id),
    MstConstant: (mstConstant, mstConstant.c.name),
    MstQuest: (mstQuest, mstQuest.c.id),
    MstBuff: (mstBuff, mstBuff.c.id),
    MstFunc: (mstFunc, mstFunc.c.id),
    MstItem: (mstItem, mstItem.c.id),
    MstBgm: (mstBgm, mstBgm.c.id),
    MstShop: (mstShop, mstShop.c.id),
    MstMasterMission: (mstMasterMission, mstMasterMission.c.id),
    MstSvtExtra: (mstSvtExtra, mstSvtExtra.c.svtId),
}

TFetchOne = TypeVar("TFetchOne", bound=BaseModelORJson)


def get_one(
    conn: Connection, schema: Type[TFetchOne], where_id: Union[int, str]
) -> Optional[TFetchOne]:
    table, where_col = schema_map_fetch_one[schema]
    stmt = select(table).where(where_col == where_id)
    entity_db = conn.execute(stmt).fetchone()
    if entity_db:
        return schema.from_orm(entity_db)

    return None


schema_table_fetch_all: dict[  # type:ignore
    Type[BaseModelORJson], tuple[Table, ColumnElement, ColumnElement]
] = {
    MstSvtCard: (mstSvtCard, mstSvtCard.c.svtId, mstSvtCard.c.cardId),
    MstSvtLimit: (mstSvtLimit, mstSvtLimit.c.svtId, mstSvtLimit.c.limitCount),
    MstCombineSkill: (mstCombineSkill, mstCombineSkill.c.id, mstCombineSkill.c.skillLv),
    MstSvtChange: (mstSvtChange, mstSvtChange.c.svtId, mstSvtChange.c.priority),
    MstSvtCostume: (mstSvtCostume, mstSvtCostume.c.svtId, mstSvtCostume.c.id),
    MstSvtExp: (mstSvtExp, mstSvtExp.c.type, mstSvtExp.c.lv),
    MstFriendship: (mstFriendship, mstFriendship.c.id, mstFriendship.c.rank),
    MstSvtComment: (mstSvtComment, mstSvtComment.c.svtId, mstSvtComment.c.id),
    MstCommandCodeComment: (
        mstCommandCodeComment,
        mstCommandCodeComment.c.commandCodeId,
        mstCommandCodeComment.c.comment,
    ),
    MstCommandCodeSkill: (
        mstCommandCodeSkill,
        mstCommandCodeSkill.c.commandCodeId,
        mstCommandCodeSkill.c.num,
    ),
    MstCombineLimit: (
        mstCombineLimit,
        mstCombineLimit.c.id,
        mstCombineLimit.c.svtLimit,
    ),
    MstCombineCostume: (
        mstCombineCostume,
        mstCombineCostume.c.svtId,
        mstCombineCostume.c.costumeId,
    ),
    MstSvtLimitAdd: (
        mstSvtLimitAdd,
        mstSvtLimitAdd.c.svtId,
        mstSvtLimitAdd.c.limitCount,
    ),
    MstMap: (mstMap, mstMap.c.warId, mstMap.c.id),
    MstWarAdd: (mstWarAdd, mstWarAdd.c.warId, mstWarAdd.c.priority),
    MstEquipSkill: (mstEquipSkill, mstEquipSkill.c.equipId, mstEquipSkill.c.num),
    MstEquipExp: (mstEquipExp, mstEquipExp.c.equipId, mstEquipExp.c.lv),
    MstEventMission: (
        mstEventMission,
        mstEventMission.c.missionTargetId,
        mstEventMission.c.id,
    ),
    MstShop: (mstShop, mstShop.c.eventId, mstShop.c.id),
    MstEventReward: (mstEventReward, mstEventReward.c.eventId, mstEventReward.c.point),
    MstEventRewardSet: (
        mstEventRewardSet,
        mstEventRewardSet.c.eventId,
        mstEventRewardSet.c.id,
    ),
    MstEventPointBuff: (
        mstEventPointBuff,
        mstEventPointBuff.c.eventId,
        mstEventPointBuff.c.id,
    ),
    MstEventPointGroup: (
        mstEventPointGroup,
        mstEventPointGroup.c.eventId,
        mstEventPointGroup.c.groupId,
    ),
    MstEventTower: (mstEventTower, mstEventTower.c.eventId, mstEventTower.c.towerId),
    MstBoxGacha: (mstBoxGacha, mstBoxGacha.c.eventId, mstBoxGacha.c.id),
    MstCombineMaterial: (
        mstCombineMaterial,
        mstCombineMaterial.c.id,
        mstCombineMaterial.c.lv,
    ),
    MstSvtPassiveSkill: (
        mstSvtPassiveSkill,
        mstSvtPassiveSkill.c.svtId,
        mstSvtPassiveSkill.c.skillId,
    ),
    MstFuncGroup: (mstFuncGroup, mstFuncGroup.c.funcId, mstFuncGroup.c.eventId),
    MstBgmRelease: (mstBgmRelease, mstBgmRelease.c.bgmId, mstBgmRelease.c.id),
}

TFetchAll = TypeVar("TFetchAll", bound=BaseModelORJson)


def get_all(
    conn: Connection, schema: Type[TFetchAll], where_id: int
) -> list[TFetchAll]:
    table, where_col, order_col = schema_table_fetch_all[schema]
    stmt = select(table).where(where_col == where_id).order_by(order_col)
    return [schema.from_orm(db_row) for db_row in conn.execute(stmt).fetchall()]


schema_table_fetch_all_multiple: dict[  # type:ignore
    Type[BaseModelORJson], tuple[Table, ColumnElement, ColumnElement]
] = {
    MstSpot: (mstSpot, mstSpot.c.mapId, mstSpot.c.id),
    MstVoice: (mstVoice, mstVoice.c.id, mstVoice.c.id),
    MstSvtGroup: (mstSvtGroup, mstSvtGroup.c.id, mstSvtGroup.c.svtId),
    MstEventMissionCondition: (
        mstEventMissionCondition,
        mstEventMissionCondition.c.missionId,
        mstEventMissionCondition.c.id,
    ),
    MstEventMissionConditionDetail: (
        mstEventMissionConditionDetail,
        mstEventMissionConditionDetail.c.id,
        mstEventMissionConditionDetail.c.id,
    ),
    MstSvtVoiceRelation: (
        mstSvtVoiceRelation,
        mstSvtVoiceRelation.c.svtId,
        mstSvtVoiceRelation.c.svtId,
    ),
    MstBgm: (mstBgm, mstBgm.c.id, mstBgm.c.id),
    MstGift: (mstGift, mstGift.c.id, mstGift.c.id),
    MstShopScript: (mstShopScript, mstShopScript.c.shopId, mstShopScript.c.shopId),
    MstItem: (mstItem, mstItem.c.id, mstItem.c.id),
    MstClosedMessage: (mstClosedMessage, mstClosedMessage.c.id, mstClosedMessage.c.id),
    MstShop: (mstShop, mstShop.c.id, mstShop.c.id),
    MstQuest: (mstQuest, mstQuest.c.id, mstQuest.c.id),
}

TFetchAllMultiple = TypeVar("TFetchAllMultiple", bound=BaseModelORJson)


def get_all_multiple(
    conn: Connection,
    schema: Type[TFetchAllMultiple],
    where_ids: Iterable[Union[int, str]],
) -> list[TFetchAllMultiple]:
    table, where_col, order_col = schema_table_fetch_all_multiple[schema]
    stmt = select(table).where(where_col.in_(where_ids)).order_by(order_col)
    return [schema.from_orm(db_row) for db_row in conn.execute(stmt).fetchall()]


schema_map_fetch_everything: dict[  # type:ignore
    Type[BaseModelORJson], tuple[Table, ColumnElement]
] = {
    MstWar: (mstWar, mstWar.c.id),
    MstEvent: (mstEvent, mstEvent.c.id),
    MstCommandCode: (mstCommandCode, mstCommandCode.c.id),
    MstEquip: (mstEquip, mstEquip.c.id),
    MstBgm: (mstBgm, mstBgm.c.id),
    MstBgmRelease: (mstBgmRelease, mstBgmRelease.c.bgmId),
    MstItem: (mstItem, mstItem.c.id),
    MstIllustrator: (mstIllustrator, mstIllustrator.c.id),
    MstCv: (mstCv, mstCv.c.id),
    MstMasterMission: (mstMasterMission, mstMasterMission.c.id),
}

TFetchEverything = TypeVar("TFetchEverything", bound=BaseModelORJson)


def get_everything(
    conn: Connection, schema: Type[TFetchEverything]
) -> list[TFetchEverything]:  # pragma: no cover
    table, order_col = schema_map_fetch_everything[schema]
    stmt = select(table).order_by(order_col)
    entities_db = conn.execute(stmt).fetchall()

    return [schema.from_orm(entity) for entity in entities_db]
