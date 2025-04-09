from typing import Any
from urllib.parse import urlencode, urljoin

from httpx import AsyncClient

from cosmo_stats.clients.models import ObjektCollectionMetadata, ObjektList
from cosmo_stats.enums import Artist, Season


class ApolloApiClient:
    DEFAULT_TIMEOUT = 30.0

    def __init__(self) -> None:
        self._client = AsyncClient(timeout=self.DEFAULT_TIMEOUT)

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

    async def get_objekts(
        self, artist: Artist, season: Season, collection_no: str | None, page: int = 0
    ) -> ObjektList:
        url = self._url(
            "api",
            "objekts",
            sort="newest",
            artist=artist,
            season=season,
            collectionNo=collection_no,
            page=page,
        )
        resp = await self._client.get(url)
        data = resp.json()
        return ObjektList.model_validate(data)

    async def get_objekt_collection_metadata(
        self, slug: str
    ) -> ObjektCollectionMetadata:
        url = self._url("api", "objekts", "metadata", slug)
        resp = await self._client.get(url)
        data = resp.json()
        return ObjektCollectionMetadata.model_validate(data)


default_apollo_api_client = ApolloApiClient()
