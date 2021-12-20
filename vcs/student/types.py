from typing import Optional, Any

import strawberry

from utils.scalars import OID


@strawberry.type
class Student:
    id: OID
    first_name: str
    last_name: str
    class_number: Optional[int]
    table_link: Optional[str]

    @classmethod
    def parse_dict(cls, data: dict[str, Any]) -> "Student":
        student = cls(
            id=data["_id"],
            first_name=data["firstName"],
            last_name=data["lastName"],
            class_number=data["classNumber"],
            table_link=data["tableLink"]
        )

        return student
