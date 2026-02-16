.DEFAULT_GOAL := dev

.PHONY: dev prod scheduler_dev scheduler_prod down clean fix_deps, restart, restart_clean

DC = docker compose

DOCKER_PATH = docker/
BASE = $(DOCKER_PATH)docker-compose.yaml
DEV = $(DOCKER_PATH)docker-compose.override.yaml

SCHED_BASE = $(DOCKER_PATH)docker-compose.scheduler.yaml
SCHED_DEV = $(DOCKER_PATH)docker-compose.scheduler.override.yaml

# API 
dev:
	$(DC) -f $(BASE) -f $(DEV) up --build

prod:
	$(DC) -f $(BASE) up --build

# Scheduler
scheduler_dev:
	$(DC) -f $(SCHED_BASE) -f $(SCHED_DEV) up --build

scheduler_prod:
	$(DC) -f $(SCHED_BASE) up --build

# Utils
fix_deps:
	-docker volume rm docker_frontend_node_modules

down:
	$(DC) -f $(BASE) -f $(DEV) down --remove-orphans
	$(DC) -f $(SCHED_BASE) -f $(SCHED_DEV) down --remove-orphans

clean:
	$(DC) -f $(SCHED_BASE) -f $(SCHED_DEV) down -v
	$(DC) -f $(BASE) -f $(DEV) down -v
	docker image prune -f

restart: down dev

restart_clean: down fix_deps dev
