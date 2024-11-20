.PHONY: build service_up init load_rss search test

build:
	docker-compose build

service_up: 
	docker-compose up

init:
	docker-compose run app python src/gossip/main.py init

load_rss:
	docker-compose run app python src/gossip/main.py load-rss

search:
	docker-compose run app python src/gossip/main.py search "Latest celebrity news"

test:
	docker-compose run app python -m pytest 
