FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install nc for database connection check
RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /code

COPY ./files/ .

# install dependencies
RUN pip install -r requirements.txt

# ensure start.sh is executable
RUN chmod +x ./start.sh

EXPOSE 8000

CMD ["./start.sh"]