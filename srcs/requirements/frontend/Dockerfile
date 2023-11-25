FROM node:lts-alpine

RUN npm install -g @vue/cli

WORKDIR /code

COPY ./conf/package*.json ./

RUN npm install

COPY . .

EXPOSE 8080

CMD ["tail", "-f", "/dev/null"]
# CMD ["npm", "run", "serve"]
