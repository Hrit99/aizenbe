import os

class Config:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
