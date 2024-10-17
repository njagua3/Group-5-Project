from extensions import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Tenant model representing a tenant in the system
class Tenant(db.Model):
    _tablename_ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    rent_amount = db.Column(db.Float, nullable=False)
    room_number = db.Column(db.String(20))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Link to User account

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'rent_amount': self.rent_amount,
            'room_number': self.room_number,
            'property_id': self.property_id
        }

# Landlord model representing a landlord in the system
class Landlord(db.Model):
    _tablename_ = 'landlords'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    properties = db.relationship('Property', backref='landlord', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Link to User account

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'properties': [property.as_dict() for property in self.properties]
        }

# Property model representing a property in the system
class Property(db.Model):
    _tablename_ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    property_type = db.Column(db.String(50))
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'))
    tenants = db.relationship('Tenant', backref='property', lazy=True)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'property_type': self.property_type,
            'landlord_id': self.landlord_id,
            'tenants': [tenant.as_dict() for tenant in self.tenants]
        }

# User model for authentication
class User(db.Model):
    _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50))  # Either 'landlord' or 'tenant'
    
    tenants = db.relationship('Tenant', backref='user', lazy=True)
    landlords = db.relationship('Landlord', backref='user', lazy=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)