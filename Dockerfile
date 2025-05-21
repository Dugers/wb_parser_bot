FROM python:3.13-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

ENV POETRY_VERSION=1.8.4
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

ENV POETRY_VIRTUALENVS_CREATE=false 

WORKDIR /app
COPY pyproject.toml poetry.lock ./

COPY . .

RUN poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "prod"]