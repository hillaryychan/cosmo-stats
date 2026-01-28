from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)


class ObjektCollectionMetadata(ApiModel):
    total: Decimal
    transferable: Decimal
    percentage: Decimal
