from typing import Annotated, Union

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, DuplicateKeyError


class MongoDB:
    client: AsyncIOMotorClient
    db: AsyncIOMotorDatabase

    def __init__(self, database_uri: str, database_name: str):
        self.database_uri = database_uri
        self.database_name = database_name

        try:
            self.client = AsyncIOMotorClient(
                self.database_uri, serverSelectionTimeoutMS=5000
            )
            self.db = self.client[self.database_name]
        except ConnectionFailure:
            if self.client:
                self.client.close()
            raise

    async def find(self, collection: str, filters: dict, multiple: bool = False):
        try:
            if self.db is None:
                raise ConnectionError("MongoDB is not connected")
            if not multiple:
                return await self.db[collection].find_one(filters)
            return self.db[collection].find(filters)
        except Exception:
            raise

    async def insert(self, collection: str, content: Union[list, dict]):
        try:
            if self.db is None:
                raise ConnectionError("MongoDB is not connected")
            if isinstance(content, list):
                await self.db[collection].insert_many(content)
            elif isinstance(content, dict):
                await self.db[collection].insert_one(content)
        except DuplicateKeyError:
            print("Item already exists")
        except Exception as e:
            raise e


async def get_mongo_instance() -> MongoDB:
    from app.main import app

    mongo: MongoDB = app.state.mongo
    return mongo


SessionDep = Annotated[MongoDB, Depends(get_mongo_instance)]
