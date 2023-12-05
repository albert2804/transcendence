# ft_transcendence

## Project setup
 - You need to set the DOMAIN from .env file in your /etc/hosts file, so that it points to 127.0.0.1 (or use localhost as DOMAIN)

## Project run
After all containers are up and running you maybe need to wait a few more seconds until the frontend is available.

Start all containers:
```
make
```
---
Build containers:
```
make build
```
---
Stop all containers:
```
make stop
```
---
Remove all containers:
```
make down
```
---
Remove all self created images (nginx, frontend, backend):
```
make iclean
```
---
Remove volumes (database):
```
make vclean
```
---
Remove all containers, images and volumes:
```
make fclean
```
---
Check the status of the project:
```
make status
```

## Routes
- DOMAIN                    -> Frontend
- DOMAIN/endpoint/api       -> Rest-API
- DOMAIN/endpoint/admin     -> Django-Admin-Panel
- DOMAIN/adminer            -> Adminer (Database-Management)

## Useful for development
- All containers are named after their service name in the docker-compose.yml file. So you can easily access them with their name.
    - For example:
        - docker restart nginx
        - docker exec -it frontend sh
        - docker logs backend
        - etc.

## Frontend-Development
- At the first start of the frontend container you need to wait a while until the node_modules folder is created after container start. (check with docker logs frontend)
- If you want to rebuild the frontend container completely, you need to remove the node_modules folder in the frontend first. (npm install will create a new one on container start)
- Development-Server updates live on changes in the frontend volume. So you can just change the code and see the changes in the browser.
- Fix many ESLint errors automatically: `docker exec -it frontend npm run lintfix`


## Backend-Development
- Development-Server should normally restart itself on changes in the backend volume but sometimes you need to restart the container manually (docker restart backend)
