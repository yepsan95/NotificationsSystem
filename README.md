# Notifications System
Basic notifications system for authenticated users.
Allows each user to manage and send notifications through different channels.

## Badges
### Coverage
[![Coverage Status](https://coveralls.io/repos/github/yepsan95/NotificationsSystem/badge.svg?branch=master)](https://coveralls.io/github/yepsan95/NotificationsSystem?branch=master)

## Features
### Authentication & Sessions
- **Log User In**: Validates assymetric cryptographic credentials and issues secure stateless cookies.
- **Refresh User Session**: Rotates security tokens using advanced Refresh Token Rotation (RTR).
- **Log User Out**: Revokes active secure sessions on the database and clears client cookies.

### User Management (CRUD)
- **Create new Users**
- **Get Users list**
- **Get User by ID**
- **Replace User (Full Update)**
- **Update User (Partial Update)**
- **Delete User**

### Notification Management (CRUD & Dispatch)
- **Create new Notification**: Persists a `PENDING` state and automatically triggers live multi-channel dispatch.
- **Get Notifications list**: Retrieves only notifications owned by the authenticated user.
- **Get Notification by ID**: Strict isolation check; prevents cross-user information leakage.
- **Replace Notification**: Idempotent full rewrite of a specific notification resource.
- **Update Notification**: Partial modifications of content or status parameters.
- **Delete Notification**: Secure removal verifying strict owner constraints.

## Database Tables
- **`users`**: Stores profile information, Argon2id password hashes, and notification target fields (`phone_number`, `device_token`).
- **`notifications`**: Relates down to `users` via cascading foreign keys, tracking multi-channel logs and sending lifecycles (`PENDING`, `SENT`, `FAILED`).
- **`refresh_tokens`**: Stores opaque random strings for active rotation lookups, timestamps, and revocation auditing states.

## Technologies
- **Language**: Python (3.14)
- **Framework**: FastAPI
- **ASGI Web Server**: Uvicorn
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Assymetric JWT Support**: PyJWT, Cryptography
- **Testing & Coverage**: Pytest, Pytest-Cov
- **Relational Database**: PostgreSQL
- **Conteinerization**: Docker, Docker Compose

## API Documentation And Testing
- [Swagger UI](http://localhost:3000/docs)
- [ReDoc](http://localhost:3000/redoc)
- [Raw Schema](http://localhost:3000/openapi.json)

## Routes
```text
├── /api/v1/auth
│   ├── POST /login
│   ├── POST /refresh
│   └── POST /logout
├── /api/v1/users
│   ├── GET /
│   ├── POST /
│   └── /api/v1/users/{user_id} (GET, PUT, PATCH, DELETE)
└── /api/v1/notifications
    ├── GET /
    ├── POST /
    └── /api/v1/notifications/{notification_id} (GET, PUT, PATCH, DELETE)
```

## Pre-requisites
### For Running The App
- Docker installed and running without `sudo` permission.
- Docker compose installed without `sudo` permission.
- Ports **3000**, **5432** and **5433** free.

### For Running Tests And Migrations
- GNU Make installed.

## Environment Variables
1. Copy the variables from `.env.example` to a new `.env` file at the root at the project.

2. Generate your assymetric RSA cryptographic keys using **OpenSSL**:
```cmd
# Generate private key PEM file
openssl genpkey -algorithm RSA -out private_key.pem -pkeyout rsa_keygen_bits:2048

# Extract public key PEM file
openssl rsa -pbout -in private_key.pem -out public_key.pem
```

3. Open the generated keys, format them as single-line strings with explicit literal `\n` character scapes, and set them into the `JWT_PRIVATE_KEY` and `JWT_PUBLIC_KEY` slots inside your `.env` file.
## How To Run The App
Start the Docker container:
```
docker compose up -d
```

## How To Shut The App Down
Stop the Docker container:
```
docker compose down
```

## How To Run The Tests
While the Docker container is running:
```
make run-tests
```

## How To Run Migrations On Real Database
```
make db-migrate
```

## How To Run Migrations On Test Database
```
make db-migrate-test
```

### Seed Database
- Seed users:
> **_COUNT:_** The amount of users to generate
```
make db-seed-users COUNT=50
```
- Seed notifications:
> **_COUNT:_** The amount of notifications to generate
```
make db-seed-notifications COUNT=50
```

### Generate New Migration
> **_name:_** The new migration name
```
make db-make-migration name="migration name"
```

## Development Instructions
### Environment setup
1. Create virtual environment:
```
python -m venv .venv
```

2. Activate virtual environment:

- **Linux/MacOS**
```
source .venv/bin/activate
```
- **Windows CMD**
```
.venv\Scripts\activate
```
- **Windows PowerShell**
```
.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```
pip install -r requirements-dev.txt
```

4. Install pre-commit hooks:
```
pre-commit install
```

## Standards Applied
- Ruff
- PEP8
- Isort
- POSIX Compliant Files

## Architecture & Technical Decisions
This project is build following **Clean Architecture** patterns, ensuring a rigid separation of concerns across Domain, User Cases (Services), and Infrastructure (Controllers & Repositories) layers.

### Multi-Channel Dispatch: The Strategy & Factory Patterns
To fullfil the core challenge contraint-*"adding a new channel must not imply modifying exiting logic"*-the system strictly implements the **Open/Closed Principle (OCP)** from SOLID:
- **`NotificationStrategy` (Abstract Core)**: Defines an immutable contract for message delivery.
- **Concrete Strategies (`Email`, `SMS` ,`Push`)**: Each delivery variant isolates its specific channel constraints.
- **`NotificationStrategyFactory`**: Acts as a registry selector. If a new channel is required in the future, developers only need to add a new strategy class and map it in the factory registry. The `NotificationService` and HTTP Controller layers remain untouched and completely closed to regression bugs.

### Enterprise-Grade Security Suite
- **Assymetric Token Cryptography (RS256)**: Access Tokens are signed via an unshared Private RSA Key and verified downstream accross infrastructure using a Public RSA Key.
- **XSS & Session Protection**: All JSON Web Tokens are stored exclusively using browser managed **`HttpOnly`**, **`Secure`** and **`SameSite=Lax`** cookies, completely sealing the identity tokens away from malicious JavaScript access.
- **Refresh Token Rotation (RTR)**: When a token is refreshed, the old refresh token is revoked on the database, and a completely brand-new secure opaque pair is issued.
- **Token Reuse Detection**: If a malicious third party intercepts a refresh token and tries to use it twice, the token is revoked in the database. The `RefreshTokenService` triggers an immediate security lockdown, revoking all sessions associated with the user instantly.
- **Anti-IdOR Design (Insecure Direct Object References)**: Controllers do not trust incoming user IDs in JSON bodies. The ownership anchor is extracted dynamically from the cryptographically validated cookie session.

## Author
**Bryan Yep Valencia**
