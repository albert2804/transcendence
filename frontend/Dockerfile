FROM node:lts-alpine3.18

ARG DOMAIN
ARG CERT_PATH
ARG CERT_KEY_PATH

ENV NUXT_ENV_DOMAIN ${DOMAIN}
ENV NODE_ENV development

WORKDIR /code

COPY ./frontend/start.sh /
RUN chmod +x /start.sh

EXPOSE 3000

CMD ["/start.sh"]