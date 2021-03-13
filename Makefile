COMPOSE?=docker-compose
RUN=$(COMPOSE) run --rm django
EXEC=$(COMPOSE) exec django
MANAGE=python manage.py
DJANGO_CONTAINER=$(shell docker ps -q --filter ancestor=appart_django)

.DEFAULT_GOAL := help
.PHONY: help start stop up build reset

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

start:      	## Start the project
	$(COMPOSE) up -d

pause:          ## Pause docker containers
	$(COMPOSE) down

stop:           ## Remove docker containers
	$(COMPOSE) kill
	$(COMPOSE) down -v

reset:          ## Reset web server container
reset:
	docker stop $(DJANGO_CONTAINER)
	docker container rm $(DJANGO_CONTAINER)
	docker image rm appart_django
	$(COMPOSE) up -d


createsuperuser:## Create superuser in db
	$(RUN) $(MANAGE) createsuperuser

tty:            ## Run django container in interactive mode
tty:
	$(RUN) /bin/bash

shell:          ## Run django shell
shell:
	$(RUN) $(MANAGE) shell

notebook:       ## Run jupyter notebook
notebook:
	$(EXEC) $(MANAGE) shell_plus --notebook
	
manage:        ## Run django manage.py
manage:
	$(RUN) $(MANAGE) $(command)

tu:            ## Run django manage.py
tu:
	$(RUN) $(MANAGE) test   --noinput --keepdb

# Internal rules

build: docker-dev.lock

docker-dev.lock: $(DOCKER_FILES)
	$(COMPOSE) pull --ignore-pull-failures
	$(COMPOSE) build --force-rm --pull
	touch docker-dev.lock

rm-docker-dev.lock:
	rm -f docker-dev.lock

up:
	$(COMPOSE) up -d --remove-orphans
	
migrate:
	$(RUN) $(MANAGE) migrate $(model)

makemigrations:
	$(RUN) $(MANAGE) makemigrations $(modelm)

logs:           ## Display logs
logs:
	$(COMPOSE) logs --timestamps --tail 200 -f django