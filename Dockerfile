FROM python:3.14-slim AS base

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./alembic.ini /code/alembic.ini

COPY ./alembic /code/alembic

COPY ./entrypoint.sh /code/entrypoint.sh

ENTRYPOINT ["sh", "/code/entrypoint.sh"]

# Local Development Target

FROM base AS development

COPY ./requirements-dev.txt /code/requirements-dev.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements-dev.txt

COPY ./src /code/src

COPY ./tests /code/tests

COPY ./pytest.ini /code/pytest.ini

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]

# Production Target

FROM base AS production

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
