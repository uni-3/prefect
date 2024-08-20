# build
FROM python:3.11-slim as builder

ENV APP_ROOT /app
WORKDIR ${APP_ROOT}

RUN pip3 install uv
# install from venv?

# RUN pip3 install poetry
# COPY poetry.lock pyproject.toml poetry.toml ./
# RUN poetry install --no-dev

# runner
FROM python:3.11-slim as runner

ENV APP_ROOT /app
ENV PREFECT_HOME "/prefect"

ENV PYTHONPATH "${PYTHONPATH}:${APP_ROOT}"
RUN useradd -r -s /bin/false appuser
WORKDIR ${APP_ROOT}
COPY --from=builder ${APP_ROOT}/.venv ${APP_ROOT}/.venv
COPY app .
USER appuser
ENTRYPOINT ["/app/.venv/bin/python", "main.py"]
