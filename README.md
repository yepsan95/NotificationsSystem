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

## Tables
- users

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

## Pre-requisites
### For Running The App
- Docker installed and running without SUDO permission
- Docker compose installed without SUDO
- Ports 3000, 5432 and 5433 free

### For Running Tests And Migrations
- Make installed

## Environment Variables
Copy the variables from `.env.example` to a new `.env` file and set their values.

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

## Standards Applied
- PEP8
- PEP257
- Appnexus
- Flake8
- Black formatting
