import unittest
from app import app, db
from models import Pet
from forms import AddPetForm, EditPetForm
from seed import seed_database

class MyAppTestCase(unittest.TestCase):
    """Test cases for MyApp"""

    def setUp(self):
        """Set up test client and create a testing database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            seed_database(db)

    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_list_pets(self):
        """Test listing pets"""
        with app.app_context():
            # Create some sample data
            cat = Species(species_name='Cat')
            db.session.add(cat)
            db.session.commit()
            fluffy = Pet(name='Fluffy', age=3, species_id=cat.id)
            db.session.add(fluffy)
            db.session.commit()

            # Make a request to the list_pets route
            response = self.client.get('/')
            data = response.data.decode('utf-8')

            # Assert that Fluffy is listed in the response
            self.assertIn('Fluffy', data)


class ModelsTestCase(unittest.TestCase):
    """Test cases for models"""

    def setUp(self):
        """Set up test client and create a testing database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            seed_database(db)

    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_pet(self):
        """Test creating a new pet"""
        with app.app_context():
            cat = Species(species_name='Cat')
            db.session.add(cat)
            db.session.commit()

            new_pet = Pet(name='Fluffy', age=3, species_id=cat.id)
            db.session.add(new_pet)
            db.session.commit()

            pet = Pet.query.filter_by(name='Fluffy').first()
            self.assertIsNotNone(pet)
            self.assertEqual(pet.age, 3)



class FormsTestCase(unittest.TestCase):
    """Test cases for forms"""

    def test_add_pet_form(self):
        """Test AddPetForm validation"""
        form_data = {
            'name': 'Fluffy',
            'species': 'Cat',
            'age': 3
        }
        form = AddPetForm(data=form_data)
        self.assertTrue(form.validate())

    def test_edit_pet_form(self):
        """Test EditPetForm validation"""
        form_data = {
            'notes': 'Fluffy is very playful.'
        }
        form = EditPetForm(data=form_data)
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
