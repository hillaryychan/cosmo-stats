import asyncio
from typing import Annotated

import typer

from cosmo_stats.enums.artms import ArtmsMember, ArtmsSeason
from cosmo_stats.enums.cli import StatsOutput
from cosmo_stats.enums.cosmo import Artist, Edition
from cosmo_stats.enums.idntt import IdnttMember, IdnttSeason
from cosmo_stats.enums.triples import TripleSMember, TripleSSeason
from cosmo_stats.objekts.service import default_objekt_service

COLLECTION_NO_HELP_TEXT = (
    "The collections to collect data for, e.g. 117Z,118Z,119Z,120Z"
)
EDITION_HELP_TEXT = (
    "The edition to collect data for. There are three editions each season."
)
FULL_STATISTICS_HELP_TEXT = "Show full statistics."
OUTPUT_HELP_TEXT = "Outputs statistics in the provided format."
SEASON_HELP_TEXT = "The season of the objekts."


app = typer.Typer(
    no_args_is_help=True, help="Retrieve objekt statistics for an artist."
)


def _confirm_all_collections() -> None:
    print(
        "No collections provided. "
        "This will collect data for all collections in the season."
    )
    while True:
        confirmation = input("Are you sure you want to do this [y/N]? ")
        match confirmation.lower().strip():
            case "yes" | "y":
                break
            case "no" | "n" | "":
                print("Aborting.")
                raise typer.Exit


def _determine_final_collection_no(
    collection_no: list[str] | None, edition: Edition | None
) -> list[str] | None:
    if collection_no is None and edition is None:
        _confirm_all_collections()
        return None
    edition_collection_no = (
        edition.collection_no
        if edition is not None and edition.collection_no is not None
        else []
    )
    collection_no = collection_no or []
    # remove duplicates and sort in alphanumeric order
    return sorted(set(collection_no + edition_collection_no))


def _parse_collection_nos(values: list[str] | None) -> list[str] | None:
    if values is None:
        return None

    result = []
    for v in values:
        result.extend(v.split(","))
    # prune out empty strings with `if x.strip()`
    return sorted([x.strip().upper() for x in result if x.strip()])


@app.command(name=Artist.TRIPLES.value)
def tripleS(  # noqa: N802
    season: Annotated[
        TripleSSeason, typer.Argument(case_sensitive=False, help=SEASON_HELP_TEXT)
    ],
    collection_no: Annotated[
        list[str] | None,
        typer.Option(callback=_parse_collection_nos, help=COLLECTION_NO_HELP_TEXT),
    ] = None,
    edition: Annotated[Edition | None, typer.Option(help=EDITION_HELP_TEXT)] = None,
    full: Annotated[bool, typer.Option(help=FULL_STATISTICS_HELP_TEXT)] = False,
    output: Annotated[
        StatsOutput, typer.Option(case_sensitive=False, help=OUTPUT_HELP_TEXT)
    ] = StatsOutput.TERM,
) -> None:
    collection_no = _determine_final_collection_no(collection_no, edition)
    asyncio.run(
        default_objekt_service.get_objekt_sales_stats(
            member_enum_cls=TripleSMember,
            season=season,
            collection_no=collection_no,
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
        list[str] | None,
        typer.Option(callback=_parse_collection_nos, help=COLLECTION_NO_HELP_TEXT),
    ] = None,
    edition: Annotated[Edition | None, typer.Option(help=EDITION_HELP_TEXT)] = None,
    full: Annotated[bool, typer.Option(help=FULL_STATISTICS_HELP_TEXT)] = False,
    output: Annotated[
        StatsOutput, typer.Option(case_sensitive=False, help=OUTPUT_HELP_TEXT)
    ] = StatsOutput.TERM,
) -> None:
    collection_no = _determine_final_collection_no(collection_no, edition)
    asyncio.run(
        default_objekt_service.get_objekt_sales_stats(
            member_enum_cls=ArtmsMember,
            season=season,
            collection_no=collection_no,
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
        list[str] | None,
        typer.Option(callback=_parse_collection_nos, help=COLLECTION_NO_HELP_TEXT),
    ] = None,
    full: Annotated[bool, typer.Option(help=FULL_STATISTICS_HELP_TEXT)] = False,
    output: Annotated[
        StatsOutput, typer.Option(case_sensitive=False, help=OUTPUT_HELP_TEXT)
    ] = StatsOutput.TERM,
) -> None:
    if collection_no is None:
        _confirm_all_collections()
    asyncio.run(
        default_objekt_service.get_objekt_sales_stats(
            member_enum_cls=IdnttMember,
            season=season,
            collection_no=collection_no,
            show_full_stats=full,
            output=output,
        )
    )
