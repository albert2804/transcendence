FROM node:lts-alpine3.18

ARG DOMAIN
ARG CERT_PATH
ARG CERT_KEY_PATH

ENV NUXT_ENV_DOMAIN ${DOMAIN}
ENV NODE_ENV development

WORKDIR /code

# copy start script
COPY ./frontend/start.sh /
RUN chmod +x /start.sh

# copy frontend app
COPY ./frontend/app/ .

# copy ssl certificates for https
# (needed for development server because of https for websockets for live reload)
COPY ${CERT_PATH} /etc/ssl/certs/cert.crt
COPY ${CERT_KEY_PATH} /etc/ssl/certs/key.key

EXPOSE 3000

# start development server (live reload)
CMD ["/start.sh"]
# CMD ["tail", "-f", "/dev/null"]