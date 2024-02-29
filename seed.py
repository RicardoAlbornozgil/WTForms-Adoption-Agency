from app import app, db
from models import Pet, Species
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def drop_database():
    logging.info('Dropping existing database...')
    with app.app_context():
        db.reflect()  # Reflect the existing database schema
        db.drop_all()
        db.session.commit()  # Commit the drop_all operation
    logging.info('Database dropped successfully.')

def seed_database():
    # Drop the existing Database
    drop_database()
    
    # Create all tables
    logging.info('Creating tables...')
    with app.app_context():
        db.create_all()
    logging.info('Tables created successfully.')

    # Add species data
    logging.info('Adding species data...')
    with app.app_context():
        cat = Species(species_name='Cat')
        dog = Species(species_name='Dog')
        ferret = Species(species_name='Ferret')
        db.session.add_all([cat, dog, ferret])
        db.session.commit()
    logging.info('Species data added successfully.')

    # Retrieve species IDs
    logging.info('Retrieving species IDs...')
    with app.app_context():
        species_ids = {s.species_name: s.id for s in Species.query.all()}
    logging.info('Species IDs retrieved successfully.')

    # Create pets data
    logging.info('Adding pets data...')
    with app.app_context():
        fluffy = Pet(name='Fluffy', age=3, species_id=species_ids.get('Cat', None), photo_url="https://th.bing.com/th/id/OIP.EYE2mQBHiIOZ-1EPjHdKNAHaG5?w=184&h=180&c=7&r=0&o=5&pid=1.7", notes='Fluffy loves to play with yarn.', available=True)
        rex = Pet(name='Rex', age=5, species_id=species_ids.get('Dog', None), photo_url="https://th.bing.com/th/id/OIP.K6mOJfsztqhNuLko4Ty4HAHaJ8?w=138&h=185&c=7&r=0&o=5&pid=1.7", notes='Rex is very friendly with children.', available=True)
        spike = Pet(name='Spike', age=2, species_id=species_ids.get('Ferret', None), photo_url="https://th.bing.com/th/id/OIP.2QXtujNDWAwMzYEk3-BJswHaFj?w=261&h=195&c=7&r=0&o=5&pid=1.7", notes='Spike likes to hide shiny objects.', available=True)
        pets = [fluffy, rex, spike]

        for pet in pets:
            if pet.species_id is not None:
                db.session.add(pet)
        db.session.commit()
    logging.info('Pets data added successfully.')

if __name__ == '__main__':
    # Seed the database
    seed_database()
    logging.info('Database seeding completed.')
