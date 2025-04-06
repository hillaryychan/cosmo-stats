from pydantic import BaseModel

from cosmo_stats.enums import Season, TripleSMember


class ObjektCollectionData(BaseModel):
    season: Season
    member: TripleSMember
    collection_no: str
    total: int
