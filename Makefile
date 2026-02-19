.DEFAULT_GOAL := dev

.PHONY: dev prod infra_dev infra_prod scheduler_dev scheduler_prod down clean fix_deps

DC = docker compose
UP = up --build
INFRA_DEV = infra/docker-compose.infra.dev.yaml
INFRA_PROD = infra/docker-compose.infra.prod.yaml
DEV = infra/docker-compose.dev.yaml
PROD = infra/docker-compose.prod.yaml
SCHED_DEV = infra/docker-compose.scheduler.dev.yaml
SCHED_PROD = infra/docker-compose.scheduler.prod.yaml

# Infra
infra_dev:
	$(DC) -f $(INFRA_DEV) $(UP) 

infra_prod:
	$(DC) -f $(INFRA_PROD) $(UP) -d

# Core
dev:
	$(DC) -f $(DEV) $(UP)

prod:
	$(DC) -f $(PROD) $(UP) -d

# Scheduler
scheduler_dev:
	$(DC) -f $(SCHED_DEV) $(UP)

scheduler_prod:
	$(DC) -f $(SCHED_PROD) $(UP) -d

# Utils
fix_deps:
	-docker volume rm infra_frontend_node_modules

down:
	$(DC) -f $(DEV) down --remove-orphans
	$(DC) -f $(SCHED_DEV) down --remove-orphans
	$(DC) -f $(INFRA_DEV) down --remove-orphans

clean:
	$(DC) -f $(DEV) down -v
	$(DC) -f $(SCHED_DEV) down -v
	$(DC) -f $(INFRA_DEV) down -v
	docker image prune -f
