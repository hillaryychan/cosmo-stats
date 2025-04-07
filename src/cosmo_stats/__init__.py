import argparse
import asyncio
import sys

from cosmo_stats.enums import Artist, Season
from cosmo_stats.objekts.service import default_objekt_service


class CosmoStatsArgsNamespace:
    artist: Artist
    season: Season


def main() -> None:
    args = CosmoStatsArgsNamespace()

    parser = argparse.ArgumentParser(prog="cosmo-stats")
    parser.add_argument(
        "artist",
        choices=[season.value for season in Artist],
        type=str,
        help="The season of the objekts",
    )
    parser.add_argument(
        "season",
        choices=[season.value for season in Season],
        type=str.capitalize,
        help="The season of the objekts",
    )
    parser.parse_args(sys.argv[1:], namespace=CosmoStatsArgsNamespace)

    # 1st edition
    collections = ["101Z", "102Z", "103Z", "103Z", "105Z", "106Z", "107Z", "108Z"]
    # 2nd edition
    collections = ["109Z", "110Z", "111Z", "112Z", "113Z", "114Z", "115Z", "116Z"]
    # 3rd edition
    collections = ["117Z", "118Z", "119Z", "120Z"]
    asyncio.run(
        default_objekt_service.get_objekt_sales_stats(
            args.artist, args.season, collections
        )
    )
