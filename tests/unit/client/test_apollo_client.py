from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient, Response

from cosmo_stats.clients.apollo_client import ApolloApiClient, ApolloClientError
from cosmo_stats.clients.models import ObjektCollectionMetadata


@pytest.fixture
def mock_response() -> AsyncMock:
    return MagicMock(spec=Response)


@pytest.fixture
def mock_client(mock_response: MagicMock) -> AsyncMock:
    mock = AsyncMock(spec=AsyncClient)
    mock.request.return_value = mock_response
    return mock


@pytest.fixture
def sut(mock_client: AsyncMock) -> ApolloApiClient:
    return ApolloApiClient(mock_client)


class TestApolloApiClient:
    @pytest.mark.asyncio
    async def test_get_objekt_collection_metadata(
        self, sut: ApolloApiClient, mock_response: MagicMock
    ) -> None:
        data = {
            "total": "1000",
            "transferable": "999",
            "percentage": "99.9",
        }
        mock_response.json.return_value = data

        res = await sut.get_objekt_collection_metadata("season-member-collection")

        assert isinstance(res, ObjektCollectionMetadata)
        assert res.total == Decimal(data["total"])
        assert res.transferable == Decimal(data["transferable"])
        assert res.percentage == Decimal(data["percentage"])

    @pytest.mark.asyncio
    async def test_get_objekt_collection_metadata_raises_on_http_error(
        self, sut: ApolloApiClient, mock_response: MagicMock
    ) -> None:
        mock_response.status = 400

        with pytest.raises(ApolloClientError):
            await sut.get_objekt_collection_metadata("season-member-collection")

    @pytest.mark.asyncio
    async def test_get_objekt_collection_metadata_raises_on_validation_error(
        self, sut: ApolloApiClient, mock_response: MagicMock
    ) -> None:
        data = {"key": "value"}
        mock_response.json.return_value = data

        with pytest.raises(ApolloClientError):
            await sut.get_objekt_collection_metadata("season-member-collection")
