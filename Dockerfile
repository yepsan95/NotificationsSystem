FROM python:3.14-slim

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./pytest.ini /code/pytest.ini

COPY ./requirements.txt /code/requirements.txt

COPY ./requirements-dev.txt /code/requirements-dev.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements-dev.txt

COPY ./src /code/src

COPY ./tests /code/tests

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
