# ft_transcendence

## Warning
- The Makefile (make clean and make vclean) deletes all images and volumes in your docker environment. Not only the ones from this project.
- Also be careful with it while developing inside the docker volumes. You will lose your data if you delete the volumes and not saved your progress somewhere else.

## Project setup
 - You need to set the DOMAIN from .env file in your /etc/hosts file, so that it points to 127.0.0.1

## Project run
After all containers are up and running you maybe need to wait a few more seconds until the frontend is available.

up:
```
make
```

down:
```
make down
```

delete images:
```
make clean
```

clear volume folders:
```
make vclean
```

check status:
```
make status
```

## Routes
- DOMAIN                    -> Frontend
- DOMAIN/endpoint/api       -> Rest-API
- DOMAIN/endpoint/admin     -> Django-Admin-Panel
- DOMAIN/adminer            -> Adminer (Database-Management)

## Frontend-Development
_The frontend is build with vue.js and bootstrap. This can be changed when we know which framework we want to use._
- Development-Server updates live on changes in the frontend volume. So you can just change the code and see the changes in the browser.

## Backend-Development
- Development-Server should normally restart itself on changes in the backend volume but sometimes you need to restart the container manually with:
`docker restart [backend-container]`
