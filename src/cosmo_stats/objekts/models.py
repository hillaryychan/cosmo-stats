from pydantic import BaseModel

from cosmo_stats.enums import ArtmsMember, Season, TripleSMember


class ObjektCollectionData(BaseModel):
    season: Season
    member: TripleSMember | ArtmsMember
    collection_no: str
    total: int
