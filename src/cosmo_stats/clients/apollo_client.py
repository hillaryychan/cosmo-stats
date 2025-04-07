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

    async def get_objekts(
        self, artist: Artist, season: Season, collections: list[str], page: int = 0
    ) -> ObjektList:
        resp = await self._client.get(
            f"{self.base_url}/api/objekts?artist={artist}&sort=newest&season={season}&collectionNo={','.join(collections)}&page={page}"
        )
        data = resp.json()
        return ObjektList.model_validate(data)

    async def get_objekt_collection_metadata(
        self, slug: str
    ) -> ObjektCollectionMetadata:
        resp = await self._client.get(f"{self.base_url}/api/objekts/metadata/{slug}")
        data = resp.json()
        return ObjektCollectionMetadata.model_validate(data)


default_apollo_api_client = ApolloApiClient()
