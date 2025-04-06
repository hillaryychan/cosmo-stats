from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

from cosmo_stats.enums import ObjektClass, Season, TripleSMember


class ApiModel(BaseModel):
    class Config:
        alias_generator = to_camel


class Objekt(ApiModel):
    id: UUID
    slug: str
    collection_id: str
    season: Season
    member: TripleSMember
    collection_no: str
    objekt_class: ObjektClass = Field(alias="class")
    como_amount: int


class ObjektList(ApiModel):
    total: int
    has_next: bool
    next_start_after: int | None = None
    objekts: list[Objekt]


class ObjektMetadataData(ApiModel):
    id: int
    collection_id: str
    description: str


class ObjektMetadata(ApiModel):
    metadata: ObjektMetadataData
    total: str
    transferable: str
    percentage: str
