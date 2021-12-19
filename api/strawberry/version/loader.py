from pymongo import DESCENDING
from strawberry.dataloader import DataLoader

from utils.env import MONGO_URI, DATABASE_NAME
from utils.mongo import MongoClient
from utils.scalars import OID
from version.types import Version


async def load_versions(version_ids: list[OID]) -> list[Version | Exception]:
    versions = []
    async with MongoClient(MONGO_URI) as client:
        version_collection = client[DATABASE_NAME]["versions"]

        for version_id in version_ids:
            version = await version_collection.find_one(
                {"_id": version_id}, sort=[("_id", DESCENDING)])

            if version:
                versions.append(
                    Version.parse_dict(version))
            else:
                versions.append(
                    Exception("No version with this OID!"))

    return versions


version_loader = DataLoader(
    load_fn=load_versions
)
