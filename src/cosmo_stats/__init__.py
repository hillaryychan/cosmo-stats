import argparse
import asyncio
import sys

from cosmo_stats.enums import Season
from cosmo_stats.objekts.service import default_objekt_service


class CosmoStatsArgsNamespace:
    season: Season


def main() -> None:
    args = CosmoStatsArgsNamespace()

    parser = argparse.ArgumentParser(prog="cosmo-stats")
    parser.add_argument(
        "season",
        choices=[season.value for season in Season],
        type=str.capitalize,
        help="The season of the objekts",
    )
    parser.parse_args(sys.argv[1:], namespace=CosmoStatsArgsNamespace)
    asyncio.run(
        default_objekt_service.get_objekt_sales_stats(
            args.season, ["117Z", "118Z", "119Z", "120Z"]
        )
    )
