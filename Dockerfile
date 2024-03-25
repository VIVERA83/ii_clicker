FROM joyzoursky/python-chromedriver

WORKDIR crawler
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UVICORN_WORKERS=1

# Uvicorn settings
ENV PORT=8005
ENV HOST=0.0.0.0
ENV LOG_LEVEL=INFO
ENV WORKERS=1
ENV RELOAD="True"

# Application settings
ENV TITLE="File Handler"
ENV DESCRIPTION="File Processing manager.\
 Files for processing are taken from the cloud drive. \
 It is part of the general engineer instructor application"
ENV VERSION="0.0.1"
ENV DOCS_URL="/docs"
ENV REDOC_URL="/redoc"
ENV OPENAPI_URL="/openapi.json"
ENV APP_HOST=${HOST}
ENV APP_PORT=${PORT}

# Settings logging
ENV LEVEL="INFO"
ENV GURU="True"
ENV TRACEBACK="false"

# Excel File settings
# 50Mb
ENV SIZE=524288000

# Yandex disk settings
ENV YA_TOKEN=NULL
ENV YA_CLIENT_ID=NULL
ENV YA_DIR="temp_folder"
ENV YA_ATTEMPT_COUNT=2

# Settings for PostgresSQL database connections
ENV POSTGRES_DB="test_db"
ENV POSTGRES_USER="test_user"
ENV POSTGRES_PASSWORD="test_password"
ENV POSTGRES_HOST="host.docker.internal"
ENV POSTGRES_PORT="5435"
ENV POSTGRES_SCHEMA="ii"

# Building
ENV UVICORN_ARGS "core.app:setup_app --host $APP_HOST --port $APP_PORT --workers $UVICORN_WORKERS"
RUN pip install --upgrade pip  --no-cache-dir
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY crawler .

CMD uvicorn $UVICORN_ARGS
