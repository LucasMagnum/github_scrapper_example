start-api:
	echo "Starting the application"
	@docker-compose run --service-ports api

start-scrapper:
	echo "Starting scrapper"
	@docker-compose run scrapper

install:
	echo "Installing everything needed"
	docker-compose build

	echo "Setting up the database"
	docker-compose run api python scripts/init_db.py

test:
	docker-compose run api py.test -vsx src/ --cov src/

lint:
	docker-compose run api isort -rc .
	docker-compose run api black . --exclude .ipython --exclude __pycache__