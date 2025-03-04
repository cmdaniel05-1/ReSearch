from datetime import date
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from flask_login import current_user
import pytest
from app import create_app, db
from app.main.models import Faculty, Position, Student, User
from config import Config
import sqlalchemy as sqla

#Command to run: pytest tests/test_routes.py

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class=TestConfig)

    testing_client = flask_app.test_client()
 
    ctx = flask_app.app_context()
    ctx.push()
 
    yield  testing_client 
    ctx.pop()

@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()

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

    student1 = Student(
            wpi_id=11111,
            username="student1",
            firstname="Bob",
            lastname="Brown",
            email="student1@wpi.edu",
            phone_num = "7819293929"
        )
    student1.set_password('student1')

    db.session.add_all([student1, faculty1])
    db.session.commit()

    yield 

    db.drop_all()

def test_home_page_logged_out(test_client):
    """
    GIVEN a Flask application configured for testing and user is not logged in
    WHEN the '/' page is requested (GET)
    THEN check that the response is a redirect
    """
    response = test_client.get('/')
    assert response.status_code == 302
    assert b"login" in response.data

def test_register(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    response = test_client.post('/register',
                                data=dict(wpi_id=11111,
                                        username="student1",
                                        firstname="Bob",
                                        lastname="Brown",
                                        email="student1@wpi.edu",
                                        phone_num = "7819293929"),
                                follow_redirects=True)
    assert response.status_code == 200
    
    user = db.session.scalar(sqla.select(User).where(User.username == 'student1'))
    assert user.email == 'student1@wpi.edu'

def test_invalid_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with incorrect credentials
    THEN check that login is refused
    """
    response = test_client.post('/login',
                                data=dict(username='faculty1', password='wrongpassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def do_login(test_client, username, password):
    response = test_client.post('/login',
                                data=dict(username=username, password=password),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Research Positions" in response.data  

def do_logout(test_client):
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign In" in response.data

def test_login_logout(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that login and logout work properly
    """
    do_login(test_client, username='faculty1', password='faculty1')
    do_logout(test_client)


def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing and user is logged in
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 302
    assert b"login" in response.data

def test_create_position(test_client, init_database):
    """
    GIVEN a logged-in faculty user
    WHEN they create a research opportunity (POST)
    THEN check that the opportunity is added successfully
    """
    do_login(test_client, username='faculty1', password='faculty1')

    response = test_client.post('/position/creation',
                                data=dict(title = "AI Research",
                                          description = "Be the future of AI",
                                          start_date = date.today(),
                                          end_date = date.today(),
                                          req_time = 5,
                                          student_count = 5),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"AI Research" in response.data
    
    position = db.session.scalar(sqla.select(Position).where(Position.title == 'AI Research'))
    assert position is not None
    
    do_logout(test_client)

def test_student_cannot_create_position(test_client, init_database):
    do_login(test_client, username='student1', password='student1')
    response = test_client.post('/position/creation', follow_redirects=True)
    assert response.status_code == 200
    assert b"Research Position" in response.data
    assert b"Create" not in response.data
    do_logout(test_client)

def test_create_position_missing_fields(test_client, init_database):
    do_login(test_client, username='faculty1', password='faculty1')
    response = test_client.post('/position/creation', data={'title': ''}, follow_redirects=True)
    assert b"is required" in response.data 
    do_logout(test_client)


def test_apply_for_position(test_client, init_database):
    pass

def test_view_applied_positions(test_client, init_database):
    pass

def test_accept_application(test_client, init_database):
    pass