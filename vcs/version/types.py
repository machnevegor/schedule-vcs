from asyncio import gather
from typing import Any

import strawberry

from schedule.loader import schedule_loader
from schedule.types import Schedule
from student.loader import student_loader
from student.types import Student
from utils.scalars import OID


@strawberry.type
class Version:
    id: OID

    @strawberry.field
    async def schedule(self) -> Schedule:
        return await schedule_loader.load(self.schedule_)

    @strawberry.field
    async def owners(self) -> list[Student]:
        owners = []

        if self.owners_:
            owners += await gather(*(
                student_loader.load(student_id)
                for student_id in self.owners_))

        return owners

    @classmethod
    def parse_dict(cls, data: dict[str, Any]) -> "Version":
        version = cls(
            id=data["_id"]
        )

        version.schedule_ = data["schedule"]
        version.owners_ = data["owners"]

        return version
