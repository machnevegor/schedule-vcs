from pymongo import DESCENDING

from schedule.loader import schedule_loader
from schedule.types import Schedule
from student.loader import student_loader
from utils.env import MONGO_URI, DATABASE_NAME
from utils.mongo import MongoClient
from utils.scalars import OID


async def find_schedule(student_id: OID) -> Schedule:
    if not await student_loader.load(student_id):
        raise Exception("No student with this OID!")

    async with MongoClient(MONGO_URI) as client:
        version_collection = client[DATABASE_NAME]["versions"]

        latest_version = await version_collection.find_one(
            {"owners": student_id}, {"schedule"}, sort=[("_id", DESCENDING)])
        schedule = await schedule_loader.load(latest_version["schedule"])

    return schedule
