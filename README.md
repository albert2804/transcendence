# ft_transcendence

## Project setup

 - You have to set the environment variables in the .env file.

## Project run

Start all containers:
```
make
```
---
Start all containers in the background:
```
make detached
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
Stop and remove all containers:
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
Remove all containers, images and volumes (except the frontend node_modules folder):
```
make clean
```
---
Remove all containers, images and volumes:
```
make fclean
```
---
Remove backend Migration files:
```
make mclean
```
---
Docker prune (remove docker cache...)
```
make prune
```
---
Check the status of the project:
```
make status
```

## Project usage

### Development

- Set the environment variables in the .env file:
```
NODE_ENV=development
DJANGO_SETTINGS_MODULE=backend.settings.development
```
- The development frontend server updates the changes automatically.
- The backend server needs to be restarted to update the changes.

### Production

- Set the environment variables in the .env file:
```
NODE_ENV=production
DJANGO_SETTINGS_MODULE=backend.settings.production
```
- To update the frontend changes, you need to run 'npm run build' and restart the frontend server.
- The backend server needs to be restarted to update the changes.