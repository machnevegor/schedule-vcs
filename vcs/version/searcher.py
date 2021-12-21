from pymongo import DESCENDING

from student.loader import student_loader
from utils.config import MONGO_URI, DATABASE_NAME
from utils.mongo import MongoClient
from utils.scalars import OID
from version.types import Version


async def find_version(student_id: OID, cursor: OID, limit: int) -> list[Version]:
    if not await student_loader.load(student_id):
        raise Exception("No student with this OID!")

    versions = []
    async with MongoClient(MONGO_URI) as client:
        version_collection = client[DATABASE_NAME]["versions"]

        filters = {"owners": student_id}
        if cursor:
            filters |= {"_id": {"$lt": cursor}}

        async for version in version_collection.find(
                filters, limit=limit, sort=[("_id", DESCENDING)]):
            versions.append(Version.parse_dict(version))

    return versions
