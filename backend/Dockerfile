FROM python:3.12

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /code

EXPOSE 8000

CMD ["./start.sh"]