
FROM python:3.7

RUN pip install pytelegrambotapi

RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python /app/app.py