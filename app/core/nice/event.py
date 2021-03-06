from collections import defaultdict

from sqlalchemy.engine import Connection

from ...config import Settings
from ...schemas.common import Language, Region
from ...schemas.enums import DETAIL_MISSION_LINK_TYPE, ITEM_BG_TYPE_NAME, NiceItemBGType
from ...schemas.gameenums import (
    COND_TYPE_NAME,
    EVENT_TYPE_NAME,
    MISSION_PROGRESS_TYPE_NAME,
    MISSION_REWARD_TYPE_NAME,
    MISSION_TYPE_NAME,
    PAY_TYPE_NAME,
    PURCHASE_TYPE_NAME,
    SHOP_TYPE_NAME,
    BoxGachaFlag,
    CondType,
    NiceItemType,
    PayType,
    PurchaseType,
)
from ...schemas.nice import (
    AssetURL,
    NiceEvent,
    NiceEventLottery,
    NiceEventLotteryBox,
    NiceEventMission,
    NiceEventMissionCondition,
    NiceEventMissionConditionDetail,
    NiceEventPointBuff,
    NiceEventPointGroup,
    NiceEventReward,
    NiceEventTower,
    NiceEventTowerReward,
    NiceGift,
    NiceItem,
    NiceItemAmount,
    NiceItemSet,
    NiceShop,
)
from ...schemas.raw import (
    MstBoxGacha,
    MstBoxGachaBase,
    MstEventMission,
    MstEventMissionCondition,
    MstEventMissionConditionDetail,
    MstEventPointBuff,
    MstEventPointGroup,
    MstEventReward,
    MstEventTower,
    MstEventTowerReward,
    MstGift,
    MstSetItem,
    MstShop,
    MstShopScript,
)
from .. import raw
from ..utils import get_traits_list, get_translation
from .gift import get_nice_gift
from .item import get_nice_item
from .script import get_script_url


settings = Settings()


def get_nice_gifts(gift_id: int, gift_maps: dict[int, list[MstGift]]) -> list[NiceGift]:
    return [get_nice_gift(gift) for gift in gift_maps[gift_id]]


def get_nice_set_item(set_item: MstSetItem) -> NiceItemSet:
    return NiceItemSet(
        id=set_item.id,
        purchaseType=PURCHASE_TYPE_NAME[set_item.purchaseType],
        targetId=set_item.targetId,
        setNum=set_item.setNum,
    )


def get_nice_shop(
    conn: Connection,
    region: Region,
    shop: MstShop,
    set_items: list[MstSetItem],
    shop_scripts: dict[int, MstShopScript],
    lang: Language,
) -> NiceShop:
    if shop.payType == PayType.FRIEND_POINT:
        shop_item_id = 4
    elif shop.payType == PayType.MANA:
        shop_item_id = 3
    else:
        shop_item_id = shop.itemIds[0]

    if shop.purchaseType == PurchaseType.SET_ITEM:
        shop_set_items = [
            get_nice_set_item(set_item)
            for set_item in set_items
            if set_item.id in shop.targetIds
        ]
    else:
        shop_set_items = []

    if shop.payType == PayType.FREE:
        cost = NiceItemAmount(
            item=NiceItem(
                id=0,
                name="",
                type=NiceItemType.stone,
                uses=[],
                detail="",
                individuality=[],
                icon=AssetURL.items.format(
                    base_url=settings.asset_url, region=region, item_id=0
                ),
                background=NiceItemBGType.zero,
                priority=0,
                dropPriority=0,
            ),
            amount=0,
        )
    else:
        cost = NiceItemAmount(
            item=get_nice_item(conn, region, shop_item_id, lang), amount=shop.prices[0]
        )

    nice_shop = NiceShop(
        id=shop.id,
        baseShopId=shop.baseShopId,
        shopType=SHOP_TYPE_NAME[shop.shopType],
        eventId=shop.eventId,
        slot=shop.slot,
        priority=shop.priority,
        name=shop.name,
        detail=shop.detail,
        infoMessage=shop.infoMessage,
        warningMessage=shop.warningMessage,
        payType=PAY_TYPE_NAME[shop.payType],
        cost=cost,
        purchaseType=PURCHASE_TYPE_NAME[shop.purchaseType],
        targetIds=shop.targetIds,
        itemSet=shop_set_items,
        setNum=shop.setNum,
        limitNum=shop.limitNum,
        defaultLv=shop.defaultLv,
        defaultLimitCount=shop.defaultLimitCount,
        openedAt=shop.openedAt,
        closedAt=shop.closedAt,
    )

    if shop.id in shop_scripts:
        shop_script = shop_scripts[shop.id]
        nice_shop.scriptName = shop_script.name
        nice_shop.scriptId = shop_script.scriptId
        nice_shop.script = get_script_url(region, shop_script.scriptId)

    return nice_shop


