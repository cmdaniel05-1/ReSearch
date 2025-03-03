import unittest
from app import db, create_app
from app.main.models import Application, Field, Language, Position, Student, Faculty

#Command to run: python -m unittest tests.test_db

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        """ Set up a test database """
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        """ Clean up database after tests """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        """Pre-populate database with necessary test objects"""
        student = Student(wpi_id=123456, username="testuser", firstname="John", lastname="Doe", email="test@example.com", phone_num="7816662121")
        student.set_password("securepassword")

        faculty = Faculty(wpi_id=789012, username="professor", firstname="Alice", lastname="Smith", email="alice@example.com", phone_num="555-1234")
        faculty.set_password("professorpass")

        db.session.add_all([student, faculty])
        db.session.commit()

    def get_student(self):
        """Helper method to reload the student from the database"""
        return Student.query.filter_by(username="testuser").first()

    def get_faculty(self):
        """Helper method to reload the faculty from the database"""
        return Faculty.query.filter_by(username="professor").first()

    def test_create_student(self):
        """ Test if a student can be retrieved from the database """
        with self.app.app_context():
            retrieved = self.get_student()
            self.assertIsNotNone(retrieved)
            self.assertTrue(retrieved.check_password("securepassword"))

    def test_create_faculty(self):
        """ Test if a faculty can be retrieved """
        with self.app.app_context():
            retrieved = self.get_faculty()
            self.assertIsNotNone(retrieved)
            self.assertTrue(retrieved.check_password("professorpass"))

    def test_create_position(self):
        """ Test if a position can be created and retrieved """
        with self.app.app_context():
            faculty = self.get_faculty()

            position = Position(faculty_id=faculty.wpi_id, title="Robotics Engineering Intern",
                                description="Build robots & code.", req_time=5, student_count=2)
            db.session.add(position)
            db.session.commit()

            retrieved = Position.query.filter_by(title="Robotics Engineering Intern").first()
            self.assertIsNotNone(retrieved)

    def test_create_application(self):
        """ Test if an application can be created and retrieved """
        with self.app.app_context():
            student = self.get_student()
            faculty = self.get_faculty()

            position = Position(faculty_id=faculty.wpi_id, title="Robotics Engineering Intern",
                                description="Build robots & code.", req_time=5, student_count=2)
            db.session.add(position)
            db.session.commit()

            application = Application(student_id=student.wpi_id, position_id=position.id,
                                      reference_id=faculty.wpi_id, statement="I love robotics")
            db.session.add(application)
            db.session.commit()

            retrieved = Application.query.filter_by(student_id=student.wpi_id, position_id=position.id).first()
            self.assertIsNotNone(retrieved)

    def test_student_applied(self):
        """ Test if student has applied to a position """
        with self.app.app_context():
            student = self.get_student()
            faculty = self.get_faculty()

            position = Position(faculty_id=faculty.wpi_id, title="Robotics Engineering Intern",
                                description="Build robots & code.", req_time=5, student_count=2)
            db.session.add(position)
            db.session.commit()

            student.apply(position, faculty, statement="I love robotics")
            db.session.commit()

            self.assertTrue(student.is_applied(position))

    def test_student_available_false_if_accepted(self):
        """Test if student is unavailable when accepted to a position"""
        with self.app.app_context():
            student = self.get_student()
            faculty = self.get_faculty()

            position = Position(faculty_id=faculty.wpi_id, title="Robotics Engineering Intern",
                                description="Build robots & code.", req_time=5, student_count=2)
            db.session.add(position)
            db.session.commit()

            student.apply(position, faculty, statement="I love robotics")
            db.session.commit()

            application = Application.query.filter_by(position_id=position.id).first()
            application.app_is_accepted = True
            db.session.commit()

            self.assertFalse(student.is_available())

    def test_student_available_true_if_rejected(self):
        """Test if student remains available when application is rejected"""
        with self.app.app_context():
            student = self.get_student()
            faculty = self.get_faculty()

            position = Position(faculty_id=faculty.wpi_id, title="Robotics Engineering Intern",
                                description="Build robots & code.", req_time=5, student_count=2)
            db.session.add(position)
            db.session.commit()

            student.apply(position, faculty, statement="I love robotics")
            db.session.commit()

            application = Application.query.filter_by(position_id=position.id).first()
            application.app_is_accepted = False
            db.session.commit()

            self.assertTrue(student.is_available())

    def test_create_field(self):
        """ Test if a field can be created and retrieved """
        with self.app.app_context():
            field = Field(name="Computer Science")
            db.session.add(field)
            db.session.commit()

            retrieved = Field.query.filter_by(name="Computer Science").first()
            self.assertIsNotNone(retrieved)

    def test_create_language(self):
        """ Test if a language can be created and retrieved """
        with self.app.app_context():
            language = Language(name="Java")
            db.session.add(language)
            db.session.commit()

            retrieved = Language.query.filter_by(name="Java").first()
            self.assertIsNotNone(retrieved)


if __name__ == '__main__':
    unittest.main()
