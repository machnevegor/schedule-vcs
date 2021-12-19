import strawberry

from schedule.loader import schedule_loader
from schedule.searcher import find_schedule
from schedule.types import Schedule
from utils.scalars import OID


@strawberry.type
class Query:
    @strawberry.field(description="Get schedule data using its OID.")
    async def schedule(self, schedule_id: OID) -> Schedule:
        return await schedule_loader.load(schedule_id)

    @strawberry.field(description="Find the student's current schedule.")
    async def find_schedule(self, student_id: OID) -> Schedule:
        return await find_schedule(student_id)
