import asyncio

from cosmo_stats.enums import Season
from cosmo_stats.objekts.service import default_objekt_service


def main() -> None:
    asyncio.run(
        default_objekt_service.get_objekt_sales_stats(
            Season.EVER01, ["117Z", "118Z", "119Z", "120Z"]
        )
    )
