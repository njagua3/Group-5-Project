from app import app, db
from faker import Faker
from models import Tenant, Landlord, Property

faker = Faker()

def seed_data():
    # Create a landlord
    landlord1 = Landlord(name=faker.name())
    db.session.add(landlord1)
    db.session.commit()

    # Create a property for that landlord
    property1 = Property(name='Property A', landlord_id=landlord1.id)
    db.session.add(property1)
    db.session.commit()

    # Create 10 tenants for that property
    for _ in range(10):
        tenant = Tenant(
            name=faker.name(),
            rent_amount=faker.random_number(digits=4),
            room_number=faker.random_number(digits=3),
            property_id=property1.id
        )
        db.session.add(tenant)
    
    db.session.commit()  # Commit all tenant entries at once

# Ensure that the seeding is run within the Flask app context
if __name__ == "__main__":
    with app.app_context():
        seed_data()