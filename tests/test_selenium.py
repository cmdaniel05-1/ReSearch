import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep

#Command to run: pytest tests/test_selenium.py

# User fixure - 1
@pytest.fixture
def student1():
    return  {'wpi_id':'123456', 'username' : 'testuser', 'firstname':'John', 'lastname':'Doe', 'email':'test@example.com', 'phone_num':'7816662121', 'password' : 'securepassword'}

# User fixure - 2
@pytest.fixture
def faculty1():
    return  {'wpi_id':'789012', 'username' : 'professor', 'firstname':'Alice', 'lastname':'Smith', 'email':'alice@example.com', 'phone_num':'555-1234', 'password' : 'professorpass'}

 # Post fixure - 1
@pytest.fixture
def position1():
    return {}

 # Post fixure - 2
@pytest.fixture
def position2():
    return {}
