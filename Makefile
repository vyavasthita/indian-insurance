all: stop run

stop:
	docker compose stop

clean:
	docker container prune -f
	docker image prune -f

run:
	docker compose up -d --build --remove-orphans

test:
	docker exec backend pytest -v

cov:
	docker exec backend pytest --cov
