# Run migrations on real database
db-migrate:
	docker exec notifications-system-api alembic upgrade head

# Run migrations on test database
db-migrate-test:
	docker exec notifications-system-api alembic -x db=test upgrade head

# Run tests
run-tests:
	docker exec notifications-system-api pytest -v /code/tests/e2e
