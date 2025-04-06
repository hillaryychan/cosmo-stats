from pydantic import BaseModel

from cosmo_stats.enums import Season, TripleSMember


class ObjektData(BaseModel):
    season: Season
    member: TripleSMember
    collection_no: str
    total: int
