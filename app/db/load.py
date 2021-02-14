import time
from typing import Any, Dict, List

import orjson
from pydantic import DirectoryPath
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine

from ..config import logger
from ..models.raw import TABLES_TO_BE_LOADED, TABLES_WITH_PK, mstSubtitle
from ..schemas.common import Region
from ..schemas.raw import get_subtitle_svtId
from .base import engines


def recreate_table(engine: Engine, table: Table) -> None:  # pragma: no cover
    table.drop(engine, checkfirst=True)
    table.create(engine, checkfirst=True)


def check_known_columns(
    data: List[Dict[str, Any]], table: Table
) -> bool:  # pragma: no cover
    table_columns = {column.name for column in table.columns}
    return set(data[0].keys()).issubset(table_columns)


def remove_unknown_columns(
    data: List[Dict[str, Any]], table: Table
) -> List[Dict[str, Any]]:  # pragma: no cover
    table_columns = {column.name for column in table.columns}
    return [{k: v for k, v in item.items() if k in table_columns} for item in data]


def update_db(region_path: Dict[Region, DirectoryPath]) -> None:  # pragma: no cover
    logger.info("Loading db …")
    start_loading_time = time.perf_counter()

    for region, master_folder in region_path.items():
        engine = engines[region]

        with engine.connect() as conn:
            for table in TABLES_WITH_PK:
                table.create(engine, checkfirst=True)
                table_json = master_folder / f"{table.name}.json"
                if table_json.exists():
                    with open(table_json, "rb") as fp:
                        id_data: List[Dict[str, Any]] = orjson.loads(fp.read())

                    insert_stmt = insert(table)
                    do_update_stmt = insert_stmt.on_conflict_do_update(
                        index_elements=[col for col in table.c if col.primary_key],
                        set_={
                            col: insert_stmt.excluded[col.name]
                            for col in table.c
                            if not col.primary_key
                        },
                    )
                    conn.execute(do_update_stmt, id_data)

            for table in TABLES_TO_BE_LOADED:
                table_json = master_folder / f"{table.name}.json"
                if table_json.exists():
                    with open(table_json, "rb") as fp:
                        data: List[Dict[str, Any]] = orjson.loads(fp.read())

                    if len(data) > 0 and not check_known_columns(data, table):
                        logger.warning(f"Found unknown columns in {table_json}")
                        data = remove_unknown_columns(data, table)

                    recreate_table(engine, table)
                    conn.execute(table.insert(), data)
                else:
                    recreate_table(engine, table)
                    logger.warning(f"Can't find file {table_json}.")

            subtitle_json = master_folder / "globalNewMstSubtitle.json"
            if subtitle_json.exists():
                with open(subtitle_json, "rb") as fp:
                    globalNewMstSubtitle = orjson.loads(fp.read())

                for subtitle in globalNewMstSubtitle:
                    subtitle["svtId"] = get_subtitle_svtId(subtitle["id"])

                recreate_table(engine, mstSubtitle)
                conn.execute(mstSubtitle.insert(), globalNewMstSubtitle)
            elif region == Region.NA:
                recreate_table(engine, mstSubtitle)
                logger.warning(f"Can't find file {subtitle_json}.")

    db_loading_time = time.perf_counter() - start_loading_time
    logger.info(f"Loaded db in {db_loading_time:.2f}s.")