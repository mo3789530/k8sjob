FROM python:3.9-slim-buster
USER root

WORKDIR /app

COPY . /app

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install -r requirements.txt


CMD ["python", "-u", "./src/main.py"]