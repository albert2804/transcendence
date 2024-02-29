FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG CERT_PATH
ARG CERT_KEY_PATH

# install nc for database connection check
RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /code

# copy backend files
COPY ./backend/files/ .

# install dependencies
RUN pip install -r requirements.txt

# COPY ${CERT_PATH} /etc/ssl/certs/cert.crt
# COPY ${CERT_KEY_PATH} /etc/ssl/certs/key.key

# ensure start.sh is executable
RUN chmod +x ./start.sh

EXPOSE 8000

CMD ["./start.sh"]