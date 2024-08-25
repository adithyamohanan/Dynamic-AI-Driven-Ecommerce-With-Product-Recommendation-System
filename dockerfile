FROM python:3.11.8-alpine

ENV PYTHONBUFFERED=1

WORKDIR /Finalyear

COPY requirements.txt requirements.txt

RUN apk add --no-cache postgresql-dev

RUN pip install -r requirements.txt

COPY . . 

CMD gunicorn Ecommerce_web.wsgi:application --bind 0.0.0.0:8000

EXPOSE 8000

