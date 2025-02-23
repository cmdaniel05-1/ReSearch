import unittest
from app import db, create_app
from app.main.models import Student, Faculty

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app()
        """ Set up a test database """
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        app = create_app()
        """ Clean up database after tests """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_student(self):
        app = create_app()
        """ Test if a student can be created and retrieved """
        with app.app_context():
            student = Student(wpi_id=123456, username="testuser", firstname="John", lastname="Doe", email="test@example.com", phone_num = "7816662121")
            student.set_password("securepassword")
            db.session.add(student)
            db.session.commit()

            retrieved = Student.query.filter_by(username="testuser").first()
            self.assertIsNotNone(retrieved)
            self.assertTrue(retrieved.check_password("securepassword"))

    def test_create_faculty(self):
        """ Test if a faculty can be created and retrieved """
        app = create_app()
        with app.app_context():
            faculty = Faculty(wpi_id=789012, username="professor", firstname="Alice", lastname="Smith", email="alice@example.com", phone_num="555-1234")
            faculty.set_password("professorpass")
            db.session.add(faculty)
            db.session.commit()

            retrieved = Faculty.query.filter_by(username="professor").first()
            self.assertIsNotNone(retrieved)
            self.assertTrue(retrieved.check_password("professorpass"))

if __name__ == '__main__':
    unittest.main()
