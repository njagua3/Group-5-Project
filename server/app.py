from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db  # Import db from extensions
from models import Tenant, Landlord, Property

app = Flask(__name__)


# Add configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'


db.init_app(app)  # Initialize the app with db
migrate = Migrate(app, db)
CORS(app)

# Helper function to serialize model instances
def serialize(model_instance):
    return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}

# Tenant Routes
@app.route('/tenants', methods=['GET', 'POST'])
def tenants():
    if request.method == 'POST':
        data = request.get_json()
        new_tenant = Tenant(
            name=data['name'],
            rent_amount=data['rent_amount'],
            room_number=data['room_number'],
            property_id=data['property_id']
        )
        db.session.add(new_tenant)
        db.session.commit()
        return jsonify({'message': 'Tenant added!'}), 201
    
    tenants = Tenant.query.all()
    return jsonify([serialize(tenant) for tenant in tenants])

@app.route('/tenants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def tenant(id):
    tenant = Tenant.query.get(id)
    if tenant is None:
        return jsonify({'error': 'Tenant not found!'}), 404
    
    if request.method == 'PUT':
        data = request.get_json()
        tenant.name = data['name']
        tenant.rent_amount = data['rent_amount']
        tenant.room_number = data['room_number']
        db.session.commit()
        return jsonify({'message': 'Tenant updated!'})
    
    elif request.method == 'DELETE':
        db.session.delete(tenant)
        db.session.commit()
        return jsonify({'message': 'Tenant deleted!'})
    
    return jsonify(serialize(tenant))


# Landlord Routes
@app.route('/landlords', methods=['GET', 'POST'])
def landlords():
    if request.method == 'POST':
        data = request.get_json()
        new_landlord = Landlord(name=data['name'])
        db.session.add(new_landlord)
        db.session.commit()
        return jsonify({'message': 'Landlord added!'}), 201
    
    landlords = Landlord.query.all()
    return jsonify([serialize(landlord) for landlord in landlords])

@app.route('/landlords/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def landlord(id):
    landlord = Landlord.query.get(id)
    if landlord is None:
        return jsonify({'error': 'Landlord not found!'}), 404
    
    if request.method == 'PUT':
        data = request.get_json()
        landlord.name = data['name']
        db.session.commit()
        return jsonify({'message': 'Landlord updated!'})
    
    elif request.method == 'DELETE':
        db.session.delete(landlord)
        db.session.commit()
        return jsonify({'message': 'Landlord deleted!'})
    
    return jsonify(serialize(landlord))


# Property Routes
@app.route('/properties', methods=['GET', 'POST'])
def properties():
    if request.method == 'POST':
        data = request.get_json()
        new_property = Property(
            name=data['name'],
            landlord_id=data['landlord_id']
        )
        db.session.add(new_property)
        db.session.commit()
        return jsonify({'message': 'Property added!'}), 201
    
    properties = Property.query.all()
    return jsonify([serialize(property) for property in properties])

@app.route('/properties/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def property(id):
    property = Property.query.get(id)
    if property is None:
        return jsonify({'error': 'Property not found!'}), 404
    
    if request.method == 'PUT':
        data = request.get_json()
        property.name = data['name']
        property.landlord_id = data['landlord_id']
        db.session.commit()
        return jsonify({'message': 'Property updated!'})
    
    elif request.method == 'DELETE':
        db.session.delete(property)
        db.session.commit()
        return jsonify({'message': 'Property deleted!'})
    
    return jsonify(serialize(property))

# Rent Payment Route
@app.route('/tenants/<int:id>/rent', methods=['PUT'])
def update_rent(id):
    tenant = Tenant.query.get(id)
    if tenant is None:
        return jsonify({'error': 'Tenant not found!'}), 404
    
    data = request.get_json()
    tenant.rent_amount = data['rent_amount']
    db.session.commit()
    return jsonify({'message': 'Tenant rent updated successfully!'})


if __name__ == '__main__':
    app.run(port=5555, debug=True)