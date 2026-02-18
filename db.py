from flask_sqlalchemy import SQLAlchemy
import enum

# Don't initialize the db here directly, just declare it
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)

# Enum for gender
class GenderEnum(enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

# Models will be defined here, if needed
class User(db.Model):
    """User model."""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum(GenderEnum))
    weight = db.Column(db.Float)
    blood_group = db.Column(db.String(5))
    location = db.Column(db.String(256))
    
    # Relationship with Activity table
    activities = db.relationship('Activity', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}, {self.email}>'

class Activity(db.Model):
    """Activity model."""
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_filename = db.Column(db.String(128), nullable=False)
    question_data = db.Column(db.JSON, nullable=True)  # Can be None initially
    disease = db.Column(db.String(64))
    accuracy = db.Column(db.Float)
    recommended_solution = db.Column(db.String(256))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))  # ForeignKey reference
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))  # ForeignKey reference
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    doctor = db.relationship('Doctor', backref='activities', lazy=True)
    product = db.relationship('Product', backref='activities', lazy=True)

    def __repr__(self):
        return f'<Activity {self.id}, Disease: {self.disease}>'

        
class Doctor(db.Model):
    """Doctor model."""
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address = db.Column(db.String(256))

    def __repr__(self):
        return f'<Doctor {self.name}, {self.address}>'

class Product(db.Model):
    """Product model."""
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    link = db.Column(db.String(256))

    def __repr__(self):
        return f'<Product {self.name}, {self.link}>'
