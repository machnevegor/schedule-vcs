from typing import Optional, Any

import strawberry

from utils.scalars import OID


@strawberry.type
class Lesson:
    number: int
    name: str
    group: Optional[str]
    teacher: Optional[str]
    room: Optional[str]

    @classmethod
    def parse_dict(cls, data: dict[str, Any]) -> "Lesson":
        lesson = cls(
            number=data["number"],
            name=data["name"],
            group=data["group"],
            teacher=data["teacher"],
            room=data["room"]
        )

        return lesson


@strawberry.type
class Day:
    name: str
    lessons: list[Lesson]

    @classmethod
    def parse_dict(cls, data: dict[str, Any]) -> "Day":
        lessons = [
            Lesson.parse_dict(lesson)
            for lesson in data["lessons"]
        ]

        day = cls(
            name=data["name"],
            lessons=lessons
        )

        return day


@strawberry.type
class Schedule:
    id: OID
    days: list[Day]

    @classmethod
    def parse_dict(cls, data: dict[str, Any]) -> "Schedule":
        days = [
            Day.parse_dict(day)
            for day in data["days"]
        ]

        schedule = cls(
            id=data["_id"],
            days=days
        )

        return schedule
