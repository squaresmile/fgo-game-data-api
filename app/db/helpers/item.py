from typing import Any, Iterable, Optional

from sqlalchemy.engine import Connection
from sqlalchemy.sql import and_, select

from ...models.raw import mstItem, mstSetItem
from ...schemas.raw import MstItem, MstSetItem


def get_mstSetItem(conn: Connection, set_item_ids: Iterable[int]) -> list[MstSetItem]:
    mstSetItem_stmt = (
        select(mstSetItem)
        .where(mstSetItem.c.id.in_(set_item_ids))
        .order_by(mstSetItem.c.id)
    )
    return [
        MstSetItem.from_orm(set_item)
        for set_item in conn.execute(mstSetItem_stmt).fetchall()
    ]


def get_all_items(conn: Connection) -> list[MstItem]:  # pragma: no cover
    all_item_stmt = select(mstItem).order_by(mstItem.c.id)
    return [MstItem.from_orm(item) for item in conn.execute(all_item_stmt).fetchall()]


def get_item_search(
    conn: Connection,
    individuality: Optional[Iterable[int]],
    item_type: Optional[Iterable[int]],
    bg_type: Optional[Iterable[int]],
    use_ids: Optional[Iterable[int]],
) -> list[MstItem]:
    where_clause: list[Any] = [True]
    if individuality:
        where_clause.append(mstItem.c.individuality.contains(individuality))
    if item_type:
        where_clause.append(mstItem.c.type.in_(item_type))
    if bg_type:
        where_clause.append(mstItem.c.bgImageId.in_(bg_type))
    if use_ids:
        where_clause.append(mstItem.c.id.in_(use_ids))

    item_search_stmt = select(mstItem).distinct().where(and_(*where_clause))

    return [
        MstItem.from_orm(item) for item in conn.execute(item_search_stmt).fetchall()
    ]