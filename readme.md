# Dockerized twitter scraper

This is a dockerized twitter scraper built on Python. It is composed of the following 5 micro-services:

1. MongoDB (database)
2. Mongo-express (database UI)
3. RabbitMQ (message queue management)
4. Nameko (microservices framework)
5. Twitter scraper (actual scraper)

## Environment variables

Using the `docker-scraper-twitter.default.env` file as reference, create a `docker-scraper-twitter.env` file in the same location with the following:

```bash
TWITTER_API_CONSUMER_KEY=***
TWITTER_API_CONSUMER_SECRET=***
TWITTER_API_ACCESS_TOKEN=***
TWITTER_API_ACCESS_TOKEN_SECRET=***
TWITTER_API_FILTER=keyword
AMQP_URI=amqp://guest:guest@rabbitmq
```

## RabbitMQ admin panel

http://localhost:15672

## MongoDB admin panel

http://localhost:8081
