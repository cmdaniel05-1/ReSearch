import os
import sys
import threading
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app import create_app

#Command to run: pytest tests/test_selenium.py

# Student fixure - 1
@pytest.fixture
def student1():
    return  {'wpi_id':'123456', 'username' : 'testuser', 'firstname':'John', 'lastname':'Doe', 'email':'test@example.com', 'phone_num':'7816662121', 'password' : 'securepassword'}

# Faculty fixure - 2
@pytest.fixture
def faculty1():
    return  {'wpi_id':'789012', 'username' : 'professor', 'firstname':'Alice', 'lastname':'Smith', 'email':'alice@example.com', 'phone_num':'555-1234', 'password' : 'professorpass'}

# Post fixure - 1
@pytest.fixture
def position1():
    return {'title' : 'Robotics Engineering Intern', 'description' : 'Build robots & code.', 'req_time' : '5', 'student_count' : '2'}

@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options) #use selenium manager
    driver.implicitly_wait(8)
    
    yield driver

    driver.quit()

@pytest.fixture(scope='module')
def flask_app():
    def run_app():
        app = create_app()
        app.run(port=3000, use_reloader=False)  

    # use threading
    app_thread = threading.Thread(target=run_app)
    app_thread.daemon = True 
    app_thread.start()

    time.sleep(2)
    
    yield 

#test that the website even loads
def test_browser_title(browser, flask_app):
    browser.get('http://localhost:3000/index')

    assert "ReSearch" in browser.title

def test_register_form(browser, student1, flask_app):
    browser.get('http://localhost:3000/register')

    select = Select(browser.find_element(By.NAME, "type"))
    select.select_by_visible_text('Student')
    time.sleep(2)
    browser.find_element(By.NAME, "wpi_id").send_keys(student1['wpi_id'])
    time.sleep(2)
    browser.find_element(By.NAME, "username").send_keys(student1['username'])
    time.sleep(2)
    browser.find_element(By.NAME, "firstname").send_keys(student1['firstname'])
    time.sleep(2)
    browser.find_element(By.NAME, "lastname").send_keys(student1['lastname'])
    time.sleep(2)
    browser.find_element(By.NAME, "email").send_keys(student1['email'])
    time.sleep(2)
    browser.find_element(By.NAME, "phone_num").send_keys(student1['phone_num'])
    time.sleep(2)
    browser.find_element(By.NAME, "password").send_keys(student1['password'])
    time.sleep(2)
    browser.find_element(By.NAME, "password2").send_keys(student1['password'])    
    time.sleep(2)
    browser.find_element(By.NAME, "submit").click()
    time.sleep(2)
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered Student!' in content