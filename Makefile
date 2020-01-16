build:
	docker-compose build

up:
	docker-compose up -d

test: up
	docker-compose run --rm --no-deps --entrypoint=pytest api /tests

logs:
	docker-compose logs --tail=25 api redis mongo

down:
	docker-compose down --remove-orphans

all: down build up test
