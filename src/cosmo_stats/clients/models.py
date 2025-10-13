from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)


class Objekt(ApiModel):
    id: UUID
    slug: str
    collection_id: str
    member: str
    collection_no: str


class ObjektList(ApiModel):
    total: int
    has_next: bool
    next_start_after: int | None = None
    objekts: list[Objekt]


class ObjektMetadata(ApiModel):
    id: int
    collection_id: str
    description: str


class ObjektCollectionMetadata(ApiModel):
    metadata: ObjektMetadata
    total: str
    transferable: str
    percentage: str
