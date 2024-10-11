
from . import db
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'  

    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(255), unique=True, nullable=False)  
    password = db.Column(db.String(255), nullable=False)  

    def set_password(self, password):
        """Hashes the password and sets it."""
        hashed_password = generate_password_hash(password).decode('utf-8')
        print(f"Setting password for {self.username}: {hashed_password}")  
        self.password = hashed_password

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        print(f"Checking password for {self.username}")  
        return check_password_hash(self.password, password)


class ImageMeta(db.Model):
    __tablename__ = 'image_meta'  

    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    filename = db.Column(db.String(255), nullable=False)  
    url = db.Column(db.String(255), nullable=False)  
    upload_date = db.Column(db.DateTime, server_default=db.func.now())  

    user = db.relationship('User', backref=db.backref('images', lazy=True))  


