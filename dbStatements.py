from app import db, create_app
from datetime import date, timedelta
from app.main.models import Position, Field, Language

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

        # Create positions
        position1 = Position(
            title="Software Engineer Intern",
            description="Develop and maintain software applications.",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=90),
            req_time=20,
            student_count=3
        )

        position2 = Position(
            title="Bioinformatics Research Assistant",
            description="Assist in analyzing biological data using computational tools.",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=180),
            req_time=15,
            student_count=2
        )

        # Associate positions with fields and languages
        position1.fields = [field1]
        position1.languages = [language1]

        position2.fields = [field1, field2]
        position2.languages = [language1, language2]

        # Add to session and commit
        db.session.add_all([field1, field2, language1, language2, position1, position2])
        db.session.commit()
        print("Database populated successfully!")

# Run the function
if __name__ == "__main__":
    populate_db()
