FROM joyzoursky/python-chromedriver

WORKDIR rpc_clicker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Settings logging
ENV LEVEL="INFO"
ENV GURU="True"
ENV TRACEBACK="false"

# Settings Clicker
ENV MIN_SEC=3
ENV MAX_SEC=6
ENV MIN_SEC_ANSWER=2
ENV MAX_SEC_ANSWER=4

# Settings for RabbitMQ
ENV RABBIT_USER="guest"
ENV RABBIT_PASSWORD="guest"
ENV RABBIT_HOST="host.docker.internal"
ENV RABBIT_PORT="5672"

# Building
RUN pip install --upgrade pip  --no-cache-dir
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY rpc_clicker .

CMD python main.py
