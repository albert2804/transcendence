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
	@echo "\033[32mRemoving volumes...\033[0m"
	-@docker volume rm ${COMPOSE_PROJECT_NAME}_frontend_data ${COMPOSE_PROJECT_NAME}_backend_data ${COMPOSE_PROJECT_NAME}_db_data ${COMPOSE_PROJECT_NAME}_nginx_data
	@echo "\033[32mCleaning volumes directory...\033[0m"
	-rm -rf ${NGINX_DATA_PATH} ${FRONTEND_DATA_PATH} ${BACKEND_DATA_PATH} ${DB_DATA_PATH}
	-mkdir -p ${NGINX_DATA_PATH} ${FRONTEND_DATA_PATH} ${BACKEND_DATA_PATH} ${DB_DATA_PATH}

status:
	@echo "\033[34m### Status ${COMPOSE_PROJECT_NAME} ###\033[0m"
	@echo "\033[32mContainers:\033[0m"
	-@docker ps -a --filter "name=nginx" --filter "name=frontend" --filter "name=backend" --filter "name=db" --filter "name=adminer"
	@echo "\033[32mImages (only self-built):\033[0m"
	-@docker image ls --format "{{.Repository}}:{{.Tag}}" | grep "${COMPOSE_PROJECT_NAME}-" | awk '{print $$1}'
	@echo "\033[32mVolumes:\033[0m"
	-@docker volume ls --format "{{.Name}}" | grep "${COMPOSE_PROJECT_NAME}_" | awk '{print $$1}'
	@echo "\033[32mNetworks:\033[0m"
	-@docker network ls --format "{{.Name}}" | grep "${COMPOSE_PROJECT_NAME}_" | awk '{print $$1}'
	@echo "\033[34m### End of Status ###\033[0m"

