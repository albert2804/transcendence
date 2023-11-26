FROM node:lts-alpine

# This Container is used for development for the frontend Vue.js app
# Development server is started on localhost:8080

RUN npm install -g @vue/cli

WORKDIR /code

COPY ./app/ .

RUN npm install

EXPOSE 8080

# build for production (ready for deployment)
RUN npm run build

# starts development server on port 8080: (needs open port 8080 in docker-compose.yml)
CMD ["npm", "run", "serve"]
