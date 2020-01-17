build:
	docker-compose build

up:
	docker-compose up -d

test: up
	docker-compose run --rm --no-deps -e API_URL='http://api:5000' --entrypoint=pytest api /tests

logs:
	docker-compose logs --tail=25 api

down:
	docker-compose down --remove-orphans

all: down build up test
