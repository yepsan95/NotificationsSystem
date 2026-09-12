# Create migration with updated models
db-make-migration:
	docker exec notifications-system-api alembic revision --autogenerate -m "$(name)"

# Run migrations on real database
db-migrate:
	docker exec notifications-system-api alembic upgrade head

# Run migrations on test database
db-migrate-test:
	docker exec notifications-system-api alembic -x db=test upgrade head

# Run users seeder
COUNT ?= 50
db-seed-users:
	docker exec notifications-system-api python -m src.cli.seed_manager users --count $(COUNT)

# Run tests
run-tests:
	docker exec notifications-system-api pytest -v /code/tests/e2e
