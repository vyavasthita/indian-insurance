# Indian Insurance

- A full-stack insurance registration platform built with Flask, providing REST APIs for user sign-up, email verification, and email blacklisting.
- Includes asynchronous email delivery via Celery, Swagger API documentation, and a fully containerized Docker deployment.

---

## Table of Contents

- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
  - [Running the Application](#running-the-application)
- [API Reference](#api-reference)
  - [Sign Up](#1-sign-up)
  - [Verify Email](#2-verify-email)
  - [Blacklist Email](#3-blacklist-email)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Email Flow](#email-flow)
- [Validation Rules](#validation-rules)
- [Testing](#testing)
- [Make Targets](#make-targets)
- [Design Decisions](#design-decisions)
- [License](#license)

---

## Architecture

```
┌──────────┐       ┌──────────────┐       ┌───────────┐
│  Client   │──────▶│ Flask + RESTX │──────▶│  MySQL 8  │
│ (Browser/ │◀──────│  (Gunicorn)   │◀──────│   :3308   │
│  Postman) │       │    :5000      │       └───────────┘
└──────────┘       └──────┬───────┘
                          │  Celery task
                          ▼
                   ┌──────────────┐       ┌───────────┐
                   │  RabbitMQ    │──────▶│  Celery    │──▶ SMTP (Email)
                   │    :5672     │       │  Worker    │
                   └──────────────┘       └───────────┘
                          ▲
                   ┌──────┴───────┐
                   │    Redis     │  (Result backend)
                   │    :6379     │
                   └──────────────┘
```

| Service     | Image / Build       | Port       | Purpose                          |
|-------------|---------------------|------------|----------------------------------|
| **backend** | `./backend`         | 5000       | Flask API server (Gunicorn)      |
| **mysql-db**| `mysql:8.0.29`      | 3308→3306  | Primary database                 |
| **db-admin**| `phpmyadmin:latest` | 8080→80    | Database management UI           |
| **redis**   | `redis:latest`      | 6379       | Celery result backend            |
| **rabbitmq**| `rabbitmq:latest`   | 5672       | Celery message broker            |
| **worker**  | `./email_worker`    | —          | Async email sending via Celery   |

---

## Tech Stack

| Layer          | Technology                                              |
|----------------|---------------------------------------------------------|
| Language       | Python 3.8+                                             |
| Web Framework  | Flask 2.3, Flask-RESTX 1.1 (Swagger UI)                |
| ORM            | SQLAlchemy 2.0, Flask-SQLAlchemy 3.0                    |
| Migrations     | Alembic via Flask-Migrate                               |
| Task Queue     | Celery 5.2 + RabbitMQ (broker) + Redis (result backend) |
| Email          | Flask-Mail (SMTP)                                       |
| Web Server     | Gunicorn (auto-scaled to CPU cores)                     |
| Database       | MySQL 8.0 (production), SQLite (dev/testing)            |
| Testing        | pytest, coverage                                        |
| Containerization | Docker, Docker Compose                                |

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Git

### Environment Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd indian-insurance
   ```

2. Create environment files from the sample:
   ```bash
   cp backend/.env.sample backend/.env.dev
   cp backend/.env.sample backend/.env.aut_test
   ```

3. Configure the following variables in `backend/.env.dev`:

   | Variable                    | Example                              | Description                        |
   |-----------------------------|--------------------------------------|------------------------------------|
   | `SECRET_KEY_DEV`            | `my-secret-key`                      | Flask secret key for sessions      |
   | `SECURITY_PASSWORD_SALT_DEV`| `my-salt-value`                      | Salt for token generation          |
   | `DB_TYPE_DEV`               | `mysql`                              | `sqlite` or `mysql`                |
   | `MYSQL_USER_DEV`            | `root`                               | MySQL user                         |
   | `MYSQL_HOST_DEV`            | `mysql-db`                           | MySQL host (Docker service name)   |
   | `MYSQL_PORT_DEV`            | `3306`                               | MySQL port inside Docker network   |
   | `MYSQL_DB_DEV`              | `indianinsurance`                    | Database name                      |
   | `MAIL_SERVER_DEV`           | `smtp.mailtrap.io`                   | SMTP server                        |
   | `MAIL_PORT_DEV`             | `587`                                | SMTP port                          |
   | `MAIL_USERNAME_DEV`         | *your SMTP username*                 | SMTP credentials                   |
   | `MAIL_PASSWORD_DEV`         | *your SMTP password*                 | SMTP credentials                   |
   | `CELERY_BROKER_URL_DEV`     | `amqp://guest:guest@rabbitmq:5672//` | RabbitMQ connection                |
   | `CELERY_RESULT_BACKEND_DEV` | `redis://redis:6379/0`               | Redis connection                   |
   | `EMAIL_TOKEN_EXPIRATION_DEV`| `3600`                               | Token validity in seconds          |
   | `PASSWORD_LENGTH_DEV`       | `12`                                 | Auto-generated password length     |

### Running the Application

```bash
# Start all services (builds images, runs migrations, starts server)
make run

# Or equivalently:
docker compose up -d --build --remove-orphans
```

Once running:
- **API + Swagger UI** → http://localhost:5000
- **phpMyAdmin** → http://localhost:8080

---

## API Reference

All API endpoints are documented via Swagger at `http://localhost:5000` when the app is running.

### 1. Sign Up

Register a new customer with an insurance plan.

```
POST /api/register/
Content-Type: application/json
```

**Request Body:**
```json
{
  "customer_name": "John Doe",
  "email_address": "john.doe@example.com",
  "insurance_plan_name": "Family",
  "insured_amount": 300000
}
```

---

### 2. Verify Email

Verify a user's email address using the token from the verification email.

```
GET /api/verify/<token>
```

**Responses:**

| Status | Description                                     |
|--------|-------------------------------------------------|
| 200    | Account activated (or already activated)         |
| 404    | Invalid or expired token                         |
| 500    | Internal server error                            |

---

### 3. Blacklist Email

Add an email address to the blacklist to prevent future sign-ups.

```
POST /api/blacklist/
Content-Type: application/json
```

**Request Body:**
```json
{
  "email_address": "spammer@example.com",
  "reason": "Fraudulent activity"
}
```

**Responses:**

| Status | Description                          |
|--------|--------------------------------------|
| 200    | Email blacklisted successfully       |
| 400    | Validation error or already listed   |
| 500    | Internal server error                |

---

## Database Schema

```
┌─────────────┐       ┌─────────────────┐
│    User      │       │   UserProfile    │
├─────────────┤       ├─────────────────┤
│ id (PK)      │◀──1:1─│ id (PK)          │
│ customer_name│       │ activated (bool)  │
│ email_address│       │ customerprofile_id│
│ password     │       │   (FK → User.id)  │
└──────┬──────┘       └─────────────────┘
       │
       │ 1:M
       ▼
┌──────────────┐       ┌─────────────────┐
│  Insurance    │       │  InsurancePlan   │
├──────────────┤       ├─────────────────┤
│ id (PK)       │  M:1  │ id (PK)          │
│ insured_amount│──────▶│insurance_plan_name│
│ user_id       │       └─────────────────┘
│  (FK→User.id) │
│ insurance_plan_id│
│  (FK→InsurancePlan.id)│
└──────────────┘

┌──────────────┐
│  Blacklist    │
├──────────────┤
│ id (PK)       │
│ email_address  │  (unique, indexed)
│ reason         │
└──────────────┘
```

---

## Project Structure

```
indian-insurance/
├── docker-compose.yaml          # Multi-container orchestration
├── Makefile                     # Build/run/test shortcuts
├── backend/
│   ├── Dockerfile               # Python 3.8 Alpine + MySQL client
│   ├── entrypoint.sh            # Runs migrations → starts Gunicorn
│   ├── wsgi.py                  # WSGI entry point + Celery import
│   ├── requirements.txt         # Python dependencies
│   ├── .env.sample              # Environment variable template
│   ├── pytest.ini               # Test markers configuration
│   ├── .coveragerc              # Coverage settings
│   ├── apps/
│   │   ├── __init__.py          # App factory (create_app)
│   │   ├── config/
│   │   │   ├── config.py        # Dev & Test configurations
│   │   │   ├── gunicorn_conf.py # Gunicorn (auto-scaled workers)
│   │   │   └── logging.conf     # Logging configuration
│   │   ├── templates/
│   │   │   └── base.html        # Bootstrap 5.3 base template
│   │   └── user/
│   │       ├── routes.py        # Blueprint + namespace registration
│   │       ├── models.py        # SQLAlchemy models
│   │       ├── dao.py           # Data Access Objects (DAO pattern)
│   │       ├── schema_validation.py  # JSON schema validation decorator
│   │       ├── data_validation.py    # Business rule validation decorator
│   │       ├── errors.py        # Custom error handlers
│   │       ├── forms.py         # Flask-WTF form definitions
│   │       ├── apis/
│   │       │   ├── namespaces/  # Flask-RESTX namespaces
│   │       │   │   ├── sign_up_namespace.py
│   │       │   │   ├── verify_namespace.py
│   │       │   │   └── blacklist_namespace.py
│   │       │   └── api_models/
│   │       │       └── sign_up.py  # Request/response models
│   │       └── templates/user/  # Email & web templates
│   ├── migrations/              # Alembic migrations
│   ├── tests/
│   │   ├── conftest.py          # Fixtures (app, client, db, session)
│   │   ├── unit/user/           # Unit tests
│   │   └── sample_test_schema/  # CSV test data
│   └── utils/
│       ├── email.py             # Celery email task
│       ├── token.py             # Token generation & validation
│       ├── security.py          # Password hashing (Werkzeug)
│       ├── password_helper.py   # Random password generator
│       ├── insurance_logger.py  # Singleton logger
│       ├── validation.py        # Email format validator
│       └── http_status.py       # HTTP status code constants
├── database/
│   └── init.sql                 # CREATE DATABASE indianinsurance
└── email_worker/
    ├── Dockerfile               # Python 3.10 + Celery worker
    ├── config.py                # Broker & SMTP configuration
    └── worker.py                # Celery task: send email via Flask-Mail
```

---

## Email Flow

1. **User signs up** via `POST /api/register/`
2. Backend generates a time-limited token (using `itsdangerous`) and queues an email task to **Celery**.
3. **RabbitMQ** brokers the task to the **Celery Worker** container.
4. The worker sends a verification email via **SMTP** (Flask-Mail).
5. User clicks the verification link → `GET /api/verify/<token>`
6. Token is validated; user profile is marked as **activated**.
7. A welcome email is sent upon successful activation.

---

## Validation Rules

The API enforces validation at multiple layers via decorators:

### Schema Validation (HTTP + JSON structure)
| Rule                                    | HTTP Status |
|-----------------------------------------|-------------|
| `Content-Type` must be `application/json` | 400       |
| Request body must be valid JSON           | 400       |
| No unexpected attributes allowed          | 400       |
| All required attributes must be present   | 400       |
| Attribute data types must match           | 400       |

### Data Validation (Business rules)
| Rule                                        | HTTP Status |
|---------------------------------------------|-------------|
| Customer name ≤ 50 characters               | 400         |
| Customer name has at most 2 spaces          | 400         |
| Email address is in valid format            | 400         |
| Email address ≤ 50 characters               | 400         |
| Insurance plan name ≤ 200 characters        | 400         |
| Insured amount ≤ 5,000,000 INR             | 400         |
| Email is not blacklisted                    | 422         |
| Email is not already registered             | 400         |

---

## Testing

Tests use **pytest** with fixtures that provide an isolated Flask app, test client, and transactional database session with automatic rollback.

```bash
# Run all tests
make test

# Run tests with coverage report
make cov
```

**Test markers** (defined in `pytest.ini`):
- `config` — Configuration validation tests
- `schema_validation` — JSON schema tests
- `data_validation` — Business rule tests
- `database` — Database operation tests

**Test data** is stored as CSV files in `tests/sample_test_schema/` for parametrized tests.

---

## Make Targets

| Command      | Description                                        |
|--------------|----------------------------------------------------|
| `make run`   | Build and start all containers                     |
| `make stop`  | Stop all containers                                |
| `make clean` | Stop containers, prune images and containers       |
| `make test`  | Run pytest inside the backend container            |
| `make cov`   | Run tests with coverage report                     |
| `make all`   | Stop and restart (default target)                  |

---

## Design Decisions

- **DAO Pattern** — All database operations are isolated in dedicated DAO classes, keeping business logic decoupled from data access.
- **Decorator-based Validation** — `@validate_schema` and `@validate_data` decorators provide layered request validation without cluttering endpoint logic.
- **App Factory Pattern** — `create_app()` enables different configurations for development, testing, and production.
- **Singleton Logger** — `InsuranceLogger` ensures a single logging instance across the application with both console and file output.
- **Async Email** — Celery + RabbitMQ offloads email sending to avoid blocking API responses.
- **Transactional DAO** — Database operations use SQLAlchemy's `session.begin()` context manager for automatic rollback on failure.
- **Environment-based Config** — Separate `.env` files for dev and testing with config classes mapped by environment name.

---

## License

Copyright © 2026 Dilip Kumar Sharma. All rights reserved.
