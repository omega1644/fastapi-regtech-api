# ============================================================
# app/infrastructure/mongo/connection.py
# ============================================================
import motor.motor_asyncio
from beanie import init_beanie
from app.core.config import get_settings
from app.infrastructure.mongo.models import VerificationDoc

settings = get_settings()

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_uri)

db = client[settings.db_name]

async def init_mongo():
    await init_beanie(database=db, document_models=[VerificationDoc])