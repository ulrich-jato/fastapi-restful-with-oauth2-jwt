import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file from the root directory
# dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv()

class Settings(BaseSettings):
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    database_url:str = os.getenv("DATABASE_URL")

    class Config:
        # env_file = dotenv_path
        env_file_encoding = "utf-8"

settings = Settings()