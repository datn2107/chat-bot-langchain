FROM python:3.11-bullseye

COPY . /app/
RUN rm -rf /app/venv
RUN rm -rf /app/**/__pycache__

WORKDIR /app
RUN python3 -m pip install -r requirements.txt
RUN alembic upgrade head

EXPOSE 8080

WORKDIR /app/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
