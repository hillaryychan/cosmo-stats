import pandas as pd

from cosmo_stats.clients.apollo_client import ApolloApiClient, default_apollo_api_client
from cosmo_stats.clients.models import Objekt
from cosmo_stats.enums import Season
from cosmo_stats.objekts.models import ObjektCollectionData


class ObjektService:
    def __init__(self, api_client: ApolloApiClient) -> None:
        self._api_client = api_client

    async def get_objekts(self, season: Season, collections: list[str]) -> list[Objekt]:
        objekts = []
        page = 0
        while True:
            resp = await self._api_client.get_objekts(season, collections, page)
            objekts.extend(resp.objekts)
            if not resp.has_next or resp.next_start_after is None:
                break
            page = resp.next_start_after

        return objekts

    async def get_objekt_collection_data(
        self, objekts: list[Objekt]
    ) -> list[ObjektCollectionData]:
        data = []
        for objekt in objekts:
            metadata = await self._api_client.get_objekt_collection_metadata(
                objekt.slug
            )
            data.append(
                ObjektCollectionData(
                    season=objekt.season,
                    member=objekt.member,
                    collection_no=objekt.collection_no,
                    total=int(metadata.total),
                )
            )
        return data

    def get_objekt_sales_stats(
        self, objekts_data: list[ObjektCollectionData]
    ) -> pd.DataFrame:
        objekts_df = pd.DataFrame(
            [objekt_data.model_dump() for objekt_data in objekts_data]
        )
        stats_df = pd.pivot_table(
            objekts_df, values="total", index=["member"], columns=["collection_no"]
        )
        stats_df.insert(0, "total", stats_df.sum(axis=1))
        return stats_df.sort_values(by="total", ascending=False)


default_objekt_service = ObjektService(default_apollo_api_client)
