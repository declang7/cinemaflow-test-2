# CinemaFlow

CinemaFlow is a refactored Flask-based cinema booking application.

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and update variables.
5. Initialize the database:
   ````
   flask db init
   flask db migrate
   flask db upgrade
   ```
6. Run the application:
   ```
   flask run
   ```

## Features

- User registration and login with hashed passwords.
- Movie listings and showtimes.
- Seat booking with unique constraints.
- Role-based access control (customers, managers).
- Modular structure using Flask Blueprints.
