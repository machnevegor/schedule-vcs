from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError


class MongoClient(AsyncIOMotorClient):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()

        if isinstance(exc_val, ServerSelectionTimeoutError):
            raise Exception("No connection to the database!")
