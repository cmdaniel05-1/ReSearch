import datetime
import os
import sys
import threading
import click
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app import create_app, db

#Command to run: pytest tests/test_selenium.py

# Student fixure - 1
@pytest.fixture
def student1():
    return  {'wpi_id':'123456', 'username' : 'student1', 'firstname':'John', 'lastname':'Doe', 'email':'test@example.com', 'phone_num':'7816662121', 'password' : 'securepassword'}

# Faculty fixure - 1
@pytest.fixture
def faculty1():
    return  {'wpi_id':'789012', 'username' : 'faculty1', 'firstname':'Alice', 'lastname':'Smith', 'email':'alice@example.com', 'phone_num':'555-1234', 'password' : 'professorpass'}

# Faculty fixure - 2
@pytest.fixture
def faculty2():
    return  {'wpi_id':'788012', 'username' : 'faculty2', 'firstname':'Joe', 'lastname':'Shmoe', 'email':'jshmoe@example.com', 'phone_num':'575-1234', 'password' : 'faculty2'}


# Post fixure - 1
@pytest.fixture
def position1():
    return {'title' : 'Robotics Engineering Intern', 'description' : 'Build robots & code.','start_date' : date.today().strftime('%m-%d-%Y'),'end_date' : date.today().strftime('%m-%d-%Y'),'req_time' : '5', 'student_count' : '2'}

@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options) #use selenium manager
    driver.implicitly_wait(8)
    
    yield driver

    driver.quit()

@pytest.fixture(scope='module', autouse=True)
def flask_app():
    app = create_app()

    # Clear database
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()

    def run_app():
        app.run(port=3000, use_reloader=False)  

    # Start flask in thread
    app_thread = threading.Thread(target=run_app)
    app_thread.daemon = True
    app_thread.start()

    time.sleep(1)
    yield app

    with app.app_context():
        db.session.remove()

def click_submit(browser):
    submit_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.NAME, "submit")))
    browser.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    try:
        submit_button.click()  # Attempt normal click
    except Exception:
        browser.execute_script("arguments[0].click();", submit_button)

#test that the website even loads
def test_browser_title(browser):
    browser.get('http://localhost:3000/index')

    assert "ReSearch" in browser.title

