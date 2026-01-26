from json import JSONDecodeError
from typing import Any, TypeVar
from urllib.parse import urlencode, urljoin

from httpx import AsyncClient, HTTPError
from pydantic import BaseModel, ValidationError

from cosmo_stats.clients.models import ObjektCollectionMetadata

T = TypeVar("T", bound=BaseModel)


class ApolloClientError(Exception):
    pass


class ApolloApiClient:
    DEFAULT_TIMEOUT = 30.0

    def __init__(self, client: AsyncClient | None = None) -> None:
        self._client = client or AsyncClient(timeout=self.DEFAULT_TIMEOUT)

    @property
    def base_url(self) -> str:
        return "https://apollo.cafe"

    def _url(self, *paths: str, **query_params: Any) -> str:
        path = "/".join(paths)
        if query_params:
            non_empty_queries = {k: v for k, v in query_params.items() if v is not None}
            queries = urlencode(non_empty_queries)
            path = f"{path}?{queries}"
        return urljoin(self.base_url, path)

    async def _request(
        self, method: str, url: str, response_model: type[T], *args: Any, **kwargs: Any
    ) -> T:
        try:
            response = await self._client.request(method, url, *args, **kwargs)
            response.raise_for_status()
        except HTTPError as exc:
            msg = f"HTTP Exception for {exc.request.url} - {exc}"
            raise ApolloClientError(msg) from exc

        try:
            data = response.json()
            return response_model(**data)
        except (JSONDecodeError, ValidationError) as exc:
            msg = (
                f"Failed to parse {url} response "
                f"to model '{response_model.__name__}': {exc}"
            )
            raise ApolloClientError(msg) from exc

    async def get_objekt_collection_metadata(
        self, slug: str
    ) -> ObjektCollectionMetadata:
        url = self._url("api", "objekts", "metadata", slug)
        return await self._request("GET", url, ObjektCollectionMetadata)


default_apollo_api_client = ApolloApiClient()
