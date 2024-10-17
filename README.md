# Group-5-project 

# Name: Tenant Management System
This is a Flask-based web application for managing tenants, landlords, and properties. It allows users to add, update, retrieve, and delete information about tenants, landlords, and properties. The application is designed with a RESTful API architecture and uses SQLite as its database.

## Relationships
Tenant to Property: Each tenant is associated with one property (property_id), and a property can have multiple tenants (defined by the tenants relationship in the Property model).

Landlord to Property: Each landlord can own multiple properties (defined by the properties relationship in the Landlord model), but each property is owned by one landlord (landlord_id).


## Database Models
Tenant
id: Unique identifier (Primary Key).
name: Name of the tenant.
rent_amount: Monthly rent amount.
room_number: Room number assigned to the tenant.
property_id: Foreign key referencing the property the tenant resides in.
## Landlord
id: Unique identifier (Primary Key).
name: Name of the landlord.
properties: One-to-Many relationship with Property. A landlord can own multiple properties.
## Property
id: Unique identifier (Primary Key).
name: Name of the property.
property_type: Type of the property (e.g., apartment, house).
landlord_id: Foreign key referencing the landlord of the property.
tenants: One-to-Many relationship with Tenant. A property can have multiple tenants.
## Features
Manage tenants: add, update, retrieve, and delete tenant information.
Manage landlords: add, update, retrieve, and delete landlord information.
Manage properties: add, update, retrieve, and delete property information.
Update tenant rent amounts.


## Technologies Used
1. Python
2. Flask
3. Flask-SQLAlchemy
4. Flask-Migrate
5. Flask-CORS
6. SQLite
7. Faker (for seeding data)

# Installation
1.  the repository:
2. Create a virtual environment
3. Install the required packages
4. Initialize the database:

bash
Copy code
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
Usage
Run the application:
for example you can run: flask run
The application will be accessible at any point specified 

Use an API client (like Postman or cURL) to interact with the endpoints.

## API Endpoints
# Tenants
GET /tenants - Retrieve all tenants.
POST /tenants - Add a new tenant.
GET /tenants/<id> - Retrieve a tenant by ID.
PUT /tenants/<id> - Update a tenant by ID.
DELETE /tenants/<id> - Delete a tenant by ID.
PUT /tenants/<id>/rent - Update the rent amount for a tenant.
# Landlords
GET /landlords - Retrieve all landlords.
POST /landlords - Add a new landlord.
GET /landlords/<id> - Retrieve a landlord by ID.
PUT /landlords/<id> - Update a landlord by ID.
DELETE /landlords/<id> - Delete a landlord by ID.
# Properties
GET /properties - Retrieve all properties.
POST /properties - Add a new property.
GET /properties/<id> - Retrieve a property by ID.
PUT /properties/<id> - Update a property by ID.
DELETE /properties/<id> - Delete a property by ID.


# License
This project is licensed under the MIT License. See the LICENSE file for details.
Feel free to customize any part of this README to better suit your application's details or structure!

# Authors 
Group five