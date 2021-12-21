from os import getenv

from dotenv import load_dotenv

load_dotenv()
MONGO_URI = getenv("MONGO_URI")
DATABASE_NAME = getenv("DATABASE_NAME")
