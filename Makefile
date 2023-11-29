all:
	@docker-compose -f ./srcs/docker-compose.yml up -d

down:
	@docker-compose -f ./srcs/docker-compose.yml down

clean:
	@docker-compose -f ./srcs/docker-compose.yml down -v
	@docker image rm $$(docker images -a -q)

vclean:	
	rm -rf srcs/volumes/*
	mkdir srcs/volumes/db_data srcs/volumes/backend_data srcs/volumes/frontend_data srcs/volumes/nginx_data
	@docker volume rm $$(docker volume ls -q)

status:
	@echo "\033[32mContainers:\033[0m"
	@docker ps -a
	@echo "\033[32mImages:\033[0m"
	@docker image ls
	@echo "\033[32mVolumes:\033[0m"
	@docker volume ls
	@echo "\033[32mNetworks:\033[0m"
	@docker network ls