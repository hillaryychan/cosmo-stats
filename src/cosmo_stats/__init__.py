import asyncio

from cosmo_stats.enums import Season
from cosmo_stats.objekts.service import default_objekt_service


async def objekt_stats(season: Season, collections: list[str]) -> None:
    objekts = await default_objekt_service.get_objekts(season, collections)
    data = await default_objekt_service.get_objekt_collection_data(objekts)
    stats = default_objekt_service.get_objekt_sales_stats(data)
    print(stats)


def main() -> None:
    asyncio.run(objekt_stats(Season.EVER01, ["117Z", "118Z", "119Z", "120Z"]))
