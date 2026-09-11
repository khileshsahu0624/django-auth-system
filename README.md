# Django CRUD Auth Project

A comprehensive Django application featuring Student CRUD operations, Role-Based Access Control (RBAC), and a secure OTP-based authentication system.

## Features

1. **Role-Based Access Control (RBAC):**
   - `SUPER_ADMIN`: Full access to Django admin and all CRUD operations on the frontend.
   - `ADMIN`: Full access to Django admin and all CRUD operations on the frontend.
   - `USER`: Read-only access to the student list on the frontend. Action buttons (Add, Edit, Delete) are hidden and restricted via decorators.
2. **OTP-Based Authentication:**
   - Passwordless login system.
   - Users enter their username to request a 6-digit One-Time Password (OTP).
   - OTP is printed directly to the server console (simulating SMS/Email dispatch).
   - Enforced 5-minute expiration window for all OTPs.
3. **Student CRUD Operations:**
   - Create, Read, Update, and Delete records for students.

## Prerequisites

- Python 3.8+
- MySQL Server

## Setup Instructions

1. **Clone or Download the Project.**

2. **Create a Virtual Environment & Activate It:**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration:**
   - Open `student_project/settings.py`.
   - Ensure your MySQL service is running.
   - Verify the `DATABASES` settings match your local MySQL credentials (default expects a `root` user with an empty password).
   - Create the database in MySQL:
     ```sql
     CREATE DATABASE student_db;
     ```

5. **Apply Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser (for initial setup):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

## Testing the OTP Login

1. Go to `http://127.0.0.1:8000/login/`.
2. Enter the username of an existing account (e.g., the superuser you just created).
3. Look at the terminal where the server is running; you will see a printed OTP code.
4. Enter that code on the Verification page to log in!
