# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster
RUN mkdir /app
ADD . /app
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]
