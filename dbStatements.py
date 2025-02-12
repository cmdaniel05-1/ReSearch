from app import db, create_app
from datetime import date, timedelta
from app.main.models import Position, Field, Language, Student, Faculty

def populate_db():
    app = create_app()
    with app.app_context():
        # Ensure all tables exist
        db.create_all()

        # Create fields
        field1 = Field(name="Computer Science")
        field2 = Field(name="Biotechnology")

        # Create languages
        language1 = Language(name="Python")
        language2 = Language(name="JavaScript")

        # Create faculty members
        faculty1 = Faculty(
            id = 0,
            wpi_id=12345,
            username="faculty1",
            firstname="John",
            lastname="Doe",
            email="jdoe@wpi.edu",
            phone_num="123-456-7890"
        )
        faculty1.set_password('faculty1')

        faculty2 = Faculty(
            id = 1,
            wpi_id=67890,
            username="faculty2",
            firstname="Alice",
            lastname="Smith",
            email="asmith@wpi.edu",
            phone_num="987-654-3210"
        )
        faculty2.set_password('faculty2')

        # Create positions
        position1 = Position(
            faculty_id=0,
            title="Software Engineer Intern",
            description="Develop and maintain software applications.",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=90),
            req_time=20,
            student_count=3
        )

        position2 = Position(
            faculty_id=1,
            title="Bioinformatics Research Assistant",
            description="Assist in analyzing biological data using computational tools.",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=180),
            req_time=15,
            student_count=2
        )

        # Create students
        student1 = Student(
            wpi_id=11111,
            username="student1",
            firstname="Bob",
            lastname="Brown",
            email="student1@wpi.edu",
            phone_num = "7819293929"
        )

        student1.set_password("student1")

        student2 = Student(
            wpi_id=22222,
            username="student2",
            firstname="Sara",
            lastname="Green",
            email="student2@wpi.edu",
            phone_num = "7810993929"
        )
        student2.set_password("student2")

        # Associate positions with fields and languages
        position1.fields = [field1]
        position1.languages = [language1]

        position2.fields = [field1, field2]
        position2.languages = [language1, language2]

        # Add to session and commit
        db.session.add_all([field1, field2, language1, language2, position1, position2, faculty1, faculty2, student1, student2])
        db.session.commit()

        print("Database populated successfully!")

# Run the function
if __name__ == "__main__":
    populate_db()