def get_bgImage_url(region: Region, bgImageId: int, event_id: int, prefix: str) -> str:
    base_settings = {"base_url": settings.asset_url, "region": region}
    return (
        AssetURL.eventReward.format(**base_settings, fname=f"{prefix}{bgImageId}")
        if bgImageId > 0
        else AssetURL.eventReward.format(**base_settings, fname=f"{prefix}{event_id}00")
    )


def get_nice_reward(
    region: Region,
    reward: MstEventReward,
    event_id: int,
    gift_maps: dict[int, list[MstGift]],
) -> NiceEventReward:
    return NiceEventReward(
        groupId=reward.groupId,
        point=reward.point,
        gifts=get_nice_gifts(reward.giftId, gift_maps),
        bgImagePoint=get_bgImage_url(
            region, reward.bgImageId, event_id, "event_rewardpoint_"
        ),
        bgImageGet=get_bgImage_url(
            region, reward.bgImageId, event_id, "event_rewardget_"
        ),
    )


def get_nice_pointGroup(
    region: Region, pointGroup: MstEventPointGroup
) -> NiceEventPointGroup:
    return NiceEventPointGroup.parse_obj(
        {
            "groupId": pointGroup.groupId,
            "name": pointGroup.name,
            "icon": AssetURL.items.format(
                base_url=settings.asset_url, region=region, item_id=pointGroup.iconId
            ),
        }
    )


def get_nice_pointBuff(
    region: Region, pointBuff: MstEventPointBuff
) -> NiceEventPointBuff:
    return NiceEventPointBuff.parse_obj(
        {
            "id": pointBuff.id,
            "funcIds": pointBuff.funcIds,
            "groupId": pointBuff.groupId,
            "eventPoint": pointBuff.eventPoint,
            "name": pointBuff.name,
            "detail": pointBuff.detail,
            "icon": AssetURL.items.format(
                base_url=settings.asset_url, region=region, item_id=pointBuff.imageId
            ),
            "background": ITEM_BG_TYPE_NAME[pointBuff.bgImageId],
            "value": pointBuff.value,
        }
    )


def get_nice_mission_cond_detail(
    cond_detail: MstEventMissionConditionDetail,
) -> NiceEventMissionConditionDetail:
    return NiceEventMissionConditionDetail(
        id=cond_detail.id,
        missionTargetId=cond_detail.missionTargetId,
        missionCondType=cond_detail.missionCondType,
        logicType=cond_detail.logicType,
        targetIds=cond_detail.targetIds,
        addTargetIds=cond_detail.addTargetIds,
        targetQuestIndividualities=get_traits_list(
            cond_detail.targetQuestIndividualities
        ),
        conditionLinkType=DETAIL_MISSION_LINK_TYPE[cond_detail.conditionLinkType],
        targetEventIds=cond_detail.targetEventIds,
    )


def get_nice_mission_cond(
    cond: MstEventMissionCondition, details: dict[int, MstEventMissionConditionDetail]
) -> NiceEventMissionCondition:
    nice_mission_cond = NiceEventMissionCondition(
        id=cond.id,
        missionProgressType=MISSION_PROGRESS_TYPE_NAME[cond.missionProgressType],
        priority=cond.priority,
        missionTargetId=cond.missionTargetId,
        condGroup=cond.condGroup,
        condType=COND_TYPE_NAME[cond.condType],
        targetIds=cond.targetIds,
        targetNum=cond.targetNum,
        conditionMessage=cond.conditionMessage,
        closedMessage=cond.closedMessage,
        flag=cond.flag,
    )
    if (
        cond.condType == CondType.MISSION_CONDITION_DETAIL
        and cond.targetIds[0] in details
    ):
        nice_mission_cond.detail = get_nice_mission_cond_detail(
            details[cond.targetIds[0]]
        )
    return nice_mission_cond


