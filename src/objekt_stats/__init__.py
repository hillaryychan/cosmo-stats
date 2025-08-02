import argparse
import asyncio
import sys

from objekt_stats.enums.artms import ArtmsSeason
from objekt_stats.enums.cli import StatsOutput
from objekt_stats.enums.cosmo import Artist, Edition, Season
from objekt_stats.enums.idntt import IdnttSeason
from objekt_stats.enums.triples import TripleSSeason
from objekt_stats.objekts.service import default_objekt_service
from objekt_stats.signals import register_signal_handlers

register_signal_handlers()


class ObjektStatsArgsNamespace:
    artist: Artist
    season: Season
    collection_no: str | None
    edition: Edition
    output: StatsOutput


ARTIST_SUBPARSERS = frozenset(
    [
        (Artist.TRIPLES, TripleSSeason),
        (Artist.ARTMS, ArtmsSeason),
        (Artist.IDNTT, IdnttSeason),
    ]
)


def main() -> None:
    args = ObjektStatsArgsNamespace()

    parser = argparse.ArgumentParser(prog="objekt-stats")
    artist_subparser = parser.add_subparsers(
        dest="artist", help="Artist to run objekt-stats on."
    )
    for artist, season_enum in ARTIST_SUBPARSERS:
        artist_parser = artist_subparser.add_parser(artist.value)
        artist_parser.add_argument(
            "season",
            choices=[season.value for season in season_enum],
            type=str.capitalize,
            help="The season of the objekts",
        )
        artist_parser.add_argument(
            "-c",
            "--collection-no",
            type=str.upper,
            help="The collections to collect data for, e.g. 117Z,118Z,119Z,120Z",
        )
        artist_parser.add_argument(
            "--edition",
            choices=[edition.value for edition in Edition],
            type=Edition,
            help=(
                "The edition to collect data for. There are three editions each season."
            ),
        )
        artist_parser.add_argument(
            "-o",
            "--output",
            choices=[report.value for report in StatsOutput],
            default=StatsOutput.TERM,
            type=str.lower,
            help="Outputs statistics in the provided format (defaults to term)",
        )

    # Show help text when no args provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(2)

    parser.parse_args(sys.argv[1:], namespace=ObjektStatsArgsNamespace)

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
            args.collection_no or (args.edition and args.edition.collection_no),
            args.output,
        )
    )
