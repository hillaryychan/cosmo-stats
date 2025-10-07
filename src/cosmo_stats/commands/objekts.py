import asyncio
from typing import Annotated

import typer

from cosmo_stats.commands.constants import (
    COLLECTION_NO_HELP_TEXT,
    EDITION_HELP_TEXT,
    FULL_STATISTICS_HELP_TEXT,
    OUTPUT_HELP_TEXT,
    SEASON_HELP_TEXT,
)
from cosmo_stats.enums.artms import ArtmsSeason
from cosmo_stats.enums.cli import StatsOutput
from cosmo_stats.enums.cosmo import Artist, Edition
from cosmo_stats.enums.idntt import IdnttSeason
from cosmo_stats.enums.triples import TripleSSeason
from cosmo_stats.objekts.service import default_objekt_service

app = typer.Typer(
    no_args_is_help=True, help="Retrieve objekt statistics for an artist."
)


def _validate_collection_no_and_edition(
    collection_no: str | None, edition: Edition | None
) -> None:
    if collection_no is None and edition is None:
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
                    raise typer.Exit

    if collection_no is not None and edition is not None:
        msg = "Provide either --collection-no or --edition not both."
        raise typer.BadParameter(msg)


@app.command(name="tripleS")
def tripleS(  # noqa: N802
    season: Annotated[
        TripleSSeason, typer.Argument(case_sensitive=False, help=SEASON_HELP_TEXT)
    ],
    collection_no: Annotated[
        str | None, typer.Option(help=COLLECTION_NO_HELP_TEXT)
    ] = None,
    edition: Annotated[Edition | None, typer.Option(help=EDITION_HELP_TEXT)] = None,
    full: Annotated[bool, typer.Option(help=FULL_STATISTICS_HELP_TEXT)] = False,
    output: Annotated[
        StatsOutput, typer.Option(case_sensitive=False, help=OUTPUT_HELP_TEXT)
    ] = StatsOutput.TERM,
) -> None:
    _validate_collection_no_and_edition(collection_no, edition)
    asyncio.run(
        default_objekt_service.get_objekt_sales_stats(
            artist=Artist.TRIPLES,
            season=season,
            collection_no=collection_no or (edition and edition.collection_no),
            show_full_stats=full,
            output=output,
        )
    )


@app.command()
def artms(
    season: Annotated[
        ArtmsSeason, typer.Argument(case_sensitive=False, help=SEASON_HELP_TEXT)
    ],
    collection_no: Annotated[
        str | None, typer.Option(help=COLLECTION_NO_HELP_TEXT)
    ] = None,
    edition: Annotated[Edition | None, typer.Option(help=EDITION_HELP_TEXT)] = None,
    full: Annotated[bool, typer.Option(help=FULL_STATISTICS_HELP_TEXT)] = False,
    output: Annotated[
        StatsOutput, typer.Option(case_sensitive=False, help=OUTPUT_HELP_TEXT)
    ] = StatsOutput.TERM,
) -> None:
    _validate_collection_no_and_edition(collection_no, edition)
    asyncio.run(
        default_objekt_service.get_objekt_sales_stats(
            artist=Artist.ARTMS,
            season=season,
            collection_no=collection_no or (edition and edition.collection_no),
            show_full_stats=full,
            output=output,
        )
    )


@app.command()
def idntt(
    season: Annotated[
        IdnttSeason, typer.Argument(case_sensitive=False, help=SEASON_HELP_TEXT)
    ],
    collection_no: Annotated[
        str | None, typer.Option(help=COLLECTION_NO_HELP_TEXT)
    ] = None,
    full: Annotated[bool, typer.Option(help=FULL_STATISTICS_HELP_TEXT)] = False,
    output: Annotated[
        StatsOutput, typer.Option(case_sensitive=False, help=OUTPUT_HELP_TEXT)
    ] = StatsOutput.TERM,
) -> None:
    asyncio.run(
        default_objekt_service.get_objekt_sales_stats(
            artist=Artist.IDNTT,
            season=season,
            collection_no=collection_no,
            show_full_stats=full,
            output=output,
        )
    )
