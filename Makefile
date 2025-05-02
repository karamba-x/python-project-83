-include .env
export

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

dev:
	flask --debug --app page_analyzer:app run

build:
	make install && psql -a -d $(DATABASE_URL) -f database.sql

start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	ruff check page_analyzer --fix