def test_register_form_student(browser, student1):
    browser.get('http://localhost:3000/register')

    select = Select(browser.find_element(By.NAME, "type"))
    select.select_by_visible_text('Student')
    time.sleep(0.5)
    browser.find_element(By.NAME, "wpi_id").send_keys(student1['wpi_id'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "username").send_keys(student1['username'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "firstname").send_keys(student1['firstname'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "lastname").send_keys(student1['lastname'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "email").send_keys(student1['email'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "phone_num").send_keys(student1['phone_num'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "password").send_keys(student1['password'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "password2").send_keys(student1['password'])    
    
    click_submit(browser=browser)

    time.sleep(1)
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered Student!' in content

def test_login_form_student(browser, student1):
    #test_register_form_student(browser, faculty1\)
    browser.get('http://localhost:3000/login')

    browser.find_element(By.NAME, "username").send_keys(student1['username'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "password").send_keys(student1['password'])
    time.sleep(1)
    click_submit(browser=browser)
    time.sleep(1)
    #verification
    content = browser.page_source
    # print(content)
    assert 'The user student1 has successfully logged in!' in content

def test_register_form_faculty(browser, faculty1):
    browser.get('http://localhost:3000/register')

    select = Select(browser.find_element(By.NAME, "type"))
    select.select_by_visible_text('Faculty')
    time.sleep(0.5)
    browser.find_element(By.NAME, "wpi_id").send_keys(faculty1['wpi_id'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "username").send_keys(faculty1['username'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "firstname").send_keys(faculty1['firstname'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "lastname").send_keys(faculty1['lastname'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "email").send_keys(faculty1['email'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "phone_num").send_keys(faculty1['phone_num'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "password").send_keys(faculty1['password'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "password2").send_keys(faculty1['password'])    
    
    click_submit(browser=browser)

    time.sleep(1)
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered Faculty!' in content

def test_login_form_faculty(browser, faculty1):
    browser.get('http://localhost:3000/login')

    browser.find_element(By.NAME, "username").send_keys(faculty1['username'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "password").send_keys(faculty1['password'])
    click_submit(browser=browser)
    time.sleep(1)
    #verification
    content = browser.page_source
    # print(content)
    assert 'The user faculty1 has successfully logged in!' in content
    

def test_create_position(browser, faculty1, position1):

    browser.get('http://localhost:3000/login')

    #login
    browser.find_element(By.NAME, "username").send_keys(faculty1['username'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "password").send_keys(faculty1['password'])
    time.sleep(1)
    browser.find_element(By.NAME, "submit").click()
    time.sleep(1)

    browser.find_element(By.NAME, "create_position").click()

    #create position
    browser.find_element(By.NAME, "title").send_keys(position1['title'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "description").send_keys(position1['description'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "start_date").send_keys(position1['start_date'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "end_date").send_keys(position1['end_date'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "req_time").send_keys(position1['req_time'])
    time.sleep(0.5)
    browser.find_element(By.NAME, "student_count").send_keys(position1['student_count'])
    time.sleep(1)
    click_submit(browser=browser)

    #verification
    content = browser.page_source
    # print(content)
    assert f"\"{position1['title']}\" has been posted." in content

def test_faculty_view_student_profile(browser, faculty1, student1):
    """
    GIVEN a logged-in faculty user
    WHEN they view a student's profile
    THEN check that the profile details are displayed correctly
    """
    
    test_login_form_faculty(browser, faculty1)

    # View the student's profile
    browser.get(f'http://localhost:3000/profile/{student1["username"]}')
    time.sleep(1)

    # Verification
    content = browser.page_source
    assert student1['firstname'] in content
    assert student1['lastname'] in content
    assert student1['email'] in content

def test_display_profile(browser, student1):
    """
    GIVEN a logged-in student user
    WHEN they view their own profile
    THEN check that the profile details are displayed correctly
    """

    test_login_form_student(browser, student1)

    # View the student's profile
    browser.get(f'http://localhost:3000/profile/{student1["username"]}')
    time.sleep(1)

    # Verification
    content = browser.page_source
    assert student1['firstname'] in content
    assert student1['lastname'] in content
    assert student1['email'] in content

def test_display_profile(browser, student1):
    """
    GIVEN a logged-in student user
    WHEN they view their own profile
    THEN check that the profile details are displayed correctly
    """

    test_login_form_student(browser, student1)

    # View the student's profile
    browser.get(f'http://localhost:3000/profile')
    time.sleep(1)

    # Verification
    content = browser.page_source
    assert student1['firstname'] in content
    assert student1['lastname'] in content
    assert student1['email'] in content

def test_edit_profile(browser, student1):
    """
    GIVEN a logged-in student user
    WHEN they edit their profile
    THEN check that the profile is updated successfully
    """

    test_login_form_student(browser, student1)

    # Edit the student's profile
    browser.get(f'http://localhost:3000/profile/edit')
    time.sleep(1)
    browser.find_element(By.NAME, "firstname").clear()
    browser.find_element(By.NAME, "firstname").send_keys("UpdatedFirstName")
    time.sleep(0.5)
    browser.find_element(By.NAME, "lastname").clear()
    browser.find_element(By.NAME, "lastname").send_keys("UpdatedLastName")
    time.sleep(0.5)
    click_submit(browser=browser)
    time.sleep(1)

    # Verification
    content = browser.page_source
    assert 'Profile updated successfully!' in content
    assert 'UpdatedFirstName' in content
    assert 'UpdatedLastName' in content

def test_student_apply(browser, student1, faculty2, position1):
    """
    GIVEN a logged-in student user
    WHEN they apply for a position
    THEN check that the application is submitted successfully
    """
    test_register_form_faculty(browser, faculty2)
    test_login_form_student(browser, student1)

    # Apply for the position
    browser.get('http://localhost:3000/index')
    # Use XPath to find the element by its text content
    position_element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//*[text()='{position1['title']}']"))
    )
    position_element.click()
    time.sleep(1)
    apply_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "apply"))
    )
    apply_button.click()
    time.sleep(1)
    browser.find_element(By.NAME, "statement").send_keys("I am very interested in this position.")
    time.sleep(1)
    select = Select(browser.find_element(By.NAME, "reference"))
    select.select_by_visible_text(faculty2['firstname'] + ' ' + faculty2['lastname'] + ' - ' + faculty2['email'])
    time.sleep(1)
    click_submit(browser=browser)
    time.sleep(1)

    # Verification
    content = browser.page_source
    assert 'You have applied to {}.'.format(position1['title']) in content

def test_view_applications(browser, student1):
    """
    GIVEN a logged-in student user
    WHEN they view their applications
    THEN check that the applications are displayed correctly
    """
    # Register and login the student
    test_login_form_student(browser, student1)

    # Get the student ID
    browser.get(f'http://localhost:3000/index')
    time.sleep(1)
    navbarDropdown = browser.find_element(By.ID, "navbarDropdown")
    navbarDropdown.click()
    time.sleep(1)
    myApplications = browser.find_element(By.LINK_TEXT, "My Applications")
    myApplications.click()
    time.sleep(1)

    # Verification
    content = browser.page_source
    assert 'Applications' in content
    assert 'Robotics Engineering Intern' in content 

    # Logout
    browser.get('http://localhost:3000/logout')
    time.sleep(1)
