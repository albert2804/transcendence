# ft_transcendence

## Warning
- The Makefile (make clean and make vclean) deletes all images and volumes in your docker environment. Not only the ones from this project.
- Also be careful with it while developing inside the docker volumes. You will lose your data if you delete the volumes and not saved your progress somewhere else.

## Project setup
 - You need to set the DOMAIN from .env file in your /etc/hosts file

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
_Bisher wird vue.js mit Bootstrap als Frontend verwendet. Kann natürlich sobald feststeht welches Framework wir verwenden auch geändert werden._
- Development-Server updates live on changes in the frontend volume (src/ and public/ folders)

- Actualize/Deploy frontend App:
`docker exec -it [frontend-container] sh -c "npm run build"`
(this builds the new frontend to the /dist folder. For some changes you need to clear the browser cache to see the changes)

## Backend-Development
- Django-Server should normally restart itself on changes in the backend volume but sometimes you need to restart the container manually with:
`docker restart [backend-container]`

- Until now, the Django development-server is used. This should be changed in the future to a production server (e.g. gunicorn)

