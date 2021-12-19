from typing import NewType

import strawberry
from bson import ObjectId

OID = strawberry.scalar(
    NewType("OID", ObjectId),
    serialize=str,
    parse_value=ObjectId
)
