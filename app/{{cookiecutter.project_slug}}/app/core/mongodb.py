import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError

class MongoDB:
    def __init__(self, database_uri: str, database_name):
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
            self.client = None
            self.db = None
            raise

    async def find(self, collection, filters: dict, multiple=False):
        try:
            if not multiple:
                return await self.db[collection].find_one(filters)
            # if multiple, await while iteration
            return self.db[collection].find(filters)
        except Exception:
            raise

    async def insert(self, collection, content):
        try:
            if isinstance(content, list):
                await self.db[collection].insert_many(content)
            if isinstance(content, dict):
                await self.db[collection].insert_one(content)
        except DuplicateKeyError:
            print("Item already exists")
            pass
        except Exception as e:
            raise e

async def get_mongo_instance() -> MongoDB:
    from main import app

    return app.state.mongo