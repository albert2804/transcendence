# ft_transcendence

## Project setup
 - You need to set the DOMAIN from .env file in your /etc/hosts file

## Project run
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
- DOMAIN/endpoint           -> Backend
- DOMAIN/endpoint/api       -> Rest-API
- DOMAIN/endpoint/admin     -> Django-Admin-Panel
- DOMAIN/adminer            -> Adminer (Database-Management)

## Frontend-Development
_Bisher wird vue.js mit Bootstrap als Frontend verwendet. Kann natürlich sobald feststeht welches Framework wir verwenden auch geändert werden._
- Development-Server (localhost:8080) updates live on changes in the frontend volume (src/ and public/ folders)

- Actualize/Deploy frontend App (DOMAIN):
`docker exec -it [frontend-container] sh -c "npm run build"`
(this builds the new frontend to the /dist folder. For some changes you need to clear the browser cache to see the changes)

## Backend-Development
- Django-Server should normally restart itself on changes in the backend volume but sometimes you need to restart the container manually with:
`docker restart [backend-container]`
- Until now, the Django development-server is used. This should be changed in the future to a production server (e.g. gunicorn)

