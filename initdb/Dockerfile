
FROM python:3.10-slim


ENV PYTHONUNBUFFERED=1


WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 5000


CMD if [ "$FLASK_ENV" = "development" ]; then \
    flask --app init_db run --host=0.0.0.0 --port=5000; \
else \
    python init_db.py; \
fi
