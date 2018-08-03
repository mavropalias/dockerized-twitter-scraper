# docker build . -t scraper-microservice

FROM python:3
WORKDIR /usr/src/app

RUN pip install nameko pymongo

COPY microservice.py .
COPY Tweet.py .

CMD ["nameko", "run", "--broker", "amqp://guest:guest@rabbitmq", "microservice"]”