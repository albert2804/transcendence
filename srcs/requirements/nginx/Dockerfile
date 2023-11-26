FROM nginx

ARG DOMAIN
ARG CERT_PATH
ARG CERT_KEY_PATH

# inject nginx config
COPY requirements/nginx/conf/nginx.conf /etc/nginx/conf.d
# manipulate nginx config
RUN sed -i "s/TRANSCENDENCE/${DOMAIN}/g" /etc/nginx/conf.d/nginx.conf

# create ssl directory
RUN mkdir /etc/nginx/ssl
# copy ssl certificate and key
COPY ${CERT_PATH} /etc/nginx/ssl/inception.crt
COPY ${CERT_KEY_PATH} /etc/nginx/ssl/inception.key
# Check if CERT_PATH and CERT_KEY_PATH are set
RUN if [ -n "${CERT_PATH}" ] && [ -n "${CERT_KEY_PATH}" ]; then \
    # If certificate and key are found, use them
    echo "SSL certificate and key found. Using them..." ; \
    else \
    rm -rf /etc/nginx/ssl/*; \
    # If the paths are empty, generate a self-signed certificate
    echo "SSL certificate or key not found. Generating self-signed certificate..." && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -subj "/C=DE/ST=BW/L=Heilbronn/O=42/OU=42Heilbronn/CN=Transcendende" \
    -out /etc/nginx/ssl/inception.crt \
    -keyout /etc/nginx/ssl/inception.key \
    ;fi

CMD ["nginx", "-g", "daemon off;"]
