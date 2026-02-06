.PHONY: dev prod down clean

dev:
	docker compose -f docker-compose.api.yaml -f docker-compose.api.override.yaml up --build

prod:
	docker compose -f docker-compose.api.yaml up --build

down:
	docker compose down

clean:
	docker compose -f docker-compose.api.yaml -f docker-compose.api.override.yaml down -v
	docker system prune -f