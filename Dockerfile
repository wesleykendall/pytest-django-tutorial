FROM python:3.7.0
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv
RUN pipenv sync
COPY . /app/
