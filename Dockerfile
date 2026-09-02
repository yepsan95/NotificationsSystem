FROM python:3.14-slim AS base

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Local Development Target

FROM base AS development

COPY ./requirements.txt /code/requirements.txt

COPY ./requirements-dev.txt /code/requirements-dev.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements-dev.txt

COPY ./src /code/src

COPY ./tests /code/tests

COPY ./pytest.ini /code/pytest.ini

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]

# Production Target

FROM base AS production

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
