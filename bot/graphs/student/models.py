from typing import Optional, Any

from attr import dataclass


@dataclass
class Student:
    id: str
    first_name: str
    last_name: str
    class_number: Optional[int]
    table_link: Optional[str]

    @classmethod
    def parse_dict(cls, data: dict[str, Any]) -> "Student":
        student = cls(
            id=data["id"],
            first_name=data["firstName"],
            last_name=data["lastName"],
            class_number=data["classNumber"],
            table_link=data["tableLink"]
        )

        return student
