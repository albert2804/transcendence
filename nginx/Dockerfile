FROM nginx

ARG DOMAIN
ARG CERT_PATH
ARG CERT_KEY_PATH

# inject nginx config
COPY nginx/conf/nginx.conf /etc/nginx/conf.d
# manipulate nginx config
RUN sed -i "s/DOMAIN/${DOMAIN}/g" /etc/nginx/conf.d/nginx.conf

# create ssl directory
RUN mkdir /etc/nginx/ssl
# copy ssl certificate and key
COPY ${CERT_PATH} /etc/nginx/ssl/inception.crt
COPY ${CERT_KEY_PATH} /etc/nginx/ssl/inception.key

CMD ["nginx", "-g", "daemon off;"]
