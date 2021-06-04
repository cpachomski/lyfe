FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY requirements.txt ./app/requirements.txt

COPY . ./app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8000
