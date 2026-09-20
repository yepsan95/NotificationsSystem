# Notifications System
Basic notifications system for authenticated users.
Allows each user to manage and send notifications through different channels.

## Features
- Create new Users
- Get Users list
- Get User by id
- Replace User
- Update User
- Delete User
- Create new Notification
- Get Notifications list
- Get Notification by id
- Replace Notification
- Update Notification
- Delete Notification
- Log User In
- Refresh User Session
- Log User Out

## Tables
- users
- notifications
- refresh_tokens

## Author
Bryan Yep Valencia

## Badges
### Coverage
[![Coverage Status](https://coveralls.io/repos/github/yepsan95/NotificationsSystem/badge.svg?branch=master)](https://coveralls.io/github/yepsan95/NotificationsSystem?branch=master)

## Technology
- Python
- FastAPI
- SQLAlchemy
- uvicorn
- pytest
- PostgreSQL
- Docker

## API Documentation And Testing
- [Swagger UI](http://localhost:3000/docs)
- [ReDoc](http://localhost:3000/redoc)
- [Raw Schema](http://localhost:3000/openapi.json)

## Routes
- /api/v1/users
- /api/v1/users/{user_id}
- /api/v1/notifications
- /api/v1/notifications/{notification_id}
- /api/v1/auth/login
- /api/v1/auth/refresh
- /api/v1/auth/logout

## Pre-requisites
### For Running The App
- Docker installed and running without SUDO permission
- Docker compose installed without SUDO
- Ports 3000, 5432 and 5433 free

### For Running Tests And Migrations
- Make installed

## Environment Variables
1. Copy the variables from `.env.example` to a new `.env` file and set their values.

2. Generate the JWT private and public keys:

- Generate JWT private key
```
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```
- Generate JWT public key
```
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

3. Copy the values of `JWT_PRIVATE_KEY` and `JWT_PUBLIC_KEY` into `.env`.
## How To Run The App
```
docker compose up -d
```

## How To Shut The App Down
```
docker compose down
```

## How To Run The Tests
While the app is running:
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

## How To Seed The Database With Mock Data
```
make db-users-seed
```
The seeder will create 50 users by default.
If you want a different number of users to be created, use the COUNT parameter:
```
make db-users-seed COUNT=20
```

## Development Instructions
### Environment setup
1. Create virtual environment:
```
python -m venv .venv
```

2. Activate virtual environment:

- Linux/MacOS
```
source .venv/bin/activate
```

- Windows

  - CMD
  ```
  .venv\Scripts\activate
  ```
  - PowerShell
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
### Seed Database
> **_COUNT:_** The amount of users to generate
```
make db-seed-users COUNT=50
```
### Generate New Migration
> **_name:_** The new migration name
```
make db-make-migration name="migration name"
```

## Standards Applied
- Ruff
- PEP8
- Isort
- POSIX Compliant Files
