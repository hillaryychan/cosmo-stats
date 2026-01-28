import asyncio
from dataclasses import asdict
from itertools import batched

import pandas as pd

from cosmo_stats.clients.apollo_client import (
    ApolloApiClient,
    ApolloClientError,
    default_apollo_api_client,
)
from cosmo_stats.enums.cli import StatsOutput
from cosmo_stats.enums.cosmo import Member, Season
from cosmo_stats.objekts.models import Objekt


class ObjektService:
    def __init__(self, api_client: ApolloApiClient) -> None:
        self._api_client = api_client

    async def _get_objekt_collection_data_from_slug(
        self, objekts: list[Objekt]
    ) -> list[Objekt]:
        data = []

        async def get_objekt_collection_data_task(objekt: Objekt) -> None:
            metadata = await self._api_client.get_objekt_collection_metadata(
                objekt.slug
            )

            objekt.total = int(metadata.total)
            data.append(objekt)

        for batch in batched(objekts, 100, strict=False):
            tasks = map(get_objekt_collection_data_task, batch)
            await asyncio.gather(*tasks)

        return data

    def _get_objekt_sales_stats_dataframe(
        self,
        objekts_data: list[Objekt],
        show_full_stats: bool,
    ) -> pd.DataFrame:
        objekts_df = pd.DataFrame([asdict(objekt_data) for objekt_data in objekts_data])
        # pivot table s.t. collection_nos are columns
        objekts_df = pd.pivot_table(
            objekts_df, values="total", index=["member"], columns=["collection_no"]
        )
        results_df = objekts_df.copy().fillna(0)

        # calculate total objekts per member
        results_df.insert(0, "total", objekts_df.sum(axis=1))
        results_df = results_df.sort_values(by="total", ascending=False)

        # add additional stats
        if show_full_stats:
            results_df.insert(1, "min", objekts_df.min(axis=1))
            results_df.insert(1, "max", objekts_df.max(axis=1))
            results_df.insert(1, "median", objekts_df.median(axis=1))
            results_df.insert(1, "mean", objekts_df.mean(axis=1))

        # calculate total of each column
        results_df.loc["total"] = results_df.sum(axis=0)

        return results_df

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
        member_enum_cls: type[Member],
        season: Season,
        collection_no: list[str] | None,
        show_full_stats: bool,
        output: StatsOutput,
    ) -> None:
        try:
            objekts = [
                Objekt(season=season, member=member, collection_no=collection)
                for member in member_enum_cls
                for collection in collection_no or []
            ]

            data = await self._get_objekt_collection_data_from_slug(objekts)
            stats = self._get_objekt_sales_stats_dataframe(data, show_full_stats)
            self._output_objekt_sales_stats(stats, output)
        except ApolloClientError as exc:
            print(exc)


default_objekt_service = ObjektService(default_apollo_api_client)
