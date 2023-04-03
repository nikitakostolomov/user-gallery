FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY backend /app/backend/

COPY poetry.lock pyproject.toml .env README.md /app/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-ansi --no-root --no-interaction
