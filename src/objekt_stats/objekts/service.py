import asyncio
from itertools import batched

import pandas as pd

from objekt_stats.clients.apollo_client import (
    ApolloApiClient,
    ApolloClientError,
    default_apollo_api_client,
)
from objekt_stats.clients.models import Objekt
from objekt_stats.enums import Artist, Season, StatsOutput
from objekt_stats.objekts.models import ObjektCollectionData


class ObjektService:
    def __init__(self, api_client: ApolloApiClient) -> None:
        self._api_client = api_client

    async def _get_objekts(
        self, artist: Artist, season: Season, collection_no: str | None
    ) -> list[Objekt]:
        objekts = []
        page = 0
        while True:
            resp = await self._api_client.get_objekts(
                artist, season, collection_no, page
            )
            objekts.extend(resp.objekts)
            if not resp.has_next or resp.next_start_after is None:
                break
            page = resp.next_start_after

        return objekts

    async def _get_objekt_collection_data(
        self, objekts: list[Objekt]
    ) -> list[ObjektCollectionData]:
        data = []

        async def get_objekt_collection_data_task(objekt: Objekt) -> None:
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

        for batch in batched(objekts, 100, strict=False):
            tasks = map(get_objekt_collection_data_task, batch)
            await asyncio.gather(*tasks)

        return data

    def _get_objekt_sales_stats_dataframe(
        self, objekts_data: list[ObjektCollectionData]
    ) -> pd.DataFrame:
        objekts_df = pd.DataFrame(
            [objekt_data.model_dump() for objekt_data in objekts_data]
        )
        # generate collection_id from season and collection number
        objekts_df["collection_id"] = objekts_df.apply(
            lambda x: x["season"][0] + x["collection_no"], axis=1
        )
        # pivot table s.t. collection_ids are columns
        stats_df = pd.pivot_table(
            objekts_df, values="total", index=["member"], columns=["collection_id"]
        )
        # calculate total sales of collection_ids per member
        stats_df.insert(0, "total", stats_df.sum(axis=1))
        return stats_df.sort_values(by="total", ascending=False)

    def _output_objekt_sales_stats(
        self, stats: pd.DataFrame, output: StatsOutput
    ) -> None:
        match output:
            case StatsOutput.CSV:
                print(stats.to_csv())
            case StatsOutput.HTML:
                print(stats.to_html())
            case StatsOutput.JSON:
                print(stats.to_json())
            case _:
                print(stats)

    async def get_objekt_sales_stats(
        self,
        artist: Artist,
        season: Season,
        collection_no: str | None,
        output: StatsOutput,
    ) -> None:
        try:
            objekts = await self._get_objekts(artist, season, collection_no)
            if len(objekts) == 0:
                print("No objekts found")
                return

            data = await self._get_objekt_collection_data(objekts)
            stats = self._get_objekt_sales_stats_dataframe(data)
            self._output_objekt_sales_stats(stats, output)
        except ApolloClientError as exc:
            print(exc)


default_objekt_service = ObjektService(default_apollo_api_client)
