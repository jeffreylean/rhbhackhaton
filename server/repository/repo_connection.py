import motor.motor_asyncio
import os

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_CONN"))
db = client.AutoCred
form_collection = db.get_collection("form_collection")
configuration_collection = db.get_collection("configuration_collection")
