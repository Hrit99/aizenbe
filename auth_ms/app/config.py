 

import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
SQLALCHEMY_TRACK_MODIFICATIONS = False


JWT_SECRET_KEY = os.getenv ('JWT_SECRET_KEY')  
