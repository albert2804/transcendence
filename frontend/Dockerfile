FROM node:lts-alpine

ARG DOMAIN
ARG CERT_PATH
ARG CERT_KEY_PATH

# vue only reads variables with prefix VUE_APP_
ENV VUE_APP_DOMAIN ${DOMAIN}
ENV NODE_ENV development

WORKDIR /code

COPY ./frontend/app/ .

# copy ssl certificates for https
# (needed for development server because of https for websockets for live reload)
COPY ${CERT_PATH} /etc/ssl/certs/cert.crt
COPY ${CERT_KEY_PATH} /etc/ssl/certs/key.key

# install dependencies (package.json)
RUN npm install -g @vue/cli
RUN npm -g install

EXPOSE 8080

# build for production (ready for deployment)
# only needed if you want to use a production server instead of the development server
# RUN npm run build

# start development server (live reload)
CMD [ "npm", "run", "serve" ]