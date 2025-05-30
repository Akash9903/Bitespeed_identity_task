# Bitespeed_Identity_Task

A Django-based backend service for contact identity reconciliation, built for the Bitespeed challenge.

---

## How to Run Locally

1️) **Clone the repo:**  
git clone https://github.com/Akash9903/Bitespeed_identity_task.git <br>
cd Bitespeed_identity_task <br>
2) Install dependencies:
pip install -r requirements.txt <br>
3) Set up your .env file:
DATABASE_URL="" <br>
4) Create initial migration for the identity app:
python manage.py makemigrations identity <br>
5) Apply migrations:
python manage.py migrate <br>
7️) Run the app:
python manage.py runserver <br>

---

## Deployment
Deployed on **Render**:  
https://bitespeed-identity-task-hvjj.onrender.com
