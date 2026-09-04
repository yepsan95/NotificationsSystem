#!/bin/bash

# Stop script if anything fails
set -e

# Run migrations on real database
echo "Running migrations on real database."

alembic upgrade head

# Run migrations on test database
echo "Running migrations on test database."

alembic -x db=test upgrade head

echo "All databases are up to date."

# Run main Dockerfile startup command
exec "$@"
