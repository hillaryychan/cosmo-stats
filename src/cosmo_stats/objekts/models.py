from pydantic import BaseModel


class ObjektCollectionData(BaseModel):
    member: str
    collection_no: str
    total: int
