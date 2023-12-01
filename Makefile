include .env

all:
	@docker-compose up -d
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
	-@docker image rm ${COMPOSE_PROJECT_NAME}_nginx ${COMPOSE_PROJECT_NAME}_frontend ${COMPOSE_PROJECT_NAME}_backend postgres adminer
	@echo "\033[32mRemoved all images\033[0m"

vclean:
	-@docker-compose down -v
	@echo "\033[32mRemoved all volumes\033[0m"

fclean: iclean vclean
	@echo "\033[32mRemoved all containers, images and volumes\033[0m"

status:
	@echo "\033[34m### Status ${COMPOSE_PROJECT_NAME} ###\033[0m"
	@echo "\033[32mContainers:\033[0m"
	-@docker ps -a --filter "name=nginx" --filter "name=frontend" --filter "name=backend" --filter "name=db" --filter "name=adminer"
	@echo "\033[32mImages (only self-built):\033[0m"
	-@docker image ls

