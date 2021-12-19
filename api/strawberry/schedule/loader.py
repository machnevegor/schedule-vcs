from pymongo import DESCENDING
from strawberry.dataloader import DataLoader

from schedule.types import Schedule
from utils.env import MONGO_URI, DATABASE_NAME
from utils.mongo import MongoClient
from utils.scalars import OID


async def load_schedules(schedule_ids: list[OID]) -> list[Schedule | Exception]:
    schedules = []
    async with MongoClient(MONGO_URI) as client:
        schedule_collection = client[DATABASE_NAME]["schedules"]

        for schedule_id in schedule_ids:
            schedule = await schedule_collection.find_one(
                {"_id": schedule_id}, sort=[("_id", DESCENDING)])

            if schedule:
                schedules.append(
                    Schedule.parse_dict(schedule))
            else:
                schedules.append(
                    Exception("No schedule with this OID!"))

    return schedules


schedule_loader = DataLoader(
    load_fn=load_schedules
)
