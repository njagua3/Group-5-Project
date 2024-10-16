from extensions import db

# Tenant model representing a tenant in the system
class Tenant(db.Model):
    __tablename__ = 'tenants'  # Name of the table in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each tenant
    name = db.Column(db.String(50), nullable=False)  # Name of the tenant
    rent_amount = db.Column(db.Float, nullable=False)  # Monthly rent amount
    room_number = db.Column(db.String(20))  # Room number where the tenant resides
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))  # Reference to the property the tenant occupies

    def as_dict(self):
        # Method to serialize the tenant object into a dictionary
        return {
            'id': self.id,
            'name': self.name,
            'rent_amount': self.rent_amount,
            'room_number': self.room_number,
            'property_id': self.property_id
        }

# Landlord model representing a landlord in the system
class Landlord(db.Model):
    __tablename__ = 'landlords'  # Name of the table in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each landlord
    name = db.Column(db.String(50), nullable=False)  # Name of the landlord
    properties = db.relationship('Property', backref='landlord', lazy=True)  # Relationship to properties owned by the landlord

    def as_dict(self):
        # Method to serialize the landlord object into a dictionary
        return {
            'id': self.id,
            'name': self.name,
            'properties': [property.as_dict() for property in self.properties]  # List of properties associated with the landlord
        }

# Property model representing a property in the system
class Property(db.Model):
    __tablename__ = 'properties'  # Name of the table in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each property
    name = db.Column(db.String(100), nullable=False)  # Name of the property
    property_type = db.Column(db.String(50))  # Type of the property (e.g., apartment, house)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'))  # Reference to the landlord of the property
    tenants = db.relationship('Tenant', backref='property', lazy=True)  # Relationship to tenants living in the property

    def as_dict(self):
        # Method to serialize the property object into a dictionary
        return {
            'id': self.id,
            'name': self.name,
            'property_type': self.property_type,
            'landlord_id': self.landlord_id,
            'tenants': [tenant.as_dict() for tenant in self.tenants]  # List of tenants associated with the property
        }