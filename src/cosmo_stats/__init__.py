import argparse
import asyncio
import sys

from cosmo_stats.enums import Artist, Edition, Season, StatsOutput
from cosmo_stats.objekts.service import default_objekt_service
from cosmo_stats.signals import register_signal_handlers

register_signal_handlers()


class CosmoStatsArgsNamespace:
    artist: Artist
    season: Season
    collection_no: str | None
    edition: Edition
    output: StatsOutput


def main() -> None:
    args = CosmoStatsArgsNamespace()

    parser = argparse.ArgumentParser(prog="cosmo-stats")
    parser.add_argument(
        "artist",
        choices=[season.value for season in Artist],
        type=str,
        help="The artist of the objekts",
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
    parser.add_argument(
        "--edition",
        choices=[edition.value for edition in Edition],
        type=Edition,
        help="The edition to collect data for. There are three editions each season.",
    )
    parser.add_argument(
        "-o",
        "--output",
        choices=[report.value for report in StatsOutput],
        default=StatsOutput.TERM,
        type=str.lower,
        help="Outputs statistics in the provided format (defaults to term)",
    )
    parser.parse_args(sys.argv[1:], namespace=CosmoStatsArgsNamespace)

    if args.collection_no is None and args.edition is None:
        print(
            "No collections provided. "
            "This will collect data for all collections in the season."
        )
        while True:
            confirmation = input("Are you sure you want to do this [y/N]? ")
            match confirmation.lower():
                case "yes" | "y":
                    break
                case "no" | "n" | "":
                    sys.exit()
    if args.collection_no is not None and args.edition is not None:
        sys.exit("Provide either --collection-no or --edition not both")

    asyncio.run(
        default_objekt_service.get_objekt_sales_stats(
            args.artist,
            args.season,
            args.collection_no or args.edition.collection_no,
            args.output,
        )
    )
