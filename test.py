import unittest
from app import app, db
from models import Pet, Species
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
            seed_database()

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
            seed_database()

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

    @classmethod
    def setUpClass(self):
        """Set up the test environment"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            seed_database()

    @classmethod
    def tearDownClass(self):
        """Tear down the test environment"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_pet_form(self):
        """Test AddPetForm validation"""
        # Mock CSRF token generation
        AddPetForm.generate_csrf_token = lambda self: 'mocked_csrf_token'

        form_data = {
            'name': 'Fluffy',
            'species': 'Cat',
            'age': 3,
            'photo_url': 'https://example.com/fluffy.jpg',  # Optional, but you may include it if needed
            'notes': 'Fluffy is a very friendly cat.',      # Optional, but you may include it if needed
        }


        with app.app_context():
            form = AddPetForm(data=form_data)
            if not form.validate():
                print("\n\n\n\n\n\n", form.errors, "\n\n\n\n\n\n")
            self.assertTrue(form.validate())

    def test_edit_pet_form(self):
        """Test EditPetForm validation"""
        # Mock CSRF token generation
        EditPetForm.generate_csrf_token = lambda self: 'mocked_csrf_token'

        form_data = {
            'notes': 'Fluffy is very playful.'
        }
        with app.app_context():    
            form = EditPetForm(data=form_data)
            self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
