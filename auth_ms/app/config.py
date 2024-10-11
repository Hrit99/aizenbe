 

import os


print(os.environ.get('DATABASE_URL'))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
SQLALCHEMY_TRACK_MODIFICATIONS = False


JWT_SECRET_KEY = os.getenv ('JWT_SECRET_KEY')  
