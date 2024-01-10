include .env

all:
	@docker-compose up
	@echo "\033[32mContainers are up and running\033[0m"

build:
	@docker-compose build
	@echo "\033[32mContainers built\033[0m"

stop:
	@docker-compose stop
	@echo "\033[32mStopped all containers\033[0m"

down:
	@docker-compose down
	@echo "\033[32mRemoved all containers\033[0m"

iclean:
	-@docker-compose down 
	-@docker image prune -a --filter "label=com.docker.compose.project=${COMPOSE_PROJECT_NAME}" -f
	-@docker image rm transcendence_backend:latest transcendence_frontend:latest transcendence_nginx:latest
	@echo "\033[32mRemoved all images\033[0m"

vclean:
	-@docker-compose down -v
	@echo "\033[32mRemoved all volumes\033[0m"

fclean: iclean vclean
	-@rm -rf ./frontend/node_modules
	-@rm -rf ./frontend/package-lock.json
	@echo "\033[32mRemoved all containers, images and volumes\033[0m"

prune:
	@docker system prune -a -f
	@echo "\033[32mdocker system prune -a -f done!\033[0m"

status:
	@echo "\033[34m### Status ${COMPOSE_PROJECT_NAME} ###\033[0m"
	@echo "\033[32mContainers:\033[0m"
	-@docker ps -a --filter "name=nginx" --filter "name=frontend" --filter "name=backend" --filter "name=db" --filter "name=adminer"
	@echo "\033[32mImages:\033[0m"
	-@docker image ls
