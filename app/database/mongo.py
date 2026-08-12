from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings


def get_mongo_database() -> AsyncIOMotorDatabase:
    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongodb_url)
    return client[settings.mongodb_database]
