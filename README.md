# Django REST API Boilerplate

A clean Django REST API boilerplate with JWT authentication, custom user model, and essential endpoints to kickstart your project.

## Features

- Django 4.2.23 + Django REST Framework
- JWT Authentication with Simple JWT
- Custom User Model (email-based login)
- User registration, login, and profile management
- Password reset functionality
- CORS support
- Docker support

## Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone and setup
git clone https://github.com/samirpatil2000/django-boiler-plate.git
cd django-boiler-plate
cp .env.example .env

# Run with Docker
docker-compose up --build

# Setup database
docker exec -it backend python manage.py migrate
docker exec -it backend python manage.py createsuperuser
```

### Option 2: Local Setup

```bash
# Clone and setup
git clone https://github.com/samirpatil2000/django-boiler-plate.git
cd django-boiler-plate

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies and setup
pip install -r requirements.txt

# Generate custom user migrations (required before migrating)
python manage.py makemigrations

# Apply migrations and start server
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoints

### System Health
- `GET /health` - Check application status, UTC timestamp, and uptime (root level)

### Authentication
**Base URL:** `http://127.0.0.1:8000/account/`

- `POST /register` - Register new user
- `POST /login` - Login and get JWT token
- `POST /token/refresh` - Refresh JWT token (returns new access token)
- `GET /register` - Get user profile (requires Bearer token auth)

> [!NOTE]
> The template-based views (such as `password-reset` and `password_change`) are registered in URLs but require HTML templates to be placed in `account/templates/account/` in order to render without `TemplateDoesNotExist` errors.

## Usage Examples

### System Health Check
```bash
curl -X GET http://127.0.0.1:8000/health
```
Response:
```json
{
  "status": "UP",
  "timestamp": "2026-05-29T19:00:54.050566+00:00",
  "uptime": "0h 0m 11s"
}
```

### Register User
```bash
curl -X POST http://127.0.0.1:8000/account/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123",
    "password2": "securepass123"
  }'
```
Response:
```json
{
  "status": 201,
  "message": "User registered successfully",
  "data": {
    "email": "user@example.com",
    "date_joined": "2026-05-29T18:56:17.922803Z"
  }
}
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/account/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```
Response:
```json
{
  "status": 200,
  "message": "successfully login",
  "data": {
    "refresh": "YOUR_REFRESH_TOKEN",
    "access": "YOUR_ACCESS_TOKEN"
  }
}
```

### Access Protected Profile Endpoint
```bash
curl -X GET http://127.0.0.1:8000/account/register \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
Response:
```json
{
  "status": 200,
  "message": "successfully register",
  "data": {
    "email": "user@example.com"
  }
}
```

### Refresh JWT Token
```bash
curl -X POST http://127.0.0.1:8000/account/token/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```
Response:
```json
{
  "access": "YOUR_NEW_ACCESS_TOKEN"
}
```

## Project Structure

- **Custom User Model**: Email-based authentication instead of username
- **JWT Authentication**: Secure token-based authentication
- **Modular Design**: Clean separation of concerns
- **API-First**: RESTful API architecture

## Database Configuration

The project supports both PostgreSQL and SQLite3 databases. Configure via the `DB_ENGINE` environment variable in your `.env` file:

**SQLite3 (Default):**
```env
DB_ENGINE=sqlite3
```

**PostgreSQL:**
```env
DB_ENGINE=postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

## Development

```bash
# Run tests
python manage.py test

# Access admin panel
http://127.0.0.1:8000/admin/
```

## Deployment

1. Set `DEBUG = False` in settings
2. Configure production database (PostgreSQL/MySQL)
3. Set up environment variables in `.env`
4. Configure static files and HTTPS
5. Update CORS settings for your domain

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