def get_nice_mission(
    mission: MstEventMission,
    conds: list[MstEventMissionCondition],
    details: dict[int, MstEventMissionConditionDetail],
    gift_maps: dict[int, list[MstGift]],
) -> NiceEventMission:
    return NiceEventMission(
        id=mission.id,
        flag=mission.flag,
        type=MISSION_TYPE_NAME[mission.type],
        missionTargetId=mission.missionTargetId,
        dispNo=mission.dispNo,
        name=mission.name,
        detail=mission.detail,
        startedAt=mission.startedAt,
        endedAt=mission.endedAt,
        closedAt=mission.closedAt,
        rewardType=MISSION_REWARD_TYPE_NAME[mission.rewardType],
        gifts=get_nice_gifts(mission.giftId, gift_maps),
        bannerGroup=mission.bannerGroup,
        priority=mission.priority,
        rewardRarity=mission.rewardRarity,
        notfyPriority=mission.notfyPriority,
        presentMessageId=mission.presentMessageId,
        conds=(get_nice_mission_cond(cond, details) for cond in conds),
    )


def get_nice_missions(
    mstEventMission: list[MstEventMission],
    mstEventMissionCondition: list[MstEventMissionCondition],
    mstEventMissionConditionDetail: list[MstEventMissionConditionDetail],
    gift_maps: dict[int, list[MstGift]],
) -> list[NiceEventMission]:
    mission_cond_details = {
        detail.id: detail for detail in mstEventMissionConditionDetail
    }
    missions = [
        get_nice_mission(
            mission,
            [cond for cond in mstEventMissionCondition if cond.missionId == mission.id],
            mission_cond_details,
            gift_maps,
        )
        for mission in mstEventMission
    ]
    return missions


def get_nice_tower_rewards(
    region: Region, reward: MstEventTowerReward, gift_maps: dict[int, list[MstGift]]
) -> NiceEventTowerReward:
    base_settings = {"base_url": settings.asset_url, "region": region}
    return NiceEventTowerReward(
        floor=reward.floor,
        gifts=get_nice_gifts(reward.giftId, gift_maps),
        boardMessage=reward.boardMessage,
        rewardGet=AssetURL.eventReward.format(
            **base_settings,
            fname=f"event_tower_rewardget_{reward.boardImageId}",
        ),
        banner=AssetURL.eventReward.format(
            **base_settings,
            fname=f"event_towerbanner_{reward.boardImageId}",
        ),
    )


def get_nice_event_tower(
    region: Region,
    tower: MstEventTower,
    rewards: list[MstEventTowerReward],
    gift_maps: dict[int, list[MstGift]],
) -> NiceEventTower:
    return NiceEventTower(
        towerId=tower.towerId,
        name=tower.name,
        rewards=[
            get_nice_tower_rewards(region, reward, gift_maps)
            for reward in rewards
            if reward.towerId == tower.towerId
        ],
    )


def get_nice_lottery_box(
    region: Region,
    box: MstBoxGachaBase,
    box_index: int,
    gift_maps: dict[int, list[MstGift]],
) -> NiceEventLotteryBox:
    base_settings = {"base_url": settings.asset_url, "region": region}
    return NiceEventLotteryBox(
        id=box.id,
        boxIndex=box_index,
        no=box.no,
        type=box.type,
        gifts=get_nice_gifts(box.targetId, gift_maps),
        maxNum=box.maxNum,
        isRare=box.isRare,
        priority=box.priority,
        detail=box.detail,
        icon=AssetURL.eventReward.format(
            **base_settings,
            fname=f"icon_event_{box.iconId}",
        ),
        banner=AssetURL.eventReward.format(
            **base_settings,
            fname=f"event_gachabanner_{box.bannerId}",
        ),
    )


