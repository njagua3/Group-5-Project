from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from extensions import db
from models import Tenant, Landlord, Property, User
from flask_bcrypt import Bcrypt

app = Flask(_name_)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

# Helper function to serialize model instances
def serialize(model_instance):
    return {c.name: getattr(model_instance, c.name) for c in model_instance._table_.columns}

# Authentication Routes
@app.route('/signup', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists!'}), 400

    user = User(username=username, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password!'}), 401

    access_token = create_access_token(identity={'username': user.username, 'role': user.role})
    return jsonify(access_token=access_token)

# Authorization Helpers
def landlord_required():
    identity = get_jwt_identity()
    if identity['role'] != 'landlord':
        abort(403, description="Access forbidden: Landlords only.")

def tenant_required():
    identity = get_jwt_identity()
    if identity['role'] != 'tenant':
        abort(403, description="Access forbidden: Tenants only.")

# Tenant Routes
@app.route('/tenants', methods=['GET'])
@jwt_required()
def get_tenants():
    tenant_required()
    identity = get_jwt_identity()
    tenants = Tenant.query.filter_by(user_id=User.query.filter_by(username=identity['username']).first().id).all()
    return jsonify([serialize(tenant) for tenant in tenants])

@app.route('/tenants/<int:id>', methods=['GET'])
@jwt_required()
def get_tenant(id):
    tenant_required()
    tenant = Tenant.query.get(id)
    if not tenant or tenant.user.username != get_jwt_identity()['username']:
        return jsonify({'error': 'Tenant not found or access forbidden!'}), 404
    return jsonify(serialize(tenant))

@app.route('/tenants/<int:id>/rent', methods=['PUT'])
@jwt_required()
def update_rent(id):
    tenant_required()
    tenant = Tenant.query.get(id)
    if not tenant or tenant.user.username != get_jwt_identity()['username']:
        return jsonify({'error': 'Tenant not found or access forbidden!'}), 404
    
    data = request.get_json()
    tenant.rent_amount = data['rent_amount']
    db.session.commit()
    return jsonify({'message': 'Tenant rent updated successfully!'})

# Landlord Routes
@app.route('/landlords', methods=['GET'])
@jwt_required()
def get_landlords():
    landlord_required()
    landlords = Landlord.query.all()
    return jsonify([serialize(landlord) for landlord in landlords])

@app.route('/landlords/<int:id>', methods=['GET'])
@jwt_required()
def get_landlord(id):
    landlord_required()
    landlord = Landlord.query.get(id)
    if landlord is None:
        return jsonify({'error': 'Landlord not found!'}), 404
    return jsonify(serialize(landlord))

# Property Routes
@app.route('/properties', methods=['GET'])
@jwt_required()
def get_properties():
    landlord_required()
    properties = Property.query.all()
    return jsonify([serialize(property) for property in properties])

@app.route('/properties/<int:id>', methods=['GET'])
@jwt_required()
def get_property(id):
    landlord_required()
    property = Property.query.get(id)
    if property is None:
        return jsonify({'error': 'Property not found!'}), 404
    return jsonify(serialize(property))

if _name_ == '_main_':
    app.run(port=5555, debug=True)