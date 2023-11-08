FROM python:3.11-alpine3.17

COPY . /protracker
WORKDIR /protracker

RUN pip install -r requirements.txt
RUN alemic upgrade head

WORKDIR /protracker/app
CMD ["uvicorn", "main:app", "--host", "--port", "8000"]
