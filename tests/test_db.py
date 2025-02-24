import unittest
from app import db, create_app
from app.main.models import Application, Field, Language, Position, Student, Faculty

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

    def test_create_position(self):
        """ Test if a position can be created and retrieved """
        app = create_app()
        with app.app_context():
            #create professor
            faculty = Faculty(wpi_id=789012, username="professor", firstname="Alice", lastname="Smith", email="alice@example.com", phone_num="555-1234")
            faculty.set_password("professorpass")
            db.session.add(faculty)

            #create position
            position = Position(faculty_id = 789012, title = "Robotics Engineering Intern", description = "Build robots & code.", req_time = 5, student_count = 2)
            db.session.add(position)
            db.session.commit()

            retrieved = Position.query.filter_by(title = "Robotics Engineering Intern").first()
            self.assertIsNotNone(retrieved)

    def test_create_application(self):
        """ Test if an application can be created and retrieved """
        app = create_app()
        with app.app_context():

            #create student
            student = Student(wpi_id=123456, username="testuser", firstname="John", lastname="Doe", email="test@example.com", phone_num = "7816662121")
            student.set_password("securepassword")
            db.session.add(student)

            #create professor
            faculty = Faculty(wpi_id=789012, username="professor", firstname="Alice", lastname="Smith", email="alice@example.com", phone_num="555-1234")
            faculty.set_password("professorpass")
            db.session.add(faculty)

            #create position
            position = Position(id = 4560, faculty_id = 789012, title = "Robotics Engineering Intern", description = "Build robots & code.", req_time = 5, student_count = 2)
            db.session.add(position)

            application = Application(student_id = 123456, position_id = 4560, reference_id = 789012, statement = "I love robotics")
            db.session.add(application)
            db.session.commit()

            retrieved = Application.query.filter_by(student_id = 123456, position_id = 4560, reference_id = 789012).first()
            self.assertIsNotNone(retrieved)

    def test_create_field(self):
        """ Test if a field can be created and retrieved """
        app = create_app()
        with app.app_context():
            field = Field(name = "Computer Science")
            db.session.add(field)
            db.session.commit()

            retrieved = Field.query.filter_by(name = "Computer Science").first()
            self.assertIsNotNone(retrieved)

    def test_create_language(self):
        """ Test if a language can be created and retrieved """
        app = create_app()
        with app.app_context():
            language = Language(name = "Java")
            db.session.add(language)
            db.session.commit()

            retrieved = Language.query.filter_by(name = "Java").first()
            self.assertIsNotNone(retrieved)

if __name__ == '__main__':
    unittest.main()
