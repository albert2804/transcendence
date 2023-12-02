FROM node:lts-alpine3.18

ARG DOMAIN
ARG CERT_PATH
ARG CERT_KEY_PATH

ENV NUXT_ENV_DOMAIN ${DOMAIN}
ENV NODE_ENV development

WORKDIR /code

COPY ./frontend/app/ .

# copy ssl certificates for https
# (needed for development server because of https for websockets for live reload)
COPY ${CERT_PATH} /etc/ssl/certs/cert.crt
COPY ${CERT_KEY_PATH} /etc/ssl/certs/key.key

# install dependencies (package.json)
RUN npm install

EXPOSE 3000

# start development server (live reload)
CMD ["npm", "run", "dev"]
# CMD ["tail", "-f", "/dev/null"]