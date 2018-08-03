# docker build . -t scraper-twitter

FROM python:3
WORKDIR /usr/src/app

RUN pip install tweepy nameko

COPY scraper_twitter.py .

CMD ["python", "-u", "scraper_twitter.py"]