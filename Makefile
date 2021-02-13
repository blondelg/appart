DOCKER_COMPOSE?=docker-compose
RUN=$(DOCKER_COMPOSE) run --rm django
EXEC=$(DOCKER_COMPOSE) exec django
MANAGE=python manage.py

.DEFAULT_GOAL := help
.PHONY: help start stop up build reset

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

start:   	## Start the project
	$(DOCKER_COMPOSE) up -d

pause:          ## Pause docker containers
	$(DOCKER_COMPOSE) down

stop:           ## Remove docker containers
	$(DOCKER_COMPOSE) kill
	$(DOCKER_COMPOSE) down -v

reset:          ## Remove docker containers
reset:
	$(DOCKER_COMPOSE) down django
	$(DOCKER_COMPOSE) rm

createsuperuser:## Create superuser in db
	$(RUN) $(MANAGE) createsuperuser

tty:            ## Run django container in interactive mode
tty:
	$(RUN) /bin/bash

shell:          ## Run django shell
shell:
	$(RUN) $(MANAGE) shell
	
manage:        ## Run django manage.py
manage:
	$(RUN) $(MANAGE) $(command)

# Internal rules

build: docker-dev.lock

docker-dev.lock: $(DOCKER_FILES)
	$(DOCKER_COMPOSE) pull --ignore-pull-failures
	$(DOCKER_COMPOSE) build --force-rm --pull
	touch docker-dev.lock

rm-docker-dev.lock:
	rm -f docker-dev.lock

up:
	$(DOCKER_COMPOSE) up -d --remove-orphans