def get_nice_lottery(
    conn: Connection,
    region: Region,
    lottery: MstBoxGacha,
    boxes: list[MstBoxGachaBase],
    gift_maps: dict[int, list[MstGift]],
    lang: Language,
) -> NiceEventLottery:
    nice_boxes: list[NiceEventLotteryBox] = []
    for box_index, base_id in enumerate(lottery.baseIds):
        for box in boxes:
            if box.id == base_id:
                nice_boxes.append(
                    get_nice_lottery_box(region, box, box_index, gift_maps)
                )

    return NiceEventLottery(
        id=lottery.id,
        slot=lottery.slot,
        payType=PAY_TYPE_NAME[lottery.payType],
        cost=NiceItemAmount(
            item=get_nice_item(conn, region, lottery.payTargetId, lang),
            amount=lottery.payValue,
        ),
        priority=lottery.priority,
        limited=lottery.flag == BoxGachaFlag.LIMIT_RESET,
        boxes=nice_boxes,
    )


def get_nice_event(
    conn: Connection, region: Region, event_id: int, lang: Language
) -> NiceEvent:
    raw_event = raw.get_event_entity(conn, event_id)

    base_settings = {"base_url": settings.asset_url, "region": region}

    shop_scripts = {
        shop_script.shopId: shop_script for shop_script in raw_event.mstShopScript
    }

    gift_maps: dict[int, list[MstGift]] = defaultdict(list)
    for gift in raw_event.mstGift:
        gift_maps[gift.id].append(gift)

    missions = get_nice_missions(
        raw_event.mstEventMission,
        raw_event.mstEventMissionCondition,
        raw_event.mstEventMissionConditionDetail,
        gift_maps,
    )

    nice_event = NiceEvent(
        id=raw_event.mstEvent.id,
        type=EVENT_TYPE_NAME[raw_event.mstEvent.type],
        name=get_translation(lang, raw_event.mstEvent.name),
        shortName=raw_event.mstEvent.shortName,
        detail=raw_event.mstEvent.detail,
        noticeBanner=AssetURL.banner.format(
            **base_settings, banner=f"event_war_{raw_event.mstEvent.noticeBannerId}"
        )
        if raw_event.mstEvent.noticeBannerId != 0
        else None,
        banner=AssetURL.banner.format(
            **base_settings, banner=f"event_war_{raw_event.mstEvent.bannerId}"
        )
        if raw_event.mstEvent.bannerId != 0
        else None,
        icon=AssetURL.banner.format(
            **base_settings, banner=f"banner_icon_{raw_event.mstEvent.iconId}"
        )
        if raw_event.mstEvent.iconId != 0
        else None,
        bannerPriority=raw_event.mstEvent.bannerPriority,
        noticeAt=raw_event.mstEvent.noticeAt,
        startedAt=raw_event.mstEvent.startedAt,
        endedAt=raw_event.mstEvent.endedAt,
        finishedAt=raw_event.mstEvent.finishedAt,
        materialOpenedAt=raw_event.mstEvent.materialOpenedAt,
        warIds=(war.id for war in raw_event.mstWar),
        shop=(
            get_nice_shop(conn, region, shop, raw_event.mstSetItem, shop_scripts, lang)
            for shop in raw_event.mstShop
        ),
        rewards=(
            get_nice_reward(region, reward, event_id, gift_maps)
            for reward in raw_event.mstEventReward
        ),
        pointGroups=(
            get_nice_pointGroup(region, pointGroup)
            for pointGroup in raw_event.mstEventPointGroup
        ),
        pointBuffs=(
            get_nice_pointBuff(region, pointBuff)
            for pointBuff in raw_event.mstEventPointBuff
        ),
        missions=missions,
        towers=(
            get_nice_event_tower(
                region, tower, raw_event.mstEventTowerReward, gift_maps
            )
            for tower in raw_event.mstEventTower
        ),
        lotteries=(
            get_nice_lottery(
                conn, region, lottery, raw_event.mstBoxGachaBase, gift_maps, lang
            )
            for lottery in raw_event.mstBoxGacha
        ),
    )

    return nice_event
