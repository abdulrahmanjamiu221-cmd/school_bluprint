# SchoolResult Pro

SchoolResult Pro is a Flask-based Secondary School Result Management System for schools in Nigeria. The project is built around a modular Flask application factory, SQLAlchemy models, and role-based access control for administrators, teachers, principals, bursars, and parents.

## Features

- School registration and multi-school isolation
- School administrator management and settings
- Staff roles and user authentication
- Student registration with admission numbers
- Class and subject management
- Academic session and term configuration
- Teacher-class-subject assignment
- Result entry and review workflow
- Parent and payment tracking
- SQLite default database with PostgreSQL-ready configuration

## Quick start

1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and adjust values.
4. Initialize the database:
   ```bash
   flask --app app db init
   flask --app app db migrate -m "Initial migration"
   flask --app app db upgrade
   ```
5. Start the app:
   ```bash
   flask --app app run --debug
   ```

## Default demo login

After the first startup, the app seeds a default super administrator account:

- Email: admin@schoolresultpro.com
- Password: admin123

## Database migration notes

The project uses Flask-Migrate and SQLAlchemy to manage schema changes. Use the Flask CLI for all migrations. Do not commit production secrets into the repository.

## Deployment notes

- Use environment variables for secrets.
- Replace SQLite with PostgreSQL in production.
- Configure a secure SECRET_KEY and database credentials in `.env`.

## License

This is a starter application created for school result management use cases.
