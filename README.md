# 🔬 ReSearch



ReSearch is a web application built to digitize and streamline the summer research recruitment process at Worcester Polytechnic Institute (WPI). It provides a centralized platform where faculty can post openings and students can discover, apply, and engage with research opportunities tailored to their interests.



## 👥 Team Members

- Connor Daniel  

- Sarah Meyer  

- April Zingher  

- Ian Wood  



## 📚 Project Overview



ReSearch bridges the gap between faculty and students by offering a dynamic portal for summer research engagement. It simplifies the application process, enhances visibility, and encourages meaningful academic connections



### Faculty Features

- Create, edit, and manage research postings

- Label postings with relevant fields and programming languages

- View the list of students who applied to a position

- Review student profiles, including accepted opportunities

- View, accept, and reject student applications and reference requests



### Student Features

- Browse, sort, and filter available research opportunities

- Receive personalized recommendations based on profile content

- Apply with a personal statement and faculty reference

- Withdraw applications at any time

- Track the status of submitted applications and reference requests



All users can login using their WPI email or Azure Single Sign-On. By requiring thoughtful application submissions, ReSearch encourages intentional engagement and helps faculty identify motivated candidates.



## ⚙️ Technologies Used



**Language & Framework**

- Python

- Flask



**Frontend**

- Flask-Bootstrap  

- Jinja2



**Authentication**

- Flask-Login 

- Authlib



**Forms & Validation**

- Flask-WTF

- WTForms

- WTForms-SQLAlchemy

- email-validator



**Database**

- Flask-SQLAlchemy

- Flask-Migrate

- psycopg2-binary



**Utilities**

- Flask-Moment

- Werkzeug

- python-dotenv



**Testing**

- pytest

- selenium



## 🚀 Getting Started



To run the application locally:



```bash

python -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt

flask run

