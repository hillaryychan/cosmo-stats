import pandas as pd

from cosmo_stats.clients.apollo_client import fetch_objekt_metadata, fetch_objekts
from cosmo_stats.clients.models import Objekt
from cosmo_stats.objekts.models import ObjektData


def get_objekts(season: str, collections: list[str]) -> list[Objekt]:
    objekts = []
    page = 0
    while True:
        resp = fetch_objekts(season, collections, page)
        objekts.extend(resp.objekts)
        if not resp.has_next or resp.next_start_after is None:
            break
        page = resp.next_start_after

    return objekts


def get_objekt_data(objekts: list[Objekt]) -> list[ObjektData]:
    data = []
    for objekt in objekts:
        metadata = fetch_objekt_metadata(objekt.slug)
        data.append(
            ObjektData(
                season=objekt.season,
                member=objekt.member,
                collection_no=objekt.collection_no,
                total=int(metadata.total),
            )
        )
    return data


def get_objekt_sales_stats(objekts: list[ObjektData]) -> pd.DataFrame:
    objekts_df = pd.DataFrame([objekt.model_dump() for objekt in objekts])
    stats_df = pd.pivot_table(
        objekts_df, values="total", index=["member"], columns=["collection_no"]
    )
    stats_df.insert(0, "total", stats_df.sum(axis=1))
    return stats_df.sort_values(by="total", ascending=False)
