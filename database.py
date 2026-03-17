import motor.motor_asyncio # this library enables async talk with MongoDB
import os # this library enables interaction with OS
from dotenv import load_dotenv # this reads .env files

load_dotenv() # look for .env files and load
MONGO_URL = os.getenv("MONGO_URL") # extract conn string (URL)

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL) # create Client (database cluster)
database = client.taskersky_db # access a database in the cluster
collection = database.tasks # access a specific collection in the database (e.g. tasks for this project)