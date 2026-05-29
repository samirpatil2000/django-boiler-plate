# Django REST API Boilerplate

[![Django Version](https://img.shields.io/badge/django-6.0.5-blue.svg)](https://www.djangoproject.com/)
[![DRF Version](https://img.shields.io/badge/django--rest--framework-3.16.0-green.svg)](https://www.django-rest-framework.org/)
[![JWT Auth](https://img.shields.io/badge/auth-Simple--JWT-orange.svg)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

A modern, highly-scalable Django 6.0+ REST API boilerplate pre-configured with stateless JWT Authentication, email-based Custom User Model, and clean RESTful patterns. This boilerplate is designed to help developers kickstart production-ready API backends instantly.

---

## Key Features

- **Django 6.0.5 + Django REST Framework 3.16**: Built on top of the latest stable Django release.
- **Stateless JWT Authentication**: Implemented via Django REST Framework Simple JWT.
- **Custom User Model**: Uses `email` instead of `username` as the primary login credential.
- **RESTful Architecture**: Follows clean REST principles (nouns for resources, standard HTTP verbs, and native HTTP response status codes).
- **Comprehensive Error Handling**: Relies on DRF's native HTTP exception handling (e.g., returning `400 Bad Request`, `401 Unauthorized`, `403 Forbidden` status codes correctly).
- **System Health Monitor**: Built-in `/health` endpoint delivering system status, UTC timestamp, and precise human-readable uptime statistics.
- **Postman Collection**: Fully configured `postman_collection.json` containing automatic token extraction test scripts.
- **Development-Ready Docker Setup**: Pre-configured `Dockerfile` (built on Python 3.13-slim) and `docker-compose.yml`.

---

## Directory Structure

```text
django-boiler-plate/
├── main/                   # Core settings and root configuration files
│   ├── settings.py         # App configurations, middleware, and DB setup
│   ├── urls.py             # Global routing system
│   ├── views.py            # Root-level health check logic
│   └── wsgi.py / asgi.py   # Deployment gateway configurations
├── users/                  # Custom user app containing model-centric REST logic
│   ├── api_views/          # REST Endpoint View classes (register, profile)
│   ├── serializers/        # Registration and representation serializers
│   ├── migrations/         # Database migrations package
│   ├── admin.py            # User management dashboard registration
│   ├── models.py           # Custom User model and UserManager class
│   ├── urls.py             # Sub-routes for /users/ namespace
│   └── tests.py            # Robust REST integration and unit tests
├── requirements.txt        # Third-party package dependencies
├── Dockerfile              # Containerization definition (Python 3.13 base)
├── docker-compose.yml      # Multi-container orchestration configurations
├── postman_collection.json # Test queries and automated script exports
└── manage.py               # Django administrative script
```

---

## Quick Start

### Option 1: Docker (Recommended)

Make sure you have Docker and Docker Compose installed:

```bash
# Clone the repository
git clone https://github.com/samirpatil2000/django-boiler-plate.git
cd django-boiler-plate

# Copy environment variables template
cp .env.example .env

# Build and launch services
docker-compose up --build -d

# Initialize database schema
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# Create your admin account
docker-compose exec backend python manage.py createsuperuser
```

The server will be running at `http://localhost:8000/`.

---

### Option 2: Local Setup

#### Prerequisites
- **Python 3.10+** (Python 3.13 is recommended)

```bash
# Clone the repository
git clone https://github.com/samirpatil2000/django-boiler-plate.git
cd django-boiler-plate

# Initialize virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and update environmental settings
cp .env.example .env

# Generate migration schema files and migrate
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

---

## API Endpoints Reference

### System Health
- **`GET /health`** - Evaluates container/application status, UTC timestamp, and uptime metric.

### User Management
- **`POST /users/`** - Registers a new user account.
- **`GET /users/me/`** - Retrieves details of the currently logged-in user profile. (Requires Bearer Token Auth).

### Authentication
- **`POST /auth/login/`** - Authenticates credentials and returns a pair of Access and Refresh tokens.
- **`POST /auth/login/refresh/`** - Generates a new short-lived Access token using a valid Refresh token.

---

## Usage & Integration Examples

### 1. System Health Check
```bash
curl -X GET http://127.0.0.1:8000/health
```
**Response (`200 OK`):**
```json
{
  "status": "UP",
  "timestamp": "2026-05-29T19:23:51.034543+00:00",
  "uptime": "0h 0m 11s"
}
```

### 2. User Registration
```bash
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@example.com",
    "password": "securepassword123",
    "password2": "securepassword123"
  }'
```
**Response (`201 Created`):**
```json
{
  "email": "developer@example.com",
  "date_joined": "2026-05-29T19:22:11.123456Z"
}
```

### 3. User Login (Retrieve JWT Tokens)
```bash
curl -X POST http://127.0.0.1:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@example.com",
    "password": "securepassword123"
  }'
```
**Response (`200 OK`):**
```json
{
  "refresh": "eyJhbGciOi...",
  "access": "eyJhbGciOi..."
}
```

### 4. Fetch Profile (Authenticated Request)
```bash
curl -X GET http://127.0.0.1:8000/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
**Response (`200 OK`):**
```json
{
  "email": "developer@example.com"
}
```

### 5. Refresh JWT Access Token
```bash
curl -X POST http://127.0.0.1:8000/auth/login/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```
**Response (`200 OK`):**
```json
{
  "access": "eyJhbGciOi..."
}
```

---

## Testing

### Automated Test Suite
A comprehensive REST integration and unit test suite is maintained inside the `users` package. Run all test suites locally:

```bash
python manage.py test users
```

### Testing with Postman
We maintain a preconfigured Postman collection at the root of the project: [postman_collection.json](postman_collection.json).

**How to Use:**
1. Import [postman_collection.json](postman_collection.json) into Postman.
2. The collection defines variables: `base_url` (defaults to `http://127.0.0.1:8000`), `access_token`, and `refresh_token`.
3. The **Login** request has a built-in post-response script that automatically updates your Postman `access_token` and `refresh_token` variables when executed.
4. Subsequent requests (like **Get Profile**) will automatically authenticate using the Bearer token variable.

---

## Environment & Database Configuration

Configure your application behavior and database connection settings by specifying variables in your `.env` configuration file:

### Feature Toggles
- **`DISABLE_AUTH`**: (Boolean, defaults to `False`). Set to `True` in development/staging environments to bypass token authentication on the `/users/me/` profile endpoint. If unauthenticated, it automatically resolves to a mock developer profile (`dev@example.com`), allowing hassle-free local endpoint testing without header configurations.

### JWT Expiry Settings
- **`JWT_ACCESS_TOKEN_LIFETIME_MINUTES`**: (Integer, defaults to `8700` / 6 days + 1 hour). The duration in minutes for which a generated JWT access token is valid.
- **`JWT_REFRESH_TOKEN_LIFETIME_DAYS`**: (Integer, defaults to `7`). The duration in days for which a generated JWT refresh token is valid.

### Database Settings
**SQLite3 (Default Developer Environment):**
```env
DB_ENGINE=sqlite3
```

**PostgreSQL (Production Environment):**
```env
DB_ENGINE=postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Contributing

We welcome contributions to make this boilerplate even better!
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## License

This project is open-source software licensed under the [MIT License](LICENSE).
