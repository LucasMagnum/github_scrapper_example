start-api:
	echo "Starting the application"
	python src/api.py

start-scrapper:
	echo "Starting scrapper"
	python src/scrapper.py

install:
	echo "Installing everything needed"
	pip install -r requirements.txt

	echo "Setting up the database"
	python scripts/init_db.py

test:
	py.test -vsx src/ --cov src/

lint:
	isort -rc .
	black . --exclude .ipython --exclude __pycache__