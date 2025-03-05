FROM python:3.10-slim as builder
WORKDIR /app
COPY ./pyproject.toml ./poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --without dev --no-root
RUN poetry export -f requirements.txt > /app/requirements.txt --without-hashes


FROM python:3.10-slim
WORKDIR /app

# Copy the requirements file
COPY --from=builder /app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY app/ app/
COPY data/ data/
COPY damage_simulator/ damage_simulator/

CMD ["gunicorn", "-w", "1", "--threads", "2", "-b", "0.0.0.0:8050", "app.app:server"]