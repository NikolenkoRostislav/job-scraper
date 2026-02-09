.DEFAULT_GOAL := api_dev

.PHONY: api_dev api_prod scheduler_dev scheduler_prod down clean

DC = docker compose

DOCKER_PATH = ../docker/backend/
API_BASE = $(DOCKER_PATH)docker-compose.api.yaml
API_DEV = $(DOCKER_PATH)docker-compose.api.override.yaml

SCHED_BASE = $(DOCKER_PATH)docker-compose.scheduler.yaml
SCHED_DEV = $(DOCKER_PATH)docker-compose.scheduler.override.yaml

# API 
api_dev:
	$(DC) -f $(API_BASE) -f $(API_DEV) up --build

api_prod:
	$(DC) -f $(API_BASE) up --build

# Scheduler
scheduler_dev:
	$(DC) -f $(SCHED_BASE) -f $(SCHED_DEV) up --build

scheduler_prod:
	$(DC) -f $(SCHED_BASE) up --build

# Utils
down:
	$(DC) -f $(API_BASE) down
	$(DC) -f $(SCHED_BASE) down

clean:
	$(DC) -f $(SCHED_BASE) -f $(SCHED_DEV) down -v
	$(DC) -f $(API_BASE) -f $(API_DEV) down -v
	docker image prune -f
