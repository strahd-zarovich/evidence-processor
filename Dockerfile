FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY defaults /app/defaults
COPY scripts /app/scripts

ENV PYTHONPATH=/app/scripts
ENV EP_CONFIG=/app/defaults/config.yaml

CMD ["python", "/app/scripts/check_mariadb.py"]