import requests

from cosmo_stats.clients.models import ObjektList, ObjektMetadata

OBJEKTS_PATH = "https://apollo.cafe/api/objekts?artist=tripleS&sort=newest&season={season}&collectionNo={collections}&page={page}"
METADATA_PATH = "https://apollo.cafe/api/objekts/metadata/{slug}"


def fetch_objekts(season: str, collections: list[str], page: int) -> ObjektList:
    path = OBJEKTS_PATH.format(
        season=season, collections=",".join(collections), page=page
    )
    resp = requests.get(path, timeout=30)
    data = resp.json()
    return ObjektList.model_validate(data)


def fetch_objekt_metadata(slug: str) -> ObjektMetadata:
    path = METADATA_PATH.format(slug=slug)
    resp = requests.get(path, timeout=30)
    data = resp.json()
    return ObjektMetadata.model_validate(data)
