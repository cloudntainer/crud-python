FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry
RUN poetry install --no-interaction --no-ansi

COPY . .

RUN poetry install --no-root

EXPOSE 50010

ENV FLASK_APP=app.__init__
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=50010

CMD ["poetry", "run", "flask", "run"]

LABEL Name="WebApp" \
      Version="1.0"
