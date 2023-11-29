FROM node:lts-alpine

ARG CERT_PATH
ARG CERT_KEY_PATH

# This Container is used for development for the frontend Vue.js app
# Development server is started on localhost:8080

RUN npm install -g @vue/cli

WORKDIR /code

COPY ./requirements/frontend/app/ .

# copy ssl certificates for https
# (needed for development server because of https for websockets for live reload)
COPY ${CERT_PATH} /etc/ssl/certs/cert.crt
COPY ${CERT_KEY_PATH} /etc/ssl/certs/key.key

RUN npm install

EXPOSE 8080

# build for production (ready for deployment)
# not needed for development server !
# RUN npm run build

# starts development server on port 8080: (needs open port 8080 in docker-compose.yml)
# CMD ["npm", "run", "serve", "--host", "0.0.0.0"]
# ENV HOST 0.0.0.0
CMD ["npm", "run", "serve", "--", "--host", "0.0.0.0"]
