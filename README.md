# ft_transcendence

## Project setup
 - You need to set the DOMAIN from .env file in your /etc/hosts file, so that it points to 127.0.0.1

## Project run
After all containers are up and running you maybe need to wait a few more seconds until the frontend is available.

Start all containers:
```
make
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
Remove all self created images:
```
make iclean
```
---
Remove all volumes and clear their directories:  
 _Be careful with it while developing inside the docker volumes. You will lose your data if you delete the volumes and not saved your progress somewhere else._ 
```
make vclean
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
_The frontend is build with vue.js and bootstrap. This can be changed when we know which framework we want to use.
Maybe nuxt.js is a good alternative because it supports SSR and SEO_
- Development-Server updates live on changes in the frontend volume. So you can just change the code and see the changes in the browser.

## Backend-Development
- Development-Server should normally restart itself on changes in the backend volume but sometimes you need to restart the container manually (docker restart backend)
