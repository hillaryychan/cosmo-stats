import argparse
import asyncio
import sys

from cosmo_stats.enums import Artist, Season
from cosmo_stats.objekts.service import default_objekt_service


class CosmoStatsArgsNamespace:
    artist: Artist
    season: Season
    collection_no: str | None


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
    parser.add_argument(
        "-c",
        "--collection-no",
        type=str.upper,
        help="The collections to collect data for, e.g. 117Z,118Z,119Z,120Z",
    )
    parser.parse_args(sys.argv[1:], namespace=CosmoStatsArgsNamespace)

    if args.collection_no is None:
        print(
            "No collections provided. "
            "This will collect data for all collections in the season."
        )
        while True:
            confirmation = input("Are you sure you want to do this [Y/n]? ")
            match confirmation.lower():
                case "yes" | "y":
                    break
                case "no" | "n":
                    sys.exit()

    asyncio.run(
        default_objekt_service.get_objekt_sales_stats(
            args.artist, args.season, args.collection_no
        )
    )
