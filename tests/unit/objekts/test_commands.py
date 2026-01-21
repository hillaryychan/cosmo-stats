from typing import Any
from unittest.mock import MagicMock

import pytest
from click.testing import Result
from pytest_mock.plugin import MockerFixture
from typer.testing import CliRunner

from cosmo_stats.enums.artms import ArtmsMember, ArtmsSeason
from cosmo_stats.enums.cli import StatsOutput
from cosmo_stats.enums.cosmo import Edition
from cosmo_stats.enums.idntt import IdnttMember, IdnttSeason
from cosmo_stats.enums.triples import TripleSMember, TripleSSeason
from cosmo_stats.main import app
from cosmo_stats.objekts.service import ObjektService

runner = CliRunner()


class TestTripleSObjektsCommand:
    @staticmethod
    def _invoke(*args: Any, **kwargs: Any) -> Result:
        return runner.invoke(app, ["objekts", "tripleS", *args], **kwargs)

    @pytest.fixture(autouse=True)
    def mock_objekt_service(self, mocker: MockerFixture) -> MagicMock:
        return mocker.patch(
            "cosmo_stats.objekts.commands.default_objekt_service", spec=ObjektService
        )

    def test_invoke_with_collection_no(self, mock_objekt_service: MagicMock) -> None:
        result = self._invoke(TripleSSeason.ATOM01.value, "--collection-no", "100z")
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=TripleSMember,
            season=TripleSSeason.ATOM01,
            collection_no=["100Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize(
        "collection_no", ["101z,102z,103z,104z", " 101z, 102z, 103z, 104z "]
    )
    def test_invoke_with_collection_no_comma_separated(
        self, collection_no: str, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            TripleSSeason.ATOM01.value, "--collection-no", collection_no
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=TripleSMember,
            season=TripleSSeason.ATOM01,
            collection_no=["101Z", "102Z", "103Z", "104Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    def test_invoke_with_multiple_collection_no(
        self, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            TripleSSeason.ATOM01.value,
            "--collection-no",
            "101z",
            "--collection-no",
            " 102z",
            "--collection-no",
            "103z ",
            "--collection-no",
            " 104z ",
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=TripleSMember,
            season=TripleSSeason.ATOM01,
            collection_no=["101Z", "102Z", "103Z", "104Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    def test_invoke_with_collection_no_sorted(
        self, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            TripleSSeason.ATOM01.value,
            "--collection-no",
            "104z,102z,103z",
            "--collection-no",
            "101z",
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=TripleSMember,
            season=TripleSSeason.ATOM01,
            collection_no=["101Z", "102Z", "103Z", "104Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("season", list(TripleSSeason))
    def test_invoke_with_season(
        self, season: TripleSSeason, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(season.value, "--collection-no", "100z")
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=TripleSMember,
            season=season,
            collection_no=["100Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("edition", list(Edition))
    def test_invoke_with_edition(
        self, edition: Edition, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(TripleSSeason.ATOM01.value, "--edition", edition.value)
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=TripleSMember,
            season=TripleSSeason.ATOM01,
            collection_no=edition.collection_no,
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    def test_invoke_with_collection_no_and_edition(
        self, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            TripleSSeason.ATOM01.value, "--collection-no", "100z", "--edition", 1
        )
        assert result.exit_code == 0

        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=TripleSMember,
            season=TripleSSeason.ATOM01,
            collection_no=[
                "100Z",
                "101Z",
                "102Z",
                "103Z",
                "104Z",
                "105Z",
                "106Z",
                "107Z",
                "108Z",
            ],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("input_value", ["YES", "yes", " yEs ", "Y", "y"])
    def test_invoke_with_no_collection_no_or_edition_confirms_action(
        self, input_value: str, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(TripleSSeason.ATOM01.value, input=input_value)
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=TripleSMember,
            season=TripleSSeason.ATOM01,
            collection_no=None,
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("input_value", ["No", "no", " nO ", "N", "n", "\n", " "])
    def test_invoke_with_no_collection_no_or_edition_does_not_confirm_action(
        self, input_value: str, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(TripleSSeason.ATOM01.value, input=input_value)
        assert result.exit_code == 0, result.output
        mock_objekt_service.get_objekt_sales_stats.assert_not_called()

    def test_invoke_with_full_stats(self, mock_objekt_service: MagicMock) -> None:
        result = self._invoke(
            TripleSSeason.ATOM01.value, "--collection-no", "100Z", "--full"
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=TripleSMember,
            season=TripleSSeason.ATOM01,
            collection_no=["100Z"],
            show_full_stats=True,
            output=StatsOutput.TERM,
        )

    def test_invoke_with_explicit_no_full_stats(
        self, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            TripleSSeason.ATOM01.value, "--collection-no", "100Z", "--no-full"
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=TripleSMember,
            season=TripleSSeason.ATOM01,
            collection_no=["100Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("stats_output", list(StatsOutput))
    def test_invoke_with_stats_output(
        self, stats_output: StatsOutput, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            TripleSSeason.ATOM01.value,
            "--collection-no",
            "100Z",
            "--output",
            stats_output.value,
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=TripleSMember,
            season=TripleSSeason.ATOM01,
            collection_no=["100Z"],
            show_full_stats=False,
            output=stats_output,
        )

    def test_invalid_season(self) -> None:
        result = self._invoke("season01")
        assert result.exit_code == 2
        assert "'season01' is not one of" in result.output


class TestArtmsObjektsCommand:
    @staticmethod
    def _invoke(*args: Any, **kwargs: Any) -> Result:
        return runner.invoke(app, ["objekts", "artms", *args], **kwargs)

    @pytest.fixture(autouse=True)
    def mock_objekt_service(self, mocker: MockerFixture) -> MagicMock:
        return mocker.patch(
            "cosmo_stats.objekts.commands.default_objekt_service", spec=ObjektService
        )

    def test_invoke_with_collection_no(self, mock_objekt_service: MagicMock) -> None:
        result = self._invoke(ArtmsSeason.ATOM01.value, "--collection-no", "100z")
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=ArtmsMember,
            season=ArtmsSeason.ATOM01,
            collection_no=["100Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    def test_invoke_with_collection_no_sorted(
        self, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            ArtmsSeason.ATOM01.value,
            "--collection-no",
            "104z,102z,103z",
            "--collection-no",
            "101z",
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=ArtmsMember,
            season=ArtmsSeason.ATOM01,
            collection_no=["101Z", "102Z", "103Z", "104Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize(
        "collection_no", ["101z,102z,103z,104z", " 101z, 102z, 103z, 104z "]
    )
    def test_invoke_with_collection_no_comma_separated(
        self, collection_no: str, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            ArtmsSeason.ATOM01.value, "--collection-no", collection_no
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=ArtmsMember,
            season=ArtmsSeason.ATOM01,
            collection_no=["101Z", "102Z", "103Z", "104Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    def test_invoke_with_multiple_collection_no(
        self, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            ArtmsSeason.ATOM01.value,
            "--collection-no",
            "101z",
            "--collection-no",
            " 102z",
            "--collection-no",
            "103z ",
            "--collection-no",
            " 104z ",
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=ArtmsMember,
            season=ArtmsSeason.ATOM01,
            collection_no=["101Z", "102Z", "103Z", "104Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("season", list(ArtmsSeason))
    def test_invoke_with_season(
        self, season: ArtmsSeason, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(season.value, "--collection-no", "100z")
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=ArtmsMember,
            season=season,
            collection_no=["100Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("edition", list(Edition))
    def test_invoke_with_edition(
        self, edition: Edition, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(ArtmsSeason.ATOM01.value, "--edition", edition.value)
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=ArtmsMember,
            season=ArtmsSeason.ATOM01,
            collection_no=edition.collection_no,
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    def test_invoke_with_collection_no_and_edition(
        self, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            ArtmsSeason.ATOM01.value, "--collection-no", "100z", "--edition", 1
        )
        assert result.exit_code == 0

        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=ArtmsMember,
            season=ArtmsSeason.ATOM01,
            collection_no=[
                "100Z",
                "101Z",
                "102Z",
                "103Z",
                "104Z",
                "105Z",
                "106Z",
                "107Z",
                "108Z",
            ],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("input_value", ["YES", "yes", " yEs ", "Y", "y"])
    def test_invoke_with_no_collection_no_or_edition_confirms_action(
        self, input_value: str, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(ArtmsSeason.ATOM01.value, input=input_value)
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=ArtmsMember,
            season=ArtmsSeason.ATOM01,
            collection_no=None,
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("input_value", ["No", "no", " nO ", "N", "n", "\n", " "])
    def test_invoke_with_no_collection_no_or_edition_does_not_confirm_action(
        self, input_value: str, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(ArtmsSeason.ATOM01.value, input=input_value)
        assert result.exit_code == 0, result.output
        mock_objekt_service.get_objekt_sales_stats.assert_not_called()

    def test_invoke_with_full_stats(self, mock_objekt_service: MagicMock) -> None:
        result = self._invoke(
            ArtmsSeason.ATOM01.value, "--collection-no", "100Z", "--full"
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=ArtmsMember,
            season=ArtmsSeason.ATOM01,
            collection_no=["100Z"],
            show_full_stats=True,
            output=StatsOutput.TERM,
        )

    def test_invoke_with_explicit_no_full_stats(
        self, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            ArtmsSeason.ATOM01.value, "--collection-no", "100Z", "--no-full"
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=ArtmsMember,
            season=ArtmsSeason.ATOM01,
            collection_no=["100Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("stats_output", list(StatsOutput))
    def test_invoke_with_stats_output(
        self, stats_output: StatsOutput, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            ArtmsSeason.ATOM01.value,
            "--collection-no",
            "100Z",
            "--output",
            stats_output.value,
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=ArtmsMember,
            season=ArtmsSeason.ATOM01,
            collection_no=["100Z"],
            show_full_stats=False,
            output=stats_output,
        )

    def test_invalid_season(self) -> None:
        result = self._invoke("season01")
        assert result.exit_code == 2
        assert "Invalid value for 'SEASON" in result.output


class TestIdnttObjektsCommand:
    @staticmethod
    def _invoke(*args: Any, **kwargs: Any) -> Result:
        return runner.invoke(app, ["objekts", "idntt", *args], **kwargs)

    @pytest.fixture(autouse=True)
    def mock_objekt_service(self, mocker: MockerFixture) -> MagicMock:
        return mocker.patch(
            "cosmo_stats.objekts.commands.default_objekt_service", spec=ObjektService
        )

    def test_invoke_with_collection_no(self, mock_objekt_service: MagicMock) -> None:
        result = self._invoke(IdnttSeason.SPRING25.value, "--collection-no", "100z")
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=IdnttMember,
            season=IdnttSeason.SPRING25,
            collection_no=["100Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize(
        "collection_no", ["101z,102z,103z,104z", " 101z, 102z, 103z, 104z "]
    )
    def test_invoke_with_collection_no_comma_separated(
        self, collection_no: str, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            IdnttSeason.SPRING25.value, "--collection-no", collection_no
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=IdnttMember,
            season=IdnttSeason.SPRING25,
            collection_no=["101Z", "102Z", "103Z", "104Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    def test_invoke_with_multiple_collection_no(
        self, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            IdnttSeason.SPRING25.value,
            "--collection-no",
            "101z",
            "--collection-no",
            " 102z",
            "--collection-no",
            "103z ",
            "--collection-no",
            " 104z ",
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=IdnttMember,
            season=IdnttSeason.SPRING25,
            collection_no=["101Z", "102Z", "103Z", "104Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    def test_invoke_with_collection_no_sorted(
        self, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            IdnttSeason.SPRING25.value,
            "--collection-no",
            "104z,102z,103z",
            "--collection-no",
            "101z",
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=IdnttMember,
            season=IdnttSeason.SPRING25,
            collection_no=["101Z", "102Z", "103Z", "104Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("season", list(IdnttSeason))
    def test_invoke_with_season(
        self, season: IdnttSeason, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(season.value, "--collection-no", "100z")
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=IdnttMember,
            season=season,
            collection_no=["100Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("input_value", ["YES", "yes", " yEs ", "Y", "y"])
    def test_invoke_with_no_collection_no_confirms_action(
        self, input_value: str, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(IdnttSeason.SPRING25.value, input=input_value)
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=IdnttMember,
            season=IdnttSeason.SPRING25,
            collection_no=None,
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("input_value", ["No", "no", " nO ", "N", "n", "\n", " "])
    def test_invoke_with_no_collection_no_does_not_confirm_action(
        self, input_value: str, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(IdnttSeason.SPRING25.value, input=input_value)
        assert result.exit_code == 0, result.output
        mock_objekt_service.get_objekt_sales_stats.assert_not_called()

    def test_invoke_with_full_stats(self, mock_objekt_service: MagicMock) -> None:
        result = self._invoke(
            IdnttSeason.SPRING25.value, "--collection-no", "100Z", "--full"
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=IdnttMember,
            season=IdnttSeason.SPRING25,
            collection_no=["100Z"],
            show_full_stats=True,
            output=StatsOutput.TERM,
        )

    def test_invoke_with_explicit_no_full_stats(
        self, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            IdnttSeason.SPRING25.value, "--collection-no", "100Z", "--no-full"
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=IdnttMember,
            season=IdnttSeason.SPRING25,
            collection_no=["100Z"],
            show_full_stats=False,
            output=StatsOutput.TERM,
        )

    @pytest.mark.parametrize("stats_output", list(StatsOutput))
    def test_invoke_with_stats_output(
        self, stats_output: StatsOutput, mock_objekt_service: MagicMock
    ) -> None:
        result = self._invoke(
            IdnttSeason.SPRING25.value,
            "--collection-no",
            "100Z",
            "--output",
            stats_output.value,
        )
        assert result.exit_code == 0
        mock_objekt_service.get_objekt_sales_stats.assert_called_once_with(
            member_enum_cls=IdnttMember,
            season=IdnttSeason.SPRING25,
            collection_no=["100Z"],
            show_full_stats=False,
            output=stats_output,
        )

    def test_invalid_season(self) -> None:
        result = self._invoke("season01")
        assert result.exit_code == 2
        assert "Invalid value for 'SEASON" in result.output
