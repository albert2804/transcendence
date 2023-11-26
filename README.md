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
- DOMAIN            -> Frontend
- DOMAIN/api        -> Backend
- DOMAIN/adminer    -> Adminer für Datenbank

## Frontend-Development
_Bisher wird vue.js mit Bootstrap als Frontend verwendet. Kann natürlich sobald feststeht welches Framework wir verwenden auch geändert werden._
- Development-Server (localhost:8080) updates live on changes in the frontend volume (src/ and public/ folders)

Deploy new vue.js frontend App (to dist/ folder):
```
docker-compose exec [frontend-container] sh -c "npm run build"
```

