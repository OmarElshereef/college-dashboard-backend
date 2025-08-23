from src.utils.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBClient:
    _client: AsyncIOMotorClient = None
    _db = None

    @staticmethod
    def get_client():
        if MongoDBClient._client is None:
            app_settings = get_settings()
            uri = app_settings.MONGO_URI
            db_name = app_settings.MONGO_DB_NAME

            if not uri or not db_name:
                raise ValueError("MONGO_URI and MONGO_DB_NAME must be set")

            MongoDBClient._client = AsyncIOMotorClient(uri)
            MongoDBClient._db = MongoDBClient._client[db_name]

        return MongoDBClient._db
